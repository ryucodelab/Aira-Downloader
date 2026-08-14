import time

from telegram import Update
from telegram.ext import ContextTypes


# =========================
# /PING
# =========================

async def ping(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    start_time = time.monotonic()

    msg = await update.message.reply_text(
        "🏓 Mengukur respons server..."
    )

    latency = (
        time.monotonic() - start_time
    ) * 1000

    latency_ms = round(latency)

    await msg.edit_text(
        f"🏓 *Pong!*\n\n"
        f"⚡ Respons: `{latency_ms}ms`",
        parse_mode="Markdown"
    )
