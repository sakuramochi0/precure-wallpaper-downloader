#!/usr/bin/env python3
import datetime
from os import path, chdir
from pprint import pprint
from bs4 import BeautifulSoup
import requests
from tumblpy import Tumblpy

def toei():
    '''東映アニメーションのページから壁紙をダウンロードする'''
    
    # init
    img_sources = []
    
    # 壁紙ページを読み込み
    url_base = 'http://www.toei-anim.co.jp/tv/precure/special/'
    r = requests.get(url_base)
    soup = BeautifulSoup(r.text)
    urls = [a['href'] for a in soup.select('.wallpaper-container a')]
     
    # 各壁紙配信ページを読み込み
    for url in urls:
        r = requests.get(url_base + url)
        soup = BeautifulSoup(r.text)
        filename = soup.select('img')[0]['src']
        
        # まだ画像をダウンロードしていなければダウンロード
        if not path.exists(filename):
            img_url = path.join(path.dirname(url_base + url), filename)
            r = requests.get(img_url)
            with open(filename, 'wb') as f:
                f.write(r.content)
                print('Downloaded:', filename)
            # tumblrに投稿する画像リストにファイル名を追加
            if '1920' in filename:
                img_sources.append(img_url)

    # tumblrに投稿する
    if img_sources:
        tumblr_post(img_sources, website='Toei Animation', source_url=url_base)

def asahi():
    '''朝日放送のページから壁紙をダウンロードする'''
    
    # init
    img_sources = []
    
    # 壁紙ページを読み込み
    url_base = 'http://asahi.co.jp/precure/princess/enjoyment/'
    r = requests.get(url_base)
    r.encoding = 'euc-ja'
    soup = BeautifulSoup(r.text)
    img_urls = [url_base + a['href'] for a in soup.select('.wallpaper-prev a')]
     
    for img_url in img_urls:
        filename = path.basename(img_url)
        # まだ画像をダウンロードしていなければダウンロード
        if not path.exists(filename):
            r = requests.get(img_url)
            with open(filename, 'wb') as f:
                f.write(r.content)
                print('Downloaded:', filename)
            # tumblrに投稿する画像リストにファイル名を追加
            if '1920' in filename:
                img_sources.append(img_url)

    # tumblrに投稿する
    if img_sources:
        tumblr_post(img_sources, website='Asahi Broadcasting Corporation', source_url=url_base)
            
def tumblr_post(img_sources, website, source_url):

    # init
    with open('../.credentials') as f:
        API_TOKEN, API_TOKEN_KEY, OAUTH_TOKEN, OAUTH_TOKEN_SECRET = f.read().strip().split()
    t = Tumblpy(API_TOKEN, API_TOKEN_KEY, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    blog_url = 'sakuramochimochi.tumblr.com'

    # ポスト用パラメータの作成
    params = dict(
        type='photo',
        source_url=source_url,
        caption='Go! Princess Precure Wallpaper for {month} on the website of {website}'.format(month=datetime.date.today().strftime('%B'), website=website),
        tags='precure,go princess precure',
        source=img_sources[0],
    )
    print(params)

    # 以上のパラメータで投稿
    post = t.post('post', blog_url=blog_url, params=params)
    print('Post to Tumblr:', '{blog_url}/post/{id}'.format(blog_url=blog_url, id=post['id']))

if __name__ == '__main__':
    chdir('img')
    asahi()
    toei()
