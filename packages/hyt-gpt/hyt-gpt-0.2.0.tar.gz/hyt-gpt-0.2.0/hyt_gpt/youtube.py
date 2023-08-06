import requests
import yt_dlp
from typing import Dict, Any, List
from .gpt import seg_transcript, chat_gpt
from .utils import is_valid_youtube_url
import traceback

headers = {
    'authority': 'api.youtube.com',
    'accept': 'application/json, text/plain, */*',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

class HytGpt:
    def __init__(self, gpt_key: str, prompt: str):
        self.gpt_key = gpt_key
        self.prompt = prompt
        
    def summary(self, ylink: str) -> Dict[str, str]:
        if not is_valid_youtube_url(ylink):
            return {'status': 'failed', 'url': ylink, 'subtitles': [], 'summaries': 'Invalid youtube url'}
        subtitles = self.__youtube_subtitle(ylink)
        if not subtitles:
            return {'status': 'failed', 'url': ylink, 'subtitles': subtitles, 'summaries': 'Subtitle retrieval failed'}

        seged_text = seg_transcript(subtitles)
        summaried_text = ''
        i = 1
        for entry in seged_text:
            try:
                response = chat_gpt(self.gpt_key, self.prompt, entry)
                print(f'Completed the {str(i)} part summary')
                i += 1
            except Exception as e:
                print(f"Exception occurred: {str(e)}")
                traceback.print_exc()
                response = 'Summary failed'
            summaried_text += response + '\n'
        response_data = {
            'status': 'success',
            'url': ylink,
            'subtitles': subtitles,
            'summaries': summaried_text,
        }
        return response_data


    def __youtube_player_list(self, yvid):
        url = f"https://www.youtube.com/watch?v={yvid}"
        response = requests.request("GET", url, headers=headers)
        return response.text


    def __get_text_from_url(self, url: str) -> str:
        response = requests.request("GET", url, headers=headers)
        return response.text


    def __parse_subtitles(self, subtitles) -> List[Dict[str, str]]:
        result = []
        subtitle_lines = subtitles.strip().split('\n')[3:]
        for i in range(0, len(subtitle_lines), 2):
            if ' --> ' not in subtitle_lines[i]:
                continue
            start, end = subtitle_lines[i].split(' --> ')
            text = subtitle_lines[i+1]
            result.append({
                'start': start,
                'end': end,
                'text': text
            })
        return result


    def __prepare_subtitle(self, subtitle: Dict[str, str]) -> str:
        text = self.__get_text_from_url(subtitle.get('url'))
        return self.__parse_subtitles(text)


    def __youtube_subtitle(self, url: str) -> List[Dict[str, str]]:
        # options for subtitle extraction
        options = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'zh-Hans'],  # You can add more languages here
            'skip_download': True,  # We don't need to download the video
            'quiet': False  # Suppress console output
        }        
        with yt_dlp.YoutubeDL(options) as ydl:
            result = ydl.extract_info(url, download=False)

        # Extract the subtitles
        subtitles = []
        for subtitle_list in result.get('subtitles', {}).values():
            for subtitle in subtitle_list:
                if subtitle.get('ext') == 'vtt':
                    subtitles.extend(self.__prepare_subtitle(subtitle))
        return subtitles


    def __to_subtitle_list(self, subtitles):
        results = []
        for subtitle in subtitles:
            if 'text' in subtitle:
                results.append(subtitle.get('text'))
        return results
