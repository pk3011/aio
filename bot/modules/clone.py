from random import SystemRandom
from string import ascii_letters, digits
from telegram.ext import CommandHandler
from threading import Thread
from time import sleep
from re import findall as re_findall

from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, delete_all_messages, update_all_messages, sendStatusMessage, sendMarkup
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.status_utils.clone_status import CloneStatus
from bot import dispatcher, LOGGER, download_dict, download_dict_lock, Interval, config_dict
from bot.helper.ext_utils.bot_utils import is_gdrive_link, is_gdtot_link, is_appdrive_link, is_hubdrive_link, is_sharer_link, is_filepress_link, new_thread
from bot.helper.mirror_utils.download_utils.direct_link_generator import gdtot, temp_appdrive, hubdrive, sharer, filepress
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException


def _clone(message, bot):
    args = message.text.split(" ", maxsplit=2)
    reply_to = message.reply_to_message
    link = ''
    multi = 0
    if len(args) > 1:
        link = args[1]
        if link.strip().isdigit():
            multi = int(link)
            link = ''
        elif message.from_user.username:
            tag = f"@{message.from_user.username}"
        else:
            tag = message.from_user.mention_html(message.from_user.first_name)
    elif reply_to:
        if len(link) == 0:
            link = reply_to.text
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    else:
        sendMessage("Send valid link along with command or by replying to the link by command\n\n<b>Supported sites:</b>\n• Gdrive\n• Gdtot\n• AppDrive and similar sites\n• HubDrive\n• DriveHub\n• Kolop\n• Katdrive\n• Sharer\n• FilePress\n\n<b>Instructions:</b>\nIf no. of links is greater than 1 & it contains some text also then send command by replying to that message.", bot, message)
    links = re_findall(r'(https?://\S+)', link)
    results = ''
    for link in links:
        is_gdtot = is_gdtot_link(link)
        is_appdrive = is_appdrive_link(link)
        is_hubdrive = is_hubdrive_link(link)
        is_sharer = is_sharer_link(link)
        is_filepress = is_filepress_link(link)
        if (is_gdtot or is_appdrive or is_hubdrive or is_sharer or is_filepress):
            msg = sendMessage(f"Processing: <code>{link}</code>", bot, message)
            try:
                if is_gdtot:
                    link = gdtot(link)
                if is_appdrive:
                    link = temp_appdrive(link)
                if is_hubdrive:
                    link = hubdrive(link)
                if is_sharer:
                    link = sharer(link)
                if is_filepress:
                    link = filepress(link)
                deleteMessage(bot, msg)
            except DirectDownloadLinkException as e:
                deleteMessage(bot, msg)
                sendMessage(str(e), bot, message)
                continue
        if is_gdrive_link(link):
            gd = GoogleDriveHelper()
            res, size, name, files = gd.helper(link)
            if res != "":
                sendMessage(res, bot, message)
                continue
            if config_dict['STOP_DUPLICATE']:
                LOGGER.info('Checking File/Folder if already in Drive...')
                smsg, button = gd.drive_list(name, True, True)
                if smsg:
                    msg = "File/Folder is already available in Drive.\nHere are the search results:"
                    sendMarkup(msg, bot, message, button)
                    continue
            if multi > 1:
                sleep(4)
                nextmsg = type('nextmsg', (object, ), {'chat_id': message.chat_id, 'message_id': message.reply_to_message.message_id + 1})
                cmsg = message.text.split()
                cmsg[1] = f"{multi - 1}"
                nextmsg = sendMessage(" ".join(cmsg), bot, nextmsg)
                nextmsg.from_user.id = message.from_user.id
                sleep(4)
                Thread(target=_clone, args=(nextmsg, bot)).start()
            if files <= 20:
                msg = sendMessage(f"Cloning: <code>{link}</code>", bot, message)
                result, button = gd.clone(link)
                deleteMessage(bot, msg)
            else:
                drive = GoogleDriveHelper(name)
                gid = ''.join(SystemRandom().choices(ascii_letters + digits, k=12))
                clone_status = CloneStatus(drive, size, message, gid)
                with download_dict_lock:
                    download_dict[message.message_id] = clone_status
                sendStatusMessage(message, bot)
                result, button = drive.clone(link)
                with download_dict_lock:
                    del download_dict[message.message_id]
                    count = len(download_dict)
                try:
                    if count == 0:
                        Interval[0].cancel()
                        del Interval[0]
                        delete_all_messages()
                    else:
                        update_all_messages()
                except IndexError:
                    pass
            results += result + "\n\n"
    cc = f'<b>cc: </b>{tag}'
    if button in ["cancelled", ""]:
        sendMessage(f"{tag} {results}", bot, message)
    else:
        sendMessage(results + cc, bot, message)
        LOGGER.info(f'Cloning Done: {name}')

@new_thread
def cloneNode(update, context):
    _clone(update.message, context.bot)

clone_handler = CommandHandler(BotCommands.CloneCommand, cloneNode,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(clone_handler)
