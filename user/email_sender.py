import requests
import os
from dotenv import load_dotenv
load_dotenv()


def send_email(subject, message, sender, *recipients):

	X_RAPID_API_KEY = os.environ.get('X_RAPID_API_KEY')

	url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

	payload = {
		"personalizations": [
			{
				"to": [{"email": f"{email}"} for email in recipients],
				"subject": f"{subject}"
			}
		],
		"from": {"email": f"{sender}"},
		"content": [
			{
				"type": "text/plain",
				"value": f"{message}"
			}
		]
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": X_RAPID_API_KEY,
		"X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
	}

	response = requests.request("POST", url, json=payload, headers=headers)

	print(response.text)
	print(f"SENT EMAIL to {recipients}")


if __name__ == '__main__':
	send_email('Subject', 'Body of email', 'sender@gmail.com', 'recipient@gmail.com')
