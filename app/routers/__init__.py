from fastapi import APIRouter
from .user import router as users_router  # Import users router
from .post import router as products_router  # Import post router
from .auth import router as auth_router
from .vote import router as vote_router

router = APIRouter()  # Create a main APIRouter

router.include_router(users_router)  # Add the users router
router.include_router(products_router)  # Add the products router
router.include_router(auth_router)
router.include_router(vote_router)
