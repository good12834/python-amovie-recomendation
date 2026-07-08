"""Gemini AI integration for Movie Buddy chatbot."""

from dotenv import load_dotenv
import os
import json
import sys

# Load environment variables from .env file
load_dotenv()

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to initialize the Gemini client
_genai_available = False
_genai_client = None

try:
    from google import genai
    _genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    _genai_available = True
except ImportError:
    pass
except Exception as e:
    print(f"[AI Chat] Warning: Could not initialize Gemini: {e}")


def is_available():
    """Check if the Gemini AI is available."""
    return _genai_available


def get_model():
    """Return the model name to use."""
    return "gemini-2.5-flash"


def generate_response(user_message, user_memory, movie_context=""):
    """
    Generate an AI-powered response using Google Gemini.

    Args:
        user_message: The user's input message.
        user_memory: Dict of user preferences (genres, actors, directors, etc.)
        movie_context: Optional context about available movies.

    Returns:
        A response string, or None if AI is unavailable.
    """
    if not _genai_available or not _genai_client:
        return None

    try:
        # Build a system prompt with the user's context
        system_prompt = _build_system_prompt(user_memory, movie_context)

        # Create the interaction with Gemini
        response = _genai_client.models.generate_content(
            model=get_model(),
            contents=[
                {"role": "user", "parts": [{"text": system_prompt + "\n\nUser: " + user_message}]}
            ]
        )

        if response and response.text:
            return response.text.strip()

    except Exception as e:
        print(f"[AI Chat] Error generating response: {e}")

    return None


def _build_system_prompt(user_memory, movie_context=""):
    """Build a system prompt with the user's context for the AI."""
    prompt_parts = [
        "You are Movie Buddy, a friendly and enthusiastic movie recommendation chatbot.",
        "You help users discover movies based on their tastes and preferences.",
        "",
        "IMPORTANT RULES:",
        "- Keep responses concise and helpful (2-4 sentences max).",
        "- Be enthusiastic about movies and recommendations.",
        "- If the user asks about a movie you don't know, be honest but helpful.",
        "- Never make up movie details you're unsure about.",
        "- Use emojis sparingly to add personality.",
        "",
    ]

    # Add user memory context
    if user_memory:
        prompt_parts.append("User Profile:")
        if user_memory.get("genres"):
            prompt_parts.append(f"- Favorite genres: {', '.join(user_memory['genres'])}")
        if user_memory.get("actors"):
            prompt_parts.append(f"- Favorite actors: {', '.join(user_memory['actors'])}")
        if user_memory.get("directors"):
            prompt_parts.append(f"- Favorite directors: {', '.join(user_memory['directors'])}")
        if user_memory.get("disliked_genres"):
            prompt_parts.append(f"- Disliked genres: {', '.join(user_memory['disliked_genres'])}")
        if user_memory.get("country"):
            prompt_parts.append(f"- Country: {user_memory['country']}")
        if user_memory.get("language"):
            prompt_parts.append(f"- Language: {user_memory['language']}")
        if user_memory.get("age"):
            prompt_parts.append(f"- Age: {user_memory['age']}")

    # Add movie context if provided
    if movie_context:
        prompt_parts.append("")
        prompt_parts.append(f"Available movie context: {movie_context}")

    prompt_parts.append("")
    prompt_parts.append("Now respond to the user conversationally and naturally.")

    return "\n".join(prompt_parts)


def generate_ai_recommendation(user_memory, movie_list_text):
    """
    Generate an AI-powered recommendation explanation.

    Args:
        user_memory: Dict of user preferences.
        movie_list_text: Text representation of recommended movies.

    Returns:
        A recommendation explanation string, or None if unavailable.
    """
    if not _genai_available or not _genai_client:
        return None

    try:
        prompt = (
            "You are Movie Buddy, a movie recommendation assistant.\n\n"
            f"User preferences: {json.dumps(user_memory)}\n\n"
            f"Here are some movies to recommend:\n{movie_list_text}\n\n"
            "Write a short, enthusiastic recommendation (2-3 sentences) explaining "
            "why these movies suit the user's taste. Be personal and engaging."
        )

        response = _genai_client.models.generate_content(
            model=get_model(),
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )

        if response and response.text:
            return response.text.strip()

    except Exception as e:
        print(f"[AI Chat] Error generating recommendation: {e}")

    return None