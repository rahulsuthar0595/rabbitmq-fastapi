from fastapi import APIRouter

from src.api.v1.services.redis.redis_config import RedisBroker

router = APIRouter(prefix="/leaderboard")

redis_broker = RedisBroker(channel="leaderboard")
redis_client = redis_broker.redis_client


@router.get("/")
async def get_leaderboard_score():
    # Fetch leaderboard from Redis
    leaderboard = redis_client.hgetall("leaderboard")
    leaderboard_data = {key: int(value) for key, value in leaderboard.items()}
    return [{"player_id": player, "score": score} for player, score in leaderboard_data.items()]


@router.post("/update-score")
async def update_leaderboard_score(player_id: int, score: int):
    # Update the leaderboard in Redis
    redis_client.hset("leaderboard", player_id, score)
    # Publish the score update
    data = {"player_id": player_id, "score": score}
    redis_broker.publish(data)
    return {"message": "Success"}
