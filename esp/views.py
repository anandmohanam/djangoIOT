import os
from django.http import HttpResponse
from django.core.serializers import serialize
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from .models import SensorData, ContactForm, Notify
from django.conf import settings

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment variable
database_url = os.getenv('DATABASE_URL')

# Path to your service account key file
cred = credentials.Certificate("./serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': database_url
})

# Define a view to render the data
def sensor(request):
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

    temperature_C=int(temperature_C)
    temperature_F = int(temperature_F)
    humi=int(humi)

    Sensor = SensorData(temperature_C=temperature_C, humidity=humi)
    Sensor.save()

    # Pass the data to the template context
    context = {
        'temperature_C': temperature_C,
        'temperature_F': temperature_F,
        'humi': humi
    }

    # Render the data in the HTML template
    return render(request, 'sensor_data.html', context)


def graph(request):
    # Get all sensor data entries ordered by timestamp
    all_data = SensorData.objects.all().order_by('timestamp')

    # Convert queryset to JSON
    data = serialize('json', all_data, fields=('timestamp', 'temperature_C', 'humidity'))

    # Pass the JSON data to the template
    return render(request, 'graph.html', {'data': data})


def notify(request):
    # Reference to the 'notify/' path in Firebase
    ref = db.reference('/notify')
    ref.set(True)  # Update directly if there's no specific sub-path

    # Get or create the Notify instance (assuming there's only one)
    notify_instance, created = Notify.objects.get_or_create(id=1)

    # Increment the counter
    notify_instance.counter += 1

    # Save the updated instance
    notify_instance.save()

    return redirect('sensor')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        message = request.POST.get('message')

        # Save to the database
        ContactForm.objects.create(name=name, email=email, contact=contact, message=message)
        subject = f"Contact Form Submission from {name}"
        email_message = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Contact: {contact}\n\n"
            f"Message:\n{message}"
        )
        recipient_list = [settings.RECIPIENT_EMAIL]  # Use recipient email from settings

        # Send the email
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list
        )

        return redirect('contact')  # Redirect to the same page or another page

    return render(request, 'contact.html')


def diagram(request):
    return render(request, 'diagram.html')