import { useState } from 'react';
import { requestRefund } from '../api/refunds';
import '../styles/RefundButton.css';

/**
 * RefundButton Component
 * Displays a button to request a refund for an order.
 * Shows inline feedback for success/error states.
 *
 * @param {object} props - Component props
 * @param {string} props.orderId - The order ID
 * @param {string} props.orderStatus - Current order status (e.g., 'Pending', 'Preparing', 'Completed')
 * @param {string} props.paymentStatus - Current payment status (e.g., 'Success', 'Pending', 'Failed')
 * @param {string} props.refundStatus - Current refund status (e.g., 'None', 'Requested', 'Approved', 'Rejected')
 * @param {function} props.onRefundSuccess - Callback function triggered after successful refund request
 */
function RefundButton({ orderId, orderStatus, paymentStatus, refundStatus, onRefundSuccess }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [reason, setReason] = useState('');
  const [showReasonForm, setShowReasonForm] = useState(false);

  // Determine if refund button should be enabled
  const isRefundEligible = 
    paymentStatus === 'Success' &&
    (orderStatus === 'Pending' || orderStatus === 'Preparing') &&
    (refundStatus === 'None' || refundStatus === null || refundStatus === undefined);

  const handleRequestRefund = async () => {
    if (!isRefundEligible) {
      setError('This order is not eligible for a refund');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await requestRefund(orderId, reason);
      setSuccess(result.message || 'Refund request submitted successfully');
      setReason('');
      setShowReasonForm(false);
      
      // Call parent callback to refresh order data
      if (onRefundSuccess) {
        onRefundSuccess();
      }
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to request refund';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (!isRefundEligible) {
    return (
      <div className="refund-button-container">
        <button 
          className="refund-button refund-button--disabled"
          disabled
          title={`Refund not available for ${orderStatus} orders with ${paymentStatus} payment`}
        >
          Refund (Not Available)
        </button>
      </div>
    );
  }

  return (
    <div className="refund-button-container">
      {!showReasonForm ? (
        <button
          className="refund-button"
          onClick={() => setShowReasonForm(true)}
          disabled={loading}
        >
          {loading ? 'Requesting...' : 'Request Refund'}
        </button>
      ) : (
        <div className="refund-form">
          <textarea
            className="refund-form__reason"
            placeholder="Optional: Reason for refund (max 200 chars)"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            maxLength={200}
            disabled={loading}
          />
          <div className="refund-form__actions">
            <button
              className="refund-form__submit"
              onClick={handleRequestRefund}
              disabled={loading}
            >
              {loading ? 'Submitting...' : 'Submit Refund Request'}
            </button>
            <button
              className="refund-form__cancel"
              onClick={() => {
                setShowReasonForm(false);
                setReason('');
                setError(null);
              }}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="refund-message refund-message--error">
          {error}
        </div>
      )}

      {success && (
        <div className="refund-message refund-message--success">
          {success}
        </div>
      )}
    </div>
  );
}

export default RefundButton;
