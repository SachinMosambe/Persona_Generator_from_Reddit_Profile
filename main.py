import sys
import re
from reddit_scraper import scrape_user_data
from vector_store import create_documents, create_vectorstore
from persona_generator import generate_user_persona

def extract_username(url):
    match = re.search(r"reddit\.com/user/([A-Za-z0-9_\-]+)/?", url)
    return match.group(1) if match else None

def save_output(username, persona):
    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona)
    print(f"\u2705 Persona saved to {filename}")

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
    else:
        url = input("Enter Reddit profile URL: ").strip()
    username = extract_username(url)
    if not username:
        print("Invalid Reddit URL")
        return

    print(f"Fetching data for {username}...")
    posts, comments = scrape_user_data(username)

    if not posts and not comments:
        print("No posts or comments found.")
        return

    docs = create_documents(posts, comments)
    vectorstore = create_vectorstore(docs)
    print("Generating persona...")
    persona = generate_user_persona(vectorstore)
    save_output(username, persona)

if __name__ == "__main__":
    main()
