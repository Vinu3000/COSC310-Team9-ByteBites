import '../styles/PricingBreakdown.css'

function PricingBreakdown({ items = [], subtotal = 0, deliveryFee = 5, tax = 0, totalPrice = 0, discountApplied = 0 }) {
  return (
    <div className="pricing-breakdown">
      <h4>Order Summary</h4>

      {items.length > 0 && (
        <ul className="pricing-breakdown__items">
          {items.map((item, idx) => (
            <li key={idx} className="pricing-breakdown__item">
              <span>{item.name}</span>
              <span>${item.price.toFixed(2)}</span>
            </li>
          ))}
        </ul>
      )}

      <div className="pricing-breakdown__summary">
        <div className="pricing-breakdown__row">
          <span>Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="pricing-breakdown__row">
          <span>Delivery Fee</span>
          <span>${deliveryFee.toFixed(2)}</span>
        </div>
        <div className="pricing-breakdown__row">
          <span>Tax</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        {discountApplied > 0 && (
          <div className="pricing-breakdown__row pricing-breakdown__row--discount">
            <span>Promo Discount</span>
            <span>-${discountApplied.toFixed(2)}</span>
          </div>
        )}
        <div className="pricing-breakdown__row pricing-breakdown__row--total">
          <span>Total</span>
          <span>${totalPrice.toFixed(2)}</span>
        </div>
      </div>
    </div>
  )
}

export default PricingBreakdown
