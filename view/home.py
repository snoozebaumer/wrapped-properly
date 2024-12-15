from nicegui import ui
from nicegui.events import MultiUploadEventArguments

from service.spotify_history_analyzer import SpotifyHistoryAnalyzer


def build_home_page(analyzer: SpotifyHistoryAnalyzer):
    def handle_upload(e: MultiUploadEventArguments):
        # Clear previous analysis
        analyzer.clear()

        for index, name in enumerate(e.names):
            try:
                file_content = e.contents[index].read().decode()
                items_count = analyzer.process_file(name, file_content)

                ui.notify(f"Processed file {name} with {items_count} streams")

            except Exception as exc:
                ui.notify(f'Error processing {name}: {str(exc)}', type='negative')
                return

        ui.navigate.to('/results')

    def page():
        with ui.column():
            ui.label("Upload Spotify Listening History").classes("text-lg font-bold")
            ui.upload(
                on_multi_upload=handle_upload,
                label="Upload JSON Files",
                multiple=True
            )
    return page