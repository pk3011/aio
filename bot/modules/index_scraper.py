from telegram.ext import CommandHandler
from threading import Thread
from bot import dispatcher
from bot.helper.index_scrape_helper.index_scrape_utils import main
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, sendMarkup
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.ext_utils.bot_utils import get_readable_file_size, new_thread
from bot.helper.ext_utils.telegraph_helper import telegraph


def index_scrape(message, bot):
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
        return sendMessage(f"Send a Bhadoo Index Folder link along with command.", bot, message)
    msg = sendMessage(f"Scraping links from \n<code>{link}</code>", bot, message)
    try:
        source_link = f"<a href='{link}'>Source Index Link</a>"
        index_links_page = main(link)
        no_of_links = index_links_page.count("href")
        html = "<h3>{}</h3>" \
               "<br><br>" \
               "<pre>{}</pre>"
        page = telegraph.create_page(
            title="Index Scraper by MirrorRage",
            content=html.format(source_link, index_links_page)
        )
        buttons = ButtonMaker()
        buttons.buildbutton("Scraped Links", page['url'])
        button = buttons.build_menu(1)
        deleteMessage(bot, msg)
        sendMarkup(
            f"<b><i><u>Index Scraper</u></i></b>\n\n"
            f"<b>{source_link}</b>\n"
            f"<b><i>Number of links:</i></b> <code>{no_of_links}</code>"
            f"\n\n<b>cc:</b> {tag}",
            bot, message, button
        )
    except Exception as err:
        deleteMessage(bot, msg)
        sendMessage(f"Error: <code>{err}</code>", bot, message)


@new_thread
def _index_scrape_handler(update, context):
    index_scrape(update.message, context.bot)


index_scrape_handler = CommandHandler(
    BotCommands.IndexScrapeCommand,
    _index_scrape_handler,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True
)
dispatcher.add_handler(index_scrape_handler)
