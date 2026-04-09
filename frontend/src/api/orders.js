const API_BASE_URL = 'http://localhost:8000/api/v1';

export const placeOrder = async (orderData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to place order');
    }
    return await response.json();
  } catch (error) {
    console.error("Order API Error:", error);
    throw error;
  }
};