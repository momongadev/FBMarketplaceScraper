"""
DISCLAIMER:
Este script es solo con fines educativos.
El autor no se hace responsable del uso que se le dé.
"""

from playwright.sync_api import sync_playwright, TimeoutError
import time
import os
import pandas as pd
from datetime import datetime

def listall(page, scrollpause=2, maxscrolls=3):
    previousheight = 0

    for i in range(maxscrolls):
        print(f"Scrolling #{i+1}")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(scrollpause)
 
        listings = page.query_selector_all("div[class*='x9f619']")
        currentcount = len(listings)

        print(f"Found {currentcount} listings")

        if currentcount == previousheight:
            print("No more new listings.")
            break

        previousheight = currentcount

    return listings

def MarketplaceScraper():
    context_storage = "fb_login.json"
    loginurl = "https://www.facebook.com/login"
    marketplaceurl = "https://www.facebook.com/marketplace/sanjosecr/search/?query=toyota%20echo%202003"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # Load storage state if exists, else create fresh context
        if os.path.exists(context_storage):
            context = browser.new_context(storage_state=context_storage)
        else:
            context = browser.new_context()

        page = context.new_page()

        page.goto(loginurl)

        # If no saved login, wait for manual login and save state
        if not os.path.exists(context_storage):
            print("Log in manually")
            try:
                page.wait_for_url("https://www.facebook.com/", timeout=120000)
            except TimeoutError:
                print("Login timeout expired")

            context.storage_state(path=context_storage)
            print("Storage state saved!")

        page.goto(marketplaceurl)
        page.wait_for_load_state("load")
        time.sleep(3)

        parsed = []

        listings = page.query_selector_all("div[class*='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x135b78x x11lfxj5 x1iorvi4 xjkvuk6 xnpuxes x1cjf5ee x17dddeq']")
        print(f"Found {len(listings)} listings:\n")

        for i, listing in enumerate(listings):
            try:
                print(f"\nOpening listing #{i+1}")

                mainpostdescription = listings[i].inner_text()
                issponsored = "Sponsored" in mainpostdescription
                if issponsored:
                    print("this one is a sponsor so skip")
                    continue
                
                modal_opened = False
                for attempt in range(2):
                    try:
                        listings = page.query_selector_all("div[class*='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x135b78x x11lfxj5 x1iorvi4 xjkvuk6 xnpuxes x1cjf5ee x17dddeq']")
                        listing = listings[i]
                        page.evaluate("(el) => el.scrollIntoView()", listing)
                        time.sleep(1)
                        listing.click()
                        page.wait_for_selector("div[role='dialog']", timeout=8000)
                        modal_opened = True
                        break
                    except:
                        print(f"Retry {attempt+1} for listing #{i+1}")
                        time.sleep(2)

                if not modal_opened:
                    print("Modal did not open")
                    continue
                time.sleep(3)

                modal = page.locator("div[role='dialog']")
                
                see_more_button = modal.get_by_role("button").filter(has_text="See more")
                if see_more_button.count() > 0:
                    try:
                        see_more_button.first.click()
                    except Exception as e:
                        pass
                try:
                    title = modal.locator("h1 span[dir='auto']").first.inner_text()
                    try:
                        price = modal.locator("span[dir='auto']").filter(has_text="CRC").first.inner_text()
                        if not "CRC" in price:
                            price = 0
                    except Exception as e:
                        print("Error extracting price:", e)
                    location = modal.locator("div[class='x14vqqas x14z9mp xod5an3 x1lziwak'] span[dir='auto']").first.inner_text()
                    description = modal.locator("div[class='xz9dl7a xyri2b xsag5q8 x1c1uobl x126k92a'] span[dir='auto']").first.inner_text()

                    print("Data scraped successfully")                    
                except Exception as e:
                    print("Error extracting data:", e)
                    continue

                parsed.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'description': description,
                })

                page.get_by_role("banner").get_by_role("button", name="Close").click()
                time.sleep(2)

            except Exception as e:
                print("Error with listing:", e)
                try:
                    page.get_by_role("banner").get_by_role("button", name="Close").click()
                    time.sleep(2)
                except:
                    pass
                continue

        browser.close()

        return parsed

if __name__ == "__main__":
    scrapeddata = MarketplaceScraper()
    print(f"Scraped {len(scrapeddata)} listings")
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        df = pd.DataFrame(scrapeddata)
        df.to_excel(f"marketplace_data{timestamp}.xlsx", index=False)
        print("Data saved to marketplace_data.csv")
    except Exception as e:
        print("Error saving data to CSV:", e)    