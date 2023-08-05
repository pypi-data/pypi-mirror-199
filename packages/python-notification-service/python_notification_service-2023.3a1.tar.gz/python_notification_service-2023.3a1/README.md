# Python Notification Service
**A Python wrapper for sending email or messages using Amazon SNS, SES, Mailgun and Zepto API**

Messaging service is a key component for many applications and comes inbuilt in some frameworks, example, Django.
However, in some cases, there is the need to have a simple Python script that allows developers manage the responsibility
of sending emails. The Python Notification Service is built to address emailing need of Python application by 
providing a function for sending email. Parameters for the various API can be provided to this function alongside with the 
email message. This gives the benefit of wrapper emailing and SMS functionality within method calls or other mechanism. 
        
## Description
The Python Messaging Service is a web based notification service built upon the Pub/Sub messaging and other HTTPS based 
emailing system. By adopting the AWS SNS and SES system, this messaging service will allow for application to application and application to person.
Emails can be sent as plain text or HTML message using templates. For the currently supported APIs (AWS, Mailgun, Zepto) users will need to obtain a valid
API to send messages. API and other configurations can be stored as environment variable with specified names as shown below.

   
~~~

# Defined API configuration

APP_NAME # An optional parameter for specifying the name of the application from which the email or message is sent

# AWS Settings
AWS_ACCESS_KEY  # User's AWS access key ID
AWS_SECRET_ACCESS_KEY  # User's AWS secret key for accessing SNS/SES service 
AWS_REGION  # AWS region for which user's SNS/SES is registered with.

ZEPTO_EMAIL_API  # Zepto API url. Default value at time of writing is 'https://api.zeptomail.com/v1.1/email/template'
MAILGUN_EMAIL_API = # Mailgun API url. The URL may require parsing to cover for region and other settings. 
# See Mailgun documentation for details (https://documentation.mailgun.com/en/latest/api-intro.html#introduction)
~~~  

  
## Dependencies
This application relies on Python requests and boto3 client to perform connection to service providers and broadcasting messages.
The target Python language for current version is Python 3.7 or later     
   
## Build Status
**Version: 2023.03.a1**

Current development of Python Notification Service is version 2023.03.a1. This is considered the Alpha Edition. 
Future releases will support SMTP mail functions alongside other HTTPS emailing services.
 
## Features
Supported features includes:
+ Send emails based on SNS topic
+ Send emails to list of recipients or single recipient
+ Register a user for a topic using email or mobile
+ Register an application for a topic using callback URLs
+ Publish/Broadcast message to a topic - this results in sending messages to all entities (applications and persons) registered to that topic.


## Contributing
Please visit application repo for further information on extending project. Ideas and comments will be reasonably appreciated. 
 
## Author
Current development is by Alpha 17 Solutions and maintained by [@frier17](https://gitlab.com/frier17). 

## License
Apache License

Version 2.0, January 2004

http://www.apache.org/licenses/

For details read license contract [here](http://www.apache.org/licenses/LICENSE-2.0)

Copyright 2019 @frier17

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
