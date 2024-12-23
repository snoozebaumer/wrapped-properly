def get_spotify_track_name(dict_record):
    """gets the track name from dict representation of one spotify stream

    key name depends on data that was uploaded:
     - Extended Streaming History: master_metadata_track_name
     - Account Data (only has streaming data for the last year): trackName"""
    return dict_record.get("master_metadata_track_name") or dict_record.get("trackName")

def get_spotify_artist_name(dict_record):
    """gets the artist name from dict representation of one spotify stream

    key name depends on data that was uploaded:
     - Extended Streaming History: master_metadata_album_artist_name
     - Account Data (only has streaming data for the last year): artistName"""
    return dict_record.get('master_metadata_album_artist_name') or dict_record.get('artistName')

def get_spotify_ms_played(dict_record):
    """gets the time played in milliseconds from dict representation of one spotify stream

    key name depends on data that was uploaded:
     - Extended Streaming History: ms_played
     - Account Data (only has streaming data for the last year): msPlayed"""
    return dict_record.get('ms_played') or dict_record.get('msPlayed', 0)

def get_spotify_timestamp(dict_record):
    """gets the timestamp (when the user streamed the song) from dict representation of one spotify stream

    key name depends on data that was uploaded:
     - Extended Streaming History: ts
     - Account Data (only has streaming data for the last year): endTime"""
    return dict_record.get('ts') or dict_record.get('endTime')