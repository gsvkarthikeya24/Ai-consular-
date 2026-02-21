from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timezone
from bson import ObjectId
from ..models.user import UserCreate, UserResponse, LoginRequest, TokenResponse, UserUpdate
from ..database import get_collection, is_mock_mode
from ..utils.auth_utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new student"""
    users_collection = get_collection("users")
    
    # Check if user exists
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_dict = user_data.model_dump(exclude={"password"})
    current_time = datetime.now(timezone.utc)
    user_dict.update({
        "password": hash_password(user_data.password),
        "role": "student",
        "created_at": current_time,
        "updated_at": current_time
    })
    
    result = users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    
    # Create access token
    access_token = create_access_token(data={"sub": user_data.email})
    
    # Prepare response
    user_response = UserResponse(
        id=user_dict["_id"],
        name=user_dict["name"],
        email=user_dict["email"],
        branch=user_dict["branch"],
        year=user_dict["year"],
        interests=user_dict["interests"],
        career_goal=user_dict["career_goal"],
        role=user_dict["role"],
        created_at=user_dict["created_at"]
    )
    
    return TokenResponse(access_token=access_token, user=user_response)


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Login user with fallback for Demo Mode"""
    users_collection = get_collection("users")
    
    # Check for demo user fallback if database is down
    if users_collection is None:
        if credentials.email == "student1@example.com" and credentials.password == "password123":
            # Return a mock demo user
            user_response = UserResponse(
                id="demo-id",
                name="Demo Student (Offline Mode)",
                email="student1@example.com",
                branch="CSE",
                year=3,
                interests=["Machine Learning", "Web Development"],
                career_goal="Job",
                role="student",
                created_at=datetime.now(timezone.utc)
            )
            access_token = create_access_token(data={"sub": credentials.email})
            return TokenResponse(access_token=access_token, user=user_response)
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is offline. Only demo login is available currently."
        )
    
    # Regular login flow
    try:
        user = users_collection.find_one({"email": credentials.email})
        
        # DEMO MODE FIX: If user not found but we are in mock mode, create the demo user on the fly
        if not user and is_mock_mode() and credentials.email == "student1@example.com" and credentials.password == "password123":
            print("[INFO] Mock mode: Creating demo user on first login")
            current_time = datetime.now(timezone.utc)
            demo_user = {
                "name": "Demo Student",
                "email": "student1@example.com",
                "password": hash_password("password123"),
                "branch": "CSE",
                "year": 3,
                "interests": ["Machine Learning", "Web Development", "AI"],
                "career_goal": "Job",
                "role": "student",
                "created_at": current_time,
                "updated_at": current_time
            }
            result = users_collection.insert_one(demo_user)
            demo_user["_id"] = result.inserted_id
            user = demo_user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection error"
        )

    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": credentials.email})
    
    # Update login stats
    current_time = datetime.now(timezone.utc)
    users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$inc": {"login_count": 1},
            "$set": {
                "last_login": current_time,
                "status": "active",
                "updated_at": current_time
            }
        }
    )
    
    # Reload user data to get updated stats for response
    user = users_collection.find_one({"_id": user["_id"]})
    
    # Prepare response
    user_response = UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        branch=user["branch"],
        year=user["year"],
        interests=user["interests"],
        career_goal=user["career_goal"],
        role=user["role"],
        login_count=user.get("login_count", 0),
        last_login=user.get("last_login"),
        status=user.get("status", "active"),
        created_at=user["created_at"]
    )
    
    return TokenResponse(access_token=access_token, user=user_response)


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse(
        id=str(current_user["_id"]),
        name=current_user["name"],
        email=current_user["email"],
        branch=current_user["branch"],
        year=current_user["year"],
        interests=current_user["interests"],
        career_goal=current_user["career_goal"],
        role=current_user["role"],
        created_at=current_user["created_at"]
    )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    updates: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile"""
    users_collection = get_collection("users")
    
    # Prepare update data
    update_data = {k: v for k, v in updates.model_dump(exclude_unset=True).items() if v is not None}
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # Update user
    users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data}
    )
    
    # Fetch updated user
    updated_user = users_collection.find_one({"_id": current_user["_id"]})
    
    return UserResponse(
        id=str(updated_user["_id"]),
        name=updated_user["name"],
        email=updated_user["email"],
        branch=updated_user["branch"],
        year=updated_user["year"],
        interests=updated_user["interests"],
        career_goal=updated_user["career_goal"],
        role=updated_user["role"],
        created_at=updated_user["created_at"]
    )


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile - used for token validation"""
    return UserResponse(
        id=str(current_user["_id"]),
        name=current_user["name"],
        email=current_user["email"],
        branch=current_user["branch"],
        year=current_user["year"],
        interests=current_user.get("interests", []),
        career_goal=current_user.get("career_goal", ""),
        role=current_user.get("role", "student"),
        created_at=current_user.get("created_at", "")
    )
