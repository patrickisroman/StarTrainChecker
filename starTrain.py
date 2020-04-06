import requests
import time
import smtplib
import ssl

from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Notification data
NOTIFICATION_EMAIL = 'your_email@example.com'
AVAILABLE_MAP = {}

# Request data
STAR_TRAIN_URL = 'https://nnry.com/pages/StarTrain.php'
REFRESH_RATE_SEC = 60 # once per minute

# Email Sending
SMTP_SERVER = 'smtp.example.com' # ex: 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_EMAIL = 'email_sender@example.com'
SMTP_PASS = 'email_sender_password'

def send_email(email_to=NOTIFICATION_EMAIL, email_from='alert@star_train_finder.com', email_subject="New Star Train Availability!", email_content=''):
	msg = MIMEText(email_content)
	msg['Subject'] = email_subject
	msg['From'] = email_from
	msg['To'] = email_to

	with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
		server.login(SMTP_EMAIL, SMTP_PASS)
		server.sendmail(email_from, email_to, msg.as_string())
		server.quit()

# Script
while True:
	response = requests.get(STAR_TRAIN_URL)

	if response.status_code != 200:
		exit(0)

	parser = BeautifulSoup(response.text, features="lxml")

	open_list = []
	for div in parser.find_all('div', class_='mini-calendar'):
		for child_div in div.findChildren():
			if child_div.has_attr('class') and child_div['class'][0] != 'sold-out':
				date = child_div.text.strip()

				if date not in AVAILABLE_MAP:
					AVAILABLE_MAP[date] = True
					open_list.append(date)

	if len(open_list) > 0:
		send_email(email_content='\n'.join(open_list))

	time.sleep(REFRESH_RATE_SEC)
