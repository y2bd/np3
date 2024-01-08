from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Rating(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    album: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    artist: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    rating: so.Mapped[int] = so.mapped_column(sa.Integer)
    review: so.Mapped[Optional[str]] = so.mapped_column(sa.VARCHAR(), nullable=True)

    def __repr__(self):
        return f'<Rating {self.artist} - {self.album} [{self.rating}]>'
