import re as regex

import requests

from notification import settings


def send_email(api: bool = False, smtp: bool = False, **kwargs) -> bool:
    subject = kwargs.get('subject')
    message = kwargs.get('message')
    from_email = kwargs.get('from_email')
    recipients = kwargs.get('recipients')
    attachments = kwargs.get('attachments')
    html_message = kwargs.get('html')

    pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    checker = regex.compile(pattern)

    valid_recipients = [email for email in recipients if checker.fullmatch(email)]
    try:
        if all(valid_recipients):
            response = requests.post(
                settings.MAILGUN_EMAIL_API,
                auth=('api', settings.MAILGUN_EMAIL_API),
                files=attachments,
                data={
                    'from': from_email,
                    'to': valid_recipients,
                    'subject': subject,
                    'text': message,
                    'html': html_message
                }
            )
            return response.json()
    except ConnectionError:
        raise
