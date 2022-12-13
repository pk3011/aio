import os
import time
from telegram.ext import CommandHandler

from bot import dispatcher
from bot.helper.bypass_utils.regex_helper import *
from bot.helper.bypass_utils.bypass_helper import *
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, deleteMessage, editMessage
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException
from bot.helper.ext_utils.telegraph_helper import telegraph

def _bypass(update, context):
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
    is_shortener_type_one = is_shortener_type_one_link(link)
    is_shortener_type_two = is_shortener_type_two_link(link)
    is_bitly = is_bitly_link(link)
    is_gtlinks = is_gtlinks_link(link)
    is_ouo = is_ouo_link(link)
    is_pkin = is_pkin_link(link)
    is_shareus = is_shareus_link(link)
    is_shortest = is_shortest_link(link)
    is_shortly = is_shortly_link(link)
    is_sirigan = is_sirigan_link(link)
    is_thinfi = is_thinfi_link(link)
    is_tinyurl = is_tinyurl_link(link)
    is_try2link = is_try2link_link(link)
    is_linkvertise = is_linkvertise_link(link)
    is_adfly = is_adfly_link(link)
    is_gplink = is_gplink_link(link)
    if (is_shortener_type_one or is_shortener_type_two or is_bitly or is_gtlinks or is_ouo or is_pkin or is_shareus or is_shortest or is_shortly or is_sirigan or is_thinfi or is_tinyurl or is_try2link or is_linkvertise or is_adfly or is_gplink):
        msg = sendMessage(f"<b>Processing: </b><code>{link}</code>\n<b>Please wait...</b>", context.bot, update.message)
        start=time.perf_counter()
        try:
            if is_shortener_type_one:
                blink = shortner_type_one_bypass_handler(link)
            elif is_shortener_type_two:
                blink = shortner_type_two_bypass_handler(link)
            elif is_bitly:
                blink = bitly_bypass(link)
            elif is_gtlinks:
                blink = gtlinks_bypass(link)
            elif is_ouo:
                blink = ouo_bypass(link)
            elif is_pkin:
                blink = pkin_bypass(link)
            elif is_shareus:
                blink = shareus_bypass(link)
            elif is_shortest:
                blink = shortest_bypass(link)
            elif is_shortly:
                blink = shortly_bypass(link)
            elif is_sirigan:
                blink = sirigan_bypass(link)
            elif is_thinfi:
                blink = thinfi_bypass(link)
            elif is_tinyurl:
                blink = tinyurl_bypass(link)
            elif is_try2link:
                blink = try2link_bypass(link)
            elif is_linkvertise:
                blink = linkvertise_bypass(link)
            elif is_adfly:
                blink = adfly_bypass(link)
            elif is_gplink:
                blink = gplinks_bypass(link)
            deleteMessage(context.bot, msg)
            end=time.perf_counter()
            bmsg = f"<b><i>Shortener Bypass</i></b>\n\n<b>Source Link: {link}</b>\n\n<b>Bypassed Link: {blink}</b>\n\n<b>Elapsed:</b> {int(end-start)}s\n\n<b>cc: {tag}</b>"
            sendMessage(bmsg, context.bot, update.message)
        except:
            deleteMessage(context.bot, msg)
            sendMessage(f"{tag}\nERROR: Something went wrong while bypassing this link.\nPlease check your link and try again.", context.bot, update.message)
    else:
        title = "Supported Sites"
        s_links = "• gplinks.co, try2link.com, adf.ly, bit.ly, ouo.io, ouo.press, shareus.in, shortly.xyz, tinyurl.com, thinfi.com, sirigan.my.id, gtlinks.me, linkvertise.com, shorte.st, earn4link.in, tekcrypt.in, link.short2url.in, go.rocklinks.net, rocklinks.net, earn.moneykamalo.com, m.easysky.in, indianshortner.in, open.crazyblog.in, link.tnvalue.in, shortingly.me, open2get.in, dulink.in, bindaaslinks.com, za.uy, pdiskshortener.com, mdiskshortner.link, go.earnl.xyz, g.rewayatcafe.com, ser2.crazyblog.in, bitshorten.com, rocklink.in, droplink.co, tnlink.in, ez4short.com, vearnl.in, adrinolinks.in, techymozo.com, linkbnao.com, linksxyz.in, short-jambo.com, ads.droplink.co.in, linkpays.in, pi-l.ink, link.tnlink.in, pkin.me"
        html = "<h3>{}</h3>" \
                    "<br><br>" \
                    "<pre>{}</pre>"
        page = telegraph.create_page(
            title="Shortener Bypass by MirrorRage",
            content=html.format(title, s_links.replace(",","\n•"))
        )
        buttons = ButtonMaker()
        buttons.buildbutton("Supported Sites", page['url'])
        button = buttons.build_menu(1)
        sendMarkup("Send a supported site link along with command or by replying to the link by command to bypass.\n\nClick below button to see supported sites.", context.bot, update.message, button)
bypass_handler = CommandHandler(BotCommands.BypassCommand, _bypass,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(bypass_handler)
