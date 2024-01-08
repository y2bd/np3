from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from itertools import groupby


class Rating(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    album: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    artist: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    rating: so.Mapped[int] = so.mapped_column(sa.Integer)
    album_art_url: so.Mapped[Optional[str]] = so.mapped_column(
        sa.VARCHAR(), nullable=True
    )
    review: so.Mapped[Optional[str]] = so.mapped_column(sa.VARCHAR(), nullable=True)

    def __repr__(self):
        return f"<Rating {self.artist} - {self.album} [{self.rating}]>"


def get_latest_ratings(order_by, limit=1000):
    if order_by == "artist":
        ratings = (
            db.session.execute(
                db.select(Rating).order_by(Rating.artist.asc()).limit(limit)
            )
            .scalars()
            .all()
        )

        return groupby(ratings, lambda r: r.artist[0].upper())
    elif order_by == "album":
        ratings = (
            db.session.execute(
                db.select(Rating).order_by(Rating.album.asc()).limit(limit)
            )
            .scalars()
            .all()
        )

        return groupby(ratings, lambda r: r.album[0].upper())
    elif order_by == "rating":
        ratings = (
            db.session.execute(
                db.select(Rating).order_by(Rating.rating.desc()).limit(limit)
            )
            .scalars()
            .all()
        )

        return groupby(ratings, lambda r: r.rating)
    else:
        ratings = (
            db.session.execute(
                db.select(Rating).order_by(Rating.timestamp.desc()).limit(limit)
            )
            .scalars()
            .all()
        )

        # return grouped by year and month
        return groupby(ratings, lambda r: r.timestamp.strftime("%b %Y"))


def store_latest_ratings(page_limit=8, page_sleep=2, user="y2bd"):
    from lib import rym
    from time import sleep

    for page in range(1, page_limit):
        ratings = rym.get_ratings_from_page(page, user)
        for rating in ratings:
            existing_rating = db.session.execute(
                db.select(Rating).filter_by(
                    artist=rating["artist"], album=rating["album"]
                )
            ).scalar_one_or_none()
            if existing_rating:
                print("found an existing rating", existing_rating)
                # We've already stored this rating, so we're done

                db.session.commit()
                return
            else:
                new_rating = Rating(
                    timestamp=rating["timestamp"],
                    album=rating["album"],
                    artist=rating["artist"],
                    rating=rating["rating"],
                    album_art_url=rating["album_art_url"],
                    review=rating["review"],
                )
                db.session.add(new_rating)
                print("added new rating", new_rating)
        db.session.commit()
        print("finished page", page)
        sleep(page_sleep)


def backfill_album_art(art_sleep=0.5, user="y2bd"):
    from lib import lastfm
    from time import sleep

    ratings = db.session.execute(
        db.select(Rating)
        .filter((Rating.album_art_url == None) | (Rating.album_art_url == ""))
        .order_by(Rating.artist.asc())
    ).scalars()

    for rating in ratings:
        if rating.album_art_url:
            continue

        rating.album_art_url = lastfm.get_album_art_url(rating.artist, rating.album)
        sleep(art_sleep)

    db.session.commit()
