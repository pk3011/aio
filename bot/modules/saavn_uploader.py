import os
from telegram.ext import CommandHandler

from bot import dispatcher, bot, DOWNLOAD_DIR
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, editMessage
from bot.helper.ext_utils.fs_utils import get_media_info, get_path_size
from bot.helper.ext_utils.bot_utils import get_readable_file_size, is_saavn_link
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException
from bot.helper.saavn_utils.saavn_downloader import download

def saavn(update, context):
    reply_to = update.message.reply_to_message
    link = ''
    if len(context.args) == 1:
        link = context.args[0]
        if update.message.from_user.username:
            tag = f"@{update.message.from_user.username}"
        else:
            tag = update.message.from_user.mention_html(update.message.from_user.first_name)
    if reply_to:
        if len(link) == 0:
            link = reply_to.text.split(maxsplit=1)[0].strip()
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    if is_saavn_link(link):
        try:
            msg = sendMessage(f"<b>Downloading</b> <code>{link}</code> <b>from JioSaavn</b>", context.bot, update.message)
            thumb, file_path = download(link)
            file_name = file_path.split("/")[-1]
            cap_mono = f"<code>{file_name}</code>"
            size = get_readable_file_size(get_path_size(file_path))
            duration , artist, title = get_media_info(file_path)
            emsg = f"Downloading complete of <b>{file_name}</b>\nNow trying to upload."
            editMessage(emsg, msg)
            context.bot.sendAudio(audio=open(file_path, 'rb'),
                                allow_sending_without_reply=True,
                                parse_mode='HTML', 
                                caption=cap_mono, 
                                duration=duration, 
                                thumb=open(thumb, 'rb'), 
                                title=file_name, 
                                performer=artist,
                                reply_to_message_id=update.message.message_id,
                                chat_id=update.message.chat_id)
            deleteMessage(context.bot, msg)
            cc = f"\n\n<b>cc: </b>{tag}"
            umsg = f"<b><a href='{link}'>JioSaavn URL</a></b>\n<b>Name:</b> {cap_mono}\n<b>Size:</b> <code>{size}</code>"
            sendMessage(umsg + cc, context.bot, update.message)                     
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            sendMessage(str(e), context.bot, update.message)
        try:
            os.remove(file_path)
            os.remove(thumb)
        except:
            pass
    else:
        sendMessage("Send a valid JioSaavn link along with command or by replying to the link by command", context.bot, update.message)
saavn_handler = CommandHandler(BotCommands.SaavnCommand, saavn,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(saavn_handler)
