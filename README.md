# ShortsStudio-Generator# 🎬 AI TikTok & YouTube Shorts Generator

Rebuilt from your n8n workflow in Python.
Automatically creates viral short-form videos using:
- OpenAI (captions + script)
- PiAPI (image/video)
- ElevenLabs (voice)
- Creatomate (final render)
- Discord webhook notification

---

## 🧱 Project Files

tiktok_youtube_generator.py # Main workflow
config.py # Loads env vars + mock mode
requirements.txt # Dependencies
.env.example # Env template
README.md # Documentation

yaml
Copy code

---

## 🚀 Quick Start

1. Create and activate environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
Copy env template:

bash
Copy code
cp .env.example .env
Leave keys empty to run in MOCK mode.

Run:

bash
Copy code
python tiktok_youtube_generator.py
⚙️ Mock Mode
If any key is missing, all API calls simulate results.
Perfect for testing logic without spending credits.

🧩 Extend It
Replace mock functions with real API implementations:

PiAPI Docs

ElevenLabs API

Creatomate API

Discord Webhooks

🕓 Schedule Automation
Run daily using cron:

bash
Copy code
0 9 * * * /usr/bin/python /path/to/tiktok_youtube_generator.py
🪪 License
MIT License © 2025

markdown
Copy code

---

✅ All 5 files ready:
1. `tiktok_youtube_generator.py`  
2. `config.py`  
3. `requirements.txt`  
4. `.env.example`  
5. `README.md`

Would you like me to **add a `video_uploader.py`** next (to push rendered videos automatically to YouTube & TikTok 
