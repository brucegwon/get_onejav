import requests
import os
from dotenv import load_dotenv
load_dotenv()

def translate_to_korean(text: str, api_key: str = None) -> str:
    """
    DeepL API를 이용해 입력된 텍스트를 한국어로 번역합니다.
    :param text: 번역할 원본 텍스트
    :param api_key: DeepL API 키 (없으면 환경변수 DEEPL_API_KEY 사용)
    :return: 번역된 한국어 텍스트
    """
    if api_key is None:
        api_key = os.getenv('DEEPL_API_KEY')
    if not api_key:
        raise ValueError('DeepL API 키가 필요합니다. 환경변수 DEEPL_API_KEY를 설정하거나 직접 전달하세요.')
    url = 'https://api-free.deepl.com/v2/translate'
    data = {
        'auth_key': api_key,
        'text': text,
        'target_lang': 'KO',
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        result = response.json()
        return result['translations'][0]['text']
    else:
        print('DeepL API 오류:', response.text)
        return ''

if __name__ == '__main__':
    # 테스트용 예시
    sample_text = 'This is a test sentence for translation.'
    print(translate_to_korean(sample_text)) 