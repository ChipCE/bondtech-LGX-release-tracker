from bs4 import BeautifulSoup

import requests

class Tracker:

    def __init__(self):
        self.productList = []
        self.url = "https://www.bondtech.se/en/product-category/extruders/"
        self.keyword = "LXG"
        self.msg = ""
        self.notificationUrl = "http://localhost:1880/notification"
        self.notificationTimeout = 500

    def sendNotification(self):
        try:
            response = requests.get(self.notificationUrl,+ "?msg=" + self.msg,header={'Content-type': 'text/plain'},timeout=self.notificationTimeout)
            if response.status_code in range(200,300):
                return True
        except Exception as e:
            print(e)
            return False

    def run(self):
        try:
            response  = requests.get(self.url)
            data = response.text
            soup = BeautifulSoup(data,features="html5lib")

            currentProductNameList = []
            productDivList = soup.find_all("div", attrs={"class": "product-small box"})
            for productDiv in productDivList:
                productName = productDiv.find("p",attrs={"class": "name product-title woocommerce-loop-product__title"})
                currentProductNameList.append(productName.get_text())

            if len(self.productList) == 0:
                self.productList = currentProductNameList
                print(currentProductNameList)
            else:
                self.msg = ""
                for product in currentProductNameList:
                    # add new product
                    if product not in self.productList:
                        self.productList.append(product)
                        self.msg = self.msg + "New product : " + product + ","
                    # remove non exist
                    tmp = []
                    for product in self.productList:
                        if product in currentProductNameList:
                            tmp.append(product)
                    self.productList = tmp
                if self.msg != "":
                    self.sendNotification()
                else:
                    print("No change")
        except Exception as e:
            print(e)

