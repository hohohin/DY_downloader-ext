from DrissionPage import ChromiumPage
from DownloadKit import DownloadKit
from datetime import datetime
import re
import os


flag = True

def stringify_current_time():
    # 获取当前时间
    current_time = datetime.now()
    # 时间字符串
    ftime = current_time.strftime("%Y-%m-%d_%H:%M:%S")  # 标准格式
    return ftime

def create_directory(path):
    try:
        # 创建目录
        os.mkdir(path)
        print(f"已建立 {path} 文件夹，你下载的文件将会保存在该文件夹")
    except FileExistsError:
        print(f"已存在 {path} 文件夹，你下载的文件将会保存在该文件夹")
    except OSError as error:
        print(f"Failed to create directory: {error}")

create_directory("Downloads")

while flag:

    text = input("粘贴抖音视频分享链接，或输入e退出")

    if text =="e":
        flag = False
        exit()
    else:
        # 正则表达式来匹配URL
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )

        urls = url_pattern.findall(text)

        if urls:
            first_url = urls[0]
            print("First URL found:", first_url)
        else:
            print("No URLs found.")

        page = ChromiumPage()

        page.get(first_url)

        video_src = page.ele('x://*[@id="douyin-right-container"]/div[2]/div/div[1]/div[2]/div/xg-video-container/video/source[1]').attr('src')

        page.get(video_src)

        d = DownloadKit(goal_path="Downloads")
        #m = d.add(video_src)
        
        file_name = stringify_current_time() + ".mp4"

        d.download(video_src, rename=file_name, suffix='')
        #print(m.file_name)

        page.quit()

