import re
from typing import Optional

from pydantic import BaseModel, model_validator

from alarm_clock.cron import JOB_REGEX, Schedule


class CronJob(BaseModel):
    id: str
    schedule: Schedule
    enabled: bool

    @model_validator(mode="before")
    def parse_cronitem(cls, cron_item):
        data = {}
        comment_match = re.match(JOB_REGEX, cron_item.comment)
        if not comment_match:
            raise ValueError(f"cannot determine id from {cron_item.comment}")
        data["id"] = comment_match.group(1)
        data["schedule"] = tuple(str(slice) for slice in cron_item.slices)
        data["enabled"] = cron_item.is_enabled()
        return data


class UpdateCronJob(BaseModel):
    id: str
    schedule: Optional[Schedule] = None
    enable: Optional[bool] = None
