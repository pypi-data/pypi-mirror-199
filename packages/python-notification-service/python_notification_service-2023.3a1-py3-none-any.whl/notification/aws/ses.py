import json
import logging
import re
from typing import List, Tuple, Union, Sequence

import boto3
import email_validator
from botocore.exceptions import ClientError

from notification import settings

#

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Simple Email Service
(Amazon SES) to manage email templates that contain replaceable tags.
"""

# Defines template tags, which are enclosed in two curly braces, such as {{tag}}.
TEMPLATE_REGEX = r'(?<={{).+?(?=}})'

logger = logging.getLogger(__name__)


class SesTemplate:
    """Encapsulates Amazon SES template functions. Class definition was adapted from AWS example code.
    See https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/ses/ses_templates.py"""

    __slots__ = ('_tags', '_template', 'client')

    def __init__(self, *, name, subject, text, html):
        self.client = boto3.client('ses')
        self._tags = set()

        try:
            template = {
                'TemplateName': name,
                'SubjectPart': subject,
                'TextPart': text,
                'HtmlPart': html}
            self.client.create_template(Template=template)
            self._template = template
            self._tags = set(re.findall(TEMPLATE_REGEX, subject + text + html))
        except ClientError:
            logger.exception("Couldn't create template %s.", name)
            raise

    def verify_tags(self, template_data: List):
        """
        Verifies that the tags in the template data are part of the template.

        :param template_data: Template data formed of key-value pairs of tags and
                              replacement text.
        :return: True when all the tags in the template data are usable with the
                 template; otherwise, False.
        """
        diff = set(template_data) - self._tags
        if diff:
            return False
        else:
            return True

    @property
    def template(self):
        return self._template if self._template is not None else None

    @template.setter
    def template(self, value):
        if isinstance(value, dict) and not {'TemplateName', 'SubjectPart', 'TextPart', 'HtmlPart'} - set(value.keys()):
            name = value.get('TemplateName')
            subject = value.get('SubjectPart')
            text = value.get('TextPart')
            html = value.get('HtmlPart')
            if isinstance(name, str) and isinstance(subject, str) and isinstance(text, str) and isinstance(html, str):
                if self.update_template(name=name, subject=subject, text=text, html=html):
                    self._template = value
                    self._tags = set(re.findall(TEMPLATE_REGEX, subject + text + html))
            else:
                raise ValueError('Invalid template parameters provided')

    @property
    def name(self):
        """
        :return: Gets the name of the template, if a template has been loaded.
        """
        return self.template['TemplateName'] if self.template is not None else None

    @property
    def subject(self):
        return self.template['SubjectPart'] if self.template is not None else None

    @property
    def text(self):
        return self.template['TextPart'] if self.template is not None else None

    def html(self):
        return self.template['HtmlPart'] if self.template is not None else None

    @property
    def tags(self):
        return self._tags

    def delete_template(self):
        """
        Deletes an email template.
        """
        try:
            self.client.delete_template(TemplateName=self.name)
            self._template = None
            self._tags = None
        except ClientError:
            logger.exception(
                "Couldn't delete template %s.", self.name)
            raise

    @classmethod
    def get_template(cls, name):
        """
        Gets a previously created email template.

        :param name: The name of the template to retrieve.
        :return: The retrieved email template.
        """
        try:
            response = cls.client.get_template(TemplateName=name)
        except ClientError:
            logger.exception("Couldn't get template %s.", name)
            raise
        else:
            return response['Template']

    @classmethod
    def list_templates(cls):
        """
        Gets a list of all email templates for the current account.

        :return: The list of retrieved email templates.
        """
        try:
            response = cls.client.list_templates()
            templates = response['TemplatesMetadata']
        except ClientError:
            logger.exception("Couldn't get templates.")
            raise
        else:
            return templates

    @classmethod
    def update_template(cls, *, name, subject, text, html):
        """
        Updates a previously created email template.

        :param name: The name of the template.
        :param subject: The subject of the email.
        :param text: The plain text version of the email.
        :param html: The HTML version of the email.
        """
        try:
            template = {
                'TemplateName': name,
                'SubjectPart': subject,
                'TextPart': text,
                'HtmlPart': html}
            cls.client.update_template(Template=template)
        except ClientError as err:
            logger.warning("Couldn't update template %s.\n%s", name, err.__traceback__)
            raise


# Manage email destination
class SesDestination:
    """Contains data about an email destination."""
    __slots__ = ('tos', 'ccs', 'bccs')

    def __init__(self, tos: Union[List[str], Tuple[str], str], ccs: Union[List[str], Tuple[str], str] = None,
                 bccs: Union[List[str], Tuple[str], str] = None):
        """
        :param tos: The list of recipients on the 'To:' line.
        :param ccs: The list of recipients on the 'CC:' line.
        :param bccs: The list of recipients on the 'BCC:' line.
        """

        def _prep(x: Sequence):
            sep = (',', ';', ' ',)
            if isinstance(x, (List, Tuple)):
                return [a for a in x if isinstance(a, str)]
            elif isinstance(x, str):
                return tos.split(',; ', -1) if any([a for a in x if a in sep]) else x

        self.tos = _prep(tos)
        self.ccs = _prep(ccs)
        self.bccs = _prep(bccs)

    def to_service_format(self):
        svc_format = {'ToAddresses': self.tos}
        if self.ccs is not None:
            svc_format['CcAddresses'] = self.ccs
        if self.bccs is not None:
            svc_format['BccAddresses'] = self.bccs
        return svc_format


class SesMailSender:
    """Encapsulates functions to send emails with Amazon SES."""

    def __init__(self):

        try:
            self.client = boto3.client('ses', region_name=settings.AWS_REGION,
                                       aws_access_key_id=settings.AWS_ACCESS_KEY,
                                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        except ClientError as err:
            logger.log(level=logging.WARNING, msg=err.__traceback__)

    def validate_email_identity(self, email: str):
        try:
            validation = email_validator.validate_email(email, check_deliverability=True)
            if validation.email:
                aws_check = self.client.verify_email_identity(EmailAddress=email)
                return aws_check

        except email_validator.EmailNotValidError as err:
            logger.log(level=logging.WARNING, msg=err.__traceback__)
        except Exception:
            raise

    def send_email(self, arn: str, source: str, destination: SesDestination, subject: str, text: str = None,
                   html: str = None,
                   reply_tos: List[str] = None, extra: dict = None):
        """
        Sends an email.

        Note: If your account is in the Amazon SES  sandbox, the source and
        destination email accounts must both be verified.
        :param arn: The unique ARN for the verified sender's email
        :param source: The source email account.
        :param destination: The destination email account.
        :param subject: The subject of the email.
        :param text: The plain text version of the body of the email.
        :param html: The HTML version of the body of the email.
        :param reply_tos: Email accounts that will receive a reply if the recipient
                          replies to the message.
        :param extra: Dictionary of key-value pair for sending email. Example, ConfigurationSetName for SES service
        :return: The ID of the message, assigned by Amazon SES.
        """
        char_set = 'UTF-8'
        if html and text:
            body = {
                'Text': {'Data': text, 'Charset': char_set},
                'Html': {'Data': html if html else '', 'Charset': char_set}
            }
        elif text and not html:
            body = {'Text': {'Data': text, 'Charset': char_set}}
        elif html and not text:
            body = {'Html': {'Data': html if html else '', 'Charset': char_set}}
        else:
            raise ValueError('Invalid message body')

        send_args = {
            'SourceArn': arn,
            'Source': source,
            'Destination': destination.to_service_format(),
            'Message': {
                'Subject': {'Data': subject, 'Charset': char_set},
                'Body': body
            }
        }
        if isinstance(reply_tos, list) and len(reply_tos) > 0:
            # validate reply_tos has valid emails
            emails = [x for x in reply_tos if email_validator.validate_email(x)]
            send_args['ReplyToAddresses'] = emails
        if extra:
            excluded = ['arn', 'source', 'destination', 'subject', 'text', 'html', 'reply_tos']
            extra = {x: y for x, y in extra.items() if x not in excluded}
            send_args.update(**extra)
        try:
            response = self.client.send_email(**send_args)
            message_id = response['MessageId']

        except ClientError:
            logger.exception(
                "Couldn't send mail from %s to %s.", source, destination.tos)
            raise
        else:
            return message_id

    def send_templated_email(
            self, arn, source, destination, template_name, template_data,
            reply_tos=None, extras: dict = None):
        """
        Sends an email based on a template. A template contains replaceable tags
        each enclosed in two curly braces, such as {{name}}. The template data passed
        in this function contains key-value pairs that define the values to insert
        in place of the template tags.

        Note: If your account is in the Amazon SES  sandbox, the source and
        destination email accounts must both be verified.

        :param arn: the AWS arn for the specified service by which messages are published.
        :param source: The source email account.
        :param destination: The destination email account.
        :param template_name: The name of a previously created template.
        :param template_data: JSON-formatted key-value pairs of replacement values
                              that are inserted in the template before it is sent.
        :param reply_tos: Email address to which a reply may be sent
        :param extras: Mapping of parameters and their corresponding values used to further customize
        broadcasting a message.
        :return: The ID of the message, assigned by Amazon SES.
        """
        send_args = {
            'Source': source,
            'Destination': destination.to_service_format(),
            'Template': template_name,
            'TemplateData': json.dumps(template_data),
            'SourceArn': arn
        }
        if reply_tos is not None:
            send_args['ReplyToAddresses'] = reply_tos
        try:
            send_args.update(**extras)
            response = self.client.send_templated_email(**send_args)
            message_id = response['MessageId']
            logger.info(
                "Sent templated mail %s from %s to %s.", message_id, source,
                destination.tos)
        except ClientError:
            logger.exception(
                "Couldn't send templated mail from %s to %s.", source, destination.tos)
            raise
        else:
            return message_id
