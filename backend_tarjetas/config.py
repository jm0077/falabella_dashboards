import os

DB_USER = os.environ.get('DB_USER', 'jm_07')
DB_PASS = os.environ.get('DB_PASS', '12345')
DB_NAME = os.environ.get('DB_NAME', 'dashboard_db')
CLOUD_SQL_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME', 'custom-curve-431820-e9:southamerica-west1:my-mysql-instance')

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@/{DB_NAME}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key_here')