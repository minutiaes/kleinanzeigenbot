import time, sys, os, csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def start_chrome():
    global driver
    path_to_extension = r'PATH' # PATH = Adblocker extension path
    chrome_options = Options()
    chrome_options.add_argument('load-extension=' + path_to_extension)
    driver = webdriver.Chrome('PATH', options=chrome_options) #PATH = chrome driver path
    driver.create_options()
    
def login():
    login_info = ['eMail', 'pw'] # Required eMail and pw to login
    login_name = ['loginMail', 'password']
    driver.get('https://www.ebay-kleinanzeigen.de/m-einloggen.html?targetUrl=/');
    driver.find_element_by_xpath("//button[contains(text(), 'Akzeptieren')]").click()
    for x in range(2):       
        searchbox = driver.find_element_by_name(login_name[x])
        searchbox.send_keys(login_info[x])
    searchbox.submit()

def csvparse(x, y):
    f = open('items.csv', 'r') #File that contains title, description and price of items
    mycsv = csv.reader(f)
    mycsv = list(mycsv)
    text = mycsv[x][y]
    return text

def add_item(x):
    blanks=['title', 'description', 'priceAmount']
    driver.get('https://www.ebay-kleinanzeigen.de/p-anzeige-aufgeben.html#?path=153/156&isParent=false')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_xpath("//span[contains(.,'Weiter')]").click()
    select = Select(driver.find_element_by_id('accessoires_schmuck.art_s'))
    select.select_by_value('muetzen_schals_handschuhe')

    for y in range(3):
        searchbox = driver.find_element_by_name(blanks[y])
        searchbox.send_keys(csvparse(x, y))

    driver.find_element_by_xpath("//span[contains(.,'Bilder hinzufügen')]").click()
    time.sleep(1)
    os.system(str(x)+'.exe') #Autoit script that chooses pictures that will be uploaded
    time.sleep(15)
    driver.find_element_by_xpath("//span[contains(.,'Anzeige aufgeben')]").click()

def del_item(x):
    driver.get('https://www.ebay-kleinanzeigen.de/m-meine-anzeigen.html')
    for y in range(x):
        driver.find_element_by_xpath("//span[contains(.,'Löschen')]").click()
        driver.find_element_by_id('modal-bulk-delete-ad-sbmt').click()
        time.sleep(2)
        driver.find_element_by_css_selector("[title*='Close (Esc)']").click()

def main(m, b):
    start_chrome()
    login()
    for n in range(m):
        if b == 1:
            add_item(n)
        elif b == 0:
            del_item(n+1)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
##    main(1, 0)
##driver.quit()

