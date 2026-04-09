import React from 'react';
import '../styles/Cart.css';

function Cart({ cart, isOpen, onClose, onPlaceOrder, onRemoveItem, onClearCart }) {
  if (!isOpen) return null;

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div className="cart-overlay" onClick={onClose}>
      <div className="cart-sidebar" onClick={(e) => e.stopPropagation()}>
        <div className="cart-header">
          <h2>Your Cart</h2>
          {cart.length > 0 && (
            <button className="clear-cart-btn" onClick={onClearCart}>Clear All</button>
          )}
          <button className="close-sidebar" onClick={onClose}>&times;</button>
        </div>

        {cart.length === 0 ? (
          <p className="empty-msg">Your cart is empty.</p>
        ) : (
          <>
            <div className="cart-items-list">
              {cart.map((item) => (
                <div key={item.id} className="cart-item-detail">
                  <div className="item-info-group">
                    <span className="item-name">{item.name}</span>
                    <div className="qty-controls">
                      <button onClick={() => onRemoveItem(item.id)} className="qty-btn">-</button>
                      <span className="item-qty">{item.quantity}</span>
                      <button onClick={() => onRemoveItem(item.id)} className="qty-btn" style={{display: 'none'}}>+</button> 
                      {/* Note: Increase is usually done via DiscoveryPage, but can be added here too */}
                    </div>
                  </div>
                  <span className="item-price-total">${(item.price * item.quantity).toFixed(2)}</span>
                </div>
              ))}
            </div>
            <div className="cart-footer">
              <div className="total-row">
                <span>Total:</span>
                <strong>${total.toFixed(2)}</strong>
              </div>
              <button className="checkout-btn" onClick={onPlaceOrder}>
                Place Order
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Cart;