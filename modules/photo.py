import logging

import requests
import instaloader

from bs4 import BeautifulSoup


logger = logging.getLogger(
    "AiraPhotoEngine"
)


L = instaloader.Instaloader()


HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10) "
        "AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36"
    )

}



# =========================
# INSTAGRAM SHORTCODE
# =========================

def get_instagram_shortcode(url):

    parts = url.strip("/").split("/")


    if "p" in parts:
        return parts[parts.index("p") + 1]


    if "reel" in parts:
        return parts[parts.index("reel") + 1]


    return None



# =========================
# INSTAGRAM PHOTO ENGINE
# =========================

def instagram_photos(url):

    shortcode = get_instagram_shortcode(
        url
    )


    if not shortcode:

        logger.warning(
            "Instagram shortcode tidak ditemukan"
        )

        return [], None



    try:

        post = instaloader.Post.from_shortcode(
            L.context,
            shortcode
        )


    except Exception as e:

        logger.warning(
            f"Instaloader gagal ambil post: {e}"
        )

        return [], None



    images = []


    if post.typename == "GraphSidecar":

        for node in post.get_sidecar_nodes():

            if not node.is_video:

                images.append(
                    node.display_url
                )


    elif not post.is_video:

        images.append(
            post.url
        )



    try:

        owner = post.owner_username


    except Exception as e:

        logger.warning(
            f"Gagal ambil owner username: {e}"
        )

        owner = None


    return images, owner



# =========================
# PINTEREST PHOTO ENGINE
# =========================

def pinterest_photos(url):

    try:

        session = requests.Session()


        r = session.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )


        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )


    except Exception as e:

        logger.warning(
            f"Pinterest fetch gagal: {e}"
        )

        return [], None



    images = []


    for tag in soup.find_all(
        "meta",
        property="og:image"
    ):

        img = tag.get("content")

        if img:
            images.append(img)



    for tag in soup.find_all(
        "meta",
        attrs={
            "name": "twitter:image"
        }
    ):

        img = tag.get("content")

        if img:
            images.append(img)



    # dedupe, jaga urutan

    seen = set()
    unique = []


    for img in images:

        if img not in seen:

            seen.add(img)
            unique.append(img)


    return unique, None



# =========================
# MAIN ENGINE
# =========================

def download_photo(url, platform):

    logger.info(
        f"Photo engine aktif: {platform}"
    )


    if platform == "Instagram":
        return instagram_photos(url)


    if platform == "Pinterest":
        return pinterest_photos(url)


    return [], None
