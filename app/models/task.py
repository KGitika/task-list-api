from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str]
    description : Mapped[str]
    completed_at : Mapped[Optional[datetime]] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"), nullable=True)
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }

        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"], # this will raise KeyError if missing
            description=task_data["description"],
            completed_at=task_data.get("completed_at") # this will not raise KeyError if missing
        )
