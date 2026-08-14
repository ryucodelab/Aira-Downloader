import os
import logging

from dotenv import load_dotenv

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)


from modules.start import start
from modules.system import (
    ping,
)

from modules.downloader import (
    handle_download,
    youtube_callback,
)



# =========================
# CONFIG
# =========================

load_dotenv()


BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)



# =========================
# LOGGING
# =========================

logging.basicConfig(
    format=
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO
)


logger = logging.getLogger(
    "AiraAIO"
)



# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:

        raise ValueError(
            "BOT_TOKEN belum diisi di .env"
        )


    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )


    # COMMAND

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "ping",
            ping
        )
    )



    # YOUTUBE BUTTON

    app.add_handler(
        CallbackQueryHandler(
            youtube_callback,
            pattern="^yt_"
        )
    )



    # DOWNLOAD ENGINE

    app.add_handler(
        MessageHandler(
            filters.TEXT
            &
            ~filters.COMMAND,
            handle_download
        )
    )



    logger.info(
        "⚡ Aira AIO Downloader aktif"
    )


    app.run_polling()



if __name__ == "__main__":

    main()
