import sys
import os
import time
import requests
import json
from mecord_crawler import utils
import logging
import urllib3
import datetime
import shutil
from urllib.parse import *
from PIL import Image

rootDir = ""
curGroupId = 0

def notifyMessage(success, msg):
    try:
        param = {
            "task_id": curGroupId,
            "finish_desc": msg
        }
        s = requests.session()
        s.keep_alive = False
        res = s.post("https://beta.2tianxin.com/common/admin/mecord/update_task_finish", json.dumps(param), verify=False)
        resContext = res.content.decode(encoding="utf8", errors="ignore")
        logging.info(f"notifyMessage res:{resContext}")
        s.close()
    except Exception as e:
        logging.info(f"notifyMessage exception :{e}")

def publish(media_type, post_text, ossurl, cover_url):
    type = 0
    if media_type == "video":
        type = 2
    elif media_type == "image":
        type = 1
    elif media_type == "audio":
        type = 3
    param = {
        "task_id": curGroupId,
        "content": ossurl,
        "content_type": type,
        "info": post_text,
        "cover_url": cover_url
    }
    s = requests.session()
    s.keep_alive = False
    res = s.post("https://beta.2tianxin.com/common/admin/mecord/add_crawler_post", json.dumps(param), verify=False)
    resContext = res.content.decode(encoding="utf8", errors="ignore")
    logging.info(f"publish res:{resContext}")
    s.close()
    
def ossPathWithSize(path):
    w = 0
    h = 0
    if "http" in path:
        w,h = utils.getOssImageSize(path)
    
    if w > 0 and h > 0:
        if "?" in path:
            return f"{path}&width={w}&height={h}"
        else:
            return urljoin(path, f"?width={w}&height={h}")
    return path

def pathWithSize(path, w, h):    
    if w > 0 and h > 0:
        if "?" in path:
            return f"{path}&width={w}&height={h}"
        else:
            return urljoin(path, f"?width={w}&height={h}")
    return path

def localFileWithSize(type, path):
    width = 0
    height = 0
    if type == "image":
        img = Image.open(path)
        imgSize = img.size
        width = img.width
        height = img.height
    elif type == "video":
        w,h,bitrate,fps = utils.videoInfo(path)
        width = w
        height = h
    
    return int(width), int(height)
    
def download(name, media_type, post_text, media_resource_url, audio_resource_url):
    ext = ".mp4"
    if media_type == "image":
        ext = ".jpg"
    elif media_type == "audio":
        ext = ".mp3"
    savePath = os.path.join(rootDir, f"{name}{ext}")
    if os.path.exists(savePath):
        os.remove(savePath)
    #download
    logging.info(f"download: {media_resource_url}, {audio_resource_url}")
    s = requests.session()
    s.keep_alive = False
    file = s.get(media_resource_url, verify=False)
    with open(savePath, "wb") as c:
        c.write(file.content)
    #merge audio & video
    if len(audio_resource_url) > 0:
        audioPath = os.path.join(rootDir, f"{name}.mp3")
        file1 = s.get(audio_resource_url)
        with open(audioPath, "wb") as c:
            c.write(file1.content)
        tmpPath = os.path.join(rootDir, f"{name}.mp4.mp4")
        utils.ffmpegProcess(f"-i {savePath} -i {audioPath} -vcodec copy -acodec copy -y {tmpPath}")
        if os.path.exists(tmpPath):
            os.remove(savePath)
            os.rename(tmpPath, savePath)
            os.remove(audioPath)
        logging.info(f"merge => {file}, {file1}")
    #cover
    coverPath = ""
    if media_type == "video":
        utils.processMoov(savePath)
        tttempPath = f"{savePath}.jpg"
        utils.ffmpegProcess(f"-i {savePath}  -ss 00:00:00.02 -frames:v 1 -y {tttempPath}")
        if os.path.exists(tttempPath):
            coverPath = tttempPath
    elif media_type == "image":
        # tttempPath = f"{savePath}.jpg"
        # shutil.copyfile(savePath, tttempPath)
        coverPath = savePath
        
    #upload
    savePathW, savePathH = localFileWithSize(media_type, savePath)
    url = utils.upload(savePath)
    ossurl = pathWithSize(url, savePathW, savePathH)
    cover_url = ""
    if os.path.exists(coverPath) and media_type == "video":
        coverW, coverH = localFileWithSize("image", coverPath)
        coverossurl = utils.upload(coverPath)
        cover_url = pathWithSize(coverossurl, coverW, coverH)
        os.remove(coverPath)
    elif os.path.exists(coverPath) and media_type == "image":
        cover_url = ossurl
        
    #publish
    logging.info(f"upload success, url = {ossurl}, cover = {cover_url}")
    s.close()
    os.remove(savePath)
    publish(media_type, post_text, ossurl, cover_url)
    
