from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import jwt
import hashlib
import base64

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection (commented out for testing without MongoDB)
# mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
# client = AsyncIOMotorClient(mongo_url)
# db = client[os.environ.get('DB_NAME', 'kimia_realestate')]

# Mock data for testing without MongoDB
mock_properties = [
    {
        "id": "1",
        "title": "Luxury Modern Villa",
        "description": "A stunning modern villa with panoramic views and premium amenities.",
        "price": 1250000,
        "location": "Beverly Hills, CA",
        "bedrooms": 5,
        "bathrooms": 4,
        "area": 3500,
        "property_type": "villa",
        "images": ["https://images.unsplash.com/photo-1580587771525-78b9dba3b914"],
        "features": ["Pool", "Garage", "Garden", "Fireplace"],
        "status": "available",
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": "2", 
        "title": "Contemporary Downtown Apartment",
        "description": "Sleek apartment in the heart of downtown with city views.",
        "price": 750000,
        "location": "Manhattan, NY",
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1800,
        "property_type": "apartment",
        "images": ["https://images.unsplash.com/photo-1613490493576-7fde63acd811"],
        "features": ["City View", "Gym", "Concierge"],
        "status": "available",
        "created_at": "2024-01-16T10:00:00Z",
        "updated_at": "2024-01-16T10:00:00Z"
    }
]

mock_blog_posts = [
    {
        "id": "1",
        "title": "First-Time Home Buyer's Guide",
        "content": "Buying your first home is an exciting milestone, but it can also be overwhelming. Here's a comprehensive guide to help you navigate the process...",
        "excerpt": "Everything you need to know about buying your first home",
        "category": "guides",
        "author": "Admin",
        "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa",
        "published": True,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    }
]

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
SECRET_KEY = "your-secret-key-change-in-production"

