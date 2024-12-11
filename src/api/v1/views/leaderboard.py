from fastapi import APIRouter

from src.api.v1.services.redis.redis_config import RedisBroker

router = APIRouter(prefix="/leaderboard")


@router.get("/")
async def get_leaderboard_score():
    redis_client = RedisBroker(channel="leaderboard").redis_client
    leaderboard = redis_client.hgetall("leaderboard")
    leaderboard = {key: int(value) for key, value in leaderboard.items()}
    return [{"player_id": player, "score": score} for player, score in leaderboard.items()]


@router.post("/update-score")
async def update_leaderboard_score(player_id: int, score: int):
    data = {"player_id": player_id, "score": score}
    redis_client = RedisBroker(channel="leaderboard").redis_client
    redis_client.hset("leaderboard", player_id, score)
    RedisBroker(channel="leaderboard").publish(data)
    return {"message": "Success"}
