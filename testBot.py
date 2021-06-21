import praw
import re
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reddit = praw.Reddit(client_id = environ["CLIENT_ID"],
                     client_secret = environ["CLIENT_SECRET"],
                     user_agent = environ["USER_AGENT"])

subreddit = reddit.subreddit("OnePunchMan")

url = ""
for submission in subreddit.new(limit = 1000):
    t = (time.time() - submission.created_utc) / 3600
    print(submission.link_flair_text, ": ", t)
    if t > 5:
        break
    if (submission.link_flair_text.lower() == "murata chapter" or submission.link_flair_text.lower() == "one chapter"):
        if t < 1:
          url = submission.url
          print(url)
          break

if url != "":

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = environ["SENDER_EMAIL"]
    receiver_email = environ["RECEIVER_EMAIL"]
    password = environ["EMAIL_PASSWORD"]

    message = MIMEMultipart("alternative")
    message["Subject"] = "New OPM Chapter"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    A new OPM chapter has been released.\n""" + url

    html = """\
    <html>
      <body>
        <p><b>Hi,</b><br>
           A new OPM chapter has been released<br>
           <a href=""" + url + """>""" + url + """</a><br>
            <img src="https://i.imgur.com/RgzkuXo.png" alt = "image not found" width = "256" height = "354.155">
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
