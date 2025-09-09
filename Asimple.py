import time
from playwright.sync_api import sync_playwright
import os
import json
import requests

BASE_DIR = "Cases"


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

    return results


def download_image(url, save_path_no_ext):
    """Скачивает картинку и подбирает расширение"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "").lower()
        ext = ".png" if "png" in content_type else ".jpg"
        save_path = save_path_no_ext + ext

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return save_path
    return None


def get_page(url):
    page = browser.new_page()
    page.goto(url)

    time.sleep(10)
    return page


def get_secret_skin(path, page):
    block_selector = "body > div.container.main-content > div:nth-child(7) > div:nth-child(1)"
    block = page.query_selector(block_selector)
    print("block", block)

    if block:
        link_el = block.query_selector("div > a:nth-child(3)")
        if link_el:
            href = link_el.get_attribute("href")
            print("Ссылка:", href)
            get_second_page(path, get_page(href))  # скачиваем секретный скин
            return href
        else:
            print("Ссылка не найдена")
    else:
        print("Блок не найден")
    return None


def get_second_page(path, page):
    case_name_selector = "body > div.container.main-content > div:nth-child(2) > div > div.inline-middle.collapsed-top-margin > h1"
    page.wait_for_selector(case_name_selector, timeout=30000)
    case_name = page.query_selector(case_name_selector).inner_text().strip()

    print("Название кейса:", case_name)

    # --- 2. Главная картинка кейса ---
    main_img_selector = "body > div.container.main-content > div:nth-child(2) > div > div:nth-child(1) > a img"
    main_img_url = page.query_selector(main_img_selector).get_attribute("src")

    os.makedirs(path, exist_ok=True)
    main_img_path = download_image(main_img_url, os.path.join(path, "case_main"))


    # --- 3. Скины в кейсе ---
    skins = []
    n = 2
    while True:
        block_selector = f"body > div.container.main-content > div:nth-child(7) > div:nth-child({n})"
        block = page.query_selector(block_selector)
        if not block:
            break  # больше блоков нет

        # h3: "AK-47 / Redline"
        h3 = block.query_selector("h3")
        if h3:
            parts = [p.strip() for p in h3.inner_text().split("|") if p.strip()]
            weapon_type = parts[0] if len(parts) > 0 else ""
            weapon_name = parts[1] if len(parts) > 1 else ""

            # картинка
            img = block.query_selector("a img")
            img_url = img.get_attribute("src") if img else None
            img_path = None
            if img_url:
                img_path = download_image(img_url,
                                          os.path.join(path, f"skin_{weapon_name.replace('', '_').lower()}_{n}"))

            skins.append({
                "weaponType": weapon_type,
                "weaponName": weapon_name,
                "image": img_path
            })

        n += 1
        # --- 4. Формируем JSON ---
        data = {
            "caseName": case_name,
            "caseImage": main_img_path,
            "skins": skins
        }

        # сохраняем
        with open(f"{str(case_name).replace('', '_').lower()}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("✅ Данные сохранены в case_data.json")


def create_directories(item):
    """Создаём папки: Cases/{span_text}"""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    # for item in items:
    folder_name = item["text"].strip().replace(" ", "_")  # заменяем пробелы на _
    path = os.path.join(BASE_DIR, folder_name)
    path_secret = os.path.join(path, "secret")
    os.makedirs(path, exist_ok=True)
    os.makedirs(path_secret, exist_ok=True)
    print(f"✅ Папка создана: {path}")
    return path, path_secret


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = get_page("https://stash.clash.gg/")
        list_of_urls = get_all_items(page)



        for url in list_of_urls[:-3]:  # пропускаем первый элемент (секретный скин)
            print(url)
            path, path_secret = create_directories(url)
            url_to_secret = get_secret_skin(path_secret, get_page(url["href"]))
            get_second_page(path, get_page(url["href"]))
            # break
        browser.close()

# --- переход по первой ссылке чтоб скачать секретный скин ---
# --- функция для создания директорий для каждого кейса отдельно --- ✅
