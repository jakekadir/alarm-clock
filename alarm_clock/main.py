from fastapi import FastAPI

app = FastAPI()


@app.get("/cron")
async def get_cron():
    ...


@app.put("/cron")
async def set_cron():
    ...
