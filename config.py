import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    OPENAI_API_KEY: str
    PIAPI_KEY: str
    ELEVENLABS_KEY: str
    CREATOMATE_KEY: str
    CREATOMATE_TEMPLATE_ID: str
    DISCORD_WEBHOOK_URL: str
    mock: bool

    @staticmethod
    def load_from_env() -> "Config":
        api_keys = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "PIAPI_KEY": os.getenv("PIAPI_KEY", ""),
            "ELEVENLABS_KEY": os.getenv("ELEVENLABS_KEY", ""),
            "CREATOMATE_KEY": os.getenv("CREATOMATE_KEY", ""),
            "CREATOMATE_TEMPLATE_ID": os.getenv("CREATOMATE_TEMPLATE_ID", ""),
            "DISCORD_WEBHOOK_URL": os.getenv("DISCORD_WEBHOOK_URL", ""),
        }
        mock = not all(api_keys.values())
        return Config(**api_keys, mock=mock)
