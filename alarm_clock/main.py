from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from alarm_clock.cron import Cron
from alarm_clock.models import CronJob, UpdateCronJob, CreateCronJob

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def create_cron(cron_job_create: CreateCronJob) -> CronJob:
    cron_job_id = cron.create(cron_job_create.schedule)
    if not cron_job_create.enabled:
        cron.disable(cron_job_id)
    return CronJob.model_validate(cron.get(cron_job_id))


@app.put("/cron")
async def edit_cron(cron_job_update: UpdateCronJob) -> CronJob:
    uuid_id = get_id(cron_job_update.id)
    cron_job = cron.get(uuid_id)
    if cron_job_update.schedule:
        cron_job = cron.set(uuid_id, cron_job_update.schedule)
    match cron_job_update.enabled:
        case True:
            cron_job = cron.enable(uuid_id)
        case False:
            cron_job = cron.disable(uuid_id)
    return CronJob.model_validate(cron_job)


@app.delete("/cron")
async def delete_cron(id: str) -> CronJob:
    uuid_id = get_id(id)
    cronjob = cron.delete(uuid_id)
    return CronJob.model_validate(cronjob)
