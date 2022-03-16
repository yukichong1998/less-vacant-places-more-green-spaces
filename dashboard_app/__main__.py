from dashboard_app import dashboard
from dashboard_app.data_prep import compute_health_score, data_cleaning, data_extraction

if __name__ == '__main__':
    app = dashboard.app
    app.run_server(debug = False, port = 8053)