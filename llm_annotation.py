from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def build_messages(examples_df, test_row, model):
    messages = []
    
    # Add the system prompt as a user message for o1-preview
    if "o1" in model:
            messages.append({
                "role": "user",
                "content": '''You are a brilliant comedian and astute cultural critic. You are reading captions to a cartoon contest, and you are tasked with "explaining the joke", identifying why the caption is funny. Specifically, we are interested in identifying the distinct 'elements' at play. Given the cartoon and caption entry, identify the core elements that make the caption funny.'''
        })
    else:
        messages.append({
            "role": "system",
                "content": '''You are a brilliant comedian and astute cultural critic. You are reading captions to a cartoon contest, and you are tasked with "explaining the joke", identifying why the caption is funny. Specifically, we are interested in identifying the elements of the joke in the caption as either "structural"-- the factual elements of the joke, or "cognitive"-- the reason the factual element/s are funny. Given the cartoon and caption entry, identify the material elements that make the caption funny. Remember, we are not interested in the inherently funny nature of the cartoon, only the joke added by the caption.'''
            })

    for _, row in examples_df.iterrows():
        if model == "o1-preview": \
            messages.append({
                    "role": "user",
                    "content": f"Cartoon description: {row['human_description']}\nCaption: {row['top_caption_1']}"
                })
        else:
            messages.append({
                "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": row["image_url"]}},
                        {"type": "text", "text": row["top_caption_1"]}
                    ]
                })
            messages.append({
                "role": "assistant",
                "content": row["example"]
            })

    if model == "o1-preview":
        messages.append({
            "role": "user",
                "content": f"Cartoon description: {test_row['human_description']}\nCaption: {test_row['top_caption_1']}"
            })
    else:
        messages.append({
            "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": test_row["image_url"]}},
                    {"type": "text", "text": test_row["top_caption_1"]}
                ]
            })
    return messages


def analyze_cartoon_caption(test_row, examples_df, model="gpt-4o-mini"):

    messages = build_messages(examples_df, test_row, model)

    print(model)
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content
