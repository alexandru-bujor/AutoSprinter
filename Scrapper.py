import os
import json
import requests
from bs4 import BeautifulSoup

# Lista de linkuri
urls = [


    "https://999.md/ro/100636029",
"https://999.md/ro/100635997",
"https://999.md/ro/83956221",
"https://999.md/ro/81273785",
"https://999.md/ro/89000731",
"https://999.md/ro/83244534",
"https://999.md/ro/89374951",
"https://999.md/ro/100267372",
"https://999.md/ro/84794548",
"https://999.md/ro/81736935",
"https://999.md/ro/86182213",
"https://999.md/ro/100518273",
"https://999.md/ro/100311126",
"https://999.md/ro/100267567",
"https://999.md/ro/100212005",
"https://999.md/ro/87674210",
"https://999.md/ro/86566152",
"https://999.md/ro/86447606",
"https://999.md/ro/86654909",
"https://999.md/ro/84429218",
"https://999.md/ro/86249590",
"https://999.md/ro/85963590",
"https://999.md/ro/86019412",
"https://999.md/ro/87581052",
"https://999.md/ro/87825954",
"https://999.md/ro/87825952",
"https://999.md/ro/87134559",
"https://999.md/ro/89072062",
"https://999.md/ro/89071989",
"https://999.md/ro/87962465",
"https://999.md/ro/87337586",
"https://999.md/ro/87337669",
"https://999.md/ro/87287551",
"https://999.md/ro/88859684",
"https://999.md/ro/88842121",
"https://999.md/ro/88798513",
"https://999.md/ro/88147633",
"https://999.md/ro/88230183",
"https://999.md/ro/89588166",
"https://999.md/ro/89588123",
"https://999.md/ro/100211961"
]

# Folder pentru imagini
base_folder = "static/foto_auto"
os.makedirs(base_folder, exist_ok=True)

# Fișierul JSON final
json_file_path = os.path.join(base_folder, "detalii.json")
all_cars_data = []

# Header pentru a evita blocarea
headers = {"User-Agent": "Mozilla/5.0"}


def extract_id(url):
    """Extract car ID from URL."""
    return url.split("/")[-1]


def extract_car_details(soup):
    """Extracts car specifications from HTML."""
    details = {}
    details_section = soup.find("div", class_="styles_features__Ws32g")

    if details_section:
        for group in details_section.find_all("div", class_="styles_group__aota8"):
            category = group.find("h2")
            category_name = category.text.strip() if category else "Altele"
            details[category_name] = {}

            for li in group.find_all("li", class_="styles_group__feature__5ZWJy"):
                key = li.find("span", class_="styles_group__key__uRhnQ")
                value = li.find("span", class_="styles_group__value__XN7OI")
                if key and value:
                    details[category_name][key.text.strip()] = value.text.strip()

    return details


def extract_price(soup):
    """Extracts price from the HTML."""
    price_tag = soup.find("span", class_="styles_footer__main__8seZ7")
    if price_tag:
        return price_tag.text.strip().replace("€", "").replace(" ", "").strip()
    return "0"


def extract_images(soup, car_id):
    """Downloads and saves images from the page."""
    car_folder = os.path.join(base_folder, car_id)
    os.makedirs(car_folder, exist_ok=True)

    image_links = []
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        if img_url and img_url.startswith("http"):
            image_links.append(img_url)

    saved_images = []
    for index, img_url in enumerate(image_links):
        img_name = f"{car_id}_{index}.jpg"
        img_path = os.path.join(car_folder, img_name)
        try:
            img_data = requests.get(img_url, headers=headers).content
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
            saved_images.append(img_name)
            print(f"✅ Salvat: {img_path}")
        except Exception as e:
            print(f"❌ Eroare la salvarea imaginii {img_url}: {e}")

    return saved_images


for url in urls:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        car_id = extract_id(url)
        title = soup.find("h1")
        title_text = title.text.strip() if title else "Fără titlu"
        caracteristici = extract_car_details(soup)
        saved_images = extract_images(soup, car_id)
        price = extract_price(soup)

        car_data = {
            "id": car_id,
            "titlu": title_text,
            "url": url,
            "preț": price,  # ✅ Price extracted
            "detalii": caracteristici,
            "imagini": saved_images
        }
        all_cars_data.append(car_data)
        print(f"✅ Date salvate pentru {title_text} - {price}€ în folderul {car_id}")
    else:
        print(f"❌ Eroare accesare {url}: {response.status_code}")

# Salvare în JSON
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(all_cars_data, json_file, ensure_ascii=False, indent=4)

print(f"✅ Toate datele au fost salvate în {json_file_path}")
