from playwright.sync_api import sync_playwright
from flask import Flask, jsonify


def get_computer(brand_name = "", detail = False):
    url = "https://webscraper.io"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url+'/test-sites/e-commerce/allinone/computers/laptops')

        laptops = page.locator("div.col-sm-4").all()
        # print(laptops)

        # extrair as informações dos laptops
        laptops_list = []
        for laptop in laptops:
            brand = laptop.locator("h4 a").text_content()
            if (brand_name != "" and brand_name.upper() not in brand.upper()): continue
            description = laptop.locator("p.description").text_content()
            link = laptop.locator("h4 a").get_attribute("href")
            price = laptop.locator("h4.price").text_content()


            # pega subvalores
            if (detail):
                hdds_list = []
                page2 = browser.new_page()
                page2.goto(url + link)
                hdds = page2.locator("div.swatches button.swatch").all()
                for hdd in hdds:
                    hd_value = hdd.text_content()
                    hdd.click()
                    hd_price = page2.locator("h4.price").text_content()
                    hdds_list.append({"hdd": hd_value, "price": hd_price})
                page2.close()
                laptops_list.append({"brand": brand, "description": description, "link": url + link, "price": price, "hdd_options":hdds_list})
            else:
                laptops_list.append({"brand": brand, "description": description, "link": url+link, "price": price})
            #print({"brand": brand, "description": description, "link": url+link, "price": price, "hdd_options":hdds_list})

        # ordenando os laptops pelo preço
        laptops_list = sorted(laptops_list, key=lambda x: x["price"])

        browser.close()

    return laptops_list

         #criando a api
app = Flask(__name__)

#criando a rota para acessar a lista de laptops ordenada
@app.route("/laptops/<brand>", methods=["GET"])
def get_laptops(brand=None):
    return jsonify(get_computer(brand))

#criando a rota para acessar a lista de laptops ordenada
@app.route("/laptops-detail/<brand>", methods=["GET"])
def get_laptops_detail(brand=None):
    return jsonify(get_computer(brand, True))

if __name__ == "__main__":
    app.run(debug=True)

