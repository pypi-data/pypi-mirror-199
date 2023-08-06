# wmul_emailer

Utility to send an email to multiple addresses. Primarily intended for cli applications. The various fields such as server host, username, etc. are entered at the command line, used to construct a wmul_emailer.EmailSender object, and that object is passed into the main part of the script. The main part of the script can use it as needed to report errors or results without having to worry about the e-mail details.

A cli is provided for testing purposes. 

## class EmailSender(server_host, port, user_name, password, from_email_address=None, destination_email_addresses=None)
`server_host` The hostname or ip address of the smtp server.  
`port` The port number on which the smtp server resides.  
`user_name` The username to authenticate with the smtp server.  
`password` The password to authenticate with the smtp server.  
`from_email_address=None` The 'from' e-mail address.  
`destination_email_addresses=None` The e-mail address to which the results should be sent. Must be a list or tuple for multiple addresses, or a str for a single address. 

### send_email(self, email_body, email_subject, from_email_address=None, destination_email_addresses=None)
`email_body` The body of the e-mail to be sent.  
`email_subject` The subject line of the e-mail to be sent.  
`from_email_address=None` The 'from' e-mail address, if provided here. If a `from_email_address` is not included when calling this method, the one provided to the constructor will be used.  
`destination_email_addresses=None` The e-mail address to which the results should be sent, if provided here. If `destination_email_addresses` are not included when calling this method, the ones provided to the constructor will be used. Must be a list or tuple for multiple addresses, or a str for a single address. 

Raises `ValueError` if either `destination_email_addresses` or `from_email_address` are omitted from both the constructor and the call to send_email.

## Command-Line Interface
A cli is provided to test that the credentials are functional and that the system can send e-mails.

`send_test_email --email destination@example.com --server smtp.example.com --port 25 --username myusername --password mypassword --from_address source@example.com`

If everything works, then `destination@example.com` will receive an e-mail from `source@example.com` with the subject `Test e-mail from wmul_emailer` and body `This is the test e-mail from wmul_emailer.py. If you are reading this, the software is configured correctly.`
