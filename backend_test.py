#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Real Estate Website
Tests all API endpoints, authentication, and database integration
"""

import requests
import json
import uuid
from datetime import datetime
import sys
import os

# Get backend URL from environment
BACKEND_URL = "https://propexplorer.preview.emergentagent.com/api"

class RealEstateBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.admin_token = None
        self.test_property_id = None
        self.test_blog_id = None
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
    def log(self, message, level="INFO"):
        """Log test messages"""
        print(f"[{level}] {message}")
        
    def test_admin_login(self):
        """Test admin authentication system"""
        self.log("Testing Admin Login...")
        
        # Test valid login
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/admin/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.admin_token = data["access_token"]
                    self.session.headers.update({'Authorization': f'Bearer {self.admin_token}'})
                    self.log("✅ Admin login successful")
                    return True
                else:
                    self.log("❌ Admin login response missing required fields", "ERROR")
                    return False
            else:
                self.log(f"❌ Admin login failed with status {response.status_code}: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Admin login error: {str(e)}", "ERROR")
            return False
            
        # Test invalid login
        try:
            invalid_login = {"username": "admin", "password": "wrong"}
            response = self.session.post(f"{self.base_url}/admin/login", json=invalid_login)
            if response.status_code == 401:
                self.log("✅ Invalid login properly rejected")
            else:
                self.log(f"⚠️ Invalid login should return 401, got {response.status_code}")
        except Exception as e:
            self.log(f"⚠️ Error testing invalid login: {str(e)}")
            
    def test_property_crud(self):
        """Test Property CRUD operations"""
        self.log("Testing Property CRUD Operations...")
        
        if not self.admin_token:
            self.log("❌ Cannot test property CRUD without admin token", "ERROR")
            return False
            
        # Test CREATE property
        property_data = {
            "title": "Luxury Downtown Condo",
            "description": "Beautiful 2-bedroom condo in the heart of downtown with stunning city views",
            "price": 450000.0,
            "location": "Downtown Seattle",
            "bedrooms": 2,
            "bathrooms": 2,
            "area": 1200.0,
            "property_type": "condo",
            "images": ["https://example.com/image1.jpg"],
            "features": ["parking", "gym", "pool", "concierge"],
            "status": "available"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/admin/properties", json=property_data)
            
            if response.status_code == 200:
                created_property = response.json()
                self.test_property_id = created_property["id"]
                self.log("✅ Property created successfully")
                
                # Verify all fields
                for key, value in property_data.items():
                    if created_property.get(key) != value:
                        self.log(f"⚠️ Property field mismatch: {key} expected {value}, got {created_property.get(key)}")
                        
            else:
                self.log(f"❌ Property creation failed with status {response.status_code}: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Property creation error: {str(e)}", "ERROR")
            return False
            
        # Test READ single property
        if self.test_property_id:
            try:
                response = self.session.get(f"{self.base_url}/properties/{self.test_property_id}")
                if response.status_code == 200:
                    property_data = response.json()
                    self.log("✅ Property retrieval successful")
                else:
                    self.log(f"❌ Property retrieval failed with status {response.status_code}", "ERROR")
            except Exception as e:
                self.log(f"❌ Property retrieval error: {str(e)}", "ERROR")
                
        # Test UPDATE property
        if self.test_property_id:
            update_data = {
                "price": 475000.0,
                "status": "pending"
            }
            
            try:
                response = self.session.put(f"{self.base_url}/admin/properties/{self.test_property_id}", json=update_data)
                if response.status_code == 200:
                    updated_property = response.json()
                    if updated_property["price"] == 475000.0 and updated_property["status"] == "pending":
                        self.log("✅ Property update successful")
                    else:
                        self.log("⚠️ Property update values not reflected correctly")
                else:
                    self.log(f"❌ Property update failed with status {response.status_code}: {response.text}", "ERROR")
            except Exception as e:
                self.log(f"❌ Property update error: {str(e)}", "ERROR")
                
        return True
        
    def test_property_filtering(self):
        """Test property search and filtering"""
        self.log("Testing Property Search and Filtering...")
        
        # Test GET all properties
        try:
            response = self.session.get(f"{self.base_url}/properties")
            if response.status_code == 200:
                properties = response.json()
                self.log(f"✅ Retrieved {len(properties)} properties")
            else:
                self.log(f"❌ Properties retrieval failed with status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Properties retrieval error: {str(e)}", "ERROR")
            return False
            
        # Test search functionality
        search_params = [
            {"search": "Downtown"},
            {"property_type": "condo"},
            {"location": "Seattle"},
            {"min_price": 400000},
            {"max_price": 500000},
            {"min_price": 400000, "max_price": 500000, "property_type": "condo"}
        ]
        
        for params in search_params:
            try:
                response = self.session.get(f"{self.base_url}/properties", params=params)
                if response.status_code == 200:
                    results = response.json()
                    self.log(f"✅ Search with {params} returned {len(results)} results")
                else:
                    self.log(f"⚠️ Search with {params} failed: {response.status_code}")
            except Exception as e:
                self.log(f"⚠️ Search error with {params}: {str(e)}")
                
        return True
        
    def test_image_upload(self):
        """Test image upload functionality"""
        self.log("Testing Image Upload Functionality...")
        
        if not self.admin_token:
            self.log("❌ Cannot test image upload without admin token", "ERROR")
            return False
            
        # Test valid base64 image upload
        valid_image_data = {
            "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
            "filename": "test_image.jpg"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/admin/upload-image", json=valid_image_data)
            
            if response.status_code == 200:
                upload_result = response.json()
                if "image_url" in upload_result and "filename" in upload_result:
                    self.log("✅ Valid image upload successful")
                else:
                    self.log("❌ Image upload response missing required fields", "ERROR")
                    return False
            else:
                self.log(f"❌ Image upload failed with status {response.status_code}: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Image upload error: {str(e)}", "ERROR")
            return False
            
        # Test invalid image format
        try:
            invalid_image_data = {
                "image": "invalid_base64_data",
                "filename": "test.jpg"
            }
            response = self.session.post(f"{self.base_url}/admin/upload-image", json=invalid_image_data)
            if response.status_code == 400:
                self.log("✅ Invalid image format properly rejected")
            else:
                self.log(f"⚠️ Invalid image should return 400, got {response.status_code}")
        except Exception as e:
            self.log(f"⚠️ Error testing invalid image: {str(e)}")
            
        # Test unauthorized image upload
        try:
            unauth_session = requests.Session()
            unauth_session.headers.update({'Content-Type': 'application/json'})
            response = unauth_session.post(f"{self.base_url}/admin/upload-image", json=valid_image_data)
            if response.status_code in [401, 403]:
                self.log("✅ Unauthorized image upload properly rejected")
            else:
                self.log(f"⚠️ Unauthorized image upload should return 401/403, got {response.status_code}")
        except Exception as e:
            self.log(f"⚠️ Error testing unauthorized image upload: {str(e)}")
            
        return True

    def test_enhanced_blog_management(self):
        """Test enhanced blog management features"""
        self.log("Testing Enhanced Blog Management...")
        
        if not self.admin_token:
            self.log("❌ Cannot test enhanced blog management without admin token", "ERROR")
            return False
            
        # Test CREATE blog post with image and draft status
        blog_data_with_image = {
            "title": "Luxury Real Estate Market Trends 2024",
            "content": "The luxury real estate market is experiencing unprecedented changes in 2024...",
            "excerpt": "Comprehensive analysis of luxury market trends",
            "category": "market-updates",
            "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
            "published": False  # Draft status
        }
        
        try:
            response = self.session.post(f"{self.base_url}/admin/blog", json=blog_data_with_image)
            
            if response.status_code == 200:
                created_blog = response.json()
                self.test_blog_id = created_blog["id"]
                self.log("✅ Blog post with image and draft status created successfully")
                
                # Verify image field
                if created_blog.get("image") == blog_data_with_image["image"]:
                    self.log("✅ Blog post image field stored correctly")
                else:
                    self.log("⚠️ Blog post image field not stored correctly")
                    
                # Verify published status
                if created_blog.get("published") == False:
                    self.log("✅ Blog post draft status set correctly")
                else:
                    self.log("⚠️ Blog post draft status not set correctly")
                        
            else:
                self.log(f"❌ Blog creation with image failed with status {response.status_code}: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Blog creation with image error: {str(e)}", "ERROR")
            return False
            
        # Test GET /api/admin/blog (admin-only, includes drafts)
        try:
            response = self.session.get(f"{self.base_url}/admin/blog")
            if response.status_code == 200:
                admin_blog_posts = response.json()
                self.log(f"✅ Admin blog endpoint retrieved {len(admin_blog_posts)} posts (including drafts)")
                
                # Verify draft posts are included
                draft_posts = [post for post in admin_blog_posts if not post.get("published", True)]
                if len(draft_posts) > 0:
                    self.log("✅ Draft posts included in admin blog endpoint")
                else:
                    self.log("⚠️ No draft posts found in admin blog endpoint")
            else:
                self.log(f"❌ Admin blog endpoint failed with status {response.status_code}: {response.text}", "ERROR")
        except Exception as e:
            self.log(f"❌ Admin blog endpoint error: {str(e)}", "ERROR")
            
        # Test public blog endpoint excludes drafts
        try:
            response = self.session.get(f"{self.base_url}/blog")
            if response.status_code == 200:
                public_blog_posts = response.json()
                self.log(f"✅ Public blog endpoint retrieved {len(public_blog_posts)} published posts")
                
                # Verify no draft posts in public endpoint
                draft_posts = [post for post in public_blog_posts if not post.get("published", True)]
                if len(draft_posts) == 0:
                    self.log("✅ Draft posts correctly excluded from public blog endpoint")
                else:
                    self.log("⚠️ Draft posts found in public blog endpoint (should be excluded)")
            else:
                self.log(f"❌ Public blog endpoint failed with status {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Public blog endpoint error: {str(e)}", "ERROR")
            
        # Test UPDATE blog post
        if self.test_blog_id:
            update_data = {
                "title": "Updated: Luxury Real Estate Market Trends 2024",
                "published": True,  # Publish the draft
                "category": "guides"
            }
            
            try:
                response = self.session.put(f"{self.base_url}/admin/blog/{self.test_blog_id}", json=update_data)
                if response.status_code == 200:
                    updated_blog = response.json()
                    if (updated_blog["title"] == update_data["title"] and 
                        updated_blog["published"] == True and 
                        updated_blog["category"] == "guides"):
                        self.log("✅ Blog post update successful")
                    else:
                        self.log("⚠️ Blog post update values not reflected correctly")
                else:
                    self.log(f"❌ Blog post update failed with status {response.status_code}: {response.text}", "ERROR")
            except Exception as e:
                self.log(f"❌ Blog post update error: {str(e)}", "ERROR")
                
        # Test DELETE blog post
        if self.test_blog_id:
            try:
                response = self.session.delete(f"{self.base_url}/admin/blog/{self.test_blog_id}")
                if response.status_code == 200:
                    self.log("✅ Blog post deletion successful")
                    # Verify deletion
                    verify_response = self.session.get(f"{self.base_url}/blog/{self.test_blog_id}")
                    if verify_response.status_code == 404:
                        self.log("✅ Deleted blog post no longer accessible")
                    else:
                        self.log("⚠️ Deleted blog post still accessible")
                else:
                    self.log(f"❌ Blog post deletion failed with status {response.status_code}: {response.text}", "ERROR")
            except Exception as e:
                self.log(f"❌ Blog post deletion error: {str(e)}", "ERROR")
                
        return True

    def test_enhanced_property_management(self):
        """Test enhanced property management with multiple images"""
        self.log("Testing Enhanced Property Management with Images...")
        
        if not self.admin_token:
            self.log("❌ Cannot test enhanced property management without admin token", "ERROR")
            return False
            
        # Test CREATE property with multiple base64 images
        property_data_with_images = {
            "title": "Stunning Waterfront Villa",
            "description": "Magnificent waterfront villa with panoramic ocean views and luxury amenities",
            "price": 2500000.0,
            "location": "Malibu, California",
            "bedrooms": 5,
            "bathrooms": 4,
            "area": 4500.0,
            "property_type": "villa",
            "images": [
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A"
            ],
            "features": ["ocean_view", "private_beach", "infinity_pool", "wine_cellar", "home_theater"],
            "status": "available"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/admin/properties", json=property_data_with_images)
            
            if response.status_code == 200:
                created_property = response.json()
                self.test_property_id = created_property["id"]
                self.log("✅ Property with multiple images created successfully")
                
                # Verify images array
                if len(created_property.get("images", [])) == 3:
                    self.log("✅ Property images array stored correctly (3 images)")
                else:
                    self.log(f"⚠️ Property images array incorrect length: expected 3, got {len(created_property.get('images', []))}")
                    
                # Verify all images are base64
                all_base64 = all(img.startswith('data:image') for img in created_property.get("images", []))
                if all_base64:
                    self.log("✅ All property images are valid base64 format")
                else:
                    self.log("⚠️ Some property images are not in valid base64 format")
                        
            else:
                self.log(f"❌ Property creation with images failed with status {response.status_code}: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Property creation with images error: {str(e)}", "ERROR")
            return False
            
        # Test UPDATE property images
        if self.test_property_id:
            new_images = [
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A",
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A8A"
            ]
            
            update_data = {
                "images": new_images,
                "price": 2750000.0
            }
            
            try:
                response = self.session.put(f"{self.base_url}/admin/properties/{self.test_property_id}", json=update_data)
                if response.status_code == 200:
                    updated_property = response.json()
                    if (len(updated_property.get("images", [])) == 2 and 
                        updated_property["price"] == 2750000.0):
                        self.log("✅ Property images update successful")
                    else:
                        self.log("⚠️ Property images update values not reflected correctly")
                else:
                    self.log(f"❌ Property images update failed with status {response.status_code}: {response.text}", "ERROR")
            except Exception as e:
                self.log(f"❌ Property images update error: {str(e)}", "ERROR")
                
        return True

    def test_blog_endpoints(self):
        """Test basic blog post endpoints (legacy test)"""
        self.log("Testing Basic Blog Post Endpoints...")
        
        if not self.admin_token:
            self.log("❌ Cannot test blog creation without admin token", "ERROR")
            return False
            
        # Test CREATE basic blog post
        blog_data = {
            "title": "Top 10 Home Buying Tips for 2024",
            "content": "Here are the essential tips every home buyer should know in 2024...",
            "excerpt": "Essential home buying tips for the current market",
            "category": "tips",
            "published": True
        }
        
        try:
            response = self.session.post(f"{self.base_url}/admin/blog", json=blog_data)
            
            if response.status_code == 200:
                created_blog = response.json()
                basic_blog_id = created_blog["id"]
                self.log("✅ Basic blog post created successfully")
                
                # Verify fields
                for key, value in blog_data.items():
                    if created_blog.get(key) != value:
                        self.log(f"⚠️ Blog field mismatch: {key} expected {value}, got {created_blog.get(key)}")
                        
            else:
                self.log(f"❌ Basic blog creation failed with status {response.status_code}: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Basic blog creation error: {str(e)}", "ERROR")
            return False
            
        # Test READ all blog posts
        try:
            response = self.session.get(f"{self.base_url}/blog")
            if response.status_code == 200:
                blog_posts = response.json()
                self.log(f"✅ Retrieved {len(blog_posts)} blog posts")
            else:
                self.log(f"❌ Blog posts retrieval failed with status {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Blog posts retrieval error: {str(e)}", "ERROR")
            
        # Test READ single blog post
        if basic_blog_id:
            try:
                response = self.session.get(f"{self.base_url}/blog/{basic_blog_id}")
                if response.status_code == 200:
                    blog_post = response.json()
                    self.log("✅ Single blog post retrieval successful")
                else:
                    self.log(f"❌ Single blog post retrieval failed with status {response.status_code}", "ERROR")
            except Exception as e:
                self.log(f"❌ Single blog post retrieval error: {str(e)}", "ERROR")
                
        # Test blog filtering by category
        try:
            response = self.session.get(f"{self.base_url}/blog", params={"category": "tips"})
            if response.status_code == 200:
                filtered_posts = response.json()
                self.log(f"✅ Blog category filtering returned {len(filtered_posts)} posts")
            else:
                self.log(f"⚠️ Blog category filtering failed: {response.status_code}")
        except Exception as e:
            self.log(f"⚠️ Blog category filtering error: {str(e)}")
            
        return True
        
    def test_authorization(self):
        """Test authorization for protected endpoints"""
        self.log("Testing Authorization...")
        
        # Create session without auth token
        unauth_session = requests.Session()
        unauth_session.headers.update({'Content-Type': 'application/json'})
        
        protected_endpoints = [
            ("POST", "/admin/properties", {"title": "Test", "price": 100000, "location": "Test", "bedrooms": 1, "bathrooms": 1, "area": 1000, "property_type": "house", "description": "Test"}),
            ("PUT", "/admin/properties/test-id", {"price": 200000}),
            ("DELETE", "/admin/properties/test-id", None),
            ("POST", "/admin/blog", {"title": "Test", "content": "Test", "excerpt": "Test", "category": "tips"})
        ]
        
        for method, endpoint, data in protected_endpoints:
            try:
                if method == "POST":
                    response = unauth_session.post(f"{self.base_url}{endpoint}", json=data)
                elif method == "PUT":
                    response = unauth_session.put(f"{self.base_url}{endpoint}", json=data)
                elif method == "DELETE":
                    response = unauth_session.delete(f"{self.base_url}{endpoint}")
                    
                if response.status_code == 401:
                    self.log(f"✅ {method} {endpoint} properly protected")
                else:
                    self.log(f"⚠️ {method} {endpoint} should return 401, got {response.status_code}")
                    
            except Exception as e:
                self.log(f"⚠️ Authorization test error for {method} {endpoint}: {str(e)}")
                
        return True
        
    def test_error_handling(self):
        """Test error handling for non-existent resources"""
        self.log("Testing Error Handling...")
        
        # Test non-existent property
        try:
            response = self.session.get(f"{self.base_url}/properties/non-existent-id")
            if response.status_code == 404:
                self.log("✅ Non-existent property returns 404")
            else:
                self.log(f"⚠️ Non-existent property should return 404, got {response.status_code}")
        except Exception as e:
            self.log(f"⚠️ Error testing non-existent property: {str(e)}")
            
        # Test non-existent blog post
        try:
            response = self.session.get(f"{self.base_url}/blog/non-existent-id")
            if response.status_code == 404:
                self.log("✅ Non-existent blog post returns 404")
            else:
                self.log(f"⚠️ Non-existent blog post should return 404, got {response.status_code}")
        except Exception as e:
            self.log(f"⚠️ Error testing non-existent blog post: {str(e)}")
            
        return True
        
    def cleanup(self):
        """Clean up test data"""
        self.log("Cleaning up test data...")
        
        # Delete test property
        if self.test_property_id and self.admin_token:
            try:
                response = self.session.delete(f"{self.base_url}/admin/properties/{self.test_property_id}")
                if response.status_code == 200:
                    self.log("✅ Test property deleted successfully")
                else:
                    self.log(f"⚠️ Test property deletion failed: {response.status_code}")
            except Exception as e:
                self.log(f"⚠️ Error deleting test property: {str(e)}")
                
        # Note: Blog posts don't have delete endpoint in current implementation
        
    def run_all_tests(self):
        """Run all backend tests"""
        self.log("=" * 60)
        self.log("STARTING ENHANCED KIMIA REAL ESTATE BACKEND TESTS")
        self.log("=" * 60)
        
        test_results = {}
        
        # Test admin authentication
        test_results['admin_auth'] = self.test_admin_login()
        
        # Test NEW FEATURE: Image upload functionality
        test_results['image_upload'] = self.test_image_upload()
        
        # Test NEW FEATURE: Enhanced blog management
        test_results['enhanced_blog_management'] = self.test_enhanced_blog_management()
        
        # Test NEW FEATURE: Enhanced property management with images
        test_results['enhanced_property_management'] = self.test_enhanced_property_management()
        
        # Test basic property CRUD
        test_results['property_crud'] = self.test_property_crud()
        
        # Test property filtering
        test_results['property_filtering'] = self.test_property_filtering()
        
        # Test basic blog endpoints
        test_results['blog_endpoints'] = self.test_blog_endpoints()
        
        # Test authorization
        test_results['authorization'] = self.test_authorization()
        
        # Test error handling
        test_results['error_handling'] = self.test_error_handling()
        
        # Cleanup
        self.cleanup()
        
        # Summary
        self.log("=" * 60)
        self.log("TEST SUMMARY")
        self.log("=" * 60)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            self.log(f"{test_name.upper()}: {status}")
            if result:
                passed += 1
                
        self.log(f"\nOVERALL: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 ALL ENHANCED BACKEND TESTS PASSED!")
            return True
        else:
            self.log("⚠️ SOME TESTS FAILED - CHECK LOGS ABOVE")
            return False

if __name__ == "__main__":
    tester = RealEstateBackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)