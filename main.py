import asyncio
from pyppeteer import launch
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
    new_items = event_checker('https://goout.net/cs/eternia-smichov/vzsvob/events/', cur, con)
    print("New Items from Eternia - Smichov")
    new_items = new_items + event_checker('https://goout.net/cs/underdogs-ballroom/vzocpb/events/', cur, con)
    print("New Items from Underdogs - Ballroom")
    new_items = new_items + event_checker('https://goout.net/cs/roxy/vzm/events/', cur, con)
    print("New Items from Roxy")
    new_items = new_items + event_checker('https://goout.net/cs/ankali/vzqivb/events/', cur, con)
    print("New Items from Ankali")
    new_items = new_items + event_checker('https://goout.net/cs/fuchs2/vzaoed/events/', cur, con)
    print("New Items from Fuchs2")
    new_items = new_items + event_checker('https://goout.net/cs/bike-jesus/vznvp/events/', cur, con)
    print("New Items from Bike Jesus")
    new_items = new_items + event_checker('https://goout.net/cs/modra-vopice/vzpd/events/', cur, con)
    print("New Items from Modrá opice")
    new_items = new_items + event_checker('https://goout.net/cs/punctum/vzkpbb/events/', cur, con)
    print("New Items from Punctum")
    if new_items:
        print("sending")
        sender(new_items)
    

if __name__ == '__main__':
    main()
