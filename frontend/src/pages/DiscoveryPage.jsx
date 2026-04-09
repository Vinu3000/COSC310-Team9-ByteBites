import React, { useState, useEffect } from 'react';
import { fetchRestaurants } from '../api/restaurants';
import '../styles/DiscoveryPage.css';

function DiscoveryPage() {
  const [restaurants, setRestaurants] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedRes, setSelectedRes] = useState(null);
  const [loadingMenu, setLoadingMenu] = useState(false);

  // Pagination State
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 4;

  const categories = ["Italian", "American", "Japanese", "Mexican", "Cafe", "Salad"];

  useEffect(() => {
    loadData(searchTerm, selectedCategory, currentPage);
  }, [currentPage, selectedCategory]);

  const loadData = async (query = "", category = "", page = 1) => {
    try {
      const data = await fetchRestaurants(query, page, pageSize, category);
      if (data && data.items) {
        setRestaurants(data.items);
        setTotalPages(data.pages || 1);
      } else {
        setRestaurants([]);
        setTotalPages(1);
      }
    } catch (err) {
      console.error("Failed to load data:", err);
      setRestaurants([]);
    }
  };

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    setCurrentPage(1); 
    loadData(value, selectedCategory, 1);
  };

  const handleCategoryClick = (cat) => {
    const newCategory = selectedCategory === cat ? "" : cat;
    setSelectedCategory(newCategory);
    setCurrentPage(1); 
  };

  const handleRestaurantClick = async (res) => {
    setLoadingMenu(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/restaurants/${res.id}`);
      const fullData = await response.json();
      setSelectedRes(fullData);
    } catch (err) {
      setSelectedRes(res);
    } finally {
      setLoadingMenu(false);
    }
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

      <div className="category-filter">
        <button 
          className={selectedCategory === "" ? "active" : ""} 
          onClick={() => handleCategoryClick("")}
        >
          All
        </button>
        {categories.map(cat => (
          <button 
            key={cat} 
            className={selectedCategory === cat ? "active" : ""}
            onClick={() => handleCategoryClick(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="restaurant-grid">
        {restaurants.length > 0 ? (
          restaurants.map(res => (
            <div key={res.id} className="restaurant-card" onClick={() => handleRestaurantClick(res)}>
              <h3>{res.name}</h3>
              <p className="cuisine">{res.cuisine_type || res.category}</p>
              <div className="rating">⭐ {res.rating}</div>
            </div>
          ))
        ) : (
          <p className="no-data">No restaurants found in this category.</p>
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button disabled={currentPage === 1} onClick={() => setCurrentPage(p => p - 1)}>Prev</button>
          <span className="page-info">Page {currentPage} of {totalPages}</span>
          <button disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => p + 1)}>Next</button>
        </div>
      )}

      {selectedRes && (
        <div className="modal-overlay" onClick={() => setSelectedRes(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h2>{selectedRes.name} - Menu</h2>
            {loadingMenu ? (
              <p>Loading menu...</p>
            ) : (
              <div className="menu-items">
                {selectedRes.menu?.map(item => (
                  <div key={item.id} className="menu-item">
                    <div className="item-info">
                      <strong>{item.name}</strong>
                      <span>${item.price?.toFixed(2)}</span>
                    </div>
                    <button onClick={() => alert(`Added ${item.name} to cart!`)}>Add</button>
                  </div>
                ))}
              </div>
            )}
            <button className="close-btn" onClick={() => setSelectedRes(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default DiscoveryPage;