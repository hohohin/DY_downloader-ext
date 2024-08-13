from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from DrissionPage import ChromiumPage
from DownloadKit import DownloadKit
from datetime import datetime
import re
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def stringify_current_time():
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d_%H:%M:%S")

def create_directory(path):
    try:
        os.mkdir(path)
        print(f"Created directory {path}, your downloads will be saved there.")
    except FileExistsError:
        print(f"Directory {path} already exists, files will be saved there.")
    except OSError as error:
        print(f"Failed to create directory: {error}")

create_directory("Downloads")

@app.route('/run_python_code', methods=['POST'])
def run_python_code():
    data = request.json
    text = data.get('url')

    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    urls = url_pattern.findall(text)
    if urls:
        first_url = urls[0]
        print("First URL found:", first_url)
    else:
        return jsonify({"message": "No URLs found."})

    page = ChromiumPage()
    page.get(first_url)

    video_src = page.ele('x://*[@id="douyin-right-container"]/div[2]/div/div[1]/div[2]/div/xg-video-container/video/source[1]').attr('src')
    page.get(video_src)

    d = DownloadKit(goal_path="Downloads")
    file_name = stringify_current_time() + ".mp4"
    d.download(video_src, rename=file_name, suffix='')

    page.quit()

    return jsonify({"message": f"Downloaded video as {file_name}"})

if __name__ == '__main__':
    app.run(port=5000)
