from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()


def get_client():

    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_model():

    return os.getenv(
        "OPENAI_MODEL",
        "deepseek-chat",
    )
