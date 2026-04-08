import React, { useState } from 'react';
import '../styles/LoginPage.css';

function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('user'); 

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!email || !password) {
      alert("Please enter both email and password");
      return;
    }

    console.log(`Logging in as ${role}`);
    if (onLogin) {
      onLogin(role);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Welcome to ByteBites</h2>
        <p>Please sign in to continue</p>
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Email Address</label>
            <input 
              type="email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              placeholder="name@example.com"
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              placeholder="••••••••"
            />
          </div>

          <div className="role-selector">
            <label>Login as:</label>
            <div className="radio-group">
              <label>
                <input 
                  type="radio" 
                  value="user" 
                  checked={role === 'user'} 
                  onChange={() => setRole('user')} 
                />
                Customer
              </label>
              <label>
                <input 
                  type="radio" 
                  value="admin" 
                  checked={role === 'admin'} 
                  onChange={() => setRole('admin')} 
                />
                Manager
              </label>
            </div>
          </div>

          <button type="submit" className="login-submit-btn">
            Sign In
          </button>
        </form>

        <div className="login-footer">
          <p>Don't have an account? <a href="#signup">Create one</a></p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;