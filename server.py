import smtplib
from flask import Flask, request, send_from_directory, redirect


app = Flask(__name__)


@app.get('/')
def sully():
    return send_from_directory(".", path="index.html")


@app.get('/api')
def hello():
    args = request.args

    text_amt = args.get("amnt")
    phone_number = args.get('pn')
    message = args.get('name')

    if not (phone_number and message and text_amt):
        return 'Invalid request (Not enough parameters)!', 401
    try:
        text_amt = int(text_amt)
    except ValueError:
        return f"The text amount value given \"{text_amt}\" is invalid!", 401

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login('YOUREMAIL@gmail.com', 'YOURPASSWORD')
    # Send text message through SMS gateway of destination number
    for x in range(text_amt):
        server.sendmail('YOUREMAIL@gmail.com',
                        f"{phone_number}@vtext.com", message)

    return redirect("http://192.168.1.214:5000/")


app.run("0.0.0.0")
