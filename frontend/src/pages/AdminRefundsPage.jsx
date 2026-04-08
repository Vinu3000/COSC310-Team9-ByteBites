import { useState, useEffect } from 'react';
import { approveRefund, rejectRefund } from '../api/refunds';
import '../styles/AdminRefundsPage.css';

/**
 * AdminRefundsPage Component
 * Admin interface for viewing and managing refund requests.
 * Shows pending refunds and allows admin to approve or reject them.
 *
 * @param {object} props - Component props
 * @param {array} props.orders - Array of orders with refund data
 * @param {function} props.onRefundActionComplete - Callback after approve/reject action
 */
function AdminRefundsPage({ orders = [], onRefundActionComplete }) {
  const [refundRequests, setRefundRequests] = useState([]);
  const [actionLoading, setActionLoading] = useState(null);
  const [message, setMessage] = useState(null);
  const [messageType, setMessageType] = useState(null);

  // Filter orders that have pending refund requests
  useEffect(() => {
    if (orders && orders.length > 0) {
      const pending = orders.filter(order => order.refund_status === 'Requested');
      setRefundRequests(pending);
    }
  }, [orders]);

  const handleApproveRefund = async (orderId) => {
    setActionLoading(orderId);
    setMessage(null);

    try {
      const result = await approveRefund(orderId);
      setMessage(`Refund approved for order ${orderId}`);
      setMessageType('success');

      // Update local state
      setRefundRequests(prev => 
        prev.map(req => 
          req.id === orderId 
            ? { ...req, refund_status: 'Approved', status: 'Cancelled', payment_status: 'Refunded' }
            : req
        ).filter(req => req.refund_status === 'Requested')
      );

      if (onRefundActionComplete) {
        onRefundActionComplete();
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to approve refund';
      setMessage(errorMsg);
      setMessageType('error');
    } finally {
      setActionLoading(null);
    }
  };

  const handleRejectRefund = async (orderId) => {
    setActionLoading(orderId);
    setMessage(null);

    try {
      const result = await rejectRefund(orderId);
      setMessage(`Refund rejected for order ${orderId}`);
      setMessageType('success');

      // Update local state
      setRefundRequests(prev => 
        prev.filter(req => req.id !== orderId)
      );

      if (onRefundActionComplete) {
        onRefundActionComplete();
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to reject refund';
      setMessage(errorMsg);
      setMessageType('error');
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="admin-refunds-page">
      <h1 className="admin-refunds-page__title">Manage Refund Requests</h1>

      {message && (
        <div className={`admin-message admin-message--${messageType}`}>
          {message}
        </div>
      )}

      {refundRequests.length === 0 ? (
        <div className="admin-refunds-page__empty">
          <p>No pending refund requests</p>
        </div>
      ) : (
        <div className="admin-refunds-page__table-container">
          <table className="admin-refunds-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Order Status</th>
                <th>Payment Status</th>
                <th>Refund Reason</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {refundRequests.map(order => (
                <tr key={order.id} className="admin-refunds-table__row">
                  <td className="admin-refunds-table__cell admin-refunds-table__cell--order-id">
                    {order.id}
                  </td>
                  <td className="admin-refunds-table__cell">
                    <span className="status-badge status-badge--order">
                      {order.status}
                    </span>
                  </td>
                  <td className="admin-refunds-table__cell">
                    <span className="status-badge status-badge--payment">
                      {order.payment_status}
                    </span>
                  </td>
                  <td className="admin-refunds-table__cell admin-refunds-table__cell--reason">
                    {order.refund_reason || 'No reason provided'}
                  </td>
                  <td className="admin-refunds-table__cell admin-refunds-table__cell--actions">
                    <button
                      className="action-button action-button--approve"
                      onClick={() => handleApproveRefund(order.id)}
                      disabled={actionLoading === order.id}
                      title="Approve refund"
                    >
                      {actionLoading === order.id ? 'Processing...' : 'Approve'}
                    </button>
                    <button
                      className="action-button action-button--reject"
                      onClick={() => handleRejectRefund(order.id)}
                      disabled={actionLoading === order.id}
                      title="Reject refund"
                    >
                      {actionLoading === order.id ? 'Processing...' : 'Reject'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default AdminRefundsPage;
