import { useState } from 'react'
import RefundButton from '../components/RefundButton'
import '../styles/OrdersPage.css'

function OrdersPage({ orders = [], onRefundSuccess, loading, onUpdateOrder }) {
  const [expandedOrderId, setExpandedOrderId] = useState(null)
  const [promoCode, setPromoCode] = useState("")
  const [promoError, setPromoError] = useState("")

  const toggleOrderDetails = (orderId) => {
    setExpandedOrderId(expandedOrderId === orderId ? null : orderId)
    setPromoError("")
    setPromoCode("")
  }

  const handleApplyPromo = async (orderId, currentSubtotal) => {
    setPromoError("") 
    
    try {
      const response = await fetch("http://localhost:8000/api/v1/promos/apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          subtotal: currentSubtotal, 
          code: promoCode 
        })
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message);
        if (onUpdateOrder) {
          // Success: Use the data returned from backend
          onUpdateOrder(orderId, data.new_total, data.discount_amount);
        }
      } else {
        // Display why it failed (e.g. "Disabled by admin")
        setPromoError(data.detail || "Failed to apply promo code.");
      }
    } catch (err) {
      setPromoError("Server connection failed. Please try again later.");
    }
  };

  // ... (The rest of your rendering code remains the same)
  if (loading) return <div className="orders-page__loading">Loading orders...</div>
  if (!orders || orders.length === 0) return <div>No orders found.</div>

  return (
    <div className="orders-page">
      <h1>My Orders</h1>
      <div className="orders-page__list">
        {orders.map(order => (
          <div key={order.id} className="order-card">
            <div className="order-card__header" onClick={() => toggleOrderDetails(order.id)}>
              <div className="order-card__summary">
                <h3>Order #{order.id}</h3>
                <div className="order-card__statuses">
                  <span className="status-badge">{order.status}</span>
                </div>
              </div>
              <div className="order-card__price">
                <strong>${order.total_price?.toFixed(2)}</strong>
              </div>
            </div>

            {expandedOrderId === order.id && (
              <div className="order-card__details">
                <div className="promo-section">
                  <h4>Promotions</h4>
                  <div className="promo-input-group">
                    <input 
                      type="text" 
                      value={promoCode}
                      onChange={(e) => setPromoCode(e.target.value)}
                      className="promo-input"
                    />
                    <button onClick={() => handleApplyPromo(order.id, order.total_price)}>Apply</button>
                  </div>
                  {promoError && <p style={{color: 'red'}}>{promoError}</p>}
                </div>
                {/* Total Section */}
                <p>Total: ${order.total_price?.toFixed(2)}</p>
                {order.discount_applied > 0 && <p>- Discount: ${order.discount_applied}</p>}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default OrdersPage;