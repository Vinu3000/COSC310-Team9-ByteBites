import { useState, useEffect } from 'react'
import './styles/App.css'
import Navbar from './components/Navbar'
import OrdersPage from './pages/OrdersPage'
import AdminRefundsPage from './pages/AdminRefundsPage'
import AdminPromosPage from './pages/AdminPromosPage'
import DiscoveryPage from './pages/DiscoveryPage'
import LoginPage from './pages/LoginPage'

function App() {
  // Initialize state from localStorage to persist after refresh
  const [currentPage, setCurrentPage] = useState(() => {
    return localStorage.getItem('currentPage') || 'discovery'
  })
  
  const [userRole, setUserRole] = useState(() => {
    return localStorage.getItem('userRole') || null
  })

  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Sync state changes to localStorage
  useEffect(() => {
    if (userRole) {
      localStorage.setItem('userRole', userRole)
    } else {
      localStorage.removeItem('userRole')
    }
  }, [userRole])

  useEffect(() => {
    localStorage.setItem('currentPage', currentPage)
  }, [currentPage])

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
    // Keep current page if it exists, otherwise go to discovery
    const targetPage = localStorage.getItem('currentPage') || 'discovery'
    setCurrentPage(targetPage)
  }

  const handleLogout = () => {
    setUserRole(null)
    setCurrentPage('discovery')
    localStorage.clear() // Clear all persisted data on logout
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

  // --- Authorization Guard ---
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
        
        {currentPage === 'discovery' && (
          <DiscoveryPage />
        )}
        
        {currentPage === 'orders' && (
          <OrdersPage 
            orders={orders} 
            onRefundSuccess={handleRefundSuccess}
            onUpdateOrder={handleUpdateOrderPrice} 
            loading={loading}
          />
        )}
        
        {currentPage === 'admin-refunds' && userRole === 'admin' && (
          <AdminRefundsPage 
            orders={orders}
            onRefundActionComplete={handleRefundSuccess}
          />
        )}

        {currentPage === 'admin-promos' && userRole === 'admin' && (
          <AdminPromosPage />
        )}

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