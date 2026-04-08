import React, { useEffect, useState } from 'react';
import { fetchPromos, togglePromoStatus } from '../api/promos';
import '../styles/AdminPromosPage.css';

function AdminPromosPage() {
  const [promos, setPromos] = useState([]);

  // Load promos when the page opens
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const data = await fetchPromos();
    setPromos(data);
  };

  const handleToggle = async (id) => {
    await togglePromoStatus(id);
    loadData(); // Refresh the table after clicking
  };

  return (
    <div className="admin-promos">
      <h1>Promotion Control Panel</h1>
      <p>As an Admin, you can enable or disable discounts here.</p>
      
      <table className="admin-table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Discount</th>
            <th>Min Spend</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {promos.map(p => (
            <tr key={p.id}>
              <td>{p.code}</td>
              <td>${p.discount_value}</td>
              <td>${p.min_spend}</td>
              <td>{p.is_active ? "✅ Active" : "❌ Disabled"}</td>
              <td>
                <button onClick={() => handleToggle(p.id)}>
                  {p.is_active ? "Deactivate" : "Activate"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminPromosPage;