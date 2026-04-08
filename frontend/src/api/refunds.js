
export const getRefundRequests = async () => {
    return []; // Return empty list so the table is just empty
};

export const approveRefund = async (id) => {
    console.log("Mock approved:", id);
    return { success: true };
};

export const rejectRefund = async (id) => {
    console.log("Mock rejected:", id);
    return { success: true };
};

export const requestRefund = async (orderId) => {
    console.log("Mock refund requested for order:", orderId);
    return { success: true };
};

export const updateRefundStatus = async (id, status) => {
    return { success: true };
};