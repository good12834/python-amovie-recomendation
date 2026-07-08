# MovieBuddy

A smart movie recommendation system with both CLI and web interfaces. MovieBuddy helps you discover movies based on your preferences, with AI-powered chat functionality for natural language interactions.

## 🎬 Features

- **Personalized Recommendations**: Get movie suggestions based on your favorite genres, actors, and directors
- **AI Chat Assistant**: Interactive chat mode powered by Gemini AI (or local fallback)
- **User Profiles**: Save your preferences, ratings, and watch history
- **Search & Browse**: Find movies by title or browse by genre
- **Favorites**: Keep track of movies you want to watch
- **Two Interfaces**: 
  - CLI application for terminal users
  - Modern web app with React frontend

## 📁 Project Structure

```
python-amovie-recomendation/
├── MovieBuddy/                 # CLI Application
│   ├── app.py                  # Main application entry point
│   ├── recommender.py          # Movie recommendation logic
│   ├── chatbot.py              # Chat functionality
│   ├── memory.py               # User data management
│   ├── database.py             # SQLite database operations
│   ├── ai_chat.py              # Gemini AI integration
│   ├── movies.json             # Movie database
│   ├── requirements.txt          # Python dependencies
│   └── .env.example            # Environment template
│
└── moviebuddy-web/             # Web Application
    ├── backend/                  # Flask API server
    │   ├── app.py              # API endpoints
    │   ├── tmdb_api.py         # TMDb API integration
    │   ├── ai_chat.py          # AI chat for web
    │   ├── requirements.txt      # Backend dependencies
    │   └── .env.example        # Environment template
    │
    └── frontend/                 # React frontend
        ├── package.json
        ├── vite.config.js
        └── src/
            ├── App.jsx
            ├── api/
            └── components/
```

## 🚀 Quick Start

### CLI Version (MovieBuddy)

1. **Install dependencies**:
   ```bash
   cd MovieBuddy
   pip install -r requirements.txt
   ```

2. **Set up environment** (optional, for AI features):
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key from https://aistudio.google.com/
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

### Web Version (moviebuddy-web)

1. **Set up backend**:
   ```bash
   cd moviebuddy-web/backend
   pip install -r requirements.txt
   cp .env.example .env
   # Add your TMDb and Gemini API keys
   ```

2. **Set up frontend**:
   ```bash
   cd moviebuddy-web/frontend
   npm install
   ```

3. **Start the application**:
   - **Windows**: Run `start.bat` from the `moviebuddy-web` directory
   - **Linux/Mac**: Run `./start.sh` from the `moviebuddy-web` directory

   Or manually:
   ```bash
   # Terminal 1 - Backend
   cd moviebuddy-web/backend
   python app.py

   # Terminal 2 - Frontend
   cd moviebuddy-web/frontend
   npm run dev
   ```

## 🔧 Configuration

### CLI Version (.env)
- `GEMINI_API_KEY`: Your Google Gemini API key for AI chat features

### Web Version (.env)
- `TMDB_API_KEY`: The Movie Database API key
- `TMDB_ACCESS_TOKEN`: TMDb access token
- `SECRET_KEY`: Flask session secret key
- `GEMINI_API_KEY`: Google Gemini API key for AI features

## 📦 Dependencies

### CLI Version
- `rich` - Rich text and beautiful formatting in the terminal
- `colorama` - Cross-platform colored terminal text
- `sentence-transformers` - Semantic search for movie recommendations
- `faiss-cpu` - Efficient similarity search
- `python-dotenv` - Environment variable management
- `google-genai` - Gemini AI API client

### Web Version
**Backend:**
- `flask` - Web framework
- `flask-cors` - Cross-origin resource sharing
- `requests` - HTTP library
- `python-dotenv` - Environment variable management
- `google-genai` - Gemini AI API client

**Frontend:**
- `react` - UI library
- `vite` - Build tool
- `lucide-react` - Icon library

## 🎯 CLI Features

1. **Login** - Create or access your user profile
2. **Get Recommendations** - Receive personalized movie suggestions
3. **Rate Movies** - Rate movies to improve recommendations
4. **View Favorites** - See your saved favorite movies
5. **Watch History** - View your recently viewed movies
6. **Chat Mode** - Talk to the AI assistant about movies
7. **Search Movies** - Find movies by title or genre
8. **Settings** - Update your profile and preferences

## 🌐 Web Features

- Modern, responsive UI built with React
- Movie browsing with TMDb integration
- AI-powered chatbot for movie discovery
- User authentication
- Movie details, trailers, and ratings

## 📄 License

MIT License