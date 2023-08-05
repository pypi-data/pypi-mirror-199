from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from thoughtful.supervisor.recorder import DataLog, MessageLog
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.timed_report import TimedReport


@dataclass
class StepReport(TimedReport):
    """
    A step report is a representation of a step's execution. This dataclass
    contains all the information that will be stored in the run report. There
    are an arbitrary number of steps reports that will be contained in the
    workflow of any given run report.
    """

    step_id: str
    """
    str: The ID of the step.
    """

    status: Status
    """
    Status: The status of the step.
    """

    message_log: MessageLog = field(default_factory=list)
    """
    MessageLog: Log of messages from the recorder object.
    """

    data_log: DataLog = field(default_factory=list)
    """
    DataLog: Log of changes to data from the recorder object.
    """

    def __json__(self) -> Dict[str, Any]:
        return {
            **super().__json__(),
            "step_id": self.step_id,
            "step_status": self.status.value,
            "data_log": self.data_log,
            "message_log": self.message_log,
        }
