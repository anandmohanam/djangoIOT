
---

# Django IoT Project

This project involves building an IoT application using Django, ESP8266, and Firebase. The application monitors sensor data (temperature and humidity) and displays it in a user-friendly interface with responsive design elements.

## Features

- **Sensor Data Monitoring**: Automatically load and display temperature and humidity data from the database.
- **Gauge Meters**: Visual representation of sensor data using responsive gauge meters in card-style containers with a glass effect.
- **Scheduler**: Automatically processes temperature and humidity data every 3 minutes.
- **User Authentication**: Customized login form with fields for name, contact, and email.
- **Navigation Bar**: Easy navigation with links to Home, Graph, Notify, and Contact pages.
- **Noyify By Email**: Easy message by email set-up.

## Technology Stack

- **Django**: Backend framework for managing the IoT application.
- **ESP8266 (NodeMCU)**: Microcontroller for reading sensor data (temperature and humidity) using DHT11.
- **Firebase**: Realtime database to store and retrieve sensor data.
- **Bootstrap**: Frontend framework for responsive design and styling.

## Project Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/anandmohanam/django_IOT.git
   cd django-iot-project
   
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the root directory with the following content:
     ```env
     RECIPIENT_EMAIL='your personal mail'
     E_MAIL=django_sending_mail_id
     PASSWORD=django_sending_mail_password
     
     FIREBASE_DB_URL=https://your-firebase-database-url.firebaseio.com/
     ```

5. **Apply Migrations**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
6.**Create Account Firebase**:
   - create serviceAccountKey.json or save from firebase project setup
   - set Real-Time Database new rules.
   ```bash
{
  "rules": {
    ".read": "true",   //Change us per your need
    ".write": "true" 
  }
}
   ```

7.**Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

8.**Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:8000/`.

9.**Access Arduino Application**:
   - modify wifi name and password
   -  database_url and api key
   - flash nodemcu.INO file .
   - power on esp8266



**## Usage**

- **contact form**: Use the custom login form with name, contact, and email fields.
- **View Sensor Data**: Access real-time temperature and humidity data on the dashboard.
- **Navigation**: Use the navigation bar to explore different sections like Home, Graph, Notify,Contact, Circuit diagram.

**## Contributing**

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

**## License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

**## Image**

Diagram([image](static/image/node.jpg))

**IMPORTANT**

"This project only works in desktop mode (not in mobile view) due to time limitations. I have not written code for responsiveness, i.e., media queries."
---

