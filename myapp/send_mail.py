from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()
email_sender = 'inkandinsights.snsct@gmail.com'
email_password = os.getenv("GMAIL_APP_PWD")



def send_mail_func(fullname, username, product, label):   
    
    email_receiver = username
    subject = ""
    body = ""

    if label == 'POSITIVE':
        subject = "Thank You for Your Feedback on our Product!"
        
        body = f'''Dear {fullname},

We wanted to express our sincere gratitude for your recent feedback regarding our product \'{product}\'.

We are committed to providing the best possible experience for our customers. Your satisfaction is our top priority, and we will continue working hard to maintain the high standards that you've come to expect from us.

Thank you once again for your support. We look forward to serving you in the future and exceeding your expectations once more.

With regards,
Team Vinta!'''
    
    
    if label == 'NEGATIVE':
        subject = "Apology and Commitment to Improvement"
        
        body = f'''Dear {fullname},

We are writing in response to your recent feedback regarding our product, and we want to express our sincerest apologies for the less-than-satisfactory experience you had.

We are genuinely sorry for any inconvenience or disappointment you may have experienced, and we want you to know that we are committed to making things right.

Our team is already taking steps to address the issues you've highlighted, and we are working diligently to improve our product. We appreciate your feedback as it helps us identify areas where we can make meaningful changes to enhance our offerings.

We truly appreciate your understanding and patience. Please do not hesitate to reach out to us if you have any further suggestions or concerns.

Sincerely,
Team Vinta!'''
    
    
    if label == 'NEUTRAL':
        subject = "Thank You for Your Feedback"
        
        body = f'''Dear {fullname},

We would like to express our gratitude for taking the time to provide feedback on our product. Your input is valuable to us, and we appreciate your effort in sharing your thoughts.

Your feedback will be instrumental in helping us continually improve our product and meet your expectations. Please rest assured that we take all feedback into consideration as we work to enhance our offerings.

If you have any further comments, suggestions, or questions, please feel free to reach out to us. Your input is always welcome, and we are here to assist you.

Thank you once again and we look forward to serving you in the future.

With regards,
Team Vinta!'''



    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    