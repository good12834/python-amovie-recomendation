import React, { useState, useEffect } from 'react';
import { Clapperboard, Menu, X } from 'lucide-react';
import './Navbar.css';

function Navbar({ user, onLoginClick, onLogout, onChatClick, onSearchClick, showChat }) {
  const [scrolled, setScrolled] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const closeMobileMenu = () => setShowMobileMenu(false);

  return (
    <>
      <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
        <div className="navbar-left">
          <a href="/" className="navbar-logo">
            <span className="logo-icon"><Clapperboard size={22} /></span>
            <span className="logo-text">
              Movie<span className="logo-accent">Buddy</span>
            </span>
          </a>
          
          {/* Mobile menu button */}
          <button
            className="mobile-menu-btn"
            onClick={() => setShowMobileMenu(true)}
            aria-label="Open menu"
          >
            <Menu size={22} />
          </button>
          
          {/* Desktop links */}
          <div className="navbar-links">
            <a href="#home" className="nav-link active">Home</a>
            <a href="#popular" className="nav-link">Popular</a>
            <a href="#top-rated" className="nav-link">Top Rated</a>
          </div>
        </div>

        <div className="navbar-right">
          <button
            className="nav-icon-btn"
            onClick={onSearchClick}
            title="Search"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
          </button>

          <button
            className={`nav-icon-btn chat-btn ${showChat ? 'active' : ''}`}
            onClick={onChatClick}
            title="AI Chat"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
            </svg>
          </button>

          {user ? (
            <div className="user-menu" onClick={() => setShowUserMenu(!showUserMenu)}>
              <div className="user-avatar">
                {user.name.charAt(0).toUpperCase()}
              </div>
              {showUserMenu && (
                <div className="user-dropdown">
                  <div className="dropdown-header">
                    <span className="dropdown-name">{user.name}</span>
                  </div>
                  <div className="dropdown-divider"></div>
                  <button className="dropdown-item" onClick={onLogout}>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" />
                      <polyline points="16 17 21 12 16 7" />
                      <line x1="21" y1="12" x2="9" y2="12" />
                    </svg>
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button className="login-btn" onClick={onLoginClick}>
              Sign In
            </button>
          )}
        </div>
      </nav>

      {/* Mobile menu overlay */}
      {showMobileMenu && (
        <div className="mobile-menu-overlay">
          <div className="mobile-menu-header">
            <a href="/" className="navbar-logo" onClick={closeMobileMenu}>
              <span className="logo-icon"><Clapperboard size={24} /></span>
              <span className="logo-text">
                Movie<span className="logo-accent">Buddy</span>
              </span>
            </a>
            <button
              className="mobile-menu-close"
              onClick={closeMobileMenu}
              aria-label="Close menu"
            >
              <X size={24} />
            </button>
          </div>
          
          <div className="mobile-nav-links">
            <a href="#home" className="mobile-nav-link active" onClick={closeMobileMenu}>Home</a>
            <a href="#popular" className="mobile-nav-link" onClick={closeMobileMenu}>Popular</a>
            <a href="#top-rated" className="mobile-nav-link" onClick={closeMobileMenu}>Top Rated</a>
          </div>
        </div>
      )}
    </>
  );
}

export default Navbar;