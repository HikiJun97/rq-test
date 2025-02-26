from fastapi import FastAPI, Body
from typing import Annotated

from redis_queue import RedisQueue
from fastapi_lifespan import lifespan

app = FastAPI(lifespan=lifespan)


@app.get("/redis-test")
async def test_redis():
    redis_client = await app.state.redis.get_redis()
    await redis_client.set("test_key", "Hello from Redis!")
    value = await redis_client.get("test_key")
    return {"redis_value": value}
    

@app.post("/enqueue")
async def enqueue(
    queue_name: Annotated[str, Body(...)],
    message: Annotated[str, Body(...)],
):
    if queue_name == "high":
        RedisQueue.high.enqueue(print, message)
    elif queue_name == "low":
        RedisQueue.low.enqueue(print, message)
    return {"message": f"Enqueued {message} to {queue_name} queue"}


if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
