from dataclasses import dataclass
from typing import List

from models.date_range import DateRange


@dataclass(frozen=True)
class Summary:
    total_streams: int
    total_playtime_hours: float
    unique_artists: int
    unique_songs: int
    processed_files: List[str]
    date_range: DateRange

    @classmethod
    def from_source(cls, total_streams, total_playtime_minutes, artist_streams, song_streams, processed_files, date_range):
        return cls(
            total_streams=total_streams,
            total_playtime_hours=round(total_playtime_minutes / 60, 2),
            unique_artists=len(artist_streams),
            unique_songs=len(song_streams),
            processed_files=processed_files,
            date_range=date_range
        )
