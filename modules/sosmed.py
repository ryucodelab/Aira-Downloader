import os
import logging

import yt_dlp

from yt_dlp.utils import DownloadError


DOWNLOAD_DIR = "downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


logger = logging.getLogger(
    "AiraSocialEngine"
)



# =========================
# PLATFORM DETECTOR
# =========================

def detect_platform(url):

    url = url.lower()


    if "tiktok.com" in url:
        return "TikTok"


    if "instagram.com" in url:
        return "Instagram"


    if (
        "facebook.com" in url
        or "fb.watch" in url
    ):
        return "Facebook"


    if (
        "x.com" in url
        or "twitter.com" in url
    ):
        return "X"


    if (
        "pinterest.com" in url
        or "pin.it" in url
    ):
        return "Pinterest"


    return "Social Media"



# =========================
# SAFE FILENAME
# =========================

def clean_filename(name):

    bad_chars = (
        '\\/:*?"<>|'
    )


    for char in bad_chars:

        name = name.replace(
            char,
            ""
        )


    return name[:80]



# =========================
# VIDEO ENGINE
# =========================

def download_social(url):

    platform = detect_platform(
        url
    )


    logger.info(
        f"Social engine aktif: {platform}"
    )


    options = {

        "outtmpl":
            os.path.join(
                DOWNLOAD_DIR,
                "%(title)s.%(ext)s"
            ),


        "format":
            "best[ext=mp4]/best",


        "merge_output_format":
            "mp4",


        "noplaylist":
            True,


        "quiet":
            True,


        "no_warnings":
            True,


        "restrictfilenames":
            False,


    }



    try:

        with yt_dlp.YoutubeDL(
            options
        ) as ydl:


            info = ydl.extract_info(
                url,
                download=True
            )


            title = (
                info.get("title")
                or "Aira Download"
            )


            title = clean_filename(
                title
            )


            filepath = ydl.prepare_filename(
                info
            )


            if not filepath.endswith(
                ".mp4"
            ):


                mp4_file = (
                    filepath.rsplit(
                        ".",
                        1
                    )[0]
                    + ".mp4"
                )


                if os.path.exists(
                    mp4_file
                ):

                    filepath = mp4_file



            logger.info(
                f"Video selesai: {filepath}"
            )


            return (
                filepath,
                title,
                platform
            )



    except DownloadError as e:


        logger.warning(
            f"yt-dlp gagal: {e}"
        )


        raise Exception(
            "Mohon Maaf Aira Downloader "
            "Saat Ini Hanya Mendukung Media Video."
        )



    except Exception as e:


        logger.error(
            f"Engine error: {e}"
        )


        raise Exception(
            "Mohon Maaf Aira Downloader "
            "Saat Ini Hanya Mendukung Media Video."
        )