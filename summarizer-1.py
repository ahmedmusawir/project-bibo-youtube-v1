from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup GPT-4.5 preview model
llm = ChatOpenAI(model="o3")
# llm = ChatOpenAI(model="gpt-4.1")
# llm = ChatOpenAI(model="gpt-4.5-preview-2025-02-27")

# File paths
TRANSCRIPT_PATH = Path("text/transcript.txt")
SUMMARY_PATH = Path("text/summary.txt")

def summarize_transcript():
    loader = TextLoader(str(TRANSCRIPT_PATH))
    docs = loader.load()

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert video script editor. Your job is to transform transcripts into engaging, informative, and natural narration scripts for YouTube videos. "
            "The final script should feel like a mini-documentary or educational storytelling piece, rich in detail and accessible in tone. Make sure the focus in on the information. The target is to give people the most information possible from the source transcript"
            "Avoid any meta instructions, introductions, or framing language like 'Here is your script'. Output only the clean narration-ready script, and make sure it ends with a complete, conclusive statement. "
            "Your script should be long enough to produce a voiceover between 5 to 6 minutes in length — aim for approximately 900 words [MUST BE FOLLOWED STRICTLY]. "
            "Prioritize completeness and engagement over strict brevity."
            "Also, the source content might have advertising content mixed in ... plz avoid that..."
            "FOCUS ON THE INFORMATIVE PARTS AND TRY HARD TO KEEP IT WITHIN 5-6 MINUTES WHICH IS ABOUT 900 WORDS. WHY THIS IS IMPORTANT? THIS IS THE WHOLE POINT OF OUR YOUTUBE CHANNEL, WE DELIVER CONTENT IN A SMALL BITE SIZE SO THAT VIEWER CAN LISTEN ON THE GO! NO TIME TO LISTEN TO LONG FROM STUFF..."
        )),
        ("user", "{context}")
    ])

    print(f"✅ Starting Summary Chain ... ")
    chain = create_stuff_documents_chain(llm, prompt)
    print(f"✅ Starting to Summarize ...")
    result = chain.invoke({"context": docs})
    SUMMARY_PATH.write_text(result, encoding='utf-8')
    print(f"✅ Summary saved to {SUMMARY_PATH}")

if __name__ == "__main__":
    summarize_transcript()
