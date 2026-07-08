import React from 'react';
import { Clapperboard, Heart, ArrowUp } from 'lucide-react';

function Footer({ showChat, onChatClick }) {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className={`footer ${showChat ? 'chat-open' : ''}`}>
      <div className="footer-content">
        <div className="footer-top">
          <div className="footer-brand">
            <div className="footer-logo">
              <Clapperboard size={24} />
              <span>MovieBuddy</span>
            </div>
            <p className="footer-tagline">
              Your personal movie recommendation companion
            </p>
          </div>
          
          <div className="footer-links">
            <div className="footer-column">
              <h4>Navigation</h4>
              <a href="#home">Home</a>
              <a href="#popular">Popular</a>
              <a href="#top-rated">Top Rated</a>
            </div>
            
            <div className="footer-column">
              <h4>Features</h4>
              <a href="#personalized">Personalized</a>
              <a href="#genres">Browse Genres</a>
              <button className="footer-link-btn" onClick={onChatClick}>
                AI Chat
              </button>
            </div>
            
            <div className="footer-column">
              <h4>Connect</h4>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="social-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14.35 6.44-1.53 6.44-6.05 0-.52-.08-1.02-.23-1.52A4.65 4.65 0 0 0 21 6.5a4.65 4.65 0 0 0-1.33-3.21 3.38 3.38 0 0 0-1.04-.63c-.52-.15-1.02-.23-1.52-.23s-1.02.08-1.52.23a3.38 3.38 0 0 0-1.04.63A4.65 4.65 0 0 0 6.5 5a4.65 4.65 0 0 0-1.33 3.21 3.38 3.38 0 0 0-.23 1.52c0 4.52 3.3 6.4 6.44 6.05a3.37 3.37 0 0 0 .94 2.61v3.87" />
                </svg>
                GitHub
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="social-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 4.48 0 0 1-7 2c9 5 20 0 20-11.5a10.5 10.5 0 0 0-.08-.5v.08A7.76 7.76 0 0 0 23 3z" />
                </svg>
                Twitter
              </a>
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="social-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z" />
                </svg>
                Facebook
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="social-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
                  <path d="M16 11.37A7 7 0 1 1 11.37 8 7 7 0 0 1 16 11.37z" />
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
                </svg>
                Instagram
              </a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p className="footer-copyright">
            © {new Date().getFullYear()} MovieBuddy. All rights reserved.
          </p>
          <div className="footer-bottom-right">
            <p className="footer-made-with">
              Made with <Heart size={14} fill="currentColor" /> for movie lovers
            </p>
            <button className="back-to-top" onClick={scrollToTop} title="Back to top">
              <ArrowUp size={18} />
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
