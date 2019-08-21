from pyquery import PyQuery
from pprint import pprint
import requests
import time

def decode_html(html_text):
    # print(html_text)
    doc = PyQuery(html_text)
    # print(doc)
    for item in doc.items('.board-wrapper dd'):
        print(item)
        yield {
            'name': item.find('.name').text(),
            'actors': item.find('.star').text(),
            'time': item.find('.releasetime').text(),
            'score': item.find('.score').text(),
        }
def download_html(url):
    try:
        r = requests.get(url)
        if r.status_code==200:
            return r.text
        else:
            print('request failed, status is {}'.format(r.status_code))
            return None
    except Exception as e:
        print(e)
        return None

def parse_url(offset):
    url = 'https://maoyan.com/board/4?offset={}'.format(offset)
    html_text = download_html(url)
    for each_movie in decode_html(html_text):
        pprint(each_movie)

def main():
    '''0开始到100，步长10：0，10,20，30'''
    for offset in range(0, 10, 10):
        parse_url(offset)


if __name__ == '__main__':
    main()
