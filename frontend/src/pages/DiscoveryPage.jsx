import React, { useState, useEffect, useCallback } from 'react';
import { fetchRestaurants } from '../api/restaurants';
import { placeOrder } from '../api/orders';
import Cart from '../components/Cart';
import '../styles/DiscoveryPage.css';
import '../styles/Cart.css';

function DiscoveryPage() {
  const [restaurants, setRestaurants] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedRes, setSelectedRes] = useState(null);
  const [loadingMenu, setLoadingMenu] = useState(false);

  // Cart State
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  // Pagination State
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 4;

  const categories = ["Italian", "American", "Japanese", "Mexican", "Cafe", "Salad"];

  // Fetch data from API
  const loadData = useCallback(async (query = "", category = "", page = 1) => {
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
  }, []);

  // Debounced Search Effect
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      loadData(searchTerm, selectedCategory, currentPage);
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm, selectedCategory, currentPage, loadData]);

  const handleCategoryClick = (cat) => {
    setSelectedCategory(prev => (prev === cat ? "" : cat));
    setCurrentPage(1); 
  };

  const handleRestaurantClick = async (res) => {
    setLoadingMenu(true);
    try {
      const response = await fetch(`/api/v1/restaurants/${res.id}`);
      const fullData = await response.json();
      setSelectedRes(fullData);
    } catch (err) {
      setSelectedRes(res);
    } finally {
      setLoadingMenu(false);
    }
  };

  // Cart Logic: Add / Increment
  const addToCart = (item) => {
    setCart(prevCart => {
      // Logic: Only one restaurant per order
      if (prevCart.length > 0 && prevCart[0].restaurantId !== selectedRes.id) {
        const confirmClear = window.confirm(
          "You can only order from one restaurant at a time. Clear cart and add this item?"
        );
        if (!confirmClear) return prevCart;
        return [{ ...item, quantity: 1, restaurantId: selectedRes.id }];
      }

      const existingItem = prevCart.find(i => i.id === item.id);
      if (existingItem) {
        return prevCart.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
      }
      return [...prevCart, { ...item, quantity: 1, restaurantId: selectedRes.id }];
    });
  };

  // Cart Logic: Remove / Decrement
  const removeFromCart = (itemId) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(i => i.id === itemId);
      if (existingItem && existingItem.quantity > 1) {
        return prevCart.map(i => i.id === itemId ? { ...i, quantity: i.quantity - 1 } : i);
      }
      return prevCart.filter(i => i.id !== itemId);
    });
  };

  // Cart Logic: Clear
  const clearCart = () => {
    if (window.confirm("Are you sure you want to clear your cart?")) {
      setCart([]);
    }
  };

  // Place Order API Call
  const handlePlaceOrder = async () => {
    if (cart.length === 0) return;

    try {
      const orderData = {
        items: cart.map(i => ({ menu_item_id: i.id, quantity: i.quantity })),
        delivery_address: "Standard Address"
      };

      await placeOrder(orderData);
      alert("Order placed successfully! This order is now finalized.");
      setCart([]); 
      setIsCartOpen(false);
    } catch (err) {
      alert(`Order Failed: ${err.message}`);
    }
  };

  return (
    <div className="discovery-container">
      {/* Floating Cart Trigger */}
      <div className="cart-trigger" onClick={() => setIsCartOpen(true)}>
        🛒 <span>{cart.reduce((sum, i) => sum + i.quantity, 0)}</span>
      </div>

      <h1>Explore Restaurants</h1>
      
      <input 
        type="text" 
        className="search-bar" 
        placeholder="Search for restaurants or cuisines..." 
        value={searchTerm}
        onChange={(e) => { setSearchTerm(e.target.value); setCurrentPage(1); }}
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
          <p className="no-data">No restaurants found.</p>
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button disabled={currentPage === 1} onClick={() => setCurrentPage(p => p - 1)}>Prev</button>
          <span className="page-info">Page {currentPage} of {totalPages}</span>
          <button disabled={currentPage === totalPages} onClick={() => setCurrentPage(p => p + 1)}>Next</button>
        </div>
      )}

      {/* Menu Modal */}
      {selectedRes && (
        <div className="modal-overlay" onClick={() => setSelectedRes(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h2>{selectedRes.name} - Menu</h2>
            {loadingMenu ? (
              <p>Loading menu...</p>
            ) : (
              <div className="menu-items">
                {selectedRes.menu?.length > 0 ? (
                  selectedRes.menu.map(item => {
                    const cartItem = cart.find(i => i.id === item.id);
                    return (
                      <div key={item.id} className="menu-item">
                        <div className="item-info">
                          <strong>{item.name}</strong>
                          <span>${item.price?.toFixed(2)}</span>
                        </div>
                        
                        {/* Stepper Logic: Add/Remove buttons */}
                        {cartItem ? (
                          <div className="menu-qty-controls">
                            <button className="qty-btn" onClick={() => removeFromCart(item.id)}>-</button>
                            <span className="qty-count">{cartItem.quantity}</span>
                            <button className="qty-btn" onClick={() => addToCart(item)}>+</button>
                          </div>
                        ) : (
                          <button className="add-btn" onClick={() => addToCart(item)}>Add</button>
                        )}
                      </div>
                    );
                  })
                ) : <p>No items available.</p>}
              </div>
            )}
            <button className="close-btn" onClick={() => setSelectedRes(null)}>Close</button>
          </div>
        </div>
      )}

      {/* Cart Sidebar Component */}
      <Cart 
        cart={cart} 
        isOpen={isCartOpen} 
        onClose={() => setIsCartOpen(false)} 
        onPlaceOrder={handlePlaceOrder} 
        onRemoveItem={removeFromCart}
        onClearCart={clearCart}
      />
    </div>
  );
}

export default DiscoveryPage;