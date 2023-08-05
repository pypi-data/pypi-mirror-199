import json
import logging
import re as regex
from abc import ABC
from collections import namedtuple
from enum import Enum
from typing import TypeVar
from typing import Union, Dict, Any, List, Tuple
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError

from notification import settings

logger = logging.getLogger(__file__)

SubscriptionResource = TypeVar('SubscriptionResource')


class SnsProtocols(Enum):
    HTTP = ('http', 2)
    HTTPS = ('https', 3)
    EMAIL = ('email', 5)
    EMAIL_JSON = ('email-json', 7)
    SMS = ('sms', 11)
    SQS = ('sqs', 13)
    APPLICATION = ('application', 17)
    LAMBDA = ('lambda', 19)
    FIREHOSE = ('firehose', 23)


TopicAttributes = namedtuple(
    'TopicAttributes',
    (
        'DeliveryPolicy',
        'DisplayName',
        'Owner',
        'Policy',
        'SubscriptionsConfirmed',
        'SubscriptionsDeleted',
        'SubscriptionsPending',
        'TopicArn',
        'EffectiveDeliveryPolicy',
        'KmsMasterKeyId',
        'FifoTopic',
        'ContentBasedDeduplication'
    ),
    defaults=None
)

DEFAULT_HTTP_DELIVERY_POLICY = {
    "http": {
        "defaultHealthyRetryPolicy": {
            "minDelayTarget": 20,
            "maxDelayTarget": 20,
            "numRetries": 5,
            "numMaxDelayRetries": 0,
            "numNoDelayRetries": 0,
            "numMinDelayRetries": 0,
            "backoffFunction": "linear"
        },
        "disableSubscriptionOverrides": False
    }
}


class BaseTopic(ABC):

    def add_permission(self, label: str, account_id: str, actions: Union[List, Tuple]): ...

    def confirm_subscription(self, token: str, target_arn: str = None,
                             authenticate_on_subscribe: Union[bool, str] = False) -> Union[
        SubscriptionResource, None]: ...

    def delete(self, target_arn: Union[None, str]) -> Union[None, str]: ...

    def load(self) -> None: ...

    def publish(self, target_arn: str, message: Union[str, Dict], subject: str, msg_structure: str,
                endpoint: str = None, msg_attributes: Dict = None, msg_duplication_id: str = None,
                msg_group_id: str = None,
                use_self: bool = False) -> Dict: ...

    def remove_permission(self, label) -> None: ...

    def set_attributes(self, name: str, value: Any): ...

    def subscribe(self, protocol: Union[str, SnsProtocols], endpoint: str, target_arn: str = None,
                  attributes: Dict = None, return_subscription_arn: bool = False) -> SubscriptionResource: ...


class BaseSubscription(ABC):

    def delete(self) -> None: ...

    def get_available_subresources(self) -> Union[List, str]: ...

    def load(self) -> None: ...

    def reload(self, resource) -> None: ...

    def set_attributes(self, name, value) -> None: ...