# Models
class Property(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    area: float  # in square feet
    property_type: str  # house, apartment, condo, etc.
    images: List[str] = []  # base64 encoded images or URLs
    features: List[str] = []  # amenities like parking, pool, etc.
    status: str = "available"  # available, sold, rented
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PropertyCreate(BaseModel):
    title: str
    description: str
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    area: float
    property_type: str
    images: List[str] = []
    features: List[str] = []
    status: str = "available"

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[float] = None
    property_type: Optional[str] = None
    images: Optional[List[str]] = None
    features: Optional[List[str]] = None
    status: Optional[str] = None

class AdminLogin(BaseModel):
    username: str
    password: str

class BlogPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    excerpt: str
    category: str  # tips, market-updates, guides
    author: str = "Admin"
    image: str = ""  # base64 image or URL
    published: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BlogPostCreate(BaseModel):
    title: str
    content: str
    excerpt: str
    category: str
    image: str = ""
    published: bool = True

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    published: Optional[bool] = None

class ImageUpload(BaseModel):
    image: str  # base64 encoded image
    filename: str

# Helper functions
def prepare_for_mongo(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data

def parse_from_mongo(item):
    if isinstance(item.get('created_at'), str):
        item['created_at'] = datetime.fromisoformat(item['created_at'])
    if isinstance(item.get('updated_at'), str):
        item['updated_at'] = datetime.fromisoformat(item['updated_at'])
    return item

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Admin Authentication
@api_router.post("/admin/login")
async def admin_login(admin: AdminLogin):
    # Simple admin credentials - in production, use database
    if admin.username == "admin" and hash_password(admin.password) == hash_password("admin123"):
        token = create_access_token({"sub": "admin", "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Image upload endpoint
@api_router.post("/admin/upload-image")
async def upload_image(image_data: ImageUpload, token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        # Validate base64 image
        if not image_data.image.startswith('data:image'):
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Return the image URL (in a real app, you'd save to storage)
        return {"image_url": image_data.image, "filename": image_data.filename}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image upload failed: {str(e)}")

# Property endpoints
@api_router.get("/properties", response_model=List[Property])
async def get_properties(
    search: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None
):
    # Filter mock data based on query parameters
    filtered_properties = mock_properties.copy()
    
    if search:
        search_lower = search.lower()
        filtered_properties = [p for p in filtered_properties 
                             if search_lower in p["title"].lower() or 
                                search_lower in p["description"].lower() or 
                                search_lower in p["location"].lower()]
    
    if property_type:
        filtered_properties = [p for p in filtered_properties 
                             if property_type.lower() in p["property_type"].lower()]
    
    if location:
        filtered_properties = [p for p in filtered_properties 
                             if location.lower() in p["location"].lower()]
    
    if min_price:
        filtered_properties = [p for p in filtered_properties if p["price"] >= min_price]
    
    if max_price:
        filtered_properties = [p for p in filtered_properties if p["price"] <= max_price]
    
    return [Property(**prop) for prop in filtered_properties]

@api_router.get("/properties/{property_id}", response_model=Property)
async def get_property(property_id: str):
    property_data = next((p for p in mock_properties if p["id"] == property_id), None)
    if not property_data:
        raise HTTPException(status_code=404, detail="Property not found")
    return Property(**property_data)

@api_router.post("/admin/properties", response_model=Property)
async def create_property(property_data: PropertyCreate, token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    property_obj = Property(**property_data.dict())
    property_dict = prepare_for_mongo(property_obj.dict())
    await db.properties.insert_one(property_dict)
    return property_obj

@api_router.put("/admin/properties/{property_id}", response_model=Property)
async def update_property(property_id: str, property_data: PropertyUpdate, token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    existing_property = await db.properties.find_one({"id": property_id})
    if not existing_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    update_data = {k: v for k, v in property_data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    prepared_data = prepare_for_mongo(update_data)
    await db.properties.update_one({"id": property_id}, {"$set": prepared_data})
    
    updated_property = await db.properties.find_one({"id": property_id})
    return Property(**parse_from_mongo(updated_property))

@api_router.delete("/admin/properties/{property_id}")
async def delete_property(property_id: str, token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.properties.delete_one({"id": property_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"message": "Property deleted successfully"}

# Blog endpoints
@api_router.get("/blog", response_model=List[BlogPost])
async def get_blog_posts(category: Optional[str] = None):
    filtered_posts = [p for p in mock_blog_posts if p["published"]]
    if category:
        filtered_posts = [p for p in filtered_posts if p["category"] == category]
    return [BlogPost(**post) for post in filtered_posts]

@api_router.get("/blog/{post_id}", response_model=BlogPost)
async def get_blog_post(post_id: str):
    post = next((p for p in mock_blog_posts if p["id"] == post_id and p["published"]), None)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return BlogPost(**post)

@api_router.get("/admin/blog", response_model=List[BlogPost])
async def get_all_blog_posts(token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return [BlogPost(**post) for post in mock_blog_posts]

@api_router.post("/admin/blog", response_model=BlogPost)
async def create_blog_post(post_data: BlogPostCreate, token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    blog_post = BlogPost(**post_data.dict())
    post_dict = prepare_for_mongo(blog_post.dict())
    await db.blog_posts.insert_one(post_dict)
    return blog_post

@api_router.put("/admin/blog/{post_id}", response_model=BlogPost)
async def update_blog_post(post_id: str, post_data: BlogPostUpdate, token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    existing_post = await db.blog_posts.find_one({"id": post_id})
    if not existing_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    update_data = {k: v for k, v in post_data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    prepared_data = prepare_for_mongo(update_data)
    await db.blog_posts.update_one({"id": post_id}, {"$set": prepared_data})
    
    updated_post = await db.blog_posts.find_one({"id": post_id})
    return BlogPost(**parse_from_mongo(updated_post))

@api_router.delete("/admin/blog/{post_id}")
async def delete_blog_post(post_id: str, token: dict = Depends(verify_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.blog_posts.delete_one({"id": post_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# @app.on_event("shutdown")
# async def shutdown_db_client():
#     client.close()