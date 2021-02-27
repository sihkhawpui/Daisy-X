# @UniBorg
# Friday Userbot
# InukaAsith
import asyncio
import math
import os
import time
from datetime import datetime
from urllib.parse import urlparse

import requests
from pySmartDL import SmartDL

from DaisyX.function.FastTelethon import upload_file


@tbot.on(events.NewMessage(pattern="^/smartdl"))
async def _(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    input_str = event.raw_text.split(" ", maxsplit=1)[1]
    mone = await event.edit("**Processing..**")
    start = datetime.now()
    url = input_str
    a = urlparse(input_str)
    file_name = os.path.basename(a.path)
    to_download_directory = TEMP_DOWNLOAD_DIRECTORY
    downloaded_file_name = os.path.join(to_download_directory, file_name)
    downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    display_message = ""
    c_time = time.time()
    while not downloader.isFinished():
        total_length = downloader.filesize if downloader.filesize else None
        downloaded = downloader.get_dl_size()
        now = time.time()
        diff = now - c_time
        percentage = downloader.get_progress() * 100
        downloader.get_speed()
        round(diff) * 1000
        progress_str = "[{0}{1}]\nProgress: {2}%".format(
            "".join(["▰" for i in range(math.floor(percentage / 5))]),
            "".join(["▱" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )
        estimated_total_time = downloader.get_eta(human=True)
        try:
            current_message = f"trying to download\n"
            current_message += f"URL: {url}\n"
            current_message += f"File Name: {file_name}\n"
            current_message += f"{progress_str}\n"
            current_message += (
                f"{humanbytes(downloaded)} of {humanbytes(total_length)}\n"
            )
            current_message += f"ETA: {estimated_total_time}"
            if round(diff % 10.00) == 0 and current_message != display_message:
                await mone.reply(current_message)
                display_message = current_message
        except Exception as e:
            logger.info(str(e))
    end = datetime.now()
    ms = (end - start).seconds
    if downloader.isSuccessful():
        c_time = time.time()
        lul = await mone.reply(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        lol_m = await upload_file(
            file_name=file_name,
            client=borg,
            file=open(downloaded_file_name, "rb"),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading This File.", downloaded_file_name
                )
            ),
        )
        await borg.send_file(
            event.chat_id,
            lol_m,
            caption=file_name,
            force_document=False,
            allow_cache=False,
        )
        await lul.delete()
        os.remove(downloaded_file_name)
    else:
        await mone.reply("Incorrect URL\n {}".format(input_str))


#    Copyright (C) Midhun Km 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


@friday.on(friday_on_cmd(pattern="zeelink"))
async def lol_kangers(event):
    if event.fwd_from:
        return
    input_str = event.raw_text.split(" ", maxsplit=1)[1]
    if "zee" in input_str:
        url = "http://devsexpo.me/zee/"
        sed = {"url": input_str}
        lmao = requests.get(url=url, headers=sed).json()
    else:
        await event.reply("Only Zee Videos Supported.")
        return
    if lmao["success"] is False:
        await event.reply("Task Failed Due To " + str(lmao["error"]))
        return
    await event.reply("Direct Link Fetched \nURL : " + str(lmao["url"]))
