import re
import sys
import os

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory import Memory
from recommender import Recommender
import ai_chat


class ChatBot:
    """The Movie Buddy chatbot that handles conversations."""

    def __init__(self, memory: Memory, recommender: Recommender):
        self.memory = memory
        self.recommender = recommender
        self.waiting_for_mood = False
        self.pending_questions = []
        self.questions_asked = set()
        self.ai_available = ai_chat.is_available()

    def process_message(self, user_input):
        """Process a user message and generate a response."""
        user_input = user_input.strip()
        if not user_input:
            return "Say something! I'm here to help you find great movies."

        # Extract preferences from the message
        preferences = self.memory.extract_preferences(user_input)
        responses = []

        # Process extracted preferences
        for pref_type, value in preferences:
            if pref_type == "genres":
                self.memory.update_memory("genres", value)
                responses.append(f"Nice! I'll remember you enjoy {value.lower()} movies.")

            elif pref_type == "disliked_genres":
                self.memory.update_memory("disliked_genres", value)
                responses.append(f"No problem! I'll avoid {value.lower()} recommendations.")

            elif pref_type == "actors":
                self.memory.update_memory("actors", value)
                responses.append(f"Great taste! I'll remember you like {value}.")

            elif pref_type == "directors":
                self.memory.update_memory("directors", value)
                responses.append(f"Awesome! I'll remember you enjoy {value}'s work.")

            elif pref_type == "watched":
                self.memory.add_watched_movie(value)
                responses.append(f"Got it! I've added {value} to your watch history.")

            elif pref_type == "favorite":
                self.memory.add_favorite(value)
                responses.append(f"Great! {value} has been added to your favorites!")

        # Handle specific commands
        user_lower = user_input.lower()

        # Recommend movies
        if any(phrase in user_lower for phrase in ["recommend", "suggest", "what should i watch", "what to watch", "give me"]):
            return self._generate_recommendation()

        # Show memory
        if any(phrase in user_lower for phrase in ["what do you know", "what do you remember", "my taste", "my preferences", "about me"]):
            memory = self.memory.get_user_memory()
            from ui.menu import print_memory_summary
            print_memory_summary(memory)
            return "That's what I've learned about you so far!"

        # Rate a movie
        rating_match = re.search(r'(\d+)/10', user_input)
        if rating_match and any(word in user_lower for word in ["rate", "rating", "score"]):
            rating = int(rating_match.group(1))
            movies = self.recommender.get_all_movies()
            for movie in movies:
                if movie["title"].lower() in user_lower:
                    self.memory.rate_movie(movie["title"], rating)
                    return f"I've rated {movie['title']} {rating}/10 for you!"

        # Search for a movie
        if any(phrase in user_lower for phrase in ["search", "find", "look for", "looking for"]):
            search_term = user_input
            for phrase in ["search ", "find ", "look for ", "looking for "]:
                search_term = re.sub(phrase, '', search_term, flags=re.IGNORECASE).strip()
            if search_term:
                results = self.recommender.search_movies(search_term)
                if results:
                    from ui.menu import print_movie_recommendation
                    print_movie_recommendation(results)
                    return f"I found {len(results)} movies matching '{search_term}'."
                else:
                    return f"Sorry, I couldn't find any movies matching '{search_term}'."

        # Handle mood-based requests
        mood_keywords = {
            "happy": "Comedy", "funny": "Comedy", "humorous": "Comedy",
            "sad": "Drama", "emotional": "Drama", "depressing": "Drama",
            "scared": "Horror", "scary": "Horror", "terrifying": "Horror",
            "excited": "Action", "thrilling": "Thriller", "suspense": "Thriller",
            "romantic": "Romance", "love": "Romance",
            "thoughtful": "Sci-Fi", "smart": "Sci-Fi", "mind-bending": "Sci-Fi"
        }

        for mood, genre in mood_keywords.items():
            if mood in user_lower:
                memory_data = self.memory.get_user_memory()
                memory_data["genres"].append(genre)
                movies = self.recommender.recommend_by_genre(
                    [genre],
                    watched=memory_data.get("watched", []),
                    disliked_genres=memory_data.get("disliked_genres", [])
                )
                if movies:
                    from ui.menu import print_movie_recommendation
                    print_movie_recommendation(movies, reason=genre)
                    return f"Since you're feeling {mood}, I recommend these {genre.lower()} movies!"

        # If we have responses, combine them
        if responses:
            return " ".join(responses)

        # Default fallback responses
        return self._handle_greeting_or_fallback(user_lower)

    def _handle_greeting_or_fallback(self, user_lower):
        """Handle greeting or provide a fallback response."""
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "what's up", "yo"]
        if any(g in user_lower for g in greetings):
            # Try AI for a more personalized greeting
            if self.ai_available:
                memory = self.memory.get_user_memory()
                ai_response = ai_chat.generate_response(user_lower, memory)
                if ai_response:
                    return ai_response
            return "Hey there! How can I help you find a great movie today?"

        thanks = ["thanks", "thank you", "appreciate it", "awesome"]
        if any(t in user_lower for t in thanks):
            return "You're welcome! Happy watching! 🎬"

        bye = ["bye", "goodbye", "see you", "later"]
        if any(b in user_lower for b in bye):
            return "Goodbye! Come back anytime for more recommendations!"

        # Ask about favorite genre if we don't know much
        memory = self.memory.get_user_memory()
        if not memory.get("genres") and not memory.get("actors"):
            return "I'd love to help you find movies! What kind of movies do you enjoy? Action? Comedy? Sci-Fi?"

        # Try AI for general fallback responses
        if self.ai_available:
            ai_response = ai_chat.generate_response(user_lower, memory)
            if ai_response:
                return ai_response

        # General fallback
        return "Interesting! Tell me more about what you're in the mood for. You can also ask me to recommend something!"

    def _generate_recommendation(self):
        """Generate a recommendation based on user memory."""
        memory = self.memory.get_user_memory()

        # If we have preferences, use hybrid recommendation
        if memory.get("genres") or memory.get("actors") or memory.get("directors"):
            movies = self.recommender.recommend_hybrid(memory)
        else:
            return "I don't know your taste yet! Tell me what kind of movies you like, and I'll find the perfect recommendation for you."

        if not movies:
            movies = self.recommender.get_top_rated(watched=memory.get("watched", []))

        if movies:
            reason = ", ".join(memory.get("genres", [memory.get("actors", [memory.get("directors", ["Top Rated"])])[0]])[0])
            return self._format_movie_response(movies, reason)
        else:
            return "I couldn't find any movies to recommend right now. Try telling me more about what you enjoy!"

    def _format_movie_response(self, movies, reason=""):
        """Format movie recommendations as a response string."""
        from ui.menu import print_movie_recommendation
        print_movie_recommendation(movies, reason)

        titles = [m["title"] for m in movies]

        # Try AI for a more engaging recommendation description
        if self.ai_available:
            memory = self.memory.get_user_memory()
            movie_list_text = "\n".join([f"- {m['title']} ({m.get('rating', 'N/A')}/10)" for m in movies[:5]])
            ai_response = ai_chat.generate_ai_recommendation(memory, movie_list_text)
            if ai_response:
                return ai_response

        return f"I recommend: {', '.join(titles[:3])}{' and more!' if len(titles) > 3 else ''}"

    def ask_smart_questions(self):
        """Ask the user smart questions to learn their preferences."""
        from ui.menu import print_smart_questions
        print_smart_questions()
        return "Let's get to know each other! Pick a question above and answer it."

    def learn_from_conversation(self):
        """Learn from the current conversation context."""
        memory = self.memory.get_user_memory()
        missing = []

        if not memory.get("genres"):
            missing.append("favorite genre")
        if not memory.get("actors"):
            missing.append("favorite actor")
        if not memory.get("directors"):
            missing.append("favorite director")

        if missing:
            return f"Can you tell me about your {', '.join(missing)}?"
        return None