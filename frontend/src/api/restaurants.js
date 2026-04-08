const API_BASE = "http://localhost:8000/api/v1";

export const fetchRestaurants = async (search = "") => {
  const res = await fetch(`${API_BASE}/restaurants?q=${search}`);
  if (!res.ok) return { items: [], total: 0 };
  return res.json();
};

export const fetchMenuByRestaurant = async (restaurantId) => {
  const res = await fetch(`${API_BASE}/restaurants/${restaurantId}`);
  if (!res.ok) return null;
  return res.json();
};