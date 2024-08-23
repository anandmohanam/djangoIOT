import os
import schedule
import time
import django
from dotenv import load_dotenv
from firebase_admin import credentials, db
from esp.models import SensorData  # Adjust to match your app name

# Load environment variables from .env file
load_dotenv()

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')  # Use 'base.settings' without .py
django.setup()

# Initialize Firebase
database_url = os.getenv('DATABASE_URL')
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': database_url
})

def fetch_and_save_data():
    try:
        # Reference to your Firebase Realtime Database
        ref = db.reference('/')

        # Define the paths
        temp_c_path = 'sensor/temperature_C'
        temp_f_path = 'sensor/temperature_F'
        humi_path = 'sensor/humi'

        # Read the data from each path
        temperature_C = ref.child(temp_c_path).get()
        temperature_F = ref.child(temp_f_path).get()
        humi = ref.child(humi_path).get()

        # Print the values to the console for debugging
        print("Temperature in Celsius:", temperature_C)
        print("Temperature in Fahrenheit:", temperature_F)
        print("Humidity:", humi)

        # Convert data to integers or floats and handle potential None values
        temperature_C = int(temperature_C) if temperature_C is not None else 0
        temperature_F = int(temperature_F) if temperature_F is not None else 0
        humi = int(humi) if humi is not None else 0

        # Save to the database
        sensor_data = SensorData(temperature_C=temperature_C, humidity=humi)
        sensor_data.save()

        print("Data saved successfully")

    except Exception as e:
        # Handle errors and provide feedback
        print(f"Error: {e}")

# Schedule the job every 3 minutes
schedule.every(3).minutes.do(fetch_and_save_data)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(1)
