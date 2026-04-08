import { useState } from 'react'
import RefundButton from '../components/RefundButton'
import '../styles/OrdersPage.css'

function OrdersPage({ orders = [], onRefundSuccess, loading }) {
  const [expandedOrderId, setExpandedOrderId] = useState(null)

  const toggleOrderDetails = (orderId) => {
    setExpandedOrderId(expandedOrderId === orderId ? null : orderId)
  }

  if (loading) {
    return <div className="orders-page__loading">Loading orders...</div>
  }

  if (!orders || orders.length === 0) {
    return (
      <div className="orders-page">
        <h1>My Orders</h1>
        <div className="orders-page__empty">
          <p>No orders found. Start ordering from our menu!</p>
        </div>
      </div>
    )
  }

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
                  <span className={`status-badge status-badge--order`}>
                    {order.status || 'Unknown'}
                  </span>
                  <span className={`status-badge status-badge--payment`}>
                    {order.payment_status || 'Unknown'}
                  </span>
                  {order.refund_status && order.refund_status !== 'None' && (
                    <span className={`status-badge status-badge--refund status-badge--refund-${order.refund_status.toLowerCase()}`}>
                      Refund: {order.refund_status}
                    </span>
                  )}
                </div>
              </div>
              <div className="order-card__price">
                <strong>${order.total_price?.toFixed(2) || '0.00'}</strong>
              </div>
              <button className="order-card__toggle">
                {expandedOrderId === order.id ? '▼' : '▶'}
              </button>
            </div>

            {expandedOrderId === order.id && (
              <div className="order-card__details">
                <div className="order-details">
                  <div className="order-details__section">
                    <h4>Order Details</h4>
                    <p><strong>Order ID:</strong> {order.id}</p>
                    <p><strong>Status:</strong> {order.status}</p>
                    <p><strong>Payment Status:</strong> {order.payment_status}</p>
                    {order.refund_status && (
                      <p><strong>Refund Status:</strong> {order.refund_status}</p>
                    )}
                    {order.refund_reason && (
                      <p><strong>Refund Reason:</strong> {order.refund_reason}</p>
                    )}
                  </div>

                  <div className="order-details__section">
                    <h4>Items</h4>
                    {order.items && order.items.length > 0 ? (
                      <ul className="order-items">
                        {order.items.map((item, idx) => (
                          <li key={idx} className="order-item">
                            <span>{item.name || 'Item'}</span>
                            <span className="order-item__price">${item.price?.toFixed(2) || '0.00'}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p>No items in this order</p>
                    )}
                  </div>

                  <div className="order-details__section">
                    <h4>Total</h4>
                    <p className="order-total">${order.total_price?.toFixed(2) || '0.00'}</p>
                  </div>

                  {/* Refund Button - Only show if order is eligible */}
                  {(order.status === 'Pending' || order.status === 'Preparing') && 
                   order.payment_status === 'Success' &&
                   (!order.refund_status || order.refund_status === 'None') && (
                    <div className="order-details__section">
                      <RefundButton
                        orderId={order.id}
                        orderStatus={order.status}
                        paymentStatus={order.payment_status}
                        refundStatus={order.refund_status}
                        onRefundSuccess={onRefundSuccess}
                      />
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default OrdersPage
