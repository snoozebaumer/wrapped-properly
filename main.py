from fastapi import FastAPI
from nicegui import ui

from service.spotify_history_analyzer import SpotifyHistoryAnalyzer
from view.analysis_results import build_analysis_results_page
from view.home import build_home_page

app = FastAPI()


# Global analyzer instance
analyzer = SpotifyHistoryAnalyzer()


@ui.page("/")
def home_page():
    return build_home_page(analyzer)()

@ui.page("/results")
def results_page():
    return build_analysis_results_page(analyzer)()


ui.run(host="0.0.0.0", port=8000)