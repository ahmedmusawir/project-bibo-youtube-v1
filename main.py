import os
import shutil
from src import transcription # Import our refactored module

def setup_project_directories(project_name):
    """Creates the necessary directory structure for a new video project."""
    base_path = os.path.join("projects", project_name)
    
    if os.path.exists(base_path):
        print(f"Project '{project_name}' already exists. Using existing directory.")
        return base_path

    os.makedirs(os.path.join(base_path, "5_images"))
    print(f"✅ Project '{project_name}' created successfully at: {base_path}")
    return base_path

def handle_youtube_url(project_path):
    """Handles the YouTube URL transcription workflow."""
    youtube_url = input("Enter the YouTube URL to transcribe: ").strip()
    if youtube_url:
        # We will call the summarizer from here later
        transcript_path = transcription.transcribe_youtube_audio(youtube_url, project_path)
        print(f"\nNext step would be to summarize the file at: {transcript_path}")
    else:
        print("URL cannot be empty.")

def handle_ready_script(project_path):
    """Handles the workflow for a user-provided script."""
    script_path = os.path.join(project_path, "1_summary.txt")
    print("\n" + "="*20)
    print("Please place your ready-made script in the following file:")
    print(script_path)
    print("="*20)
    input("Press Enter after you have saved the file...")
    
    if os.path.exists(script_path) and os.path.getsize(script_path) > 0:
        print(f"✅ Script detected at {script_path}.")
        print("Next step would be to generate audio from this script.")
    else:
        print("Script file not found or is empty. Please try again.")


def main_menu(project_name, project_path):
    """Displays the main menu and handles user choices."""
    while True:
        print("\n" + "--- Main Menu ---")
        print(f"Project: {project_name}")
        print("-------------------")
        print("Choose your input source:")
        print("1. Transcribe from YouTube URL")
        print("2. Scrape from Article URL (coming soon)")
        print("3. Use a Ready-Made Script")
        print("9. Exit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            handle_youtube_url(project_path)
        elif choice == '2':
            print("This feature will be implemented soon using crawl4ai.")
        elif choice == '3':
            handle_ready_script(project_path)
        elif choice == '9':
            print("Exiting.")
            break
        else:
            print("Invalid choice, please try again.")

def main():
    """Main function to run the video generator application."""
    project_name = input("Please enter a project name (e.g., 'MyNewVideo'): ").strip()
    
    if not project_name:
        print("Project name cannot be empty. Exiting.")
        return

    project_path = setup_project_directories(project_name)
    main_menu(project_name, project_path)


if __name__ == "__main__":
    main()