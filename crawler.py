from twikit import Client
import json
import pandas as pd
import base64
import os
import shadowsocks
import requests

from twikit import Client

USERNAME = 'example_user'
EMAIL = 'email@example.com'
PASSWORD = 'password0000'
port=7897

# 使用twikit.Client并添加代理
# 需要找到本地梯子的端口号,proxy='http://127.0.0.1:{port}'
client = Client('en-US',proxy=f'http://127.0.0.1:{port}')
# 修复f-string中的引号问题

client.login(auth_info_1=USERNAME, auth_info_2=EMAIL,password=PASSWORD)
client.save_cookies('cookies.json')
client.load_cookies(path='cookies.json')

# 用户名列表
usernames = [ 'BBCEarth','historyinmemes','designboom','NYTimesTravel','SmithsonianMag','ThePhotoSociety']
counts= [50,60,30,30,50,50]
#选取爬虫用户中，对应每个用户爬取的数据条目数

# 创建保存所有用户信息的列表
all_tweets_to_store = []

# 创建保存图片和文本信息的文件
output_file = 'tweets_images_texts.txt'

def download_image(text, url, file_path):
    # 尝试次数
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            # 检查请求是否成功
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f'图片下载并保存成功：{file_path}')
                image_num = url.split('/')[-1]
                with open(output_file, 'a') as out_file:
                    out_file.write(f'{image_num},{text.strip()}\n')             
                return True
        except (ChunkedEncodingError, ConnectionError) as e:
            print(f'下载图片失败：{e}，正在重试... ({attempt+1}/{max_retries})')
            time.sleep(2)
    print('图片下载失败。')
    return False

# 处理每个用户名
for i,username in enumerate(usernames):
    user = client.get_user_by_screen_name(username)
    tweets = user.get_tweets('Tweets')
    num=counts[i]
    while(num!=0):
        tweets_to_store = []
        for tweet in tweets:
            try:
                url = tweet.media[0]['media_url_https']
            except:
                continue
            response = requests.get(url)
            text = tweet.full_text.replace('\n', ' ').replace('\r', ' ')
            # 检查请求是否成功
            if response.status_code == 200:
                # 创建保存图片的文件夹
                folder_path = os.path.join('twitter_imgs')
                os.makedirs(folder_path, exist_ok=True)
                image_num = url.split('/')[-1]
                # 图片保存路径
                file_path = os.path.join(folder_path, image_num)
                if os.path.exists(file_path):
                    print(username)
                    print(f'图片已存在：{file_path}')
                else:
                    if not download_image(text,url, file_path):
                        continue
                    
        num-=1
        tweets=tweets.next()