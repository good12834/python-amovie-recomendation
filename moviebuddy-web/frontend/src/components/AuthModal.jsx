import React, { useState } from 'react';
import { Clapperboard, Target, Heart, Bot, Save } from 'lucide-react';
import './AuthModal.css';

function AuthModal({ onLogin, onClose }) {
  const [name, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError('Please enter your name');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      await onLogin(name.trim());
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="auth-modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        <div className="auth-logo">
          <span className="auth-logo-icon"><Clapperboard size={40} /></span>
          <h2 className="auth-title">
            Welcome to <span className="auth-accent">MovieBuddy</span>
          </h2>
        </div>

        <p className="auth-subtitle">
          Sign in to get personalized movie recommendations, save favorites, and chat with our AI assistant!
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-input-group">
            <label className="auth-label">Your Name</label>
            <input
              type="text"
              className="auth-input"
              placeholder="Enter your name..."
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                setError('');
              }}
              autoFocus
              disabled={isLoading}
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button
            type="submit"
            className="auth-submit"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="auth-loading-spinner" />
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="auth-features">
          <div className="auth-feature">
            <span className="feature-icon"><Target size={18} /></span>
            <span className="feature-text">Personalized recommendations</span>
          </div>
          <div className="auth-feature">
            <span className="feature-icon"><Heart size={18} /></span>
            <span className="feature-text">Save favorites & rate movies</span>
          </div>
          <div className="auth-feature">
            <span className="feature-icon"><Bot size={18} /></span>
            <span className="feature-text">AI chat assistant</span>
          </div>
          <div className="auth-feature">
            <span className="feature-icon"><Save size={18} /></span>
            <span className="feature-text">Your taste remembered</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AuthModal;