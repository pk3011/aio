import os
import re
import requests
import mimetypes
from urllib.parse import unquote_plus
from telegram.ext import CommandHandler
from subprocess import run
from threading import Thread
from bot import dispatcher
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, sendMarkup
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.ext_utils.bot_utils import get_readable_file_size, new_thread
from bot.helper.ext_utils.telegraph_helper import telegraph


def extract_mediainfo(message, bot):
    args = message.text.split()
    reply_to = message.reply_to_message
    link = ''
    if len(args) > 1:
        link = args[1].strip()
        if message.from_user.username:
            tag = f"@{message.from_user.username}"
        else:
            tag = message.from_user.mention_html(message.from_user.first_name)
    elif reply_to:
        if len(link) == 0:
            link = reply_to.text.split(maxsplit=1)[0].strip()
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    else:
        return sendMessage(f"Send a streamable link along with command or by replying to the link by command!", bot, message)
    __response = requests.head(link, stream=True)
    msg = sendMessage(f"<b>Getting MediaInfo of </b>\n<code>{link}</code>", bot, message)
    try:
        file_size = get_readable_file_size(int(__response.headers["Content-Length"].strip()))
        file_name = unquote_plus(link).rsplit('/', 1)[-1]
        mime_type = __response.headers.get("Content-Type", mimetypes.guess_type(file_name)).rsplit(";", 1)[0]
        result = run(f'mediainfo "{link}"', capture_output=True, shell=True)
        stderr = result.stderr.decode('utf-8')
        stdout = result.stdout.decode('utf-8')
        metadata = re.sub(
            rf"http(s)?://.*\.{link.rsplit('.', 1)[-1]}",
            file_name, stdout.replace("\r", "")
        )
        html = "<h3>Metadata of {}</h3>" \
               "<br><br>" \
               "<pre>{}</pre>"
        page = telegraph.create_page(
            title="Mediainfo by MirrorRage",
            content=html.format(file_name, metadata)
        )
        buttons = ButtonMaker()
        buttons.buildbutton("MediaInfo", page['url'])
        button = buttons.build_menu(1)
        deleteMessage(bot, msg)
        sendMarkup(
            f"<b>File Name:</b> <code>{file_name}</code>\n"
            f"<b>File Size:</b> <code>{file_size}</code>\n"
            f"<b>Type:</b> <code>{mime_type}</code>\n"
            f"\n<b>cc:</b> {tag}",
            bot, message, button
        )
    except KeyError:
        deleteMessage(bot, msg)
        sendMessage("Not a valid direct downloadable video!", bot, message)
    except Exception as err:
        deleteMessage(bot, msg)
        sendMessage(f"Error: <code>{err}</code>", bot, message)


@new_thread
def mediainfo_cmd_handler(update, context):
    extract_mediainfo(update.message, context.bot)


mi_cmd_handler = CommandHandler(
    BotCommands.MediaInfoCommand,
    mediainfo_cmd_handler,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True
)
dispatcher.add_handler(mi_cmd_handler)
