import React, { useState, useEffect, createContext, useContext } from 'react';
import './App.css';

// Auth Context
const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  const login = (tokenData) => {
    setToken(tokenData);
    setUser({ role: 'admin' });
    localStorage.setItem('token', tokenData);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => useContext(AuthContext);

// Components
const Navbar = ({ currentView, setCurrentView }) => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand" onClick={() => setCurrentView('home')}>
          🏡 Kimia RealEstate
        </div>
        
        <div className="nav-links">
          <button 
            className={currentView === 'home' ? 'active' : ''}
            onClick={() => setCurrentView('home')}
          >
            Home
          </button>
          <button 
            className={currentView === 'properties' ? 'active' : ''}
            onClick={() => setCurrentView('properties')}
          >
            Properties
          </button>
          <button 
            className={currentView === 'blog' ? 'active' : ''}
            onClick={() => setCurrentView('blog')}
          >
            Blog
          </button>
          
          {user ? (
            <>
              <button 
                className={currentView === 'admin' ? 'active admin-btn' : 'admin-btn'}
                onClick={() => setCurrentView('admin')}
              >
                Admin Panel
              </button>
              <button className="logout-btn" onClick={logout}>
                Logout
              </button>
            </>
          ) : (
            <button 
              className="login-btn"
              onClick={() => setCurrentView('login')}
            >
              Admin Login
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

const HomePage = () => {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-background">
          <img 
            src="https://images.unsplash.com/photo-1513584684374-8bab748fbf90?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBob3VzZXN8ZW58MHx8fHwxNzU4MzkzNTU5fDA&ixlib=rb-4.1.0&q=85" 
            alt="Luxury Home"
            className="hero-image"
          />
          <div className="hero-overlay"></div>
        </div>
        <div className="hero-content">
          <h1>Discover Your Perfect Home</h1>
          <p>Experience luxury living with Kimia RealEstate - Where dreams meet reality</p>
          <div className="hero-buttons">
            <button className="btn-primary" onClick={() => window.scrollTo(0, window.innerHeight)}>
              Explore Properties
            </button>
            <button className="btn-secondary">
              Get Expert Consultation
            </button>
          </div>
        </div>
      </section>
      
      <section className="features">
        <div className="container">
          <h2>Why Choose Kimia RealEstate?</h2>
          <p className="features-subtitle">Your trusted partner in luxury real estate</p>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-image">
                <img 
                  src="https://images.unsplash.com/photo-1526948531399-320e7e40f0ca" 
                  alt="Professional Service"
                />
              </div>
              <div className="feature-icon">🔍</div>
              <h3>Expert Consultation</h3>
              <p>Professional guidance from experienced real estate experts who understand your needs</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-image">
                <img 
                  src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750" 
                  alt="Luxury Properties"
                />
              </div>
              <div className="feature-icon">🏆</div>
              <h3>Premium Properties</h3>
              <p>Carefully curated selection of luxury homes and premium real estate investments</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-image">
                <img 
                  src="https://images.unsplash.com/photo-1627161683077-e34782c24d81" 
                  alt="Personalized Service"
                />
              </div>
              <div className="feature-icon">💎</div>
              <h3>Personalized Service</h3>
              <p>Tailored solutions and dedicated support throughout your property journey</p>
            </div>
          </div>
        </div>
      </section>
      
      <section className="showcase-properties">
        <div className="container">
          <h2>Featured Properties</h2>
          <div className="showcase-grid">
            <div className="showcase-item">
              <img 
                src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914" 
                alt="Modern Villa"
              />
              <div className="showcase-info">
                <h3>Modern Luxury Villa</h3>
                <p>Contemporary design with premium amenities</p>
              </div>
            </div>
            <div className="showcase-item">
              <img 
                src="https://images.unsplash.com/photo-1613490493576-7fde63acd811" 
                alt="Contemporary Home"
              />
              <div className="showcase-info">
                <h3>Contemporary Estate</h3>
                <p>Architectural excellence meets comfort</p>
              </div>
            </div>
            <div className="showcase-item">
              <img 
                src="https://images.unsplash.com/photo-1503174971373-b1f69850bded" 
                alt="Luxury Interior"
              />
              <div className="showcase-info">
                <h3>Luxury Interiors</h3>
                <p>Elegant design and premium finishes</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

const PropertyCard = ({ property, onClick }) => {
  return (
    <div className="property-card" onClick={() => onClick(property)}>
      <div className="property-image">
        {property.images && property.images.length > 0 ? (
          <img src={property.images[0]} alt={property.title} />
        ) : (
          <div className="no-image">📷 No Image</div>
        )}
        <div className="property-status">{property.status}</div>
      </div>
      
      <div className="property-info">
        <h3>{property.title}</h3>
        <p className="property-location">📍 {property.location}</p>
        <p className="property-price">${property.price?.toLocaleString()}</p>
        
        <div className="property-details">
          <span>🛏 {property.bedrooms} beds</span>
          <span>🚿 {property.bathrooms} baths</span>
          <span>📐 {property.area} sq ft</span>
        </div>
        
        <div className="property-type">{property.property_type}</div>
      </div>
    </div>
  );
};

const PropertiesPage = () => {
  const [properties, setProperties] = useState([]);
  const [filteredProperties, setFilteredProperties] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    search: '',
    property_type: '',
    min_price: '',
    max_price: '',
    location: ''
  });

  useEffect(() => {
    fetchProperties();
  }, []);

  useEffect(() => {
    filterProperties();
  }, [properties, filters]);

  const fetchProperties = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/properties`);
      const data = await response.json();
      setProperties(data);
      setFilteredProperties(data);
    } catch (error) {
      console.error('Error fetching properties:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterProperties = () => {
    let filtered = [...properties];

    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      filtered = filtered.filter(property => 
        property.title.toLowerCase().includes(searchLower) ||
        property.description.toLowerCase().includes(searchLower) ||
        property.location.toLowerCase().includes(searchLower)
      );
    }

    if (filters.property_type) {
      filtered = filtered.filter(property => 
        property.property_type.toLowerCase().includes(filters.property_type.toLowerCase())
      );
    }

    if (filters.location) {
      filtered = filtered.filter(property => 
        property.location.toLowerCase().includes(filters.location.toLowerCase())
      );
    }

    if (filters.min_price) {
      filtered = filtered.filter(property => property.price >= parseFloat(filters.min_price));
    }

    if (filters.max_price) {
      filtered = filtered.filter(property => property.price <= parseFloat(filters.max_price));
    }

    setFilteredProperties(filtered);
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  if (selectedProperty) {
    return (
      <PropertyDetails 
        property={selectedProperty} 
        onBack={() => setSelectedProperty(null)} 
      />
    );
  }

  return (
    <div className="properties-page">
      <div className="container">
        <div className="page-header">
          <h1>Premium Properties</h1>
          <p>Discover exceptional homes curated by Kimia RealEstate</p>
        </div>

        <div className="filters-section">
          <div className="filters-grid">
            <input
              type="text"
              placeholder="Search properties..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              className="filter-input"
            />
            
            <select
              value={filters.property_type}
              onChange={(e) => handleFilterChange('property_type', e.target.value)}
              className="filter-select"
            >
              <option value="">All Types</option>
              <option value="house">House</option>
              <option value="apartment">Apartment</option>
              <option value="condo">Condo</option>
              <option value="villa">Villa</option>
            </select>
            
            <input
              type="text"
              placeholder="Location..."
              value={filters.location}
              onChange={(e) => handleFilterChange('location', e.target.value)}
              className="filter-input"
            />
            
            <input
              type="number"
              placeholder="Min Price"
              value={filters.min_price}
              onChange={(e) => handleFilterChange('min_price', e.target.value)}
              className="filter-input"
            />
            
            <input
              type="number"
              placeholder="Max Price"
              value={filters.max_price}
              onChange={(e) => handleFilterChange('max_price', e.target.value)}
              className="filter-input"
            />
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading premium properties...</div>
        ) : (
          <div className="properties-grid">
            {filteredProperties.map(property => (
              <PropertyCard 
                key={property.id} 
                property={property} 
                onClick={setSelectedProperty}
              />
            ))}
          </div>
        )}

        {!loading && filteredProperties.length === 0 && (
          <div className="no-results">
            <h3>No properties found</h3>
            <p>Try adjusting your search criteria</p>
          </div>
        )}
      </div>
    </div>
  );
};

const PropertyDetails = ({ property, onBack }) => {
  return (
    <div className="property-details">
      <div className="container">
        <button className="back-btn" onClick={onBack}>
          ← Back to Properties
        </button>
        
        <div className="property-header">
          <h1>{property.title}</h1>
          <div className="property-meta">
            <span className="price">${property.price?.toLocaleString()}</span>
            <span className="status">{property.status}</span>
          </div>
        </div>

        <div className="property-images">
          {property.images && property.images.length > 0 ? (
            <div className="images-grid">
              {property.images.map((image, index) => (
                <img key={index} src={image} alt={`Property ${index + 1}`} />
              ))}
            </div>
          ) : (
            <div className="no-image-large">📷 No Images Available</div>
          )}
        </div>

        <div className="property-content">
          <div className="property-info-detailed">
            <h3>Property Details</h3>
            <div className="details-grid">
              <div className="detail-item">
                <span className="label">Location:</span>
                <span className="value">📍 {property.location}</span>
              </div>
              <div className="detail-item">
                <span className="label">Type:</span>
                <span className="value">{property.property_type}</span>
              </div>
              <div className="detail-item">
                <span className="label">Bedrooms:</span>
                <span className="value">🛏 {property.bedrooms}</span>
              </div>
              <div className="detail-item">
                <span className="label">Bathrooms:</span>
                <span className="value">🚿 {property.bathrooms}</span>
              </div>
              <div className="detail-item">
                <span className="label">Area:</span>
                <span className="value">📐 {property.area} sq ft</span>
              </div>
            </div>

            {property.features && property.features.length > 0 && (
              <div className="features-section">
                <h4>Features</h4>
                <div className="features-list">
                  {property.features.map((feature, index) => (
                    <span key={index} className="feature-tag">✓ {feature}</span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="property-description">
            <h3>Description</h3>
            <p>{property.description}</p>
          </div>

          <div className="contact-section">
            <h3>Interested in this property?</h3>
            <p>Contact Kimia RealEstate for more information or to schedule a viewing.</p>
            <div className="contact-buttons">
              <button className="btn-primary">Schedule Viewing</button>
              <button className="btn-secondary">Contact Agent</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const BlogPage = () => {
  const [blogPosts, setBlogPosts] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBlogPosts();
  }, []);

  const fetchBlogPosts = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/blog`);
      const data = await response.json();
      setBlogPosts(data);
    } catch (error) {
      console.error('Error fetching blog posts:', error);
    } finally {
      setLoading(false);
    }
  };

  if (selectedPost) {
    return (
      <BlogPostDetail 
        post={selectedPost} 
        onBack={() => setSelectedPost(null)} 
      />
    );
  }

  return (
    <div className="blog-page">
      <div className="container">
        <div className="page-header">
          <h1>Real Estate Insights</h1>
          <p>Expert tips, market updates, and guides from Kimia RealEstate</p>
        </div>

        {loading ? (
          <div className="loading">Loading articles...</div>
        ) : (
          <div className="blog-grid">
            {blogPosts.map(post => (
              <div key={post.id} className="blog-card" onClick={() => setSelectedPost(post)}>
                {post.image && (
                  <div className="blog-image">
                    <img src={post.image} alt={post.title} />
                  </div>
                )}
                <div className="blog-content">
                  <div className="blog-category">{post.category}</div>
                  <h3>{post.title}</h3>
                  <p>{post.excerpt}</p>
                  <div className="blog-meta">
                    <span>By {post.author}</span>
                    <span>{new Date(post.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && blogPosts.length === 0 && (
          <div className="no-results">
            <h3>No blog posts available</h3>
            <p>Check back soon for expert real estate insights!</p>
          </div>
        )}
      </div>
    </div>
  );
};

const BlogPostDetail = ({ post, onBack }) => {
  return (
    <div className="blog-detail">
      <div className="container">
        <button className="back-btn" onClick={onBack}>
          ← Back to Blog
        </button>
        
        {post.image && (
          <div className="blog-detail-image">
            <img src={post.image} alt={post.title} />
          </div>
        )}
        
        <div className="blog-detail-content">
          <div className="blog-category">{post.category}</div>
          <h1>{post.title}</h1>
          <div className="blog-meta">
            <span>By {post.author}</span>
            <span>{new Date(post.created_at).toLocaleDateString()}</span>
          </div>
          <div className="blog-content">
            {post.content.split('\n').map((paragraph, index) => (
              paragraph.trim() && <p key={index}>{paragraph}</p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const LoginPage = () => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });

      if (response.ok) {
        const data = await response.json();
        login(data.access_token);
      } else {
        setError('Invalid credentials');
      }
    } catch (error) {
      setError('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-form">
          <h2>Admin Login</h2>
          <p>Access the Kimia RealEstate admin panel</p>
          
          {error && <div className="error-message">{error}</div>}
          
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={credentials.username}
                onChange={(e) => setCredentials(prev => ({ ...prev, username: e.target.value }))}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={credentials.password}
                onChange={(e) => setCredentials(prev => ({ ...prev, password: e.target.value }))}
                required
              />
            </div>
            
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
          
          <div className="login-help">
            <p><small>Default credentials: admin / admin123</small></p>
          </div>
        </div>
      </div>
    </div>
  );
};

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('properties');
  const [properties, setProperties] = useState([]);
  const [blogPosts, setBlogPosts] = useState([]);
  const [showPropertyForm, setShowPropertyForm] = useState(false);
  const [showBlogForm, setShowBlogForm] = useState(false);
  const [editingProperty, setEditingProperty] = useState(null);
  const [editingBlogPost, setEditingBlogPost] = useState(null);
  const { token } = useAuth();

  useEffect(() => {
    if (activeTab === 'properties') {
      fetchProperties();
    } else if (activeTab === 'blog') {
      fetchBlogPosts();
    }
  }, [activeTab]);

  const fetchProperties = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/properties`);
      const data = await response.json();
      setProperties(data);
    } catch (error) {
      console.error('Error fetching properties:', error);
    }
  };

  const fetchBlogPosts = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/blog`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setBlogPosts(data);
    } catch (error) {
      console.error('Error fetching blog posts:', error);
    }
  };

  const deleteProperty = async (propertyId) => {
    if (!window.confirm('Are you sure you want to delete this property?')) return;

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/properties/${propertyId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        setProperties(prev => prev.filter(p => p.id !== propertyId));
      }
    } catch (error) {
      console.error('Error deleting property:', error);
    }
  };

  const deleteBlogPost = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this blog post?')) return;

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/blog/${postId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        setBlogPosts(prev => prev.filter(p => p.id !== postId));
      }
    } catch (error) {
      console.error('Error deleting blog post:', error);
    }
  };

  return (
    <div className="admin-panel">
      <div className="container">
        <div className="admin-header">
          <h1>Admin Panel</h1>
          <p>Manage your Kimia RealEstate content</p>
        </div>

        <div className="admin-tabs">
          <button 
            className={activeTab === 'properties' ? 'active' : ''}
            onClick={() => setActiveTab('properties')}
          >
            Properties
          </button>
          <button 
            className={activeTab === 'blog' ? 'active' : ''}
            onClick={() => setActiveTab('blog')}
          >
            Blog Posts
          </button>
        </div>

        {activeTab === 'properties' && (
          <div className="properties-admin">
            <div className="admin-actions">
              <button 
                className="btn-primary"
                onClick={() => setShowPropertyForm(true)}
              >
                Add New Property
              </button>
            </div>

            <div className="admin-table">
              <h3>Properties ({properties.length})</h3>
              <div className="table-responsive">
                <table>
                  <thead>
                    <tr>
                      <th>Title</th>
                      <th>Location</th>
                      <th>Price</th>
                      <th>Type</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {properties.map(property => (
                      <tr key={property.id}>
                        <td>{property.title}</td>
                        <td>{property.location}</td>
                        <td>${property.price?.toLocaleString()}</td>
                        <td>{property.property_type}</td>
                        <td>
                          <span className={`status-badge ${property.status}`}>
                            {property.status}
                          </span>
                        </td>
                        <td>
                          <div className="action-buttons">
                            <button 
                              className="btn-edit"
                              onClick={() => {
                                setEditingProperty(property);
                                setShowPropertyForm(true);
                              }}
                            >
                              Edit
                            </button>
                            <button 
                              className="btn-delete"
                              onClick={() => deleteProperty(property.id)}
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'blog' && (
          <div className="blog-admin">
            <div className="admin-actions">
              <button 
                className="btn-primary"
                onClick={() => setShowBlogForm(true)}
              >
                Add New Blog Post
              </button>
            </div>

            <div className="admin-table">
              <h3>Blog Posts ({blogPosts.length})</h3>
              <div className="table-responsive">
                <table>
                  <thead>
                    <tr>
                      <th>Title</th>
                      <th>Category</th>
                      <th>Author</th>
                      <th>Published</th>
                      <th>Date</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {blogPosts.map(post => (
                      <tr key={post.id}>
                        <td>{post.title}</td>
                        <td>{post.category}</td>
                        <td>{post.author}</td>
                        <td>
                          <span className={`status-badge ${post.published ? 'available' : 'sold'}`}>
                            {post.published ? 'Published' : 'Draft'}
                          </span>
                        </td>
                        <td>{new Date(post.created_at).toLocaleDateString()}</td>
                        <td>
                          <div className="action-buttons">
                            <button 
                              className="btn-edit"
                              onClick={() => {
                                setEditingBlogPost(post);
                                setShowBlogForm(true);
                              }}
                            >
                              Edit
                            </button>
                            <button 
                              className="btn-delete"
                              onClick={() => deleteBlogPost(post.id)}
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {showPropertyForm && (
          <PropertyForm 
            property={editingProperty}
            onClose={() => {
              setShowPropertyForm(false);
              setEditingProperty(null);
            }}
            onSuccess={() => {
              fetchProperties();
              setShowPropertyForm(false);
              setEditingProperty(null);
            }}
            token={token}
          />
        )}

        {showBlogForm && (
          <BlogForm 
            blogPost={editingBlogPost}
            onClose={() => {
              setShowBlogForm(false);
              setEditingBlogPost(null);
            }}
            onSuccess={() => {
              fetchBlogPosts();
              setShowBlogForm(false);
              setEditingBlogPost(null);
            }}
            token={token}
          />
        )}
      </div>
    </div>
  );
};

const PropertyForm = ({ property, onClose, onSuccess, token }) => {
  const [formData, setFormData] = useState({
    title: property?.title || '',
    description: property?.description || '',
    price: property?.price || '',
    location: property?.location || '',
    bedrooms: property?.bedrooms || 1,
    bathrooms: property?.bathrooms || 1,
    area: property?.area || '',
    property_type: property?.property_type || 'house',
    features: property?.features?.join(', ') || '',
    status: property?.status || 'available'
  });

  const [images, setImages] = useState(property?.images || []);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImages(prev => [...prev, e.target.result]);
      };
      reader.readAsDataURL(file);
    });
  };

  const removeImage = (index) => {
    setImages(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      ...formData,
      price: parseFloat(formData.price),
      bedrooms: parseInt(formData.bedrooms),
      bathrooms: parseInt(formData.bathrooms),
      area: parseFloat(formData.area),
      features: formData.features.split(',').map(f => f.trim()).filter(f => f),
      images: images
    };

    try {
      const url = property 
        ? `${process.env.REACT_APP_BACKEND_URL}/api/admin/properties/${property.id}`
        : `${process.env.REACT_APP_BACKEND_URL}/api/admin/properties`;
      
      const method = property ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        onSuccess();
      }
    } catch (error) {
      console.error('Error saving property:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>{property ? 'Edit Property' : 'Add New Property'}</h3>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="property-form">
          <div className="form-grid">
            <div className="form-group">
              <label>Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                required
              />
            </div>

            <div className="form-group">
              <label>Price ($)</label>
              <input
                type="number"
                value={formData.price}
                onChange={(e) => setFormData(prev => ({ ...prev, price: e.target.value }))}
                required
              />
            </div>

            <div className="form-group">
              <label>Location</label>
              <input
                type="text"
                value={formData.location}
                onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
                required
              />
            </div>

            <div className="form-group">
              <label>Property Type</label>
              <select
                value={formData.property_type}
                onChange={(e) => setFormData(prev => ({ ...prev, property_type: e.target.value }))}
              >
                <option value="house">House</option>
                <option value="apartment">Apartment</option>
                <option value="condo">Condo</option>
                <option value="villa">Villa</option>
              </select>
            </div>

            <div className="form-group">
              <label>Bedrooms</label>
              <input
                type="number"
                value={formData.bedrooms}
                onChange={(e) => setFormData(prev => ({ ...prev, bedrooms: e.target.value }))}
                min="0"
              />
            </div>

            <div className="form-group">
              <label>Bathrooms</label>
              <input
                type="number"
                value={formData.bathrooms}
                onChange={(e) => setFormData(prev => ({ ...prev, bathrooms: e.target.value }))}
                min="0"
              />
            </div>

            <div className="form-group">
              <label>Area (sq ft)</label>
              <input
                type="number"
                value={formData.area}
                onChange={(e) => setFormData(prev => ({ ...prev, area: e.target.value }))}
                required
              />
            </div>

            <div className="form-group">
              <label>Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData(prev => ({ ...prev, status: e.target.value }))}
              >
                <option value="available">Available</option>
                <option value="sold">Sold</option>
                <option value="rented">Rented</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              rows="4"
              required
            />
          </div>

          <div className="form-group">
            <label>Features (comma-separated)</label>
            <input
              type="text"
              value={formData.features}
              onChange={(e) => setFormData(prev => ({ ...prev, features: e.target.value }))}
              placeholder="Pool, Garage, Garden, Fireplace"
            />
          </div>

          <div className="form-group">
            <label>Property Images</label>
            <input
              type="file"
              multiple
              accept="image/*"
              onChange={handleImageUpload}
              className="file-input"
            />
            
            {images.length > 0 && (
              <div className="image-preview">
                {images.map((image, index) => (
                  <div key={index} className="image-item">
                    <img src={image} alt={`Property ${index + 1}`} />
                    <button 
                      type="button" 
                      onClick={() => removeImage(index)}
                      className="remove-image"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Saving...' : property ? 'Update Property' : 'Add Property'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const BlogForm = ({ blogPost, onClose, onSuccess, token }) => {
  const [formData, setFormData] = useState({
    title: blogPost?.title || '',
    content: blogPost?.content || '',
    excerpt: blogPost?.excerpt || '',
    category: blogPost?.category || 'tips',
    published: blogPost?.published !== undefined ? blogPost.published : true
  });

  const [image, setImage] = useState(blogPost?.image || '');
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      ...formData,
      image: image
    };

    try {
      const url = blogPost 
        ? `${process.env.REACT_APP_BACKEND_URL}/api/admin/blog/${blogPost.id}`
        : `${process.env.REACT_APP_BACKEND_URL}/api/admin/blog`;
      
      const method = blogPost ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        onSuccess();
      }
    } catch (error) {
      console.error('Error saving blog post:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>{blogPost ? 'Edit Blog Post' : 'Add New Blog Post'}</h3>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <form onSubmit={handleSubmit} className="blog-form">
          <div className="form-grid">
            <div className="form-group">
              <label>Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                required
              />
            </div>

            <div className="form-group">
              <label>Category</label>
              <select
                value={formData.category}
                onChange={(e) => setFormData(prev => ({ ...prev, category: e.target.value }))}
              >
                <option value="tips">Tips</option>
                <option value="market-updates">Market Updates</option>
                <option value="guides">Guides</option>
              </select>
            </div>

            <div className="form-group">
              <label>Published</label>
              <select
                value={formData.published}
                onChange={(e) => setFormData(prev => ({ ...prev, published: e.target.value === 'true' }))}
              >
                <option value="true">Published</option>
                <option value="false">Draft</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Excerpt</label>
            <textarea
              value={formData.excerpt}
              onChange={(e) => setFormData(prev => ({ ...prev, excerpt: e.target.value }))}
              rows="3"
              required
            />
          </div>

          <div className="form-group">
            <label>Content</label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData(prev => ({ ...prev, content: e.target.value }))}
              rows="10"
              required
            />
          </div>

          <div className="form-group">
            <label>Featured Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="file-input"
            />
            
            {image && (
              <div className="image-preview">
                <img src={image} alt="Blog featured image" />
              </div>
            )}
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Saving...' : blogPost ? 'Update Post' : 'Add Post'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

function App() {
  const [currentView, setCurrentView] = useState('home');

  const renderCurrentView = () => {
    switch (currentView) {
      case 'home':
        return <HomePage />;
      case 'properties':
        return <PropertiesPage />;
      case 'blog':
        return <BlogPage />;
      case 'login':
        return <LoginPage />;
      case 'admin':
        return <AdminPanel />;
      default:
        return <HomePage />;
    }
  };

  return (
    <AuthProvider>
      <div className="App">
        <Navbar currentView={currentView} setCurrentView={setCurrentView} />
        <main className="main-content">
          {renderCurrentView()}
        </main>
      </div>
    </AuthProvider>
  );
}

export default App;