import asyncio
from pyppeteer.launcher import launch
from bs4 import BeautifulSoup

import sqlite3

from sender import send_email

from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

port = os.environ.get("PORT")
smtp_server = os.environ.get("SMTP_SERVER")
sender_email = os.environ.get("SENDER_EMAIL")
password = os.environ.get("PASSWORD")
email = os.environ.get("RECEIVER_EMAIL")
path_to_file = os.environ.get("VENUES")

async def pyppetet(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.waitFor(7000)
    ## Get HTML
    html = await page.content()
    await browser.close()
    return html

def compare_with_db(items, cur):
    new_items = []
    res = cur.execute("SELECT DISTINCT url FROM events")
    old_items = [item[0] for item in res.fetchall()]
    for item in items:
        if item not in old_items:
            new_items.append(item)
    return new_items

def save_to_db(items, cur):
    for item in items:
        cur.execute("""INSERT INTO events (url) 
               VALUES (?);""", (item,))

def prune_db(cur):
    pass

def get_event_array(url):
    html_response = asyncio.get_event_loop().run_until_complete(pyppetet(url))
    ## Load HTML Response Into BeautifulSoup
    soup = BeautifulSoup(html_response, "html.parser")
    items_row = soup.find_all("div", class_="items row")[0]
    items = []
    for item in items_row.find_all("a", class_="title"):
        link = "https://goout.net" + item.get("href")
        items.append(link)
    return items

def sender(events):
    subject = "Goout Watchdog"
    text = "Ahoj Kris,\n\n Mám pro tebe nové akce:\n"
    for event in events:
        text = text + event + "\n\n"
    message = f"From: {sender_email}\r\nTo: {email}\r\nSubject:{subject}\r\n{text}"
    send_email(port, smtp_server, sender_email, password, email, message)

def event_checker(url, cur, con):
    items = get_event_array(url)
    new_items = compare_with_db(items, cur)
    save_to_db(new_items,cur)
    con.commit()
    #prune_db(cur)
    #con.commit()
    return new_items

def main():
    con = sqlite3.connect("events.db")
    cur = con.cursor()

    with open(path_to_file) as file:
        new_items = []
        for line in file.readlines():
            print(line)
            new_items = new_items + event_checker(line, cur, con)
        if new_items:
            print("sending")
            sender(new_items)
   
    
    

if __name__ == '__main__':
    main()
