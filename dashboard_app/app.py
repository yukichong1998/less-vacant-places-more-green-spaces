import sys
from dashboard_app import dashboard

def run():
    app = dashboard.app
    app.run_server(debug = False, port = 8053)