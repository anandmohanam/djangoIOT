import schedule
import time
from django.core.management.base import BaseCommand
from firebase_admin import credentials, db
from esp.models import SensorData
from dotenv import load_dotenv
import os
import django

class Command(BaseCommand):
    help = 'Fetch sensor data and save to database every 3 minutes'

    def handle(self, *args, **options):
        load_dotenv()
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
        django.setup()

        database_url = os.getenv('DATABASE_URL')
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })

        def fetch_and_save_data():
            try:
                ref = db.reference('/')
                temp_c_path = 'sensor/temperature_C'
                temp_f_path = 'sensor/temperature_F'
                humi_path = 'sensor/humi'

                temperature_C = ref.child(temp_c_path).get()
                temperature_F = ref.child(temp_f_path).get()
                humi = ref.child(humi_path).get()

                print("Temperature in Celsius:", temperature_C)
                print("Temperature in Fahrenheit:", temperature_F)
                print("Humidity:", humi)

                temperature_C = int(temperature_C) if temperature_C is not None else 0
                temperature_F = int(temperature_F) if temperature_F is not None else 0
                humi = int(humi) if humi is not None else 0

                sensor_data = SensorData(temperature_C=temperature_C, humidity=humi)
                sensor_data.save()

                print("Data saved successfully")

            except Exception as e:
                print(f"Error: {e}")

        schedule.every(3).minutes.do(fetch_and_save_data)

        print("Scheduler started...")

        while True:
            schedule.run_pending()
            time.sleep(1)
