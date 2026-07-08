import sys
import os

# Ensure the script directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory import Memory
from recommender import Recommender
from chatbot import ChatBot
from database import Database
from ui.menu import (
    clear_screen, print_header, print_welcome, print_menu,
    get_choice, get_settings_choice, print_bot_message, print_user_message,
    print_movie_recommendation, print_memory_summary,
    print_movie_list, print_settings_menu, print_smart_questions
)
from ui.colors import Colors


class MovieBuddyApp:
    """Main application controller."""

    def __init__(self):
        self.memory = Memory()
        self.recommender = Recommender()
        self.chatbot = ChatBot(self.memory, self.recommender)
        self.db = Database()
        self.current_user = None

        # Import movies into database
        self.db.import_movies_from_json()

    def run(self):
        """Run the application main loop."""
        while True:
            print_welcome(self.current_user)
            print_menu()
            choice = get_choice()

            if choice == 1:
                self.login_menu()
            elif choice == 2:
                self.recommend_movie()
            elif choice == 3:
                self.rate_movie_menu()
            elif choice == 4:
                self.show_favorites()
            elif choice == 5:
                self.show_watch_history()
            elif choice == 6:
                self.chat_mode()
            elif choice == 7:
                self.search_movie_menu()
            elif choice == 8:
                self.settings_menu()
            elif choice == 9:
                self.exit_app()
                break
            else:
                print(f"\n{Colors.WARNING} Invalid option. Please try again.")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def login_menu(self):
        """Handle user login."""
        clear_screen()
        print_header()
        print(f"{Colors.BOLD}{Colors.CYAN}Login{Colors.RESET}\n")

        name = input(f"{Colors.ARROW} Enter your name: ").strip()
        if not name:
            return

        self.current_user = name
        user_data = self.memory.login(name)

        # Also login to database
        db_user = self.db.get_or_create_user(name)
        if user_data.get("country"):
            self.db.update_user(db_user["id"], country=user_data["country"])
        if user_data.get("language"):
            self.db.update_user(db_user["id"], language=user_data["language"])
        if user_data.get("age"):
            self.db.update_user(db_user["id"], age=user_data["age"])

        print(f"\n{Colors.GREEN}✓ Logged in as {name}{Colors.RESET}")

        # Show memory if exists
        memory = self.memory.get_user_memory()
        has_preferences = any([memory.get("genres"), memory.get("actors"), memory.get("directors")])
        if has_preferences:
            print_memory_summary(memory)

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def recommend_movie(self):
        """Show movie recommendations."""
        if not self.current_user:
            print(f"\n{Colors.WARNING} Please login first (Option 1).")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        clear_screen()
        print_header()
        print(f"{Colors.BOLD}{Colors.YELLOW}Movie Recommendations{Colors.RESET}\n")

        memory = self.memory.get_user_memory()

        if memory.get("genres") or memory.get("actors") or memory.get("directors"):
            movies = self.recommender.recommend_hybrid(memory)
            reason = ", ".join(memory.get("genres", [])) if memory.get("genres") else ""
            print_movie_recommendation(movies, reason)
        else:
            # No preferences yet - ask what they like
            print(f"{Colors.ROBOT} I don't know your taste yet!\n")
            genres = self.recommender.get_genres()
            print(f"{Colors.BOLD}Available genres:{Colors.RESET}")
            for i, genre in enumerate(genres, 1):
                print(f"   {Colors.CYAN}{i}.{Colors.RESET} {genre}")
            print()

            try:
                choice = int(input(f"{Colors.ARROW} Choose a genre (number): ").strip())
                if 1 <= choice <= len(genres):
                    selected_genre = genres[choice - 1]
                    self.memory.update_memory("genres", selected_genre)
                    movies = self.recommender.recommend_by_genre([selected_genre])
                    print_movie_recommendation(movies, selected_genre)
            except ValueError:
                pass

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def rate_movie_menu(self):
        """Rate a movie."""
        if not self.current_user:
            print(f"\n{Colors.WARNING} Please login first (Option 1).")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        clear_screen()
        print_header()
        print(f"{Colors.BOLD}{Colors.YELLOW}Rate a Movie{Colors.RESET}\n")

        title = input(f"{Colors.ARROW} Movie title: ").strip()
        if not title:
            return

        # Search for the movie
        results = self.recommender.search_movies(title)
        if not results:
            print(f"\n{Colors.WARNING} Movie not found in database.")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        # Show results
        print(f"\n{Colors.BOLD}Matching movies:{Colors.RESET}")
        for i, movie in enumerate(results[:5], 1):
            print(f"   {Colors.CYAN}{i}.{Colors.RESET} {movie['title']} ({movie.get('rating', 'N/A')}/10)")

        try:
            idx = int(input(f"\n{Colors.ARROW} Choose movie number: ").strip())
            if 1 <= idx <= len(results[:5]):
                selected = results[idx - 1]
                rating = int(input(f"{Colors.ARROW} Rating (1-10): ").strip())
                if 1 <= rating <= 10:
                    self.memory.rate_movie(selected["title"], rating)
                    print(f"\n{Colors.GREEN}✓ Rated {selected['title']} {rating}/10{Colors.RESET}")
                else:
                    print(f"\n{Colors.WARNING} Rating must be between 1 and 10.")
        except ValueError:
            pass

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def show_favorites(self):
        """Show user's favorite movies."""
        if not self.current_user:
            print(f"\n{Colors.WARNING} Please login first (Option 1).")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        clear_screen()
        print_header()
        favorites = self.memory.get_favorites()
        print_movie_list("Your Favorites", favorites)

        if favorites:
            print(f"{Colors.CYAN}1{Colors.RESET}  Add to Favorites")
            print(f"{Colors.CYAN}2{Colors.RESET}  Back")
            print()
            choice = get_choice()

            if choice == 1:
                title = input(f"{Colors.ARROW} Movie title: ").strip()
                if title:
                    # Check if movie exists
                    movie = self.recommender.get_movie_by_title(title)
                    if movie:
                        self.memory.add_favorite(movie["title"])
                        print(f"\n{Colors.GREEN}✓ Added {movie['title']} to favorites!{Colors.RESET}")
                    else:
                        print(f"\n{Colors.WARNING} Movie not found. You can still add it.")
                        self.memory.add_favorite(title)
                        print(f"\n{Colors.GREEN}✓ Added {title} to favorites!{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        else:
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def show_watch_history(self):
        """Show user's watch history."""
        if not self.current_user:
            print(f"\n{Colors.WARNING} Please login first (Option 1).")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        clear_screen()
        print_header()
        history = self.memory.get_watch_history()
        titles = [h["movie"] for h in history]
        print_movie_list("Watch History", titles)
        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def chat_mode(self):
        """Interactive chat mode."""
        if not self.current_user:
            print(f"\n{Colors.WARNING} Please login first (Option 1).")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        clear_screen()
        print_header()

        # Show AI availability badge
        import ai_chat
        ai_badge = f"{Colors.GREEN}[AI] " if ai_chat.is_available() else f"{Colors.DIM}[Local] "
        print(f"{Colors.ROBOT} {Colors.BOLD}Chat Mode {ai_badge}{Colors.RESET}")
        if ai_chat.is_available():
            print(f"{Colors.GREEN}✓ Gemini AI is active for smarter responses{Colors.RESET}")
        print(f"{Colors.DIM}Type 'exit' to go back to menu{Colors.RESET}\n")

        memory = self.memory.get_user_memory()
        has_preferences = any([memory.get("genres"), memory.get("actors"), memory.get("directors")])

        if has_preferences:
            print(f"{Colors.ROBOT} Welcome back, {Colors.GREEN}{self.current_user}{Colors.RESET}!")
            print_memory_summary(memory)
            print(f"{Colors.ROBOT} What movie are you looking for today?\n")
        else:
            print(f"{Colors.ROBOT} Welcome! I'm Movie Buddy, your personal movie recommender!")
            print(f"   Tell me what kind of movies you enjoy, and I'll learn your taste!\n")

        while True:
            try:
                user_input = input(f"{Colors.BOLD}You: {Colors.RESET}").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.lower() in ["exit", "quit", "back", "menu"]:
                break

            if user_input:
                print_user_message(user_input)
                response = self.chatbot.process_message(user_input)
                print_bot_message(response)

    def search_movie_menu(self):
        """Search for movies."""
        clear_screen()
        print_header()
        print(f"{Colors.BOLD}{Colors.YELLOW}Search Movies{Colors.RESET}\n")

        query = input(f"{Colors.ARROW} Search: ").strip()
        if query:
            results = self.recommender.search_movies(query)
            if results:
                from ui.menu import print_movie_recommendation
                print_movie_recommendation(results)
            else:
                print(f"\n{Colors.WARNING} No movies found matching '{query}'.")
        else:
            # Show all movies grouped by genre
            genres = self.recommender.get_genres()
            print(f"{Colors.BOLD}Browse by Genre:{Colors.RESET}\n")
            for i, genre in enumerate(genres, 1):
                count = len(self.recommender.get_movies_by_genre(genre))
                print(f"   {Colors.CYAN}{i}.{Colors.RESET} {genre} ({count} movies)")

            try:
                choice = int(input(f"\n{Colors.ARROW} Choose genre (number): ").strip())
                if 1 <= choice <= len(genres):
                    genre = genres[choice - 1]
                    movies = self.recommender.get_movies_by_genre(genre)
                    print_movie_list(f"{genre} Movies", [m["title"] for m in movies])
            except ValueError:
                pass

        input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    def settings_menu(self):
        """Settings menu."""
        if not self.current_user:
            print(f"\n{Colors.WARNING} Please login first (Option 1).")
            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
            return

        while True:
            clear_screen()
            print_header()
            print_settings_menu()
            choice = get_settings_choice()

            if choice == 1:
                name = input(f"{Colors.ARROW} New name: ").strip()
                if name:
                    old_user = self.current_user
                    self.current_user = name
                    user_data = self.memory.login(name)
                    print(f"\n{Colors.GREEN}✓ Name changed from '{old_user}' to '{name}'{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == 2:
                country = input(f"{Colors.ARROW} Country: ").strip()
                if country:
                    self.memory.update_memory("country", country)
                    print(f"\n{Colors.GREEN}✓ Country set to '{country}'{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == 3:
                language = input(f"{Colors.ARROW} Language: ").strip()
                if language:
                    self.memory.update_memory("language", language)
                    print(f"\n{Colors.GREEN}✓ Language set to '{language}'{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == 4:
                age = input(f"{Colors.ARROW} Age: ").strip()
                if age:
                    self.memory.update_memory("age", age)
                    print(f"\n{Colors.GREEN}✓ Age set to '{age}'{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == 5:
                confirm = input(f"\n{Colors.WARNING} Clear all memory? (yes/no): ").strip().lower()
                if confirm == "yes":
                    self.memory.clear_memory()
                    print(f"\n{Colors.GREEN}✓ Memory cleared!{Colors.RESET}")
                input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

            elif choice == 6:
                break

    def exit_app(self):
        """Exit the application."""
        clear_screen()
        print_header()
        print(f"{Colors.ROBOT} Thanks for using Movie Buddy! See you next time! 🎬\n")
        self.db.close()


def main():
    """Application entry point."""
    try:
        app = MovieBuddyApp()
        app.run()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Colors.ROBOT} Goodbye! 🎬\n")
    except Exception as e:
        print(f"\n{Colors.CROSS} Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()