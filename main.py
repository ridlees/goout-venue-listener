import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def pyppetet(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.waitFor(5000)
    ## Get HTML
    html = await page.content()
    await browser.close()
    return html

def save_to_db(item):
    


def get_event_array(url):
    html_response = asyncio.get_event_loop().run_until_complete(pyppetet(url))
    ## Load HTML Response Into BeautifulSoup
    soup = BeautifulSoup(html_response, "html.parser")
    items_row = soup.find_all("div", class_="items row")[0]
    items = []
    for item in items_row.find_all("a", class_="title"):
        link = "https://goout.net" + item.get("href")
        items.appedn(link)
        print(link)
        print("\n\n\n----------------")
    return items



def main():
    items = get_event_array('https://goout.net/en/forum-karlin/vzvcu/events/')
    
