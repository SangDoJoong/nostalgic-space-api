from app.config.database_init import conn


async def startup():
    print("Starting up...")
    conn()


async def shutdown():
    print("Shutting down...")
