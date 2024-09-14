from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.user import User, Base
from app.models.document import Document
from sqlalchemy.exc import IntegrityError
import dotenv
import os

# load the environment variables
dotenv.load_dotenv()


# database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# creating the database engine
engine = create_async_engine(DATABASE_URL, echo=True)
# create the session class
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# initializing the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# function to create a new user
async def create_user(user_id: str):
    async with AsyncSessionLocal() as session:
        try:
            new_user = User(user_id="test", api_calls=1)
            session.add(new_user)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise

# creating a new user
async def get_user(user_id: str):
    async with AsyncSessionLocal() as session: # creating a new session
        res = await session.execute(select(User).where(User.user_id == user_id))
        user = res.scalars().first()
        return user
        # new_user = User(user_id=user_id, api_calls=1)
        # session.add(new_user)
        # await session.commit()

# update the user api calls
async def update_user_calls(user_id: str):
    async with AsyncSessionLocal() as session: # create a new session
        res = await session.execute(select(User).where(User.user_id == user_id)) # query the user
        user = res.scalars().first()

        # update the user api calls
        if user:
            user.api_calls += 1
            await session.commit()

async def fetch_documents(indices):
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Document).where(Document.id.in_(indices)))
        documents = res.scalars().all()
        return [{"id": doc.id, "content": doc.content, "embedding": doc.embedding} for doc in documents]