from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors


try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'flaskapp'


def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'gmail-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def main():
	"""Shows basic usage of the Gmail API.

	Creates a Gmail API service object and outputs a list of label names
	of the user's Gmail account.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	###################################################################
	############################TEST CODE##############################
	###################################################################
	# results = service.users().labels().list(userId='me').execute()
	# labels = results.get('labels', [])
	# if not labels:
	#     print('No labels found.')
	# else:
	#   print('Labels:')
	#   for label in labels:
	#     print(label['name'])
	###################################################################

	body =  { # A draft email in the user's mailbox.
				"message": { # An email message. # The message content of the draft.
					# "internalDate": "A String", # The internal message creation timestamp (epoch ms), which determines ordering in the inbox. For normal SMTP-received email, this represents the time the message was originally accepted by Google, which is more reliable than the Date header. However, for API-migrated mail, it can be configured by client to be based on the Date header.
					# "historyId": "A String", # The ID of the last history record that modified this message.
					# "payload": { # A single MIME message part. # The parsed email structure in the message parts.
					"body": { # The body of a single MIME message part. # The message part body for this part, which may be empty for container MIME message parts.
						"data": "A String", # The body data of a MIME message part as a base64url encoded string. May be empty for MIME container types that have no message body or when the body data is sent as a separate attachment. An attachment ID is present if the body data is contained in a separate attachment.
						# "attachmentId": "A String", # When present, contains the ID of an external attachment that can be retrieved in a separate messages.attachments.get request. When not present, the entire content of the message part body is contained in the data field.
						# "size": 42, # Number of bytes for the message part data (encoding notwithstanding).
					},
					"mimeType": "text/plain", # The MIME type of the message part.
					# "partId": "A String", # The immutable ID of the message part.
					# "filename": "A String", # The filename of the attachment. Only present if this message part represents an attachment.
					
					"headers": [ # List of headers on this message part. For the top-level message part, representing the entire message payload, it will contain the standard RFC 2822 email headers such as To, From, and Subject.
						{
						  "name": "To", # The name of the header before the : separator. For example, To.
						  "value": "k.raghuram@iitg.ac.in", # The value of the header after the : separator. For example, someuser@example.com.
						},
						{
						  "name" : "Subject",
						  "value" : "TEST",
						}
					],
					
					# "parts": [ # The child MIME message parts of this part. This only applies to container MIME message parts, for example multipart/*. For non- container MIME message part types, such as text/plain, this field is empty. For more information, see RFC 1521.
					# # Object with schema name: MessagePart
					# ],
					# },
					# "snippet": "A String", # A short part of the message text.
					# "raw": "A String", # The entire email message in an RFC 2822 formatted and base64url encoded string. Returned in messages.get and drafts.get responses when the format=RAW parameter is supplied.
					# "sizeEstimate": 42, # Estimated size in bytes of the message.
					# "threadId": "A String", # The ID of the thread the message belongs to. To add a message or draft to a thread, the following criteria must be met:
					# # - The requested threadId must be specified on the Message or Draft.Message you supply with your request.
					# # - The References and In-Reply-To headers must be set in compliance with the RFC 2822 standard.
					# # - The Subject headers must match.
					# "labelIds": [ # List of IDs of labels applied to this message.
					# "A String",
					# ],
					# "id": "A String", # The immutable ID of the message.
				},
				"id": "1", # The immutable ID of the draft.
			}

	####################################################################
	####DETAILS AT : https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.drafts.html#send
	####################################################################
	# send(userId=*, body=None, media_body=None, media_mime_type=None)
	service.users().drafts().create(userId='me', body=body)

if __name__ == '__main__':
	main()