def processPosts(uuid, data):
    post_text = data["text"]
    medias = data["medias"]
    idx = 0
    for it in medias:
        media_type = it["media_type"]
        media_resource_url = it["resource_url"]
        audio_resource_url = ""
        if "formats" in it:
            formats = it["formats"]
            quelity = 0
            for format in formats:
                if format["quality"] > quelity and format["quality"] <= 1080:
                    quelity = format["quality"]
                    media_resource_url = format["video_url"]
                    audio_resource_url = format["audio_url"]
        try:
            download(f"{uuid}_{idx}", media_type, post_text, media_resource_url, audio_resource_url)
        except Exception as e:
            print(f"============== download+process+upload error! {str(e)}")
        idx += 1

def aaaapp(multiMedia, url, cursor, page):
    param = {
        "userId": "D042DA67F104FCB9D61B23DD14B27410",
        "secretKey": "b6c8524557c67f47b5982304d4e0bb85",
        "url": url,
        "cursor": cursor,
    }
    requestUrl = "https://h.aaaapp.cn/posts"
    # if "youtube.com/watch" in url or "youtube.com/shorts" in url or "instagram.com/p/" in url or "tiktok.com/t/" in url or "douyin.com/video" in url or "/video/" in url:
    #     isSingle = True
    if multiMedia == False:
        requestUrl = "https://h.aaaapp.cn/single_post"
    logging.info(f"=== request: {requestUrl} cursor={cursor}")
    s = requests.session()
    s.keep_alive = False
    res = s.post(requestUrl, params=param, verify=False)
    logging.info(f"=== res: {res.content}")
    if len(res.content) > 0:
        data = json.loads(res.content)
        if data["code"] == 200:
            idx = 0
            if multiMedia == False:
                processPosts(f"{curGroupId}_{page}_{idx}", data["data"])
            else:
                posts = data["data"]["posts"]
                for it in posts:
                    processPosts(f"{curGroupId}_{page}_{idx}", it)
                    idx+=1
            if "next_cursor" in data["data"] and len(data["data"]["next_cursor"]) > 0:
                if "no" not in data["data"]["next_cursor"]:
                    aaaapp(multiMedia, url, data["data"]["next_cursor"], page+1)
        else:
            notifyMessage(False, data["msg"])
    else:
        notifyMessage(False, "无法抓取")
    s.close()
    notifyMessage(True, "成功")

def main():
    if len(sys.argv) < 2:
        return
    
    global rootDir
    global curGroupId
    
    urllib3.disable_warnings()
    d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(filename=f"{thisFileDir}/mecord_crawler_{d}.log", 
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        encoding="utf-8",
                        level=logging.DEBUG)
    
    if sys.argv[1] == "test":
        curGroupId = 0
        aaaapp(False, "https://www.instagram.com/meowbot_iv/", "", 0)
        return
    if sys.argv[1] == "test1":
        utils.ffmpegTest()
        return
    
    rootDir = sys.argv[1]
    if os.path.exists(rootDir) == False:
        print(f"path {rootDir} is not exist")
        return
    while(os.path.exists(os.path.join(thisFileDir, "stop.now")) == False):
        try:
            s = requests.session()
            s.keep_alive = False
            res = s.get("https://beta.2tianxin.com/common/admin/mecord/get_task", verify=False)
            s.close()
            if len(res.content) > 0:
                data = json.loads(res.content)
                curGroupId = data["id"]
                logging.info(f"================ begin {curGroupId} ===================")
                logging.info(f"========== GetTask: {res.content}")
                link_url_list = data["link_url_list"]
                multiMedia = False
                if "is_set" in data:
                    multiMedia = data["is_set"]
                for s in link_url_list:
                    aaaapp(multiMedia, s, "", 0)
                print(f"complate => {curGroupId}")
                logging.info(f"================ end {curGroupId} ===================")
        except Exception as e:
            notifyMessage(False, str(e))
            logging.error("====================== uncatch Exception ======================")
            logging.error(e)
            logging.error("======================      end      ======================")
        time.sleep(10)
    os.remove(os.path.join(thisFileDir, "stop.now"))
    print(f"stoped !")
        
if __name__ == '__main__':
        main()

# urllib3.disable_warnings()
# d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# thisFileDir = os.path.dirname(os.path.abspath(__file__))
# logging.basicConfig(filename=f"{thisFileDir}/mecord_crawler_{d}.log", 
#                         format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         encoding="utf-8",
#                         level=logging.DEBUG)
# aaaapp(False, "https://www.tiktok.com/t/ZTRW3bfwQ/", "", 0)