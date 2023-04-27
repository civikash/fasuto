from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.common.exceptions import WebDriverException
from mysql.connector import connect, Error
import csv
import socket
import time


REMOTE_SERVER = "one.one.one.one" 
def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2) 
        s.close()
        return True
    except Exception:
        pass
    return False


def hrefs_from_yandex_csv(all_hrefs):
    with open("parsers/org_data/yandex_data.csv", encoding='utf-16') as r_file:
        file_reader = csv.reader(r_file, delimiter = ";")
        for row in file_reader:
                z = row[4] + "reviews"
                all_hrefs.append(z)
        return all_hrefs
                

def hrefs_from_gis_csv(all_hrefs):
    with open("parsers/org_data/gis_data.csv", encoding='utf-16') as r_file:
        file_reader = csv.reader(r_file, delimiter = ";")
        for row in file_reader:
                z = row[4] + "/tab/reviews"
                all_hrefs.append(z)
        return all_hrefs


def parse_yandex(browser):
    all_inform = []
    if is_connected(REMOTE_SERVER):
        try:
            BS_body = BeautifulSoup(browser.page_source, 'lxml')
            all_info = BS_body.find_all("div", class_="business-review-view")
            for f in all_info:
                name = f.find("div", class_="business-review-view__author").find("span").getText() # текст отзыва
                review = f.find("span", class_="business-review-view__body-text").getText() # текст отзыва
                info = [name, review]
                all_inform.append(info)
                print("данные собраны")
            print(all_inform)
            insert_data_in_database(all_inform)
        except:
            pass
    else:
        print("СОЕДИНЕНИЕ УТРАЧЕНО")
        time.sleep(30)
        is_connected(REMOTE_SERVER)


def parse_gis(browser):
    all_inform = []
    if is_connected(REMOTE_SERVER):
        try:
            print("начат парсинг гис")
            reviews_count = int(browser.find_element(By.CLASS_NAME, "_1xhlznaa").text)
            organisation_name = browser.find_element(By.CLASS_NAME, "_tvxwjf")

            if reviews_count < 12:
                zagl2 = BeautifulSoup(browser.page_source, 'lxml')
                all_names = zagl2.find_all("div", class_="_11gvyqv")
                for f in all_names:
                    name = f.find("span", class_="_16s5yj36").getText() # имя
                    review_text = f.find("a", class_="_ayej9u3")
                    if review_text is None:
                        review_text = f.find("a", class_="_1it5ivp")
                    review = review_text.getText() # текст отзыва
                    info = [name, review]
                    print(info)
                    all_inform.append(info)
                insert_data_in_database(all_inform)
            else:
                while True:
                    # Проматываем страницу вниз
                    browser.execute_script("arguments[0].scrollIntoView();", organisation_name)

                    try:
                        upload_button = browser.find_element(By.CLASS_NAME, "_1iczexgz")
                    except Exception as e:
                        continue  # Не нашли элемент, попробуем на следующей итерации

                    actions = ActionChains(browser)
                    actions.move_to_element(upload_button).perform()

                    try:
                        browser.implicitly_wait(10)
                        upload_button = browser.find_element(By.CLASS_NAME, "_1iczexgz")
                    except WebDriverException:
                        print("Все долистано")
                        zagl2 = BeautifulSoup(browser.page_source, 'lxml')
                        all_names = zagl2.find_all("div", class_="_11gvyqv")

                        for f in all_names:
                            name = f.find("span", class_="_16s5yj36").getText() # имя
                            review_text = f.find("a", class_="_ayej9u3")
                            if review_text is None:
                                review_text = f.find("a", class_="_1it5ivp")
                            review = review_text.getText() # текст отзыва
                            info = [name, review]
                            print(info)
                            all_inform.append(info)
                        insert_data_in_database(all_inform)
                        break
        except:
            pass
    else:
        print("СОЕДИНЕНИЕ УТРАЧЕНО")
        time.sleep(30)
        is_connected(REMOTE_SERVER)


def insert_data_in_database(all_info):
    try:
        with connect(
            host="localhost",
            user="root",
            password="root",
            database="Mydatabase",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.executemany('INSERT INTO test_table(name, review_text) VALUES (%s,%s)', all_info)
                connection.commit()
                print("успешно")

    except Error as e:
        print(e)


def main():
    all_hrefs = []

    options = webdriver.ChromeOptions()
    options.headless = True
    hrefs_from_yandex_csv(all_hrefs)
    hrefs_from_gis_csv(all_hrefs)

    for i in all_hrefs:
        # print(i)
        browser = webdriver.Chrome(executable_path="parsers/chromedriver", options = options) 
        browser.maximize_window()
        browser.get(i)
        if "yandex.ru" in i:
            print("это яндекс")
            parse_yandex(browser)
        if "2gis.ru" in i:
            print("это гис")
            parse_gis(browser)
        print("успешно прошла организация")
    browser.close()
    browser.quit()
main()

# яндекс
# 1) зашли на сайт по ссылке
# 2) взяли данные через бс4
# 3) 2  пункт обернуть в трай эксепт, если отзывов нет, то выйдет на ошибку 404

# 2гис
# 1) зашли на сайт по ссылке
# 2) взяли данные через бс4
# 3) 2 пункт обернуть в трай эксепт, на сайт зайдет нормально, 
# уведомление об отсутствии отзывов есть на карточке орг.
