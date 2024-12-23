import json
from collections import Counter
from datetime import datetime

from models.date_range import DateRange
from models.summary import Summary
from service.json_utils import get_spotify_artist_name, get_spotify_track_name, get_spotify_ms_played, \
    get_spotify_timestamp


class SpotifyHistoryAnalyzer:
    def __init__(self):
        # Counters for tracking
        self.artist_streams = Counter()
        self.song_streams = Counter()
        self.artist_total_playtime = Counter()
        self.song_total_playtime = Counter()

        # additional tracking
        self.total_streams = 0
        self.total_playtime_minutes = 0
        self.processed_files = []
        self.date_range = DateRange()

    def process_file(self, filename: str, file_content: str):
        try:
            data = json.loads(file_content)

            if isinstance(data, dict):
                data = [data]

            for record in data:
                artist = get_spotify_artist_name(record)
                song = f'{get_spotify_track_name(record)} - {artist}'
                ms_played = get_spotify_ms_played(record)
                timestamp = get_spotify_timestamp(record)

                if artist and song:
                    self.artist_streams[artist] += 1
                    self.song_streams[song] += 1

                    self.artist_total_playtime[artist] += ms_played
                    self.song_total_playtime[song] += ms_played
                    self.total_playtime_minutes += ms_played / 60000  # convert to minutes

                    self.total_streams += 1

                if timestamp:
                    try:
                        parsed_ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        self._check_if_new_earliest_date(parsed_ts)
                        self._check_if_new_latest_date(parsed_ts)
                    except ValueError:
                        pass

            self.processed_files.append(filename)

            return len(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decode error in {filename}: {str(e)}")

    def _check_if_new_earliest_date(self, parsed_ts):
        if (not self.date_range.earliest) or (parsed_ts < self.date_range.earliest):
            self.date_range.earliest = parsed_ts

    def _check_if_new_latest_date(self, parsed_ts):
        if (not self.date_range.latest) or (parsed_ts > self.date_range.latest):
            self.date_range.latest = parsed_ts

    def get_top_artists(self, n=10):
        return self.artist_streams.most_common(n)

    def get_top_songs(self, n=10):
        return self.song_streams.most_common(n)

    def get_artist_playtime(self, n=10):
        milliseconds_in_an_hour = 3600000
        return [(artist, round(playtime / milliseconds_in_an_hour, 1))
                for artist, playtime in self.artist_total_playtime.most_common(n)]

    def get_song_playtime(self, n=10):
        milliseconds_in_an_hour = 3600000
        return [(song, round(playtime / milliseconds_in_an_hour, 1))
                for song, playtime in self.song_total_playtime.most_common(n)]

    def get_summary(self):
        return Summary.from_source(
            total_streams=self.total_streams,
            total_playtime_minutes=self.total_playtime_minutes,
            artist_streams=self.artist_streams,
            song_streams=self.song_streams,
            processed_files=self.processed_files,
            date_range=self.date_range)

    def clear(self):
        self.artist_streams.clear()
        self.song_streams.clear()
        self.artist_total_playtime.clear()
        self.total_streams = 0
        self.total_playtime_minutes = 0
        self.processed_files.clear()
        self.date_range = DateRange()