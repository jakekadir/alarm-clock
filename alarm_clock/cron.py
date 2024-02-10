import re
import sys
from pathlib import Path
from uuid import UUID, uuid4

from crontab import CronItem, CronSlices, CronTab

RING_PATH = str((Path(__name__).parent / "ring.py").resolve())
COMMAND = f"{sys.executable} {RING_PATH}"
CRON_TAB = "alarm_clock"
COMMAND_NAME = "alarm_clock_"
JOB_REGEX = re.compile(COMMAND_NAME + "([a-f0-9-]+)")

Schedule = tuple[str, str, str, str, str]


class Cron:
    def __init__(self):
        self.crontab = self._get_crontab()

    def _get_crontab(self) -> CronTab:
        return CronTab(user=True)

    def validate_cron(self, cron_schedule: Schedule) -> None:
        if not CronSlices.is_valid(cron_schedule):
            raise ValueError("invalid cron value")

    def get_cron_name(self, id: UUID) -> str:
        return COMMAND_NAME + str(id)

    def get_all(self) -> tuple[CronItem, ...]:
        return tuple(job for job in self.crontab.find_comment(JOB_REGEX))

    def create(self, cron_schedule: Schedule):
        self.validate_cron(cron_schedule)

        id = uuid4()
        with self.crontab as cron:
            cron_job = cron.new(command=COMMAND, comment=self.get_cron_name(id))
            cron_job.setall(cron_schedule)

            return id

    def get(self, id: UUID) -> CronItem:
        cron_name = self.get_cron_name(id)
        jobs = tuple(job for job in self.crontab.find_comment(cron_name))

        if len(jobs) != 1:
            raise ValueError(f"found {len(jobs)} cron jobs with id {cron_name}")

        return jobs[0]

    def set(self, id: UUID, cron_schedule: Schedule):
        self.validate_cron(cron_schedule)

        with self.crontab:
            cron_job = self.get(id)
            cron_job.clear()
            cron_job.setall(cron_schedule)

            return cron_job

    def enable(self, id: UUID):
        with self.crontab:
            job = self.get(id)
            job.enable(enabled=True)
            return job

    def disable(self, id: UUID):
        with self.crontab:
            job = self.get(id)
            job.enable(enabled=False)
            return job

    def delete(self, id: UUID):
        with self.crontab:
            cron_job = self.get(id)
            self.crontab.remove(cron_job)
        return cron_job
