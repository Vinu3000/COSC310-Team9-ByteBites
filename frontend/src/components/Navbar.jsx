import React, { useState } from 'react';
import NotificationBell from './NotificationBell';
import '../styles/Navbar.css';

function Navbar({ currentPage, onNavigate, userRole, onLogin, onLogout }) {
  // Local state to show/hide a simple login dropdown
  const [showLoginOptions, setShowLoginOptions] = useState(false);

  return (
    <nav className="navbar">
      <div className="navbar__container">
        <div className="navbar__logo">
          <h1>🍕 ByteBites</h1>
        </div>
        
        <ul className="navbar__links">
          <li>
            <button
              className={`navbar__link ${currentPage === 'discovery' ? 'navbar__link--active' : ''}`}
              onClick={() => onNavigate('discovery')}
            >
              Explore
            </button>
          </li>

          {/* Users can track history. 
              Only show Orders if a user is logged in (role is user or admin) */}
          {userRole && (
            <li>
              <button
                className={`navbar__link ${currentPage === 'orders' ? 'navbar__link--active' : ''}`}
                onClick={() => onNavigate('orders')}
              >
                Orders
              </button>
            </li>
          )}
          
          {/* Authorization for Manager/Admin roles only */}
          {userRole === 'admin' && (
            <>
              <li>
                <button
                  className={`navbar__link ${currentPage === 'admin-refunds' ? 'navbar__link--active' : ''}`}
                  onClick={() => onNavigate('admin-refunds')}
                >
                  Admin: Refunds
                </button>
              </li>
              <li>
                <button
                  className={`navbar__link ${currentPage === 'admin-promos' ? 'navbar__link--active' : ''}`}
                  onClick={() => onNavigate('admin-promos')}
                >
                  Admin: Promos
                </button>
              </li>
            </>
          )}
        </ul>

        {userRole && <NotificationBell />}

        <div className="navbar__user">
          {!userRole ? (
            <div className="auth-actions">
              <button className="login-trigger" onClick={() => setShowLoginOptions(!showLoginOptions)}>
                Log In
              </button>
              {showLoginOptions && (
                <div className="login-dropdown">
                  <button onClick={() => { onLogin('user'); setShowLoginOptions(false); }}>As Regular User</button>
                  <button onClick={() => { onLogin('admin'); setShowLoginOptions(false); }}>As Manager</button>
                </div>
              )}
            </div>
          ) : (
            <div className="user-info">
              <span className="navbar__role">
                {userRole === 'admin' ? '🛡️ Manager' : '👤 Customer'}
              </span>
              <button className="logout-btn" onClick={onLogout}>Log Out</button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;