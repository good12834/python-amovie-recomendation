import os
from .colors import Colors


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the main header."""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'=' * 26}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}   {Colors.MOVIE} Movie Buddy{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'=' * 26}{Colors.RESET}")
    print()


def print_welcome(username=None):
    """Print welcome message for a user."""
    clear_screen()
    print_header()
    if username:
        print(f"{Colors.BOLD}Welcome back, {Colors.GREEN}{username}{Colors.RESET}!\n")
    else:
        print(f"{Colors.BOLD}Welcome to Movie Buddy!{Colors.RESET}\n")


def print_menu():
    """Print the main menu options."""
    print(f"{Colors.CYAN}1{Colors.RESET}  Login")
    print(f"{Colors.CYAN}2{Colors.RESET}  Recommend Movie")
    print(f"{Colors.CYAN}3{Colors.RESET}  Rate Movie")
    print(f"{Colors.CYAN}4{Colors.RESET}  Favorites")
    print(f"{Colors.CYAN}5{Colors.RESET}  Watch History")
    print(f"{Colors.CYAN}6{Colors.RESET}  Chat")
    print(f"{Colors.CYAN}7{Colors.RESET}  Search Movie")
    print(f"{Colors.CYAN}8{Colors.RESET}  Settings")
    print(f"{Colors.CYAN}9{Colors.RESET}  Exit")
    print()


def get_choice(prompt="Choose an option: "):
    """Get a menu choice from the user. Accepts numbers or text commands."""
    raw = input(f"{Colors.ARROW} {prompt}").strip().lower()
    # Try numeric first
    try:
        return int(raw)
    except ValueError:
        pass
    # Map text commands to numbers
    cmd_map = {
        "login": 1, "log in": 1, "sign in": 1,
        "recommend": 2, "recommendation": 2, "recommendations": 2, "suggest": 2,
        "rate": 3, "rating": 3,
        "favorites": 4, "favorite": 4, "fav": 4, "favs": 4,
        "history": 5, "watch history": 5, "watched": 5,
        "chat": 6, "talk": 6, "converse": 6,
        "search": 7, "find": 7, "browse": 7,
        "settings": 8, "setting": 8, "preferences": 8, "prefs": 8,
        "exit": 9, "quit": 9, "bye": 9, "goodbye": 9, "leave": 9, "back": 9
    }
    return cmd_map.get(raw, -1)


def get_settings_choice(prompt="Choose an option: "):
    """Get a settings menu choice. Accepts numbers or text commands."""
    raw = input(f"{Colors.ARROW} {prompt}").strip().lower()
    try:
        return int(raw)
    except ValueError:
        pass
    cmd_map = {
        "name": 1, "change name": 1, "rename": 1,
        "country": 2, "set country": 2,
        "language": 3, "lang": 3, "set language": 3, "set lang": 3,
        "age": 4, "set age": 4,
        "clear": 5, "clear memory": 5, "reset": 5, "wipe": 5,
        "back": 6, "return": 6, "menu": 6, "main": 6, "exit": 6, "quit": 6
    }
    return cmd_map.get(raw, -1)


def print_bot_message(message):
    """Print a message from the bot."""
    print(f"\n{Colors.ROBOT} {Colors.BOLD}Movie Buddy:{Colors.RESET}")
    print(f"   {message}")
    print()


def print_user_message(message):
    """Print a user message."""
    print(f"\n{Colors.BOLD}You:{Colors.RESET}")
    print(f"   {message}")
    print()


def print_movie_recommendation(movies, reason=""):
    """Print a list of recommended movies."""
    if reason:
        print(f"\n{Colors.ROBOT} {Colors.BOLD}Because you enjoy {Colors.YELLOW}{reason}{Colors.RESET}...\n")
    else:
        print(f"\n{Colors.ROBOT} {Colors.BOLD}Based on your taste, I recommend:{Colors.RESET}\n")

    for i, movie in enumerate(movies, 1):
        rating_str = ""
        if movie.get("rating"):
            rating_str = f" {Colors.DIM}({movie['rating']}/10){Colors.RESET}"
        genre_str = ""
        if movie.get("genre"):
            genre_str = f" {Colors.DIM}[{movie['genre']}]{Colors.RESET}"
        print(f"   {Colors.STAR} {Colors.BOLD}{movie['title']}{Colors.RESET}{genre_str}{rating_str}")

    print()


def print_memory_summary(memory):
    """Print a summary of what the bot remembers about the user."""
    print(f"\n{Colors.ROBOT} {Colors.BOLD}I remember you like:{Colors.RESET}\n")

    if memory.get("genres"):
        for g in memory["genres"]:
            print(f"   {Colors.CHECK} {Colors.GREEN}{g}{Colors.RESET}")

    if memory.get("actors"):
        for a in memory["actors"]:
            print(f"   {Colors.CHECK} {Colors.CYAN}{a}{Colors.RESET}")

    if memory.get("directors"):
        for d in memory["directors"]:
            print(f"   {Colors.CHECK} {Colors.MAGENTA}{d}{Colors.RESET}")

    print()


def print_movie_list(title, movies):
    """Print a list of movies with a title."""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{title}{Colors.RESET}\n")
    if not movies:
        print(f"   {Colors.DIM}No movies yet.{Colors.RESET}\n")
        return
    for i, movie in enumerate(movies, 1):
        print(f"   {Colors.CYAN}{i}.{Colors.RESET} {Colors.BOLD}{movie}{Colors.RESET}")
    print()


def print_settings_menu():
    """Print settings menu."""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}Settings{Colors.RESET}\n")
    print(f"{Colors.CYAN}1{Colors.RESET}  Change Name")
    print(f"{Colors.CYAN}2{Colors.RESET}  Set Country")
    print(f"{Colors.CYAN}3{Colors.RESET}  Set Language")
    print(f"{Colors.CYAN}4{Colors.RESET}  Set Age")
    print(f"{Colors.CYAN}5{Colors.RESET}  Clear Memory")
    print(f"{Colors.CYAN}6{Colors.RESET}  Back")
    print()


def print_smart_questions():
    """Print smart questions the bot can ask."""
    print(f"\n{Colors.ROBOT} {Colors.BOLD}Let me ask you a few questions:{Colors.RESET}\n")
    questions = [
        "What's your favorite genre?",
        "Favorite actor?",
        "Favorite director?",
        "Do you prefer old or new movies?",
        "Marvel or DC?",
        "Do you enjoy anime?",
        "Which languages?",
        "How much time do you have?",
        "Happy or sad mood?"
    ]
    for q in questions:
        print(f"   {Colors.ARROW} {q}")
    print()