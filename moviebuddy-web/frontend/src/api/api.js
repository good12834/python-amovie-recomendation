const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const config = {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Something went wrong');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError') {
      throw new Error('Network error. Is the server running?');
    }
    throw error;
  }
}

export const api = {
  // Auth
  login: (name) =>
    request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ name }),
    }),

  getMe: () =>
    request('/auth/me'),

  logout: () =>
    request('/auth/logout', { method: 'POST' }),

  // Movies
  getPopular: (page = 1) =>
    request(`/movies/popular?page=${page}`),

  getTopRated: (page = 1) =>
    request(`/movies/top-rated?page=${page}`),

  searchMovies: (query, page = 1) =>
    request(`/movies/search?query=${encodeURIComponent(query)}&page=${page}`),

  getMovieDetails: (movieId) =>
    request(`/movies/${movieId}`),

  getMoviesByGenre: (genre, page = 1) =>
    request(`/movies/genre/${encodeURIComponent(genre)}?page=${page}`),

  getGenres: () =>
    request('/genres'),

  getMovieVideos: (movieId) =>
    request(`/movies/${movieId}/videos`),

  getMovieRecommendations: (movieId) =>
    request(`/movies/recommendations/${movieId}`),

  // Personalized recommendations
  getPersonalized: () =>
    request('/recommendations/personalized'),

  // User preferences
  getPreferences: () =>
    request('/user/preferences'),

  updatePreferences: (data) =>
    request('/user/preferences', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Favorites
  addFavorite: (movie) =>
    request('/user/favorites', {
      method: 'POST',
      body: JSON.stringify(movie),
    }),

  removeFavorite: (movieTitle) =>
    request('/user/favorites', {
      method: 'DELETE',
      body: JSON.stringify({ movie_title: movieTitle }),
    }),

  // Ratings
  addRating: (movieTitle, rating, movieId) =>
    request('/user/ratings', {
      method: 'POST',
      body: JSON.stringify({ movie_title: movieTitle, rating, movie_id: movieId }),
    }),

  // Watch history
  addToWatchHistory: (movieTitle, movieId) =>
    request('/user/watch-history', {
      method: 'POST',
      body: JSON.stringify({ movie_title: movieTitle, movie_id: movieId }),
    }),

  // Chat
  sendMessage: (message) =>
    request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    }),

  getChatHistory: () =>
    request('/chat/history'),
};