from sqlalchemy import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.user import User, Base


# database URL
DATABASE_URL = "mysql+aiomysql://root:12345678@localhost/Test"

# creating the database engine
engine = create_async_engine(DATABASE_URL, echo=True)
# create the session class
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# initializing the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# creating a new user
async def get_user(user_id: str):
    async with AsyncSessionLocal() as session: # creating a new session
        new_user = User(user_id=user_id, api_calls=1)
        session.add(new_user)
        await session.commit()

# update the user api calls
async def update_user_calls(user_id: str):
    async with AsyncSessionLocal() as session: # create a new session
        res = await session.execute(select(User).where(User.user_id == user_id)) # query the user
        user = res.scalars().first()

        # update the user api calls
        if user:
            user.api_calls += 1
            await session.commit()