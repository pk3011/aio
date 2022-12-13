from telegram.ext import CommandHandler

from bot import dispatcher
from bot.helper.poster_helper.poster_utils import amzn, nf, bd, imdb
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, psendMessage 
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.exceptions import DirectDownloadLinkException


def all_poster(update, context):
    mesg = update.message.text.split(maxsplit=2)
    is_amzn = False
    is_nf = False
    is_bd = False
    is_imdb = False

    if len(mesg) > 1:
        args = mesg[1].lower()
        link = mesg[2].strip()
    else:
        help_msg = f"<i>Send a title with arguments along with command to get its poster with Info.</i>\n\n<u>Instructions</u>\n<b>Currently Available Sites - \nNetflix, Amazon, Blu-ray & IMDb.</b>\n\nArguments for these sites:\n• Netflix - <code>nf</code>\n• Amazon - <code>amzn</code>\n• Blu-ray - <code>bd</code>\n• IMDb - <code>imdb</code>\n\nExample :\nNetflix 👉 <code>/poster nf Sacred games</code>\nAmazon 👉 <code>/poster amzn Mirzapur</code>\nBlu-ray 👉 <code>/poster bd Avengers</code>\nIMDb 👉 <code>/poster imdb Avatar</code>\n\nNote for IMDb : You can specify year with title for better results.\nExample - <code>/poster imdb Avatar (2009)</code>\nAnd you can also send IMDb link."  
        return sendMessage(help_msg, context.bot, update.message)
    
    if len(args) > 0:
        x = args.strip()
        if x == 'amzn':
            is_amzn = True
        elif x == 'nf':
            is_nf = True
        elif x == 'bd':
            is_bd = True
        elif x == 'imdb':
            is_imdb = True
                
    if update.message.from_user.username:
        tag = f"@{update.message.from_user.username}"
    else:
        tag = update.message.from_user.mention_html(update.message.from_user.first_name)
        
    try:
        if is_amzn:
            umsg = sendMessage(f"Searching for <b>{link}</b> on <b>Amazon</b>", context.bot, update.message)
            data = amzn(link)
            msg = f"Amazon Poster:\n{data['image']}\n\n{data['title']} ({data['year']})"
        elif is_nf:
            umsg = sendMessage(f"Searching for <b>{link}</b> on <b>Netflix</b>", context.bot, update.message)
            data = nf(link)
            msg = f"Netflix Poster:\n{data['image']}\n\n{data['title']} ({data['year']})"
        elif is_bd:
            umsg = sendMessage(f"Searching for <b>{link}</b> on <b>Blu-ray</b>", context.bot, update.message)
            data = bd(link)
            msg = data
        elif is_imdb:
            umsg = sendMessage(f"Searching for <b>{link}</b> on <b>IMDb</b>", context.bot, update.message)
            data = imdb(link)
            msg = f"{data['image']}\n\nTitle : {data['title']}\nRating : {data['rating']}"
        deleteMessage(context.bot, umsg)
    except DirectDownloadLinkException as e:
        deleteMessage(context.bot, umsg)
        sendMessage(str(e), context.bot, update.message)
    cc = f'\n\n<b>cc: </b>{tag}'
    psendMessage(msg + cc, context.bot, update.message)
    
    
poster_handler = CommandHandler(BotCommands.PosterCommand, all_poster,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)

dispatcher.add_handler(poster_handler)
