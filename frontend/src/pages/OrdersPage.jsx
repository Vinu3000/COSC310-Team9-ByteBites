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

  // --- Apply Promo Logic ---
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
        alert(`🔔 ${data.message}`);
        if (onUpdateOrder) {
          onUpdateOrder(orderId, data.new_total, data.discount_amount);
        }
      } else {
        setPromoError(data.detail || "Failed to apply promo code.");
      }
    } catch (err) {
      setPromoError("Server connection failed.");
    }
  };

  // --- REAL Simulated Payment Logic ---
  const handleSimulatePayment = async (orderId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/orders/${orderId}/pay`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });

      const data = await response.json();

      if (response.ok) {
        alert(`✅ ${data.message}`);
        
        if (onRefundSuccess) {
          onRefundSuccess();
        }
      } else {
        alert(`❌ Payment failed: ${data.detail || "Unknown error"}`);
      }
    } catch (err) {
      console.error("Payment connection error:", err);
      alert("Server connection failed during payment.");
    }
  };

  if (loading) return <div className="orders-page__loading">Loading orders...</div>
  if (!orders || orders.length === 0) return <div className="no-orders">No orders found.</div>

  return (
    <div className="orders-page">
      <h1>My Orders</h1>
      <div className="orders-page__list">
        {orders.map(order => (
          <div key={order.id} className={`order-card ${expandedOrderId === order.id ? 'active' : ''}`}>
            
            <div className="order-card__header" onClick={() => toggleOrderDetails(order.id)}>
              <div className="order-card__summary">
                <h3>Order #{order.id}</h3>
                <div className="order-card__statuses">
                  {/* Delivery Status Tracking */}
                  <span className={`status-badge status--${order.status.toLowerCase().replace(/\s/g, '-')}`}>
                    {order.status === 'Preparing' ? '👨‍🍳 ' : '🚴 '}{order.status}
                  </span>
                  <span className={`payment-badge ${order.payment_status.toLowerCase()}`}>
                    {order.payment_status}
                  </span>
                </div>
              </div>
              <div className="order-card__price">
                <strong>${order.total_price?.toFixed(2)}</strong>
              </div>
            </div>

            {expandedOrderId === order.id && (
              <div className="order-card__details">
                <hr />
                
                {/* Detailed Cost Calculation */}
                <div className="details-section">
                  <h4>Order Summary</h4>
                  <ul className="items-list">
                    {order.items?.map((item, idx) => (
                      <li key={idx}>{item.name} <span>${item.price.toFixed(2)}</span></li>
                    ))}
                  </ul>
                  <div className="calculation-box">
                    <p>Subtotal: <span>${order.subtotal?.toFixed(2)}</span></p>
                    <p>Delivery Fee: <span>$5.00</span></p>
                    <p>Tax (10%): <span>${(order.subtotal * 0.1).toFixed(2)}</span></p>
                    {order.discount_applied > 0 && (
                      <p className="discount-text">Promo Discount: <span>-${order.discount_applied.toFixed(2)}</span></p>
                    )}
                    <p className="final-total">Total: <span>${order.total_price?.toFixed(2)}</span></p>
                  </div>
                </div>

                {/* Promo Section */}
                <div className="details-section promo-section">
                  <h4>Offers</h4>
                  <div className="promo-input-group">
                    <input 
                      type="text" 
                      placeholder="Enter Promo Code"
                      value={promoCode}
                      onChange={(e) => setPromoCode(e.target.value)}
                      className="promo-input"
                    />
                    <button onClick={() => handleApplyPromo(order.id, order.subtotal)}>Apply</button>
                  </div>
                  {promoError && <p className="error-text">{promoError}</p>}
                </div>

                {/* Payment Action */}
                {order.payment_status === 'Pending' && (
                  <div className="details-section">
                    <button className="pay-button" onClick={() => handleSimulatePayment(order.id)}>
                      Complete Payment
                    </button>
                  </div>
                )}

                {/* Refund Feature */}
                <div className="details-section">
                  <RefundButton orderId={order.id} onRefundSuccess={onRefundSuccess} />
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default OrdersPage;