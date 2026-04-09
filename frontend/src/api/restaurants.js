const API_BASE = "/api/v1";

export const fetchRestaurants = async (search = "", page = 1, size = 10, category = "") => {
  const params = new URLSearchParams({
    q: search,
    page: page,
    size: size,
    category: category
  });

  const res = await fetch(`${API_BASE}/restaurants?${params.toString()}`);
  
  if (!res.ok) {
    return { items: [], total: 0, page: 1, size: 10, pages: 0 };
  }
  return res.json();
};

export const fetchMenuByRestaurant = async (restaurantId) => {
  const res = await fetch(`${API_BASE}/restaurants/${restaurantId}`);
  if (!res.ok) return null;
  return res.json();
};