import React, { useState, useEffect } from 'react';
import { fetchRestaurants } from '../api/restaurants';
import '../styles/DiscoveryPage.css';

function DiscoveryPage() {
  const [restaurants, setRestaurants] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRes, setSelectedRes] = useState(null); 

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async (query = "") => {
    try {
      const data = await fetchRestaurants(query);
      console.log("Fetched Data:", data); 
      
      if (data && Array.isArray(data.items)) {
        setRestaurants(data.items);
      } 
      else if (Array.isArray(data)) {
        setRestaurants(data);
      } 
      else {
        setRestaurants([]);
      }
    } catch (err) {
      console.error("Failed to load data:", err);
      setRestaurants([]);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    loadData(e.target.value); 
  };

  return (
    <div className="discovery-container">
      <h1>Explore Restaurants</h1>
      
      <input 
        type="text" 
        className="search-bar" 
        placeholder="Search for pizza, burgers..." 
        value={searchTerm}
        onChange={handleSearch}
      />

      <div className="restaurant-grid">
        {restaurants.length > 0 ? (
          restaurants.map(res => (
            <div key={res.id} className="restaurant-card" onClick={() => setSelectedRes(res)}>
              <h3>{res.name}</h3>
              <p className="cuisine">{res.cuisine_type}</p>
              <div className="rating">⭐ {res.rating}</div>
            </div>
          ))
        ) : (
          <p className="no-data">No restaurants found.</p>
        )}
      </div>

      {selectedRes && (
        <div className="menu-modal">
          <div className="modal-content">
            <h2>{selectedRes.name} - Menu</h2>
            <div className="menu-items">
              {selectedRes.menu && selectedRes.menu.map(item => (
                <div key={item.id} className="menu-item">
                  <div className="item-info">
                    <strong>{item.name}</strong>
                    <span>${item.price.toFixed(2)}</span>
                  </div>
                  <button onClick={() => alert(`Added ${item.name} to cart!`)}>Add</button>
                </div>
              ))}
            </div>
            <button className="close-btn" onClick={() => setSelectedRes(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DiscoveryPage;