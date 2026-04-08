import { useState, useEffect } from 'react'
import './styles/App.css'
import Navbar from './components/Navbar'
import OrdersPage from './pages/OrdersPage'
import AdminRefundsPage from './pages/AdminRefundsPage'

function App() {
  const [currentPage, setCurrentPage] = useState('orders')
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [userRole, setUserRole] = useState('user') // 'user' or 'admin'

  // Fetch orders from backend
  const fetchOrders = async () => {
    setLoading(true)
    setError(null)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/v1/orders', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
      if (!response.ok) throw new Error('Failed to fetch orders')
      const data = await response.json()
      setOrders(data)
    } catch (err) {
      setError(err.message)
      console.error('Fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchOrders()
  }, [])

  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  const handleRefundSuccess = () => {
    fetchOrders()
  }

  return (
    <div className="app">
      <Navbar currentPage={currentPage} onNavigate={handleNavigate} userRole={userRole} />
      
      <main className="app__main">
        {loading && <div className="loading">Loading...</div>}
        {error && <div className="error">Error: {error}</div>}
        
        {currentPage === 'orders' && (
          <OrdersPage 
            orders={orders} 
            onRefundSuccess={handleRefundSuccess}
            loading={loading}
          />
        )}
        
        {currentPage === 'admin-refunds' && userRole === 'admin' && (
          <AdminRefundsPage 
            orders={orders}
            onRefundActionComplete={handleRefundSuccess}
          />
        )}

        {currentPage === 'admin-refunds' && userRole !== 'admin' && (
          <div className="unauthorized">
            <h2>Access Denied</h2>
            <p>You do not have permission to access this page.</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
