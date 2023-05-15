import os
import dotenv
import requests

dotenv.load_dotenv()


def generate_card_text(reason, person, likes="", tones=""):
    prompt = f"write a creative inside message of a maximum of 50 words for {reason}, to {person}"
    if likes:
        prompt = prompt + f", who likes {likes}"
    if tones:
        prompt = f"write a creative {tones} inside message of a maximum of 50 words for {reason}, to {person}, who " \
                 f"likes {likes}. "

    json = {
        "model": os.environ["OPENAI_MODEL_ID"],
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": "Bearer " + os.environ.get("OPENAI_API_KEY"),
    }
    response = requests.post(
        os.environ.get("OPENAI_API_URL"),
        headers=headers,
        json=json,
        timeout=200,
    )

    if response.json().get("error"):
        return response.json().get("error")["message"]

    return response.json()["choices"][0]["message"]["content"]
