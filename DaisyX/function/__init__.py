import argparse
import asyncio
import os
import random
import shutil
import string
import time
from pathlib import Path

from DaisyX import ubot as borg
import hachoir
import requests
import wget
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from selenium import webdriver
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

headers = {"UserAgent": UserAgent().random}
import asyncio
import json
import math
import os
import re
import shlex
import subprocess
import time
import webbrowser
from os.path import basename
from typing import List, Optional, Tuple, Union

import eyed3
import requests
import telethon
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from pymediainfo import MediaInfo
from telethon import Button, custom, events, functions
from telethon.tl.types import InputMessagesFilterDocument, MessageMediaPhoto

from DaisyX.function.FastTelethon import download_file

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
BASE_URL = "https://isubtitles.org"
import os
import zipfile

import aiohttp

from DaisyX import TMP_DOWNLOAD_DIRECTORY
from DaisyX.function.FastTelethon import upload_file

session = aiohttp.ClientSession()

sedpath = TMP_DOWNLOAD_DIRECTORY


async def convert_to_image(event, borg):
    lmao = await event.get_reply_message()
    if not (
        lmao.gif
        or lmao.audio
        or lmao.voice
        or lmao.video
        or lmao.video_note
        or lmao.photo
        or lmao.sticker
        or lmao.media
    ):
        await event.edit("`Format Not Supported.`")
        return
    else:
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                lmao.media,
                sedpath,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "`Downloading...`")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "Downloaded to `{}` successfully.".format(downloaded_file_name)
            )
    if not os.path.exists(downloaded_file_name):
        await event.edit("Download Unsucessfull :(")
        return
    if lmao and lmao.photo:
        lmao_final = downloaded_file_name
    elif lmao.sticker and lmao.sticker.mime_type == "application/x-tgsticker":
        rpath = downloaded_file_name
        image_name20 = os.path.join(sedpath, "SED.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {downloaded_file_name} {image_name20}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(rpath)
        lmao_final = image_name20
    elif lmao.sticker and lmao.sticker.mime_type == "image/webp":
        pathofsticker2 = downloaded_file_name
        image_new_path = sedpath + "image.png"
        os.rename(pathofsticker2, image_new_path)
        if not os.path.exists(image_new_path):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = image_new_path
    elif lmao.audio:
        sed_p = downloaded_file_name
        hmmyes = sedpath + "stark.mp3"
        imgpath = sedpath + "starky.jpg"
        os.rename(sed_p, hmmyes)
        await runcmd(f"ffmpeg -i {hmmyes} -filter:v scale=500:500 -an {imgpath}")
        os.remove(sed_p)
        if not os.path.exists(imgpath):
            await event.edit("`Wasn't Able To Fetch Shot.`")
            return
        lmao_final = imgpath
    elif lmao.gif or lmao.video or lmao.video_note:
        sed_p2 = downloaded_file_name
        jpg_file = os.path.join(sedpath, "image.jpg")
        await take_screen_shot(sed_p2, 0, jpg_file)
        os.remove(sed_p2)
        if not os.path.exists(jpg_file):
            await event.edit("`Couldn't Fetch. SS`")
            return
        lmao_final = jpg_file
    await event.edit("`Almost Completed.`")
    return lmao_final


async def apk_dl(app_name, path, event):
    await event.edit(
        "`Searching, For Apk File. This May Take Time Depending On Your App Size`"
    )
    res = requests.get(f"https://m.apkpure.com/search?q={app_name}")
    soup = BeautifulSoup(res.text, "html.parser")
    result = soup.select(".dd")
    for link in result[:1]:
        s_for_name = requests.get("https://m.apkpure.com" + link.get("href"))
        sfn = BeautifulSoup(s_for_name.text, "html.parser")
        ttl = sfn.select_one("title").text
        noneed = [" - APK Download"]
        for i in noneed:
            name = ttl.replace(i, "")
            res2 = requests.get(
                "https://m.apkpure.com" + link.get("href") + "/download?from=details"
            )
            soup2 = BeautifulSoup(res2.text, "html.parser")
            result = soup2.select(".ga")
        for link in result:
            dl_link = link.get("href")
            r = requests.get(dl_link)
            with open(f"{path}/{name}@DaisyXBot.apk", "wb") as f:
                f.write(r.content)
    await event.edit("`Apk, Downloaded. Let me Upload It here.`")
    final_path = f"{path}/{name}@DaisyXBot.apk"
    return final_path, name


async def _ytdl(url, is_it, event, tgbot):
    await event.edit(
        "`Ok Downloading This Video / Audio - Please Wait.` \n**Powered By @DaisyXbot**"
    )
    if is_it:
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "480",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    else:
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except Exception as e:
        await event.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    if song:
        file_stark = f"{ytdl_data['id']}.mp3"
        lol_m = await upload_file(
            file_name=f"{ytdl_data['title']}.mp3",
            client=tgbot,
            file=open(file_stark, "rb"),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "Uploading Youtube Audio..", file_stark)
            ),
        )
        await event.edit(
            file=lol_m, text=f"{ytdl_data['title']} \n**Uploaded Using @FRidayOt**"
        )
        os.remove(file_stark)
    elif video:
        file_stark = f"{ytdl_data['id']}.mp4"
        lol_m = await upload_file(
            file_name=f"{ytdl_data['title']}.mp4",
            client=tgbot,
            file=open(file_stark, "rb"),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "Uploading Youtube Video..", file_stark)
            ),
        )
        await event.edit(
            file=lol_m, text=f"{ytdl_data['title']} \n**Uploaded Using @FRidayOt**"
        )
        os.remove(file_stark)


async def _deezer_dl(word, event, tgbot):
    await event.edit(
        "`Ok Downloading This Audio - Please Wait.` \n**Powered By @DaisyXBot**"
    )
    urlp = f"https://starkapi.herokuapp.com/deezer/{word}"
    datto = requests.get(url=urlp).json()
    mus = datto.get("url")
    mello = datto.get("artist")
    # thums = urlhp["album"]["cover_medium"]
    sname = f"""{datto.get("title")}.mp3"""
    doc = requests.get(mus)
    with open(sname, "wb") as f:
        f.write(doc.content)
    car = f"""
**Song Name :** {datto.get("title")}
**Duration :** {datto.get('duration')} Seconds
**Artist :** {mello}
Music Downloaded And Uploaded By @DaisyXBot
Please Share and support @DaisyXBot"""
    await event.edit("Song Downloaded.  Waiting To Upload. 🥳🤗")
    c_time = time.time()
    uploaded_file = await upload_file(
        file_name=sname,
        client=tgbot,
        file=open(sname, "rb"),
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "Uploading..", sname)
        ),
    )

    await event.edit(file=uploaded_file, text=car)
    os.remove(sname)
