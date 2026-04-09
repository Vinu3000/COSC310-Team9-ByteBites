import React from 'react';
import '../styles/Cart.css';

const DELIVERY_FEE = 5.00;
const TAX_RATE = 0.10;

function Cart({ cart, isOpen, onClose, onPlaceOrder, onRemoveItem, onClearCart }) {
  if (!isOpen) return null;

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const tax = subtotal * TAX_RATE;
  const total = subtotal + DELIVERY_FEE + tax;

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
                    </div>
                  </div>
                  <span className="item-price-total">${(item.price * item.quantity).toFixed(2)}</span>
                </div>
              ))}
            </div>

            {/* Feature 6: Pricing Breakdown */}
            <div className="cart-pricing">
              <div className="cart-pricing__row">
                <span>Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="cart-pricing__row">
                <span>Delivery Fee</span>
                <span>${DELIVERY_FEE.toFixed(2)}</span>
              </div>
              <div className="cart-pricing__row">
                <span>Tax (10%)</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <div className="cart-pricing__row cart-pricing__row--total">
                <span>Total</span>
                <strong>${total.toFixed(2)}</strong>
              </div>
            </div>

            <div className="cart-footer">
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
