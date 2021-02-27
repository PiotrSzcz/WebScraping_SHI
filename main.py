from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common import exceptions  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time

quantity_of_series = int(input("Podaj ilość serii do sprawdzenia: "))
#odaplenie przeglądarki wraz z driverem
web_controller = webdriver.Edge(executable_path="C:\\Users\\piosz\\Desktop\\programowanie\\Python\\Web_Scraping\\msedgedriver.exe")
web_controller.get('https://shinden.pl/series/season/current')

def popup_interrupter():
    popup_cookies = web_controller.find_element(By.XPATH , "/html/body/div[14]/div[1]/div[2]/div/div[2]/button[2]")
    ActionChains(web_controller).click(popup_cookies).perform()
    time.sleep(1)
    popup_pri = web_controller.find_element(By.XPATH , "/html/body/div[3]/p/a[1]")
    ActionChains(web_controller).click(popup_pri).perform()

def list_of_search():
    #Odczyt listy serialii
    season_group = web_controller.find_element(By.CSS_SELECTOR, "#group-tv > ul")
    title_list = season_group.find_elements(By.CLASS_NAME, "box-title")
    print('id    Tytuł')
    for i in range(0, quantity_of_series):
        print(i, "   ",title_list[i].text)

if __name__ == "__main__":
    #Wyłączenie popup
    popup_interrupter()

    lib_ep = {}
    title_list = []
    for i in range(0, quantity_of_series):
        try:
            if(i==2)or(i==4):
                title_list.append("error")
                continue
            season_group = web_controller.find_element(By.CSS_SELECTOR, "#group-tv > ul")
            title_list.append(season_group.find_elements(By.CLASS_NAME, "box-title"))

            current_title = title_list[i][i].text
            ActionChains(web_controller).click(title_list[i][i]).perform()
            time.sleep(1)
            action_list = web_controller.find_element(By.CSS_SELECTOR,"body > div.l-global-width.l-container-primary > div > nav > ul > li:nth-child(2) > a")
            ActionChains(web_controller).click(action_list).perform()
            time.sleep(1)
            episode_list = web_controller.find_element(By.CSS_SELECTOR,"body > div.l-global-width.l-container-primary > div > article > section:nth-child(2) > div.table-responsive > table > tbody")
            time.sleep(1)

            translated_ep = []
            for row in episode_list.find_elements(By.TAG_NAME, "tr"):
                one_line = []
                for kol in row.find_elements(By.TAG_NAME, "td"):
                    one_line.append(kol.text)
                if(one_line[3] == "     ")or(one_line[3] == "   ")or(one_line[3] == " "):
                    translated_ep.append(one_line[0])

            lib_ep[current_title] = translated_ep
            web_controller.get('https://shinden.pl/series/season/current')
            time.sleep(2)
        except(exceptions.NoSuchElementException):
            title_list.append("error")
            web_controller.get('https://shinden.pl/series/season/current')
            time.sleep(2)
            continue

    for title, ep in lib_ep.items():
        print(f'{title[0:40]:<41}{ep}')

    web_controller.quit()
    sleep = input()