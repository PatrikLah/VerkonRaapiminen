from requests_html import HTMLSession
import pandas as pd
import time
#Render Dynamic Pages - Web Scraping Product Links with Python
#Virvoitusjuomat = 1022 | sivuja n. 5
#Mehut = 1018 | sivuja n. 9
#Vedet = 1028 | sivuja n. 4
#Energiajuomat = 1038 | n. 2

category_code = 1008
page_count = 1
category_string = ""

if category_code == 1022:
    category_string = "virkkarit"
    page_count = 5
elif category_code == 1018:
    category_string = "mehut"
    page_count = 9
elif category_code == 1028:
    category_string = "vedet"
    page_count = 4
elif category_code == 1038:
    category_string = "energiajuomat"
    page_count = 2



url =f"https://www.foodie.fi/products/{kategoria_koodi}"
s = HTMLSession()
product_info_list = []

def removeFormatting(s):
    return "".join(i for i in s if ord(i) < 126 and ord(i) > 31)

def request(url):
    r = s.get(url)
    r.html.render(sleep=1)
    return r.html.xpath("/html/body/div[5]/div[2]/div[7]/div/div[2]/div[2]/div/div[2]/div/ul", first = True)

def parse(products):
    for item in products.absolute_links:
        r = s.get(item)
        try:
            gtin = (r.html.find('div.aisle', first = True).text)
            gtin = gtin[18:]
            #print("GTIN: " + gtin)
            brand = (r.html.find('div.col-sm-7 > h2', first = True).text)
            name = (r.html.find("div.col-sm-7 > h1", first = True).text)
            #print("Nimi: " + name)
            price = (r.html.find("div.price", first = True).text)
            #print("Price: " + price)
            quantity = (r.html.find("div.js-quantity", first = True).text)
            #print("Quantity: " + quantity)
            likes = (r.html.find('span.js-like-count', first = True).text)
            dislikes = (r.html.find('span.js-dislike-count', first = True).text)
            #print("Like count: " + likes + ", Dislike count: " + dislikes)
            #Valmistaja = (r.html.find('div.active > p', second = True).text)
            #Valmistaja = (r.html.xpath('//*[@id="origin"]/p'))
            country = (r.html.find('#origin > p', first = True).text)
            #print("Maa:" + country.text)
            nutr_info = (r.html.find('div.nutritions > table.data-table', first = True))
            nutrition_table = nutr_info
            formatted_nutr_table = removeFormatting(nutr_info.text)
            #print("Ravintosisältö: " + formatted_nutr_table)
        except:
            print("Tuotteen tietoja puuttui")


        prod = {
            "GTIN":gtin,
            "Brand":brand,
            "name":name,
            "price":price,
            "quantity":quantity,
            "likes":likes,
            "dislikes":dislikes,
            "country":country,
            "nutrition table":formatted_nutr_table
        }
        product_info_list.append(prod)
    
def output():
    df = pd.DataFrame(product_info_list)
    df.to_csv(f"prisma_{category_string}.csv", index=False)
    print("Tallennettu")

x=1
while x <= page_count:
    products = request(f"https://www.foodie.fi/products/{category_code}/page/{x}?main_view=1")
    print(f"Sivulla: {x}")
    parse(products)
    print("Saatiin tuotteita:", len(product_info_list))
    x += 1
    time.sleep(3)

output()