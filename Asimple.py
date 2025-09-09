import time
from playwright.sync_api import sync_playwright


def get_all_items(page):
    # Ждём и открываем меню
    page.wait_for_selector("button.hamburger", timeout=30000)
    page.click("button.hamburger")

    # Ждём 7-й tab
    page.wait_for_selector("div.mobile-menu.no-scrollbar.open > div > mobile-nav-tab:nth-child(7)", timeout=30000)

    # Все <a> внутри group-items
    group_items = page.query_selector_all(
        "div.mobile-menu.no-scrollbar.open > div > mobile-nav-tab:nth-child(7) div.group-items > a"
    )

    results = []
    for el in group_items:
        href = el.get_attribute("href")
        span = el.query_selector("span")
        text = span.inner_text() if span else ""
        results.append({"text": text, "href": href})

    print("Найденные элементы:")
    for r in results:
        print(f"{r['text']} -> {r['href']}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://stash.clash.gg/case/422/Fever-Case")

    # get_all_items(page)



    time.sleep(10)
    browser.close()
