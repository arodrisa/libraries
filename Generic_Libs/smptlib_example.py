import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 465  # For starttls
sender_email = "arodrisaai@gmail.com"
# password = input("Type your password and press enter: ")
password = "0Mierdas"
# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    # TODO: Send email here
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit() 