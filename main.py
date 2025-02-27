import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


def reply(chat_id, text, bot):
    message_id = bot.send_message(chat_id, f"Запускаю таймер...")
    bot.create_countdown(
        parse(text),
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        bot=bot
    )
    bot.create_timer(parse(text), end_time, chat_id=chat_id, bot=bot)


def notify_progress(secs_left, chat_id, message_id, text, bot):
    rp = render_progressbar(parse(text), parse(text) - secs_left)
    bot.update_message(
        chat_id,
        message_id,
        f"Осталось {secs_left} секунд \n{rp}"
    )


def end_time(chat_id, bot):
    bot.send_message(chat_id, f"Время вышло")


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    load_dotenv()
    bot = ptbot.Bot(os.environ["TG_TOKEN"])
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()

if __name__ == "__main__":
    main()
