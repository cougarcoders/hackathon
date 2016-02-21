# Larry Wells
# 02/20/2016

# Send email to text to user 

import smtplib
import shorten_url

#List of cell carriers
cell_carriers = ["tmomail.net", "mms.att.net", "email.uscc.net","messaging.sprintpcs.com"]



# smtp setup
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("divvytext@gmail.com", "cougarcoders2016")

# Send SMS Message
def send_sms_message(cell_number, carrier, content_title, content_link):
	# Check if link is null, and format appropriatly
	if content_link == '':
		sms_message = content_title
	else:
		sms_message = format_sms_message(content_title, content_link)
	server.sendmail('divvy', cell_number + '@' + carrier, sms_message)

# Send Email Message
def send_email_message(email, content_title, content_description, content_link):
	# Check if link is null and format appropriatly
	if content_title == '' and content_description == '':
		email_message = content_title
	else:
		email_message = format_email_message(content_title, content_description, content_link)
	server.sendmail('divvytext@gmail.com', email, email_message)

# Format SMS Message Body - Shortens URL
def format_sms_message(content_title, content_link):
	return content_title + "\n" + shorten_url.shortenURL(content_link)

# Format Email Message Body
def format_email_message(content_title, content_description, content_link):
	return content_title + "\n" + content_description + "\n" + content_link



# DEBUG Tools
def debug_send_test_sms_message():
	send_sms_message('6602345627', cell_carriers[1], 'Test Title', '')

def debug_send_test_email_message():
	send_email_message('lgwells1@me.com', 'Test email', '', '')