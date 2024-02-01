import requests
import os
from django.core.mail import send_mail


def send_email(subject, body, sender, recipient):
	send_mail(subject, body, sender, [recipient])

	print("Email sent successfully!")

	return True


if __name__ == '__main__':
	r = send_email('Subject', 'Body of email', 'techygeekr@gmail.com', 'jaminonuegbu@gmail.com')
	print("done")
	print(r)
