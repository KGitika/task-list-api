from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from sqlalchemy.orm import relationship

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):
        return{
            "id" : self.id,
            "title" : self.title
        }

    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title = goal_data["title"]
        )