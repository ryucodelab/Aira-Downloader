# ⚡ Aira Downloader

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/python--telegram--bot-21%2B-2CA5E0?logo=telegram&logoColor=white" alt="python-telegram-bot">
  <img src="https://img.shields.io/badge/yt--dlp-2025.1%2B-red?logo=youtube&logoColor=white" alt="yt-dlp">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
</p>

<p align="center">
  A single Telegram bot that downloads video and photo content from popular social media platforms — just send a link, Aira picks the best engine automatically.
</p>

---

## ✨ Features

| Platform | Video | Photo / Carousel |
|---|:---:|:---:|
| 🎬 YouTube | ✅ (video + audio) | — |
| 🎵 TikTok | ✅ | ❌ *(not supported yet)* |
| 📸 Instagram | ✅ | ✅ (single + sidecar/carousel) |
| 🐦 X / Twitter | ✅ | — |
| 👍 Facebook | ✅ | — |
| 📌 Pinterest | ✅ | ✅ (resolved via OpenGraph) |

Other things Aira handles out of the box:

- 🎯 **Auto engine detection** — just paste a link, no commands needed
- 🎚️ **YouTube format picker** — choose Audio or Video via inline buttons
- 🖼️ **Smart photo fallback** — for Instagram/Pinterest, Aira tries to resolve photos first before falling back to the video engine
- 📤 **Post owner credit** — Instagram photo captions automatically show who posted it
- 🏓 `/ping` — check bot latency
- 👥 Works in both private chats and groups

---

## 🧰 Tech Stack

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — Telegram bot framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — video engine for YouTube, TikTok, X, Facebook, Pinterest
- [instaloader](https://github.com/instaloader/instaloader) — Instagram photo/carousel resolver
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — Pinterest OpenGraph scraping
- [SaveNow API](https://p.savenow.to) — YouTube download backend

---

## 📦 Requirements

- Python **3.10+**
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- A SaveNow API key (for the YouTube engine)

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/aira-downloader.git
cd aira-downloader
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token
SAVENOW_API_KEY=your_savenow_api_key
```

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Telegram bot token from [@BotFather](https://t.me/BotFather) |
| `SAVENOW_API_KEY` | API key from [savenow.to](https://p.savenow.to), used by the YouTube engine |

### 5. Run the bot

```bash
python main.py
```

If everything is configured correctly, you'll see:

```
⚡ Aira AIO Downloader aktif
```

---

## 📁 Project Structure

```
aira-downloader/
├── main.py                 # Entry point, handler registration
├── requirements.txt
├── .env                     # Not committed — create this yourself
└── modules/
    ├── start.py             # /start command & welcome message
    ├── system.py             # /ping command
    ├── downloader.py         # Main routing logic, reactions, captions
    ├── sosmed.py              # Video engine (yt-dlp) for social platforms
    ├── youtube.py             # YouTube engine (SaveNow API)
    └── photo.py               # Photo engine for Instagram & Pinterest
```

---

## 💬 Usage

1. Add the bot to a group, or message it privately
2. Send a link from any supported platform
3. For YouTube links, choose **Audio** or **Video** from the inline buttons
4. Sit back — Aira reacts to your message and delivers the media directly in chat

---

## ⚠️ Known Limitations

- **Threads** is not supported — no stable extractor available yet
- **TikTok photo slideshows** are not supported — yt-dlp doesn't natively resolve them
- Instagram scraping may be rate-limited without a logged-in session, since it relies on public, unauthenticated requests

---

## 🙏 Credits

- Developed by [**@oneofrisuofc**](https://t.me/oneofrisuofc)
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp), [instaloader](https://github.com/instaloader/instaloader), and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- YouTube downloads powered by [SaveNow](https://p.savenow.to)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center"><i>⚡ Powered By Aira Downloader</i></p>
