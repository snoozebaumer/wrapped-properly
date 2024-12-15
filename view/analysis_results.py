from nicegui import ui

from service.spotify_history_analyzer import SpotifyHistoryAnalyzer


def build_analysis_results_page(analyzer: SpotifyHistoryAnalyzer):
    def page():
        summary = analyzer.get_summary()
        if summary.get('total_streams') == 0:
            ui.navigate.to('/')
            return

        with ui.column().classes("w-full"):
            # Display overall summary
            ui.label("Spotify Listening History").classes("text-2xl font-bold")

            # Stats row
            with ui.row().classes("w-full justify-between"):
                ui.label(f'Total Streams\t{summary["total_streams"]}')
                ui.label(f'Total Listening Time\t{summary["total_playtime_hours"]} hours')
                ui.label(f'Unique Artists\t{summary["unique_artists"]}')

            # Date Range
            if summary['date_range']['earliest'] and summary['date_range']['latest']:
                ui.label(
                    f"Listening Period: {summary['date_range']['earliest'].date()} to {summary['date_range']['latest'].date()}").classes(
                    "text-sm text-gray-500")

            # Top Artists by Streams
            with ui.card().classes("w-full mt-4"):
                ui.label("Top Artists (by Streams)").classes("text-xl font-bold")
                top_artists = analyzer.get_top_artists(10)
                for rank, (artist, count) in enumerate(top_artists, 1):
                    with ui.row().classes("w-full items-center"):
                        ui.label(f"{rank}. {artist}").classes("flex-grow")
                        ui.badge(f'{count} streams', color="primary")

            # Top Artists by Listening Time
            with ui.card().classes("w-full mt-4"):
                ui.label("Top Artists (by Listening Time)").classes("text-xl font-bold")
                top_artists_time = analyzer.get_artist_playtime(10)
                for rank, (artist, hours) in enumerate(top_artists_time, 1):
                    with ui.row().classes("w-full items-center"):
                        ui.label(f"{rank}. {artist}").classes("flex-grow")
                        ui.badge(f"{hours} h", color="secondary")

            # Top Songs Section
            with ui.card().classes("w-full mt-4"):
                ui.label("Top Songs").classes("text-xl font-bold")
                top_songs = analyzer.get_top_songs(10)
                for rank, (song, count) in enumerate(top_songs, 1):
                    with ui.row().classes("w-full items-center"):
                        ui.label(f"{rank}. {song}").classes("flex-grow")
                        ui.badge(f'{count} streams', color="accent")

            # Processed Files
            with ui.expansion("Processed Files").classes("w-full mt-4"):
                for file in summary['processed_files']:
                    ui.label(file)

            # Reset button
            ui.button("Analyze Another Dataset", on_click=lambda: ui.navigate.to("/"))
    return page