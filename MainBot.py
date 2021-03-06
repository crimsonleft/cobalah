"""
    YA GW TAU INI BELOM JADI
    maafkan segala dosaku kawan" ...
"""
from utilBot import ChopeBot
from telegram.ext import Filters
import utilDB
import utilBrowser
mainBot = None


def parrot(bot, update):
    print(update)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text)


def unknown_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="I can't understand your command")
    help_cmd(bot, update)


def help_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="some random ass command list")
    pass


def tgusername_check(bot, update):
    username = update.message.from_user.username
    if username is not None:
        return True
    return False


def ask_username(bot, update):
    global mainBot
    mainBot.ask(bot, update, "username apaan ?", ans_username)


def ans_username(bot, update):
    global mainBot
    utilDB.set_username(
        tgUsername=update.message.from_user.username,
        username=update.message.text)
    ask_password(bot, update)


def ask_password(bot, update):
    global mainBot
    mainBot.ask(bot, update, "password apaan ?", ans_password)


def ans_password(bot, update):
    global mainBot
    utilDB.set_password(
        tgUsername=update.message.from_user.username,
        password=update.message.text,
        chatID=update.message.chat_id)
    start_cmd(bot, update)


def login_check(bot, update):
    username = update.message.from_user.username
    chatID = update.message.chat_id

    usr = utilDB.get_username(username)
    pwd = utilDB.get_password(username, chatID)
    canLogin = utilBrowser.try_login(usr, pwd)
    return canLogin


def start_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Let me first run some checks")

    if not tgusername_check(bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text="bikin username dlu sana /start")
        return

    print("user have username")

    if not login_check(bot, update):
        ask_username(bot, update)
        return

    print("user can log in")

    bot.send_message(
        chat_id=update.message.chat_id,
        text="SUCCESSFUL")

    prio_cmd(bot, update)


def prio_cmd(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="here is the list of your prio")

    listPrio = utilDB.get_prio(update.message.from_user.username)

    msg = ""
    for key, val in listPrio.items():
        msg += str(key) + ": " + str(val) + "\n"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg)

    # keyboard = [
    #     [InlineKeyboardButton("Option 1", callback_data='1'),
    #     InlineKeyboardButton("Option 2", callback_data='2')],

    #         [InlineKeyboardButton("Option 3", callback_data='3')]]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    # update.message.reply_text('Please choose:', reply_markup=reply_markup)


def convo_handler(bot, update):
    global mainBot
    func = mainBot.phase(update)
    if (func is not None):
        func(bot, update)
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="tulis /start dong... kita may have baru abis reboot")

        bot.send_message(
            chat_id=update.message.chat_id,
            text="Baru on jam" + mainBot.firstOnline)


def main():
    global mainBot
    mainBot = ChopeBot('377140861:AAEiMIj-VOwB68HcftvMILjr5wc6LJJml6g')
    mainBot.handle_msg(Filters.text, convo_handler)
    mainBot.handle_cmd('start', start_cmd)
    mainBot.handle_cmd('prio', prio_cmd)
    mainBot.handle_cmd('help', help_cmd)
    mainBot.handle_msg(Filters.command, unknown_cmd)
    mainBot.deploy()


if __name__ == '__main__':
    main()