class TopicService(BaseTopic):
    def __init__(self):
        try:
            sns_resource = boto3.client(
                'sns',
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            self.sns_resource = sns_resource
            self._attributes = None
            self._topic_arn = None

        except ClientError as err:
            logger.log(level=logging.WARNING, msg=err.__traceback__)

    def __del__(self):
        del self._topic_arn
        del self._attributes

    def create_topic(self, name, attributes: Dict = None, tags: Union[Dict, List, Tuple] = None):
        try:
            attr_keys = {
                'DeliveryPolicy',
                'DisplayName',
                'FifoTopic',
                'Policy',
                'KmsMasterKeyId',
                'ContentBasedDeduplication'
            }
            check_tags = False
            if isinstance(tags, (List, Tuple)):
                tags = [{'Key': x, 'Value': y} for x, y in tags if isinstance(x, str) and isinstance(y, str)]
                check_tags = bool(tags)
            elif isinstance(tags, Dict):
                tags = [{'Key': x, 'Value': y} for x, y in tags.items() if isinstance(x, str) and isinstance(y, str)]
                check_tags = bool(tags)

            if attributes:
                check_attr = attr_keys.issubset(set(attributes.keys()))
            else:
                check_attr = False

            if attributes and tags:
                if not (check_attr or check_tags):
                    raise ValueError('Topic attributes with invalid keys or tags provided with invalid key-value types')
                topic = self.sns_resource.create_topic(Name=name, Attributes=attributes, Tags=tags)
            elif attributes and not tags:
                if not check_attr:
                    raise ValueError('Topic attributes with invalid keys')
                topic = self.sns_resource.create_topic(Name=name, Attributes=attributes)
            elif tags and not attributes:
                if not check_tags:
                    raise ValueError('Topic tags provided with invalid key-value types')
                topic = self.sns_resource.create_topic(Name=name, Tags=tags)
            else:
                # assume no attributes or tags
                topic = self.sns_resource.create_topic(Name=name)

            arn = topic.get('TopicArn')
            self._topic_arn = arn
            return arn

        except ClientError as err:
            logger.log(level=logging.WARNING, msg=err.__traceback__)

    def add_permission(self, label: str, account_id: Union[str, List], actions: Union[List, Tuple]) -> None:
        # retrieve a given topic and add permission
        if isinstance(account_id, str):
            self.sns_resource.add_permission(
                TopicArn=self._topic_arn,
                Label=label,
                AWSAccountId=[account_id],
                ActionName=actions)
        elif isinstance(account_id, (List, Tuple)):
            if all([x for x in account_id if isinstance(x, str)]):
                self.sns_resource.add_permission(
                    TopicArn=self._topic_arn,
                    Label=label,
                    AWSAccountId=account_id,
                    ActionName=actions)
            else:
                raise ValueError('Invalid account ID provided. Account ID can be a valid string or list of strings')

    def confirm_subscription(self, token: str, target_arn: str = None,
                             authenticate_on_subscribe: Union[bool, str] = False) -> Union[SubscriptionResource, None]:
        # confirm the subscription for a given topic
        if target_arn:
            subscription = self.sns_resource.confirm_subscription(
                TopicArn=target_arn,
                Token=token,
                AuthenticateOnUnsubscribe='true' if authenticate_on_subscribe else 'false'
            )
        else:
            subscription = self.sns_resource.confirm_subscription(
                TopicArn=self._topic_arn,
                Token=token,
                AuthenticateOnUnsubscribe='true' if authenticate_on_subscribe else 'false'
            )
        if subscription:
            return subscription.get('SubscriptionArn')

    def delete(self, target_arn: str = None) -> Union[None, str]:
        try:
            if target_arn:
                self.sns_resource.delete_topic(TopicArn=target_arn)
                return target_arn
            else:
                self.sns_resource.delete_topic(TopicArn=self._topic_arn)
                return self._topic_arn
        except Exception as err:
            logger.log(logging.WARNING, msg=err.__traceback__)

    def load(self) -> None:
        attr = self.sns_resource.get_topic_attributes(TopicArn=self._topic_arn)
        if attr:
            self._attributes = attr.get('Attributes')

    def publish(self, target_arn: str, message: Union[str, Dict], subject: str, msg_structure: str,
                endpoint: str = None, msg_attributes: Dict = None, msg_duplication_id: str = None,
                msg_group_id: str = None,
                use_self: bool = False) -> Dict:

        publication = None
        kwargs = {}
        if msg_structure == 'json':
            if isinstance(message, Dict):
                message = json.dumps(message)
            if not isinstance(message, str):
                raise ValueError(
                    'Invalid message parameter. Message should be a valid string or dictionary with specified keys')
        if msg_group_id:
            kwargs.update(MessageGroupId=msg_group_id)
        if msg_duplication_id:
            kwargs.update(MessageDeduplicationId=msg_duplication_id)
        if msg_attributes:
            kwargs.update(MessageAttributes=msg_attributes)
        try:
            if target_arn and not endpoint:
                if kwargs:
                    publication = self.sns_resource.publish(
                        TargetArn=target_arn,
                        Message=message,
                        Subject=subject,
                        MessageStructure=msg_structure,
                        **kwargs
                    )
                else:
                    publication = self.sns_resource.publish(
                        TargetArn=target_arn,
                        Message=message,
                        Subject=subject,
                        MessageStructure=msg_structure,
                    )
            elif endpoint and not target_arn:
                if use_self:
                    if kwargs:
                        publication = self.sns_resource.publish(
                            TopicArn=self._topic_arn,
                            Message=message,
                            Subject=subject,
                            MessageStructure=msg_structure,
                            **kwargs
                        )
                    else:
                        publication = self.sns_resource.publish(
                            TopicArn=self._topic_arn,
                            Message=message,
                            Subject=subject,
                            MessageStructure=msg_structure,
                        )
                else:
                    if kwargs:
                        publication = self.sns_resource.publish(
                            PhoneNumber=endpoint,
                            Message=message,
                            Subject=subject,
                            MessageStructure=msg_structure,
                            **kwargs
                        )
                    else:
                        publication = self.sns_resource.publish(
                            PhoneNumber=endpoint,
                            Message=message,
                            Subject=subject,
                            MessageStructure=msg_structure,
                        )
            return publication
        except ClientError as err:
            logger.log(level=logging.WARNING, msg=err.__traceback__)
        except Exception:
            raise

    def remove_permission(self, label) -> None:
        self.sns_resource.remove_permission(TopicArn=self._topic_arn, Label=label)

    def set_attributes(self, name: str, value: Any):
        self.sns_resource.set_topic_attributes(TopicArn=self._topic_arn, AttributeName=name, AttributeValue=value)

    def subscribe(self, protocol: Union[str, SnsProtocols], endpoint: str, target_arn: str = None,
                  attributes: Dict = None,
                  return_subscription_arn: bool = False) -> SubscriptionResource:
        if isinstance(protocol, SnsProtocols):
            protocol = protocol.value[0].lower()
        elif isinstance(protocol, str):
            protocol = protocol.lower()

        delivery = True if protocol in ('http', 'https', 'sqs',) else False

        if attributes:
            if not (attributes.get('FilterPolicy') or attributes.get('DeliveryPolicy') or attributes.get(
                    'RawMessageDelivery')):
                raise ValueError('Invalid subscription attribute provided. Attribute data should be a valid '
                                 'dictionary with specified fields.')
        else:
            attributes = {
                "FilterPolicy": json.dumps({
                    "anyMandatoryKey": ["any", "of", "these"],
                    "anyOtherOptionalKey": ["any", "of", "these"]
                })
            }

            if protocol in ('https', 'http'):
                attributes.update({"DeliveryPolicy": json.dumps(
                    {
                        "defaultHealthyRetryPolicy": {
                            "minDelayTarget": 20,
                            "maxDelayTarget": 20,
                            "numRetries": 5,
                            "numMaxDelayRetries": 0,
                            "numNoDelayRetries": 0,
                            "numMinDelayRetries": 0,
                            "backoffFunction": "linear"
                        }
                    }
                )})
            if delivery:
                attributes.update({"RawMessageDelivery": 'true'})

        subscription = self.sns_resource.subscribe(
            TopicArn=target_arn if target_arn else self._topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
            Attributes=attributes,
            ReturnSubscriptionArn=return_subscription_arn
        )
        if subscription:
            return subscription.get('SubscriptionArn')

    @property
    def arn(self):
        if self.sns_resource:
            return self._topic_arn

    @property
    def attributes(self):
        self.load()
        return self._attributes


class EmailService(TopicService):
    # Provide messaging services for emails
    def publish(self, target_arn: str, message: Union[str, Dict], subject: str, msg_structure: str,
                endpoint: str = None, msg_attributes: Dict = None, msg_duplication_id: str = None,
                msg_group_id: str = None,
                use_self: bool = False) -> Dict:
        email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        if not regex.match(email_pattern, endpoint):
            raise ValueError('Invalid email provided')
        if 'email' not in message or 'email-json' not in message:
            raise ValueError('Invalid protocol provided for emailing service')

        return super(EmailService, self).publish(
            target_arn=target_arn,
            endpoint=endpoint,
            message=message,
            subject=subject,
            msg_structure=msg_structure,
            msg_attributes=msg_attributes,
            msg_duplication_id=msg_duplication_id,
            msg_group_id=msg_group_id
        )


class WebService(TopicService):
    # Provide messaging service for the HTTP and HTTPS protocol
    def publish(self, target_arn: str, message: Union[str, Dict], subject: str, msg_structure: str,
                endpoint: str = None, msg_attributes: Dict = None, msg_duplication_id: str = None,
                msg_group_id: str = None,
                use_self: bool = False) -> Dict:
        try:
            check = urlparse(endpoint)
            if all([check.scheme, check.netloc]):
                return super(WebService, self).publish(
                    target_arn=target_arn,
                    endpoint=endpoint,
                    message=message,
                    subject=subject,
                    msg_structure=msg_structure,
                    msg_attributes=msg_attributes,
                    msg_duplication_id=msg_duplication_id,
                    msg_group_id=msg_group_id
                )
        except ValueError:
            raise ValueError("Invalid URL provided for web messaging protocol. "
                             "Target endpoint should be 'https://' or 'http://' protocol")


class TextMessagingService(TopicService):
    # Provide messaging service for SMS and MMS protocol
    def publish(self, target_arn: str, message: Union[str, Dict], subject: str, msg_structure: str,
                endpoint: str = None, msg_attributes: Dict = None, msg_duplication_id: str = None,
                msg_group_id: str = None,
                use_self: bool = False) -> Dict:
        def _msg_size(m):
            if isinstance(m, str):
                msg_size = len(message.encode('utf-8'))
                return msg_size <= 256

        if msg_structure == 'json':
            if isinstance(message, Dict):
                message = json.dumps(message)
            else:
                raise ValueError('Message should be a valid dictionary or mapping with acceptable '
                                 'keys for service platform')
        elif msg_structure is None:
            if isinstance(message, Dict):
                message = message.get('default', None)
                if message is None:
                    raise ValueError('Empty message cannot be delivered. Provide message as string or valid '
                                     'mapping structure')
                elif not _msg_size(message):
                    raise ValueError('Message exceeds allowed size or limit')
            elif isinstance(message, str):
                if not _msg_size(message):
                    raise ValueError('Message exceeds allowed size or limit')

        return super(TextMessagingService, self).publish(
            target_arn=target_arn,
            endpoint=endpoint,
            message=message,
            subject=subject,
            msg_attributes=msg_attributes,
            msg_structure=msg_structure,
            msg_duplication_id=msg_duplication_id
        )


class SubscriptionService(BaseSubscription):
    def __init__(self, *, topic: TopicService, protocol: str, endpoint: str, attributes: Dict, flag: bool):
        self._subscription = topic.subscribe(protocol=protocol, endpoint=endpoint, attributes=attributes,
                                             return_subscription_arn=flag)

    def delete(self) -> None:
        # delete a subscription
        self._subscription.delete()

    def get_available_subresources(self) -> Union[List, str]:
        return self._subscription.get_available_subresources()

    def load(self) -> None:
        self._subscription.load()

    def reload(self, resource) -> None:
        self._subscription.reload(resource)

    def set_attributes(self, name, value) -> None:
        self._subscription.set_attributes(name, value)
