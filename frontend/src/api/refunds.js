const API_BASE = "/api/v1";

export const getRefundRequests = async () => {
    // Refunds are derived from orders data — no separate endpoint needed
    return [];
};

export const approveRefund = async (id) => {
    const res = await fetch(`${API_BASE}/refunds/${id}/approve`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};

export const rejectRefund = async (id) => {
    const res = await fetch(`${API_BASE}/refunds/${id}/reject`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};

export const requestRefund = async (orderId, reason) => {
    const res = await fetch(`${API_BASE}/refunds/${orderId}/request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reason: reason || null })
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to request refund");
    }
    return await res.json();
};

export const updateRefundStatus = async (id, status) => {
    return { success: true };
};
