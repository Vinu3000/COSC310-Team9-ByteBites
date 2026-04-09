const API_BASE = "/api/v1";

export const getRefundRequests = async () => {
    try {
        const res = await fetch(`${API_BASE}/refunds`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error("Failed to fetch refunds:", err);
        return [];
    }
};

export const approveRefund = async (id) => {
    const res = await fetch(`${API_BASE}/refunds/${id}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};

export const rejectRefund = async (id) => {
    const res = await fetch(`${API_BASE}/refunds/${id}/reject`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};

export const requestRefund = async (orderId, reason) => {
    const res = await fetch(`${API_BASE}/refunds`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_id: String(orderId), reason: reason || null })
    });
    if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to request refund");
    }
    return await res.json();
};

export const updateRefundStatus = async (id, status) => {
    const res = await fetch(`${API_BASE}/refunds/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};
