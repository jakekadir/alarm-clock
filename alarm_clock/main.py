from uuid import UUID

from fastapi import FastAPI, HTTPException

from alarm_clock.cron import Cron
from alarm_clock.models import CronJob, Schedule

app = FastAPI()

cron = Cron()


def get_id(id: str):
    try:
        return UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID provided.")


@app.get("/cron")
async def get_cron(id: str) -> CronJob:
    uuid_id = get_id(id)
    return CronJob.model_validate(cron.get(uuid_id))


@app.get("/crons")
async def get_all_cron() -> list[CronJob]:
    cron_jobs = cron.get_all()
    raw_cron_jobs = [CronJob.model_validate(job) for job in cron_jobs]
    return raw_cron_jobs


@app.post("/cron")
async def create_cron(schedule: Schedule) -> CronJob:
    cronjob = cron.create(schedule)
    return CronJob.model_validate(cronjob)


@app.put("/cron")
async def edit_cron(id: str, schedule: Schedule) -> CronJob:
    uuid_id = get_id(id)
    cronjob = cron.set(uuid_id, schedule)
    return CronJob.model_validate(cronjob)


@app.delete("/cron")
async def delete_cron(id: str) -> CronJob:
    uuid_id = get_id(id)
    cronjob = cron.delete(uuid_id)
    return CronJob.model_validate(cronjob)
