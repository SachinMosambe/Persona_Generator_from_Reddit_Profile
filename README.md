# Persona Generator from Reddit Profile

An AI-powered tool that generates detailed user personas from Reddit profiles using LangChain and OpenAI.

## Overview
This project uses:
- OpenAI's API for generating embeddings and personas
- PRAW (Python Reddit API Wrapper) for fetching Reddit data
- LangChain for creating a processing pipeline
- FAISS for efficient vector storage and similarity search

## Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure Environment**:
Create a `.env` file with your API keys:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
OPENAI_API_KEY=your_openai_key
```

## Usage

Run with a Reddit profile URL:
```bash
python main.py https://www.reddit.com/user/username/
```

The script will:
1. Fetch the user's posts and comments
2. Generate embeddings using OpenAI
3. Create a detailed persona
4. Save the result to a text file

## Project Structure
```
├── main.py              # Entry point
├── reddit_scraper.py    # Reddit data collection
├── vector_store.py      # Vector storage handling
├── persona_generator.py # Persona generation logic
└── requirements.txt     # Dependencies
```

## Author
Sachin Mosambe