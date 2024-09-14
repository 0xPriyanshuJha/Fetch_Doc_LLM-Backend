import sys
import os
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from app.db import init_db, get_user, update_user_calls, create_user
from app.services.retrieval import search_documents
from app.rediscache import redis_client
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

@app.on_event("startup")

# initialize the database on server startup
async def startup_event():
    try:
        await init_db()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")

# Health check endpoint to ensure our API is up and running
@app.get("/health")
async def health():
    return{"status": "API is up and running"}


@app.get("/search")
async def search(
        text: str,
        top_k: int = 5,
        threshold: float = 0.8,
        user_id: str = None
):
    """
    Search for the documents based on the query text by the user.
    Params:
    text: The query text entered by the user
    top_k: The number of top results to return
    threshold: The minimum similarity score to consider for the search
    user_id: The user id of the user who is searching(for rate limiting).

    Returns:
    The list of top k documents with the similarity search and inference time.
    """
    start_time = time.time()

    if not user_id:
        raise HTTPException(status_code=400, detail="User id is Must")

    # check if the user has exceeded the rate limit
    try:
        user = await get_user(user_id)
        if user and user.api_calls >=5:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving Data")
    
    # check if the results are already cached
    cache_key = f"search:{user_id}:{text}"
    try:
        cached_res = redis_client.get(cache_key)
        if cached_res:
            return {"results": cached_res, "cached": True}
    except Exception as e:
        print("Redis Cache Error")

    # search the documents
    try:
        res = search_documents(text, top_k, threshold)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occured while searching")
    
    # Cache the results
    try:
        redis_client.set(cache_key, res, ex=3600)
    except Exception as e:
        print("Failed to set the cache")

    # update the user api calls
    try:
        if user:
            await update_user_calls(user_id)
        else:
            await create_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating user calls")

    inference_time = time.time() - start_time
    return {"results": res, "inference_time": inference_time, "cached": False}

@app.on_event("shutdown")
async def shutdown():
    try:
        await redis_client.close()
    except Exception as e:
        print("Error closing the redis connection")

# Global error handling
async def global_e_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )
