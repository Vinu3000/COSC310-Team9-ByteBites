const API_BASE = "http://localhost:8000/api/v1/promos";

// For the Admin Page to see all codes
export const fetchPromos = async () => {
  const res = await fetch(`${API_BASE}/`);
  return res.json();
};

// For the Admin Page to turn a code on/off
export const togglePromoStatus = async (id) => {
  const res = await fetch(`${API_BASE}/${id}/toggle`, { method: "PATCH" });
  return res.json();
};