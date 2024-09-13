from fastapi import FastAPI, HTTPException, Request, Depends
from app.db import init_db, get_user, create_user, update_user_calls
from app.services.document_retrieval import search_documents
from app.redis_cache import redis_client
import time


app = FastAPI()

@app.on_event("startup")

# initialize the database on server startup
async def startup_event():
    await init_db()

# Health check endpoint to ensure our API is up and running
@app.get("/health")
async def Health():
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

    # check if the user has exceeded the rate limit
    user = await get_user(user_id)
    if user and user.api_calls >=5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # check if the results are already cached
    cache_key = f"search:{user_id}:{text}"
    cached_res = redis_client.get(cache_key)
    if cached_res:
        return {"results": cached_res, "cached": True}
    
    # search the documents
    res = search_documents(text, top_k, threshold)

    # Cache the results
    redis_client.set(cache_key, res, ex=3600)

    # update the user api calls
    if user:
        await update_user_calls(user_id)
    else:
        await create_user(user_id)

    inference_time = time.time() - start_time
    return {"results": res, "inference_time": inference_time, "cached": False}
