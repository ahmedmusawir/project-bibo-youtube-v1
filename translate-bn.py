from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = OpenAI()

# Paths
SUMMARY_PATH = Path("text/summary.txt")
TRANSLATION_PATH = Path("text/translated_bn.txt")

# Load the original summary text
english_text = SUMMARY_PATH.read_text(encoding="utf-8")

# Translation prompt, optimized for Bangladeshi YouTube audience
translation_prompt = (
    "You are an expert Bengali translator for a popular YouTube channel in Bangladesh. "
    "Translate the following English narration into clear, natural Bangla that sounds like everyday conversation — casual, easy to follow, and friendly. "
    "This video is for the general public, not academics. Make it feel like someone is telling a story to a friend. Avoid formal or complex vocabulary. "
    "Don’t add formatting like bold or special characters — the output will be used for voice synthesis only. "
    "At the end of the translation, add a short, natural Bangla outro — something like: "
    "'এই ভিডিওটি এখানেই শেষ করছি। ভালো লাগলে লাইক দিন, চ্যানেলটি সাবস্ক্রাইব করুন। দেখা হবে পরের ভিডিওতে।' "
    "Do not add extra commentary. DO NOT ADD ** OR ANY OTHER CHARACTERS. THIS TRANSCRIPT IS FOR AUDIO GENERATION. IF YOU ADD STUPID CHARACTES LIKE ** THAT WILL DESTROY THE AUDIO PRODUCTION. Just return the final translated script."
)


# Perform the translation
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": translation_prompt},
        {"role": "user", "content": english_text},
    ]
)

# Save the translated output
translated_text = response.choices[0].message.content
TRANSLATION_PATH.write_text(translated_text, encoding="utf-8")
print("Bengali translation saved to", TRANSLATION_PATH)
