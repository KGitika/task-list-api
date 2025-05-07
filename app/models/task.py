from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str]
    description : Mapped[str]
    completed_at : Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"], # this will raise KeyError if missing
            description=task_data["description"],
            completed_at=task_data.get("completed_at") # this will not raise KeyError if missing
        )
