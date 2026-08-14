from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes


# =========================
# CONFIG
# =========================

BOT_USERNAME = "Aira_AIODownbot"
DEVELOPER_USERNAME = "oneofrisuofc"


# =========================
# START TEXT
# =========================

START_TEXT = {

    "id": (
        "👋 *Selamat datang di Aira Downloader* ⚡\n\n"

        "Satu bot untuk mengunduh berbagai media "
        "dari platform populer:\n\n"

        "🎬 YouTube\n"
        "🎵 TikTok\n"
        "📸 Instagram\n"
        "🐦 X / Twitter\n"
        "📌 Pinterest Video\n\n"

        "Cukup kirimkan tautan media, "
        "dan Aira akan memilih engine terbaik secara otomatis.\n\n"

        "📌 Perintah:\n"
        "🏓 /ping — Cek respons server\n\n"

        "👥 Dapat digunakan secara pribadi "
        "maupun di grup Telegram.\n\n"

        "⚡ *Powered By Aira Downloader*"
    ),


    "en": (
        "👋 *Welcome to Aira Downloader* ⚡\n\n"

        "One bot to download media "
        "from popular platforms:\n\n"

        "🎬 YouTube\n"
        "🎵 TikTok\n"
        "📸 Instagram\n"
        "🐦 X / Twitter\n"
        "📌 Pinterest Video\n\n"

        "Just send a media link, "
        "and Aira will automatically pick the best engine.\n\n"

        "📌 Commands:\n"
        "🏓 /ping — Check server response\n\n"

        "👥 Available for both private use "
        "and Telegram groups.\n\n"

        "⚡ *Powered By Aira Downloader*"
    )
}


# =========================
# HANDLER
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lang = "id"

    text = START_TEXT[lang]


    buttons = [
        [
            InlineKeyboardButton(
                "➕ Tambahkan ke Grup",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                "👨‍💻 Developer",
                url=f"https://t.me/{DEVELOPER_USERNAME}"
            )
        ]
    ]


    keyboard = InlineKeyboardMarkup(buttons)


    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )
