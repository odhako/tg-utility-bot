class Settings:
    schedule_active = False

    def __init__(self):
        pass

    def start_schedule(self):
        self.schedule_active = True

    def stop_schedule(self):
        self.schedule_active = False


settings = Settings()
