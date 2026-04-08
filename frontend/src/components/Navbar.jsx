import '../styles/Navbar.css'

function Navbar({ currentPage, onNavigate, userRole }) {
  return (
    <nav className="navbar">
      <div className="navbar__container">
        <div className="navbar__logo">
          <h1>🍕 ByteBites</h1>
        </div>
        
        <ul className="navbar__links">
          <li>
            <button
              className={`navbar__link ${currentPage === 'orders' ? 'navbar__link--active' : ''}`}
              onClick={() => onNavigate('orders')}
            >
              Orders
            </button>
          </li>
          
          {userRole === 'admin' && (
            <li>
              <button
                className={`navbar__link ${currentPage === 'admin-refunds' ? 'navbar__link--active' : ''}`}
                onClick={() => onNavigate('admin-refunds')}
              >
                Admin: Refunds
              </button>
            </li>
          )}
        </ul>

        <div className="navbar__user">
          <span className="navbar__role">{userRole === 'admin' ? '👤 Admin' : '👤 User'}</span>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
