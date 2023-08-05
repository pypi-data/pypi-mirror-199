import logging
from typing import List, Tuple, Dict

import requests

from notification import settings

logger = logging.getLogger(__file__)


def _prep_recipient(recipients):
    try:
        if isinstance(recipients, str):
            return [{'email_address': {'address': x}} for x in recipients.split(',; ', maxsplit=-1)]
        elif isinstance(recipients, (List, Tuple)):
            return [{'email_address': {'address': x, 'name': y}} for x, y in recipients]
    except (ValueError, KeyError):
        raise ValueError('Invalid email address or data provided')


def send_email(
        source: str,
        subject: str,
        *,
        tos: List | Tuple | str,
        ccs: List | Tuple | str = None,
        bccs: List | Tuple | str = None,
        replies: List | Tuple | str = None,
        data: Dict = None,
        text: str = None,
        template: bool | str = False,
        config: Dict = None,
):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": config.get('token')
    }
    response = None
    if template or template == 'html':
        response = requests.post(
            settings.ZEPTO_EMAIL_API,
            headers=headers,
            json={
                'subject': subject,
                'template_key': config.get('template'),
                'bounce_address': config.get('bounce_address'),
                'from': {
                    'address': source,
                    'name': config.get('sender')
                },
                'to': _prep_recipient(tos),
                'cc': _prep_recipient(ccs),
                'bcc': _prep_recipient(bccs),
                'reply_to': _prep_recipient(replies),
                'client_reference': None,
                'merge_info': data
            }
        )
    else:
        response = requests.post(
            settings.ZEPTO_EMAIL_API,
            headers=headers,
            json={
                'bounce_address': config.get('bounce_address'),
                'from': {
                    'address': source,
                    'name': config.get('sender')
                },
                'to': _prep_recipient(tos),
                'cc': _prep_recipient(ccs),
                'bcc': _prep_recipient(bccs),
                'reply_to': _prep_recipient(replies),
                'subject': subject,
                'htmlbody': text
            }
        )
    if response and response.status_code >= 400:
        logger.log(logging.WARNING, response.json())
    else:
        return response.json()
