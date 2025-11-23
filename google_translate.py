# google_translate.py
import os
import json

from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

_translate_client = None


def _get_client():
    global _translate_client
    if _translate_client is not None:
        return _translate_client

    if "GOOGLE_TRANSLATE_KEY" in os.environ:
        key_json = json.loads(os.environ["GOOGLE_TRANSLATE_KEY"])
        credentials = service_account.Credentials.from_service_account_info(key_json)
        _translate_client = translate.Client(credentials=credentials)
        print("[Translate] Client initialized from GOOGLE_TRANSLATE_KEY env")
    elif os.path.exists("google_translate_key.json"):
        credentials = service_account.Credentials.from_service_account_file(
            "google_translate_key.json"
        )
        _translate_client = translate.Client(credentials=credentials)
        print("[Translate] Client initialized from local google_translate_key.json")
    else:
        _translate_client = None
        print("[Translate] No credentials found; translation disabled.")

    return _translate_client


def translate_text(text: str, target_lang: str) -> str:
    client = _get_client()
    if client is None or not text:
        return text

    try:
        result = client.translate(text, target_language=target_lang)
        return result["translatedText"]
    except Exception as e:
        print("[Translate] Error while translating:", e)
        return text
