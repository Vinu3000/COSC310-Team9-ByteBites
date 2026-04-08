import { useState, useEffect } from 'react'
import './styles/App.css'
import Navbar from './components/Navbar'
import OrdersPage from './pages/OrdersPage'
import AdminRefundsPage from './pages/AdminRefundsPage'
import AdminPromosPage from './pages/AdminPromosPage'
import DiscoveryPage from './pages/DiscoveryPage'
import LoginPage from './pages/LoginPage' // Import the new LoginPage

function App() {
  const [currentPage, setCurrentPage] = useState('discovery') 
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  // Start with null to force login
  const [userRole, setUserRole] = useState(null) 

  const fetchOrders = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('http://localhost:8000/api/v1/orders')
      if (!response.ok) throw new Error('Failed to fetch orders')
      const data = await response.json()
      setOrders(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (userRole) {
      fetchOrders()
    }
  }, [userRole])

  const handleLogin = (role) => {
    setUserRole(role)
    setCurrentPage('discovery')
  }

  const handleLogout = () => {
    setUserRole(null)
    setCurrentPage('discovery')
  }

  const handleUpdateOrderPrice = (orderId, newTotal, discountAmount) => {
    setOrders(prevOrders => 
      prevOrders.map(order => 
        order.id === orderId 
          ? { ...order, total_price: newTotal, discount_applied: discountAmount } 
          : order
      )
    )
  }

  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  const handleRefundSuccess = () => {
    fetchOrders()
  }

  // ---Authorization Guard ---
  // If no user is logged in, show ONLY the Login Page
  if (!userRole) {
    return <LoginPage onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <Navbar 
        currentPage={currentPage} 
        onNavigate={handleNavigate} 
        userRole={userRole} 
        onLogout={handleLogout} 
      />
      
      <main className="app__main">
        {loading && <div className="loading">Loading...</div>}
        {error && <div className="error">Error: {error}</div>}
        
        {/* Discovery Page */}
        {currentPage === 'discovery' && (
          <DiscoveryPage />
        )}
        
        {/* User View: Orders Page */}
        {currentPage === 'orders' && (
          <OrdersPage 
            orders={orders} 
            onRefundSuccess={handleRefundSuccess}
            onUpdateOrder={handleUpdateOrderPrice} 
            loading={loading}
          />
        )}
        
        {/* Admin View: Refunds Page (Feat 1 Authorization) */}
        {currentPage === 'admin-refunds' && userRole === 'admin' && (
          <AdminRefundsPage 
            orders={orders}
            onRefundActionComplete={handleRefundSuccess}
          />
        )}

        {/* Admin View: Promos Page (Feat 1 Authorization) */}
        {currentPage === 'admin-promos' && userRole === 'admin' && (
          <AdminPromosPage />
        )}

        {/* Access Denied Guard */}
        {(currentPage === 'admin-refunds' || currentPage === 'admin-promos') && userRole !== 'admin' && (
          <div className="unauthorized">
            <h2>Access Denied</h2>
            <p>Manager permissions required to view this page.</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App