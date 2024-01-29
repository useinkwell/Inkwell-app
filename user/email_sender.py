import requests
import os
from dotenv import load_dotenv
load_dotenv()

import resend

resend.api_key = "re_Q11JVdGL_2h6DWiCDRjB3Gac1ZNoKJUSX"

def send_email(subject, message, sender, *recipients):

	RESEND_API_KEY = os.environ.get('X_RAPID_API_KEY')


	r = resend.Emails.send({
	"from": sender,
	"to": recipients,
	"subject": subject,
	"text": message
	})

	print(r)


if __name__ == '__main__':
	send_email('Subject', 'Body of email', 'sender@gmail.com', 'recipient@gmail.com')

