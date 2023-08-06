import requests
import traceback
import re
from .gpt import chat, segTranscipt
from .notion import insert2notion
# from .settings import chatgpt_key, notion_database_id, notion_token, sect
from typing import Dict, List, Tuple, Union
import logging

headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
}


class HBiliGpt:
    def __init__(self, chatgpt_key, prompt, notion_database_id=None, notion_token=None):
        self.chatgpt_key = chatgpt_key
        self.prompt = prompt
        self.notion_database_id = notion_database_id
        self.notion_token = notion_token

    def summary(self, blink: str) -> Dict[str, str]:
        if not self.__is_valid_bilibili_url(blink):
            return {'status': 'failed', 'url': blink, 'subtitles': [], 'summaries': 'Invalid bilibili url'}
        bvid = blink.split('/')[4]
        logging.info(f'Start processing video information: {bvid}')
        subtitles = self.__bili_subtitle(
            bvid, self.__bili_player_list(bvid)[0])
        if not subtitles:
            return {'status': 'failed', 'url': blink, 'subtitles': [], 'summaries': 'No subtitles found'}
        logging.info('Subtitle obtained successfully')
        seged_text = segTranscipt(subtitles)
        summarized_text = ''
        i = 1
        for entry in seged_text:
            try:
                response = chat(self.chatgpt_key, self.prompt, entry)
                logging.info(f'Completed summary of part {str(i)}')
                i += 1
            except Exception as e:
                # logging.info the exception message and traceback
                logging.info(f"Exception occurred: {str(e)}")
                traceback.print_exc()
                response = 'Summary failed'
            summarized_text += '\n'+response
        return {'status': 'success', 'url': blink, 'subtitles': subtitles, 'summaries': summarized_text}

    def __is_valid_bilibili_url(self, url):
        pattern = re.compile(r'https?://(www\.)?bilibili\.com(/[\w\-]*)*/?')
        return bool(pattern.match(url))

    def __bili_player_list(self, bvid):
        url = 'https://api.bilibili.com/x/player/pagelist?bvid='+bvid
        response = requests.get(url, headers=headers)
        logging.info('response:', response.content)
        cid_list = [x['cid'] for x in response.json()['data']]
        logging.info('cid_list:', cid_list)
        return cid_list

    def __bili_subtitle_list(self, bvid, cid):
        url = f'https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}'
        response = requests.get(url, headers=headers)
        logging.info('response:', response.content)
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            logging.info('subtitles:', subtitles)
            return ['https:' + x['subtitle_url'] for x in subtitles]
        else:
            return []

    def __bili_subtitle(self, bvid, cid):
        subtitles = self.__bili_subtitle_list(bvid, cid)
        if subtitles:
            response = requests.get(subtitles[0], headers=headers)
            if response.status_code == 200:
                body = response.json()['body']
                return body
        return []

    # subtitle_text = bili_subtitle(bvid, bili_player_list(bvid)[0])

    def __bili_info(self, bvid):
        params = (
            ('bvid', bvid),
        )
        response = requests.get(
            'https://api.bilibili.com/x/web-interface/view', params=params)
        return response.json()['data']

    def __bili_tags(self, bvid):
        params = (
            ('bvid', bvid),
        )

        response = requests.get(
            'https://api.bilibili.com/x/web-interface/view/detail/tag', params=params)
        data = response.json()['data']
        if data:
            tags = [x['tag_name'] for x in data]
            if len(tags) > 5:
                tags = tags[:5]
        else:
            tags = []
        return tags
