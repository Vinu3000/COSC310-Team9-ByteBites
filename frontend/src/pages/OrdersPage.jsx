import { useState } from 'react'
import RefundButton from '../components/RefundButton'
import '../styles/OrdersPage.css'

const PAYMENT_STATUS_MAP = {
  'Pending':  { label: 'Awaiting Payment', icon: '⏳', cls: 'pending' },
  'Success':  { label: 'Payment Successful', icon: '✅', cls: 'success' },
  'Failed':   { label: 'Payment Failed', icon: '❌', cls: 'failed' },
  'Refunded': { label: 'Refunded', icon: '↩️', cls: 'refunded' },
}

function OrdersPage({ orders = [], onRefundSuccess, loading, onUpdateOrder }) {
  const [expandedOrderId, setExpandedOrderId] = useState(null)
  const [promoCode, setPromoCode] = useState("")
  const [promoError, setPromoError] = useState("")
  // Feature 7: per-order payment simulation state
  const [paymentStates, setPaymentStates] = useState({})

  const toggleOrderDetails = (orderId) => {
    setExpandedOrderId(expandedOrderId === orderId ? null : orderId)
    setPromoError("")
    setPromoCode("")
  }

  const handleApplyPromo = async (orderId, currentSubtotal) => {
    setPromoError("")
    try {
      const response = await fetch("/api/v1/promos/apply", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subtotal: currentSubtotal, code: promoCode })
      })
      const data = await response.json()
      if (response.ok) {
        if (onUpdateOrder) onUpdateOrder(orderId, data.new_total, data.discount_amount)
      } else {
        setPromoError(data.detail || "Failed to apply promo code.")
      }
    } catch (err) {
      setPromoError("Server connection failed.")
    }
  }

  // Feature 7: replace alert() with inline status feedback
  const handleSimulatePayment = async (orderId) => {
    setPaymentStates(prev => ({ ...prev, [orderId]: { status: 'processing', message: '' } }))
    try {
      const response = await fetch(`/api/v1/orders/${orderId}/pay`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      })
      const data = await response.json()
      if (response.ok) {
        setPaymentStates(prev => ({
          ...prev,
          [orderId]: { status: 'success', message: data.message || 'Payment successful!' }
        }))
        if (onRefundSuccess) onRefundSuccess()
      } else {
        setPaymentStates(prev => ({
          ...prev,
          [orderId]: { status: 'failed', message: data.detail || 'Payment was rejected.' }
        }))
      }
    } catch (err) {
      setPaymentStates(prev => ({
        ...prev,
        [orderId]: { status: 'failed', message: 'Server connection failed.' }
      }))
    }
  }

  const resetPaymentState = (orderId) => {
    setPaymentStates(prev => ({ ...prev, [orderId]: { status: 'idle', message: '' } }))
  }

  if (loading) return <div className="orders-page__loading">Loading orders...</div>
  if (!orders || orders.length === 0) return <div className="no-orders">No orders found.</div>

  return (
    <div className="orders-page">
      <h1>My Orders</h1>
      <div className="orders-page__list">
        {orders.map(order => {
          const payState = paymentStates[order.id] || { status: 'idle', message: '' }
          const payInfo = PAYMENT_STATUS_MAP[order.payment_status] || { label: order.payment_status, icon: '', cls: 'unknown' }

          return (
            <div key={order.id} className={`order-card ${expandedOrderId === order.id ? 'active' : ''}`}>

              <div className="order-card__header" onClick={() => toggleOrderDetails(order.id)}>
                <div className="order-card__summary">
                  <h3>Order #{order.id}</h3>
                  <div className="order-card__statuses">
                    <span className={`status-badge status--${order.status.toLowerCase().replace(/\s/g, '-')}`}>
                      {order.status === 'Preparing' ? '👨‍🍳 ' : '🚴 '}{order.status}
                    </span>
                    {/* Feature 7: descriptive payment badge */}
                    <span className={`payment-badge payment-badge--${payInfo.cls}`}>
                      {payInfo.icon} {payInfo.label}
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

                  <div className="details-section">
                    <h4>Order Summary</h4>
                    <ul className="items-list">
                      {order.items?.map((item, idx) => (
                        <li key={idx}>{item.name} <span>${item.price.toFixed(2)}</span></li>
                      ))}
                    </ul>
                    <div className="calculation-box">
                      <p>Subtotal: <span>${order.subtotal?.toFixed(2)}</span></p>
                      <p>Delivery Fee: <span>${order.delivery_fee?.toFixed(2) ?? '5.00'}</span></p>
                      <p>Tax: <span>${order.tax?.toFixed(2)}</span></p>
                      {order.discount_applied > 0 && (
                        <p className="discount-text">Promo Discount: <span>-${order.discount_applied.toFixed(2)}</span></p>
                      )}
                      <p className="final-total">Total: <span>${order.total_price?.toFixed(2)}</span></p>
                    </div>
                  </div>

                  <div className="details-section promo-section">
                    <h4>Promo Code</h4>
                    <div className="promo-input-group">
                      <input
                        type="text"
                        placeholder="Enter promo code"
                        value={promoCode}
                        onChange={(e) => setPromoCode(e.target.value)}
                        className="promo-input"
                      />
                      <button onClick={() => handleApplyPromo(order.id, order.subtotal)}>Apply</button>
                    </div>
                    {promoError && <p className="error-text">{promoError}</p>}
                  </div>

                  {/* Feature 7: Payment simulation with inline status */}
                  {order.payment_status === 'Pending' && (
                    <div className="details-section payment-section">
                      <h4>Payment</h4>
                      {payState.status === 'idle' && (
                        <button className="pay-button" onClick={() => handleSimulatePayment(order.id)}>
                          Complete Payment
                        </button>
                      )}
                      {payState.status === 'processing' && (
                        <div className="payment-status payment-status--processing">
                          <span className="payment-spinner" /> Processing payment...
                        </div>
                      )}
                      {payState.status === 'success' && (
                        <div className="payment-status payment-status--success">
                          ✅ {payState.message}
                        </div>
                      )}
                      {payState.status === 'failed' && (
                        <div className="payment-status payment-status--failed">
                          <p>❌ {payState.message}</p>
                          <button className="pay-button pay-button--retry" onClick={() => resetPaymentState(order.id)}>
                            Retry Payment
                          </button>
                        </div>
                      )}
                    </div>
                  )}

                  <div className="details-section">
                    <RefundButton
                      orderId={order.id}
                      orderStatus={order.status}
                      paymentStatus={order.payment_status}
                      refundStatus={order.refund_status}
                      onRefundSuccess={onRefundSuccess}
                    />
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default OrdersPage
