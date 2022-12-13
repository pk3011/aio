import time
import re
from requests import get as rget
from threading import Thread
from bs4 import BeautifulSoup

from asyncio import run
from telegram.ext import CommandHandler

from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot import dispatcher
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import is_psa_link, is_mkv_link, is_pmz_link, is_toon_link, is_ola_link, is_katmoviehd_link, is_hdhub4u_link, is_vega_link, is_gdrive_link, is_gdtot_link, new_thread
from bot.helper.fucking_utils.fucking import psa, gtl, sora_main, pmz, toon, ola_main, vega
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException
from bot.helper.mirror_utils.download_utils.direct_link_generator import gdtot

@new_thread
def _fuck(update, context):
    reply_to = update.message.reply_to_message
    source_link = ''
    bypassed_link = ''
    if len(context.args) == 1:
        source_link = context.args[0]
        if update.message.from_user.username:
            tag = f"@{update.message.from_user.username}"
        else:
            tag = update.message.from_user.mention_html(update.message.from_user.first_name)
    if reply_to:
        if len(source_link) == 0:
            source_link = reply_to.text.split(maxsplit=1)[0].strip()
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    is_psa = is_psa_link(source_link)
    is_mkv = is_mkv_link(source_link)
    is_pmz = is_pmz_link(source_link)
    is_toon = is_toon_link(source_link)
    is_ola = is_ola_link(source_link)
    is_katmoviehd = is_katmoviehd_link(source_link)
    is_hdhub4u = is_hdhub4u_link(source_link)
    is_vega = is_vega_link(source_link)

    if (is_psa or is_mkv or is_pmz or is_toon or is_ola or is_hdhub4u or is_katmoviehd or is_vega):
        try:
            msg = sendMessage(f"<b>Bypassing: </b><code>{source_link}</code>", context.bot, update.message)
            start=time.perf_counter()
            if is_psa:
                bypassed_link = psa(source_link)
                name = "PSA"
            if (is_mkv or is_katmoviehd or is_hdhub4u):
                bypassed_link = run(sora_main(rget(source_link).url,12))
                if is_mkv:
                    name = "MkvCinemas"
                if is_katmoviehd:
                    name = "KatMovieHd"
                if is_hdhub4u:
                    name = "HdHub4u"
            if is_pmz:
                bypassed_link = pmz(source_link)
                name = "PrivateMoviez"
            if is_toon:
                bypassed_link = toon(source_link)
                name = "ToonWorld4all"
            if is_ola:
                bypassed_link = run(ola_main(source_link))[0]
                name = "OlaMovies"
            if is_vega:
                bypassed_link = vega(source_link)
                name = "VegaMovies"
            end=time.perf_counter()
            deleteMessage(context.bot, msg)
            msg = f"<b><u>{name} Bypass</u></b>\n\n<b><a href='{source_link}'>Source Link</a></b>\n<b>Bypassed Link - {bypassed_link}</b>\n"
            cc = f'\n<b>cc: </b>{tag}'
            eta = f"\n<b>Elapsed:</b> {int(end-start)}s"
            sendMessage(msg + cc + eta, context.bot, update.message)
        except:
            deleteMessage(context.bot, msg)
            sendMessage("ERROR: Something went wrong, Please try again!", context.bot, update.message)
    else:
        msg = f"Send a valid link along with command or by replying to the link by command\n\nCurrently Supported Sites:\n• PSA\n• MkvCinemas\n• ToonWorld4all\n• PrivateMoviez\n• OlaMovies\n• KatMovieHD\n• HdHub4u\n• VegaMovies\n\nNote - Send a Single link by copying from above mentioned sites."
        sendMessage(msg, context.bot, update.message)
    if is_gdtot_link(bypassed_link):
        try:
            msg = sendMessage(f"Processing: <code>{bypassed_link}</code>", context.bot, update.message)
            bypassed_link = gdtot(bypassed_link)
            deleteMessage(context.bot, msg)
        except DirectDownloadLinkException as e:
            deleteMessage(context.bot, msg)
            return sendMessage(str(e), context.bot, update.message)
    if is_gdrive_link(bypassed_link):
        gd = GoogleDriveHelper()
        res, size, name, files = gd.helper(bypassed_link)
        if res != "":
            return sendMessage(res, context.bot, update.message)
        msg = sendMessage(f"Cloning: <code>{bypassed_link}</code>", context.bot, update.message)
        result, button = gd.clone(bypassed_link)
        deleteMessage(context.bot, msg)
        cc = f'\n\n<b>cc: </b>{tag}'
        sendMessage(result + cc, context.bot, update.message)


fuck_handler = CommandHandler(BotCommands.FuckCommand, _fuck,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(fuck_handler)
