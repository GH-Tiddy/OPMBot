import praw
import re
import requests
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from os import environ

reddit = praw.Reddit(client_id = os.environ.get("CLIENT_ID"),
                     client_secret = os.environ.get("CLIENT_SECRET"),
                     user_agent = os.environ.get("USER_AGENT"))

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
  
    req = requests.get(url, 'html.parser')
    source_text = req.text
    p = re.compile("og:image\" content=\"([a-zA-Z0-9_:/. ]+)\"")
    m = p.search(source_text)
    image = "https://i.imgur.com/RgzkuXo.png";
    if m:
        image = m.group(1)


    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

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
            <img src=""" + image + """ alt = "image not found" width = "256" height = "354.155">
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
