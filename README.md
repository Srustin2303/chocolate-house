
Chocolate House Application

This is a simple Flask application for managing a fictional chocolate house. It uses SQLite to manage seasonal flavors, ingredients, and customer feedback.

Features
- Manage seasonal flavor offerings
- Track ingredient inventory
- Collect customer suggestions and allergy concerns


Prerequisite
- Python 3.x
- Docker (optional)

Installation
1. Clone the repository:
git clone https://github.com/Srustin2303/chocolate_house.git cd chocolate_house
2. Install dependencies:
pip install -r requirements.txt



Running the Application

To start the application, run:
python app.py


Then, open your web browser and go to http://127.0.0.1:5000/

Using Docker

If you want to run the application using Docker, follow these steps:

1. Build the Docker image:
docker build -t chocolate_house .
2. Run the Docker container:
docker run -p 5000:5000 chocolate_house

Testing the Application

1. Go to the home page to add seasonal flavors
2. Check the inventory page to manage ingredients
3. View customer suggestions on the suggestions page

Acknowledgments
This assessment was provided by L7 Informatics
