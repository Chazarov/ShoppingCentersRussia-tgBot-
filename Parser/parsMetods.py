from bs4 import BeautifulSoup
import time
import requests
import lxml

from Parser import saveFunc
from Parser.correctText import removeWhitespaace, removePrefix, GetName
from Parser import netData

CentersData = []

def pageEnums():

    pageUrl = "https://zdanie.info/бизнес_центры_и_торговые_центры/торговые_центры_городов_россии/off/"

    data = list()

    for page in range(49):
        data = list()
        time.sleep(1)
        currentPageUrl = pageUrl + str(page)
        res = requests.get(currentPageUrl, allow_redirects=True,headers=netData.headers)
        soup = BeautifulSoup(res.text, "lxml")
        data = getCatalog(soup, page)
        saveFunc.saveJson(data, page)
        
def getCatalog(soup:BeautifulSoup, page: int):
    items = soup.find_all("div", class_ = "hover-shd p-5 border bg-6")

    centersDataList = list()

    k = 0
    for i in items:
        centerData = dict()

        description = i.find("div", class_ = "object-standart-text_wrap col-xs-20").get_text()
        id = str(page) + "." + str(k)
        if(description):
            name = GetName(i.find("h2").text)
            if(name == None): name = "Имя не найдено"

            img_link = "https://zdanie.info" + i.find("img").get("src")
            img_requests = requests.get(img_link, allow_redirects=True,headers=netData.headers)
            img_file_bin = img_requests.content
            city, adress = getAdressFromDescription(i)
            contacts = get_contacts(i.find("h2"))
            
            if(img_file_bin != None): 
                saveFunc.saveImg(img_file_bin, id)
            centerData["id"] = id
            centerData["image"] = f"Parser/DATA/IMG/{id}.jpg"
            centerData["city"] = city
            centerData["name"] = name
            centerData["adress"] = adress
            centerData["description"] = description
            centerData["contacts"] = contacts

            print(name + " was loaded successesfuly")
        else: print("  --something went wrong--  ")

        saveFunc.database_save_center(centerData)
        centersDataList.append(centerData)

        k += 1

    return centersDataList
    

def getAdressFromDescription(soup:BeautifulSoup):

    result = ""
    adressItems = soup.find_all("a", class_ = "cl-text cl-hover-blue")
    if(adressItems != None):
        get_city = False
        for i in adressItems:
            if not get_city:
                city = i.get_text()
                get_city = True
            result += "/" + i.get_text()

    else: return "Город не указан", "Адрес не указан"
    return city, result

def getPricesTable(soup: BeautifulSoup):
    table_items_str_list = list()
    headings = soup.find("table", class_ = "table table-small table-object-properties").find("thead").find_all("th")
    for i in headings:
        table_items_str_list.append(i.get_text())
    table_data = soup.find("tbody").find_all("td")
    k = 0
    for i in table_data:
        table_items_str_list[k] += ": " + i.get_text() + "; "
        k+=1
    return "".join(table_items_str_list)

def get_contacts(soup: BeautifulSoup):#Со странички торгового центра получить контактную информацию из таблицы
    src = removePrefix(soup.a.get("href"))
    res = requests.get(netData.StartPage + src, allow_redirects=True,headers=netData.headers)
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.find("div", class_ = "tabs tabs-default active-grey contact-wrap border-l_blue").find("table", class_ = "object-contact")
    if table == None:
        return "Контактная информация не найдена"
    items = table.find_all("tr")

    k = 0
    website = "Вебсайт не найден"
    company = "Компания не найдена"
    number = "Номер не найден"
    owner = "Владелец не найден"

    for item in items:
        if(k == 0):
            company = item.get_text()
        if(k == 2):
            owner = item.get_text()
        if(k == 3):
            number = item.find(class_ = "border-b").get_text()
        if(k == 4):
            website = item.find(class_ = "border-b").get_text()
        k += 1

        company = removeWhitespaace(company, "\n")
        owner = removeWhitespaace(owner, "\n")
        number = removeWhitespaace(number, "\n")
        website = removeWhitespaace(website, "\n")

    return f"{company}\n владелец: {owner}\n Сайт: {website}\n Номер телефона: {number}"






    
        