import json
from collections import Counter
from datetime import datetime


class SpotifyHistoryAnalyzer:
    def __init__(self):
        # Counters for tracking
        self.artist_streams = Counter()
        self.song_streams = Counter()
        self.artist_total_playtime = Counter()

        # Additional tracking
        self.total_streams = 0
        self.total_playtime_minutes = 0
        self.processed_files = []
        self.date_range = {
            'earliest': None,
            'latest': None
        }

    def process_file(self, filename: str, file_content: str):
        try:
            data = json.loads(file_content)

            if isinstance(data, dict):
                data = [data]

            for record in data:
                artist = record.get('master_metadata_album_artist_name')
                song = f'{record.get("master_metadata_track_name")} - {artist}'
                ms_played = record.get('ms_played', 0)
                timestamp = record.get('ts')

                if artist and song:
                    self.artist_streams[artist] += 1
                    self.song_streams[song] += 1

                    self.artist_total_playtime[artist] += ms_played
                    self.total_playtime_minutes += ms_played / 60000  # convert to minutes

                    self.total_streams += 1

                if timestamp:
                    try:
                        parsed_ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        if (not self.date_range['earliest']) or (parsed_ts < self.date_range['earliest']):
                            self.date_range['earliest'] = parsed_ts
                        if (not self.date_range['latest']) or (parsed_ts > self.date_range['latest']):
                            self.date_range['latest'] = parsed_ts
                    except ValueError:
                        pass

            self.processed_files.append(filename)

            return len(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decode error in {filename}: {str(e)}")

    def get_top_artists(self, n=10):
        return self.artist_streams.most_common(n)

    def get_top_songs(self, n=10):
        return self.song_streams.most_common(n)

    def get_artist_playtime(self, n=10):
        milliseconds_in_an_hour = 3600000
        return [(artist, round(playtime / milliseconds_in_an_hour, 1))
                for artist, playtime in self.artist_total_playtime.most_common(n)]

    def get_summary(self):
        return {
            'total_streams': self.total_streams,
            'total_playtime_hours': round(self.total_playtime_minutes / 60, 2),
            'unique_artists': len(self.artist_streams),
            'unique_songs': len(self.song_streams),
            'processed_files': self.processed_files,
            'date_range': self.date_range
        }

    def clear(self):
        self.artist_streams.clear()
        self.song_streams.clear()
        self.artist_total_playtime.clear()
        self.total_streams = 0
        self.total_playtime_minutes = 0
        self.processed_files.clear()
        self.date_range = {
            'earliest': None,
            'latest': None
        }