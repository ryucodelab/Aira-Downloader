import os
import re
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReactionTypeEmoji,
)

from telegram.ext import (
    ContextTypes,
)

from modules.sosmed import download_social
from modules.youtube import download_youtube
from modules.photo import download_photo


logger = logging.getLogger(
    "AiraDownloader"
)


URL_PATTERN = re.compile(
    r"(https?://\S+)"
)



# =========================
# PLATFORM DETECTION
# =========================

def detect_engine(url):

    url = url.lower()


    if (
        "youtube.com" in url
        or "youtu.be" in url
    ):
        return "youtube"



    if any(
        x in url
        for x in [
            "tiktok.com",
            "instagram.com",
            "x.com",
            "twitter.com",
            "pinterest.com",
            "pin.it",
            "facebook.com",
            "fb.watch"
        ]
    ):
        return "social"



    return None





def detect_platform(url):

    url = url.lower()



    if (
        "youtube" in url
        or "youtu.be" in url
    ):
        return "YouTube"



    if "tiktok" in url:
        return "TikTok"



    if "instagram" in url:
        return "Instagram"



    if (
        "x.com" in url
        or "twitter.com" in url
    ):
        return "X"



    if (
        "pinterest" in url
        or "pin.it" in url
    ):
        return "Pinterest"



    if (
        "facebook.com" in url
        or "fb.watch" in url
    ):
        return "Facebook"



    return "Unknown"





# =========================
# REACTION
# =========================

async def react(
    update,
    emoji
):

    try:

        await update.message.set_reaction(
            reaction=[
                ReactionTypeEmoji(
                    emoji=emoji
                )
            ]
        )


    except Exception as e:

        logger.warning(
            f"Reaction gagal: {e}"
        )





def social_reaction(platform):

    return {

        "TikTok": "⚡",

        "Instagram": "🤩",

        "X": "🤔",

        "Pinterest": "🔥",

        "Facebook": "👍"

    }.get(
        platform,
        "⚡"
    )





# =========================
# CAPTION
# =========================

def build_caption(
    title,
    source,
    user,
    media_type="video",
    owner=None
):

    username = (
        f"@{user.username}"
        if user.username
        else user.first_name
    )


    icon = (
        "📸"
        if media_type == "photo"
        else "🎬"
    )


    owner_line = (
        f"📤 Post By: {owner}\n\n"
        if owner
        else ""
    )


    return (
        f"{owner_line}"

        f"{icon} *{title}*\n\n"

        f"📥 Sumber: {source}\n"
        f"👤 Peminta: {username}\n\n"

        f"⚡ Powered By Aira Downloader"
    )





# =========================
# SEND PHOTOS
# =========================

async def send_photos(
    update,
    images,
    caption
):

    if len(images) == 1:

        await update.message.reply_photo(
            photo=images[0],
            caption=caption,
            parse_mode="Markdown"
        )


        return



    media = [
        InputMediaPhoto(media=img)
        for img in images[:10]
    ]


    media[0] = InputMediaPhoto(
        media=media[0].media,
        caption=caption,
        parse_mode="Markdown"
    )


    await update.message.reply_media_group(
        media
    )



# =========================
# YOUTUBE MENU
# =========================

async def youtube_menu(
    update,
    url
):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎵 Audio",
                    callback_data=f"yt_audio|{url}"
                ),

                InlineKeyboardButton(
                    "🎬 Video",
                    callback_data=f"yt_video|{url}"
                )
            ]
        ]
    )


    await update.message.reply_text(
        "▶️ *YouTube terdeteksi*\n\n"
        "Pilih format yang ingin diunduh:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )





# =========================
# YOUTUBE CALLBACK
# =========================

async def youtube_callback(
    update,
    context
):

    query = update.callback_query


    await query.answer()



    action, url = query.data.split(
        "|",
        1
    )


    mode = action.replace(
        "yt_",
        ""
    )



    status = await query.edit_message_text(
        "⚡ Permintaan diterima.\n\n"
        "⬇️ Sedang mengunduh media..."
    )



    filepath = None



    try:

        filepath, title, media = download_youtube(
            url,
            mode
        )



        caption = build_caption(
            title,
            "YouTube",
            query.from_user
        )



        with open(
            filepath,
            "rb"
        ) as file:



            if media == "audio":

                await query.message.reply_audio(
                    audio=file,
                    caption=caption,
                    parse_mode="Markdown"
                )


            else:

                await query.message.reply_video(
                    video=file,
                    caption=caption,
                    parse_mode="Markdown"
                )



        await status.delete()



    except Exception as e:


        logger.error(e)



        await status.edit_text(
            "❌ Proses gagal.\n\n"
            f"Detail: `{e}`",
            parse_mode="Markdown"
        )



    finally:

        if filepath and os.path.exists(filepath):

            os.remove(filepath)





# =========================
# MAIN HANDLER
# =========================

async def handle_download(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    if not update.message:

        return



    text = update.message.text or ""



    match = URL_PATTERN.search(
        text
    )



    if not match:

        return



    url = match.group(1)



    engine = detect_engine(
        url
    )



    if not engine:

        return



    platform = detect_platform(
        url
    )





    # =====================
    # YOUTUBE
    # =====================

    if engine == "youtube":


        await react(
            update,
            "👀"
        )


        await youtube_menu(
            update,
            url
        )


        return





    # =====================
    # SOCIAL MEDIA
    # =====================

    await react(
        update,
        social_reaction(platform)
    )



    status = await update.message.reply_text(
        "⚡ Permintaan diterima.\n\n"
        "⬇️ Sedang mengunduh media..."
    )



    filepath = None



    try:


        # =====================
        # COBA ENGINE FOTO DULU
        # (khusus Instagram & Pinterest)
        # =====================

        images = []
        owner = None


        if platform in (
            "Instagram",
            "Pinterest"
        ):

            images, owner = download_photo(
                url,
                platform
            )



        if images:

            caption = build_caption(
                f"{platform} Photo",
                platform,
                update.effective_user,
                media_type="photo",
                owner=owner
            )


            await send_photos(
                update,
                images,
                caption
            )


            await status.delete()

            return



        # =====================
        # FALLBACK KE VIDEO
        # =====================

        filepath, title, source = download_social(
            url
        )



        caption = build_caption(
            title,
            source,
            update.effective_user
        )



        with open(
            filepath,
            "rb"
        ) as file:



            await update.message.reply_video(
                video=file,
                caption=caption,
                parse_mode="Markdown"
            )



        await status.delete()



    except Exception as e:


        logger.error(e)



        await status.edit_text(
            "❌ Proses gagal.\n\n"
            f"Detail: `{e}`",
            parse_mode="Markdown"
        )



    finally:


        if filepath and os.path.exists(filepath):

            os.remove(filepath)


            logger.info(
                f"Cleanup file: {filepath}"
            )