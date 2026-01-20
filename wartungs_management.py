from typing import Self
from datetime import datetime
import uuid

from serializable import Serializable
from database import DatabaseConnector


class Maintenance(Serializable):
    db_connector = DatabaseConnector().get_table("maintenance")

    def __init__(self, appointment_date: datetime, reason: str, id: str = None, creation_date: datetime = None,
                 last_update: datetime = None) -> None:
        if id is None:
            id = str(uuid.uuid4())

        super().__init__(id, creation_date, last_update)
        self.appointment_date = appointment_date
        self.reason = reason

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(
            appointment_date=data['appointment_date'],
            reason=data['reason'],
            id=data['id'],
            creation_date=data['creation_date'],
            last_update=data['last_update']
        )

    def __str__(self) -> str:
        return f"Wartung: {self.appointment_date} - {self.reason}"

    @classmethod
    def get_next_maintenance(cls) -> Self | None:

        all_entries = cls.find_all()
        now = datetime.now()

        future_entries = [m for m in all_entries if m.appointment_date > now]

        if not future_entries:
            return None

        future_entries.sort(key=lambda x: x.appointment_date)

        return future_entries[0]