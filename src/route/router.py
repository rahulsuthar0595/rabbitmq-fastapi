from fastapi import APIRouter
from src.api.v1.views import order, leaderboard
router = APIRouter(prefix="/api/v1")

# router.include_router(order.router, tags=["Order API"])
router.include_router(leaderboard.router, tags=["Redis Leaderboard API"])