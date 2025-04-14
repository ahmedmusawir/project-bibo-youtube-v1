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
    "PLEASE MAKE SURE IT IS SIMPLE + CONVERSATIONAL + EASY BANGLA THAT PEOPLE FROM BANGLADESH CAN UNDERSTAND. MAKE SURE A HIGHSCHOOL BOY OR GIRL CAN EASILY UNDERSTAND THIS. "
    "This video is for the general public, not academics. Make it feel like someone is telling a story to a friend. Avoid formal or complex vocabulary. "

    "IMPORTANT: Here’s an example of the kind of formal Bangla writing you should AVOID — like something you’d see in a newspaper or textbook: "
    "উইন্ডোজ অপারেটিং সিস্টেমের জন্য তৈরি ক্রোম ব্রাউজারে ভয়ংকর নিরাপত্তা ত্রুটির সন্ধান পেয়েছে সাইবার নিরাপত্তাপ্রতিষ্ঠান ক্যাসপারস্কি। "
    "জিরো ডে ঘরানার এই ত্রুটি কাজে লাগিয়ে ক্রোম ব্রাউজার ব্যবহারকারীদের কম্পিউটার থেকে তথ্য চুরি করতে পারে সাইবার অপরাধীরা। "

    "Instead of writing like that, we want you to translate like you’re talking to a friend on the street or over tea. "
    "Keep the sentences short, smooth, natural — like spoken Bangla. "

    "MAKE SURE SOME ENGLISH WORDS LIKE 'Prompt, Prompt Engineering, AI, Generative AI, Windows Operating System etc.'-- you don't need to translate into Bengali, keep them exactly as is because when we create audio out of this script it fails to pronounce those words correctly ... you Must follow this exactly"
    "Don’t add formatting like **, bold, or any other special characters — this text will be used for voice synthesis. "

    "At the end of the translation, add a short, natural Bangla outro — something like: "
    "'এই ভিডিওটি এখানেই শেষ করছি। ভালো লাগলে লাইক দিন, চ্যানেলটি সাবস্ক্রাইব করুন। দেখা হবে পরের ভিডিওতে।' "

    "Do not add any extra commentary. DO NOT ADD ** OR ANY OTHER CHARACTERS. THIS TRANSCRIPT IS FOR AUDIO GENERATION. JUST RETURN THE FINAL TRANSLATED SCRIPT."
)



# Perform the translation
response = client.chat.completions.create(
    model="gpt-4.5-preview-2025-02-27",
    messages=[
        {"role": "system", "content": translation_prompt},
        {"role": "user", "content": english_text},
    ]
)

# Save the translated output
translated_text = response.choices[0].message.content
TRANSLATION_PATH.write_text(translated_text, encoding="utf-8")
print("Bengali translation saved to", TRANSLATION_PATH)
