# Goout venue listener

A simple script utilising pyppeteer to scrap new events from Goout.net, compare them with database of scrapped events and send email to friend's email. 

## Dependencies
- pyppeteer
- dotenv
- BeautifulSoup
- SQLite

## Installation

`pip install -r requirements.txt`

## Setup
0. Empty the *venues.txt* file
1. Copy the `.example-env` to `.env`
2. Fill in the details. The `.example-env` has port and SMTP server for google.
    * **SENDER_EMAIL** is your email 
    * **PASSWORD** is password to your email
  * **RECEIVER_EMAIL** email is the email on which you send the new events
  * **VENUES** is the location of your *venues.txt* file
3. Go to [Goout](https://goout.net) and visit venue you want to subscribe to. On it, click on **Upcoming Events** and copy the URL. 
4. Add it to *venues.txt*
5. Repeat 3. and 4. for all venues you want.

## Running

* Go to the Goout venue listener folder and run `python3 main.py`.
> It will go through all your venues and check all incoming events. On each run, it sends you all events that are not in the *events.db*. That can be quite a lot on first runs.



