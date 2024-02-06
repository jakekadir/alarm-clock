import sys
from pathlib import Path

from crontab import CronItem, CronSlices, CronTab

RING_PATH = str((Path(__name__).parent / "ring.py").resolve())
COMMAND = f"{sys.executable} {RING_PATH}"
CRON_TAB = "alarm_clock"
COMMAND_NAME = "alarm_clock_"


class Cron:
    def __init__(self):
        self.crontab = self._get_crontab()

    def _get_crontab(self) -> CronTab:
        return CronTab(user=True)

    def validate_cron(self, cron_schedule: str) -> None:
        if not CronSlices.is_valid(cron_schedule):
            raise ValueError("invalid cron value")

    def get_cron_name(self, id: int) -> str:
        return COMMAND_NAME + str(id)

    def create_cron(self, id: int, cron_schedule: str):
        self.validate_cron(cron_schedule)

        with self.crontab as cron:
            cron_job = cron.new(command=COMMAND, comment=self.get_cron_name(id))
            cron_job.setall(cron_schedule)

            return cron_job

    def get_cron(self, id: int) -> CronItem:
        cron_name = self.get_cron_name(id)
        jobs = tuple(job for job in self.crontab.find_comment(cron_name))

        if len(jobs) != 1:
            raise ValueError(f"found {len(jobs)} cron jobs with id {cron_name}")

        return jobs[0]

    def set_cron(self, id: int, cron_schedule: str):
        self.validate_cron(cron_schedule)

        with self.crontab:
            cron_job = self.get_cron(id)
            cron_job.clear()
            cron_job.setall(cron_schedule)

            return cron_job
