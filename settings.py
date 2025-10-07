import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


class Settings:
    schedule_active = False

    api_id = int(os.environ.get('api_id'))
    api_hash = os.environ.get('api_hash')
    bot_token = os.environ.get('bot_token')

    admin = int(os.environ.get('admin'))
    public_from = int(os.environ.get('public_from'))
    public_to = int(os.environ.get('public_to'))

    database_file = os.environ.get('database_file')

    def start_schedule(self):
        self.schedule_active = True

    def stop_schedule(self):
        self.schedule_active = False


settings = Settings()
