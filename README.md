Movie Management Application
This is a Flask-based web application for managing a personal movie collection. The application allows users to add movies from the TMDb database, edit movie details, and delete movies from their collection. The movies are stored in a SQLite database, and the application uses Flask-Bootstrap for styling and Flask-WTF for form handling.

Features
Add Movies: Search for movies using the TMDb API and add them to your collection.
Edit Movies: Update the rating and review for any movie in your collection.
Delete Movies: Remove movies from your collection.
Rank Movies: Movies are ranked based on their rating, with the highest-rated movies appearing first.
Installation
Prerequisites
Python 3.x
Flask
Flask-Bootstrap
Flask-SQLAlchemy
Flask-WTF
Requests
Installing Required Packages
First, ensure that you have all the required packages installed. You can install them using the requirements.txt file.

For Windows:

bash
Copy code
python -m pip install -r requirements.txt
For MacOS:

bash
Copy code
pip3 install -r requirements.txt
Database Setup
The application uses SQLite as the database. The database will be automatically created and populated with data when you run the application for the first time.

Usage
Running the Application
To run the application, navigate to the project directory and execute the following command:

bash
Copy code
python app.py
The application will be accessible at http://127.0.0.1:5001/ by default.

Application Routes
Home (/): Displays all the movies in your collection, sorted by their ranking.
Edit Movie (/edit?id=<movie_id>&title=<movie_title>): Edit the rating and review for a specific movie.
Delete Movie (/delete?id=<movie_id>): Delete a movie from your collection.
Add Movie (/add): Search for movies by title and add them to your collection.
Movie Details (/movie?movie_id=<movie_id>): Get details for a specific movie from TMDb and add it to your collection.
Project Structure
app.py: The main Flask application file.
templates/: Directory containing HTML templates for rendering different pages.
index.html: Home page template displaying the list of movies.
edit.html: Template for editing movie details.
add.html: Template for adding new movies.
select.html: Template for selecting a movie from search results.
static/: Directory for static files like CSS and JavaScript.
my-movie-store.db: SQLite database file (created automatically).
