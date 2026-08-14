import os
import time
import logging
import requests

from dotenv import load_dotenv


load_dotenv()


logger = logging.getLogger(
    "AiraYouTubeEngine"
)


DOWNLOAD_DIR = "downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


API_KEY = os.getenv(
    "SAVENOW_API_KEY"
)


BASE_URL = (
    "https://p.savenow.to/ajax"
)



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


    return name[:100]



# =========================
# CREATE REQUEST
# =========================

def create_download(
    url,
    media_type
):


    if media_type == "audio":

        fmt = "mp3"

    else:

        # default video
        fmt = "720"



    params = {

        "url": url,

        "format": fmt,

        "apikey": API_KEY,

        "add_info": "1",

        "allow_extended_duration": "1",

        "no_merge": "0"

    }


    logger.info(
        f"YouTube format: {fmt}"
    )


    response = requests.get(
        f"{BASE_URL}/download.php",
        params=params,
        timeout=30
    )


    response.raise_for_status()


    data = response.json()


    if not data.get(
        "success"
    ):

        raise Exception(
            "Gagal membuat permintaan download"
        )


    return data



# =========================
# CHECK PROGRESS
# =========================

def wait_download(
    download_id
):


    logger.info(
        f"Menunggu ID: {download_id}"
    )


    while True:


        response = requests.get(
            f"{BASE_URL}/progress.php",
            params={
                "id": download_id
            },
            timeout=30
        )


        response.raise_for_status()


        data = response.json()


        progress = data.get(
            "progress",
            0
        )


        logger.info(
            f"Progress: {progress}"
        )


        if (
            data.get("success")
            and progress >= 1000
        ):

            return data



        time.sleep(3)



# =========================
# SAVE FILE
# =========================

def save_file(
    url,
    filename
):


    filepath = os.path.join(
        DOWNLOAD_DIR,
        filename
    )


    logger.info(
        "Mengunduh file hasil API"
    )


    with requests.get(
        url,
        stream=True,
        timeout=120
    ) as response:


        response.raise_for_status()


        with open(
            filepath,
            "wb"
        ) as file:


            for chunk in response.iter_content(
                chunk_size=8192
            ):

                if chunk:

                    file.write(
                        chunk
                    )


    return filepath



# =========================
# MAIN ENGINE
# =========================

def download_youtube(
    url,
    media_type
):


    request = create_download(
        url,
        media_type
    )


    download_id = request.get(
        "id"
    )


    info = request.get(
        "info",
        {}
    )


    title = (
        info.get("title")
        or "Aira YouTube"
    )


    title = clean_filename(
        title
    )



    result = wait_download(
        download_id
    )


    download_url = result.get(
        "download_url"
    )


    if not download_url:

        raise Exception(
            "Link download tidak ditemukan"
        )



    extension = (
        "mp3"
        if media_type == "audio"
        else "mp4"
    )


    filename = (
        f"{title}.{extension}"
    )



    filepath = save_file(
        download_url,
        filename
    )


    logger.info(
        f"Selesai: {filepath}"
    )


    return (
        filepath,
        title,
        media_type
    )