import React, { useState, useRef, useEffect } from 'react';
import { Bot, Target, Clapperboard, Smile, Search, Clapperboard as ClapperboardIcon, Save } from 'lucide-react';
import { api } from '../api/api';
import './ChatBot.css';

function ChatBot({ user, onLoginClick, onClose, onMovieClick }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (user) {
      loadChatHistory();
    } else {
      setMessages([{
        role: 'assistant',
        content: 'Hey there! Sign in to start chatting with me. I\'ll help you discover amazing movies!',
        timestamp: new Date().toISOString()
      }]);
    }
  }, [user]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatHistory = async () => {
    try {
      const data = await api.getChatHistory();
      if (data.messages && data.messages.length > 0) {
        setMessages(data.messages);
      } else {
        setMessages([{
          role: 'assistant',
          content: `Welcome back, ${user.name}! Tell me what kind of movies you're in the mood for, and I'll find the perfect recommendation for you!`,
          timestamp: new Date().toISOString()
        }]);
      }
    } catch {
      setMessages([{
        role: 'assistant',
        content: 'Hey there! Tell me what kind of movies you enjoy, and I\'ll help you find your next favorite film!',
        timestamp: new Date().toISOString()
      }]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    if (!user) {
      onLoginClick();
      return;
    }

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await api.sendMessage(userMessage.content);
      const botMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I had trouble connecting. Please try again!',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAction = async (action) => {
    if (!user) {
      onLoginClick();
      return;
    }
    setInput(action);
    // Auto-submit after brief delay
    setTimeout(() => {
      const form = document.querySelector('.chat-form');
      if (form) form.dispatchEvent(new Event('submit', { cancelable: true }));
    }, 100);
  };

  return (
    <div className={`chat-container ${isOpen ? 'open' : ''}`}>
      <div className="chat-header">
        <div className="chat-header-left">
          <div className="chat-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
            </svg>
          </div>
          <div className="chat-header-info">
            <h3 className="chat-header-title">MovieBuddy AI</h3>
            <span className="chat-header-status">Online</span>
          </div>
        </div>
        <div className="chat-header-actions">
          <button className="chat-header-btn" onClick={onClose} title="Close chat">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.role}`}>
            {msg.role === 'assistant' && (
              <div className="message-avatar"><Bot size={18} /></div>
            )}
            <div className="message-content">
              <p>{msg.content}</p>
              <span className="message-time">
                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="chat-message assistant">
            <div className="message-avatar"><Bot size={18} /></div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {user && messages.length <= 1 && (
        <div className="chat-quick-actions">
          <p className="quick-actions-title">Try asking:</p>
          <div className="quick-actions-grid">
            <button
              className="quick-action-btn"
              onClick={() => handleQuickAction('Recommend me a movie')}
            >
              <Target size={16} /> Recommend
            </button>
            <button
              className="quick-action-btn"
              onClick={() => handleQuickAction('I like Action movies')}
            >
              <Clapperboard size={16} /> Action
            </button>
            <button
              className="quick-action-btn"
              onClick={() => handleQuickAction('I feel like watching Comedy')}
            >
              <Smile size={16} /> Comedy
            </button>
            <button
              className="quick-action-btn"
              onClick={() => handleQuickAction('Search for Inception')}
            >
              <Search size={16} /> Search
            </button>
            <button
              className="quick-action-btn"
              onClick={() => handleQuickAction('I like Christopher Nolan movies')}
            >
              <ClapperboardIcon size={16} /> Directors
            </button>
            <button
              className="quick-action-btn"
              onClick={() => handleQuickAction('Remember me what you know')}
            >
              <Save size={16} /> My Taste
            </button>
          </div>
        </div>
      )}

      {!user && (
        <div className="chat-login-prompt">
          <button className="chat-login-btn" onClick={onLoginClick}>
            Sign in to Chat
          </button>
        </div>
      )}

      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          className="chat-input"
          placeholder={user ? "Ask me about movies..." : "Sign in to chat..."}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={!user || isLoading}
        />
        <button
          type="submit"
          className="chat-send-btn"
          disabled={!input.trim() || !user || isLoading}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </form>
    </div>
  );
}

export default ChatBot;