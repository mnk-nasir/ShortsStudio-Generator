#!/usr/bin/env python3
"""
AI Automated TikTok/Youtube Shorts/Reels Generator
--------------------------------------------------
Python version of the n8n workflow that creates short-form videos using:
- OpenAI for captions and scripts
- PiAPI (Flux + Kling) for image & video generation
- ElevenLabs for voiceover
- Creatomate for final rendering
- Google Sheets + Drive for management
- Discord Webhook notification

Runs in MOCK mode automatically if no API keys are found.
"""

import os
import time
import logging
import requests
from openai import OpenAI
from config import Config

log = logging.getLogger("tiktok_youtube_generator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
cfg = Config.load_from_env()

# --- MOCK HELPERS ---
def mock_response(name: str):
    log.info(f"[MOCK] Simulating {name} API call.")
    return {"status": "success", "mock": True, "url": f"https://mock.api/{name.lower()}"}


# --- OPENAI FUNCTIONS ---
def generate_video_captions(idea: str):
    """Generate 5 TikTok captions."""
    if cfg.mock:
        return [f"Mock caption {i+1} for idea: {idea}" for i in range(5)]

    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Generate 5 short, wild TikTok captions for the topic below."},
            {"role": "user", "content": idea}
        ]
    )
    captions = response.choices[0].message.content.strip().split("\n")
    return [c.strip("- ") for c in captions if c.strip()]


def generate_image_prompts(captions):
    """Generate detailed Flux prompts for each caption."""
    if cfg.mock:
        return [f"POV Flux prompt for '{c}'" for c in captions]
    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    prompts = []
    for caption in captions:
        res = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "Expand short caption into a detailed image generation prompt."},
                {"role": "user", "content": caption}
            ]
        )
        prompts.append(res.choices[0].message.content)
    return prompts


def generate_script(captions):
    """Generate voiceover script text."""
    if cfg.mock:
        return "Mock narration script matching the captions."
    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Write a funny narration for these TikTok captions."},
            {"role": "user", "content": "\n".join(captions)}
        ]
    )
    return res.choices[0].message.content


# --- API CALLS ---
def generate_image(prompt):
    """Generate image with PiAPI Flux."""
    if cfg.mock:
        return mock_response("generate_image")
    url = "https://api.piapi.ai/api/v1/task"
    headers = {"X-API-Key": cfg.PIAPI_KEY}
    body = {
        "model": "Qubico/flux1-dev",
        "task_type": "txt2img",
        "input": {"prompt": prompt, "width": 540, "height": 960},
    }
    return requests.post(url, headers=headers, json=body).json()


def generate_video(image_url, prompt):
    """Generate 5s video with Kling (PiAPI)."""
    if cfg.mock:
        return mock_response("generate_video")
    url = "https://api.piapi.ai/api/v1/task"
    headers = {"X-API-Key": cfg.PIAPI_KEY}
    body = {
        "model": "kling",
        "task_type": "video_generation",
        "input": {"prompt": prompt, "image_url": image_url, "duration": 5},
    }
    return requests.post(url, headers=headers, json=body).json()


def generate_voice(script):
    """Generate voiceover audio with ElevenLabs."""
    if cfg.mock:
        return mock_response("generate_voice")
    url = "https://api.elevenlabs.io/v1/text-to-speech/onwK4e9ZLuTAKqWW03F9"
    headers = {"xi-api-key": cfg.ELEVENLABS_KEY}
    res = requests.post(url, headers=headers, json={"text": script})
    return res.json()


def render_final_video(video_urls, captions, audio_url):
    """Render the final combined video using Creatomate."""
    if cfg.mock:
        return mock_response("render_final_video")
    url = "https://api.creatomate.com/v1/renders"
    headers = {
        "Authorization": f"Bearer {cfg.CREATOMATE_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "template_id": cfg.CREATOMATE_TEMPLATE_ID,
        "modifications": {
            "Video-1.source": video_urls[0],
            "Audio-1.source": audio_url,
            "Text-1.text": captions[0],
        }
    }
    return requests.post(url, headers=headers, json=body).json()


def notify_discord(message):
    """Send a webhook message to Discord."""
    if not cfg.DISCORD_WEBHOOK_URL:
        log.info("[SKIP] Discord webhook not set.")
        return
    requests.post(cfg.DISCORD_WEBHOOK_URL, json={"content": message})


# --- MAIN WORKFLOW ---
def main():
    log.info("🎬 Starting TikTok/YouTube Generator Workflow")

    idea = "How AI helps me land my dream job"
    captions = generate_video_captions(idea)
    log.info(f"Generated captions: {captions}")

    prompts = generate_image_prompts(captions)
    images = [generate_image(p) for p in prompts]
    log.info("Images generated")

    videos = [generate_video(img.get("url"), p) for img, p in zip(images, prompts)]
    log.info("Videos created")

    script = generate_script(captions)
    audio = generate_voice(script)
    log.info("Voiceover done")

    final = render_final_video(
        [v.get("url") for v in videos],
        captions,
        audio.get("url")
    )
    log.info("Render complete")

    notify_discord(f"✅ Video ready! {final.get('url')}")

    log.info("Workflow finished successfully.")


if __name__ == "__main__":
    main()
