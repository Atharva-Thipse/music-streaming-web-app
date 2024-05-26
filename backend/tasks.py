import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import sqlite3
from celery_config import celery

"""
Function to send an email.

Args:
    - to_email (str): The recipient's email address.
    - html_content (str): The HTML content of the email.
    - subject (str): The subject of the email.

Returns:
    - None
"""
def send_email(to_email,html_content,subject):
    # Set the sender's email address
    from_email = "21f3002319@ds.study.iitm.ac.in"

    # Create a MIME message
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the HTML content to the message
    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    # Set the SMTP server and port
    smtp_server = 'localhost'
    smtp_port = 1025

    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.send_message(msg)

@celery.task
def update_visited():
    # Connect to SQLite database
    db_path = os.path.abspath('../music_streaming_application.db')
    connect_db = sqlite3.connect(db_path)
    cursor = connect_db.cursor()

    # Update visited to 0 for records where type is not equal to 'admin'
    cursor.execute('UPDATE account SET visited = 0 WHERE type != ?', ('admin',))
    connect_db.commit()

    # Close database connection
    connect_db.close()

@celery.task
def generate_monthly_report():
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year

    db_path = os.path.abspath('../music_streaming_application.db')
    connect_db = sqlite3.connect(db_path)
    cursor = connect_db.cursor()

    cursor.execute("SELECT * FROM account WHERE type='creator'")
    users = cursor.fetchall()

    subject = "Monthly Activity Report"

    # Loop through each creator
    for user in users:
        # Fetch the total number of songs uploaded by the creator
        cursor.execute('SELECT COUNT(*) AS total_songs FROM songs where owner = ?',(user[0],))
        total_songs = cursor.fetchone()[0]

        # Fetch the average rating of the creator's songs
        cursor.execute('SELECT AVG(avg_rating) AS average_rating FROM songs WHERE owner = ?', (user[0],))
        average_rating = cursor.fetchone()[0]

        # Fetch the total number of albums created by the creator
        cursor.execute('SELECT COUNT(*) FROM album WHERE username = ?', (user[0],))
        total_albums = cursor.fetchone()[0]

        # Fetch the top 3 songs of the month by rating
        cursor.execute('SELECT song_name, avg_rating FROM songs WHERE owner = ? ORDER BY avg_rating DESC LIMIT 3', (user[0],))
        data = cursor.fetchall()

        # Extract labels (song names) and values (average ratings) from the data
        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Activity Report</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Monthly Report - {current_month}, {current_year}</h1>
            <p>This is your summary for the month of {current_month}:</p>
            <div class="card m-3" style="height: 14rem;">
                <div class="d-flex flex-nowrap">
                    <div class="card m-4 ms-auto" style="width: 19rem; height: 11rem;">
                        <div class="card-body" align="center">
                            <h5>Total Songs Uploaded</h5><br>
                            <h1>{total_songs}</h1>
                        </div>
                    </div>
                    <div class="card m-4 mx-auto" style="width: 19rem; height: 11rem;">
                        <div class="card-body" align="center">
                            <h5>Average Rating</h5><br>
                            <h1>{average_rating}</h1>
                        </div>
                    </div>
                    <div class="card m-4 me-auto" style="width: 19rem; height: 11rem;">
                        <div class="card-body" align="center">
                            <h5>Total Albums</h5><br>
                            <h1>{total_albums}</h1>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <div class="card" style="height: 25rem;">
                        <div class="card-body">
                            <h3 class="card-title">Your Top 3 Songs of the Month {current_month}, {current_year} By Rating</h3>
                            <canvas id="top3SongsByAvgRatings" width="1050" style="max-height: 325px;"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            <script>
                const labels = {json.dumps(labels)};
                const values = {json.dumps(values)};
                const ctx = document.getElementById('top3SongsByAvgRatings').getContext('2d');

                new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: labels,
                        datasets: [{{
                            label: 'Average Rating',
                            data: values,
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        '''
        send_email(user[4],html_content,subject)
    
    connect_db.close()

@celery.task
def generate_daily_report():
    db_path = os.path.abspath('../music_streaming_application.db')
    connect_db = sqlite3.connect(db_path)
    cursor = connect_db.cursor()

    # Fetch users who have not visited the app
    cursor.execute("SELECT * FROM account WHERE visited=0")
    users = cursor.fetchall()

    connect_db.close()

    subject = "Come Back & Listen to Your Favourite Songs & Albums"

    # Iterate over users and send reminder emails
    for user in users:
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Daily Reminder</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
        </head>
        <body>
            <h1>Come and Visit Us</h1>
            <p>Log In to Our Website and Listen to you Favourite Songs, Albums & Artists</p>
            <button class="btn btn-success"><a class="text-decoration-none text-light" href="http://localhost:8081/login">Login</a></button>
        </body>
        </html>
        '''
        send_email(user[4],html_content,subject)