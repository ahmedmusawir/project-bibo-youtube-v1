from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.chat_models import init_chat_model
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# # Setup Claude 3.5 Sonnet
# if not os.environ.get("ANTHROPIC_API_KEY"):
#     os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter API key for Anthropic: ")

llm = init_chat_model("claude-3-5-sonnet-20240620", model_provider="anthropic")

# File paths
TRANSCRIPT_PATH = Path("text/transcript.txt")
SUMMARY_PATH = Path("text/summary.txt")

def summarize_transcript():
    loader = TextLoader(str(TRANSCRIPT_PATH))
    docs = loader.load()

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert video script editor. Your job is to transform transcripts into natural, engaging, and informative summaries for YouTube explainer videos. "
            "The final script should feel like a mini documentary or educational storytelling, rich in detail, but easy to follow. Keep a friendly tone, and retain key insights and interesting facts. "
            "Your goal is to create a voiceover script that lasts between 5 to 6 minutes when read aloud at a conversational pace."
        )),
        ("user", "{context}")
    ])

    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", "You are an expert video script editor. Your job is to turn a transcript into a natural, engaging, and informative summary, as if it were meant to be narrated in a YouTube explainer video for a general audience. Focus on clarity, tone, and narrative structure."),
    #     ("user", "{context}")
    # ])


    chain = create_stuff_documents_chain(llm, prompt)
    result = chain.invoke({"context": docs})
    SUMMARY_PATH.write_text(result)
    print(f"✅ Summary saved to {SUMMARY_PATH}")

if __name__ == "__main__":
    summarize_transcript()
