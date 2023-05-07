from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.common.exceptions import WebDriverException
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from mysql.connector import connect, Error


def get_data_from_database(db_info, db_all_info, hrefs):
    print("Соединение с бд")
    try:
        print("Начато соединение")
        with connect(
            user="fasuto",
            password="123qweASD",
            host="localhost",
            port=3306,
            database="branch_db",
        ) as connection:
            with connection.cursor() as cursor:
                select_movies_query = "SELECT id, re_firstname, re_lastname, office, review_text FROM adminc_reviewsemployee WHERE status_id = '1' AND space_id = '1'"
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    id = row[0]
                    name = row[1] + " " + (row[2])
                    href = row[3]
                    review = row[4]
                    info = [id, name, review, href]
                    rev_info = [name, review]
                    
                    db_all_info.append(info)
                    db_info.append(rev_info)
                    hrefs.append(href)
                return db_all_info, db_info, hrefs

    except Error as e:
        print(e)


def update_data_from_database(db_all_info, db_info, all_information, count):
    try:
        with connect(
            user="fasuto",
            password="123qweASD",
            host="localhost",
            port=3306,
            database="branch_db",
        ) as connection:
            with connection.cursor() as cursor:
                count = 0
                for i in all_information:
                    print("это i", i)
                    if i in db_info:
                        # print("Ура!!!")
                        d = (db_all_info[count])
                        print(d)
                        count += 1
                        f = str(d[0])
                        update_query = (f"""
                        UPDATE
                            adminc_reviewsemployee
                        SET
                            status_id = '2'
                        WHERE
                            id = '{f}'
                        """)
                        print("Запись о " + f + " id была успешно добавлена")
                        with connection.cursor() as cursor:
                            cursor.execute(update_query)
                            connection.commit()
                    else:
                        pass
    except Error as e:
        print(e)


def get_date(date, date_formatted):
    months = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
    }

    if "," in date:
        print("Запятая есть")
        date = (date.split(","))[0]
    day, month_str, year = date.split()
    month = months[month_str]
    date_obj = datetime.strptime(f'{day} {month} {year}', '%d %m %Y')
    date_formatted = date_obj.strftime('%d-%m-%y')
    return date_formatted


def get_info(browser, all_information):
    date_formatted = ''

    try:

        organisation_name = browser.find_element(By.CLASS_NAME, "_tvxwjf")
        reviews_number = browser.find_element(By.CLASS_NAME, "_1xhlznaa").text
        if int(reviews_number) < 12:
            zagl2 = BeautifulSoup(browser.page_source, 'lxml')
            all_names = zagl2.find_all("div", class_="_11gvyqv")

            for f in all_names:
                name = f.find("span", class_="_16s5yj36").getText() # имя

                review_text = f.find("a", class_="_ayej9u3")
                if review_text is None:
                    review_text = f.find("a", class_="_1it5ivp")
                review = review_text.getText() # текст отзыва

                rating = len(f.find("div", class_="_1fkin5c").find_all("span")) # рейтинг

                date = f.find("div", class_="_4mwq3d").getText() # дата

                all_data = [name, review]
                all_information.append(all_data)
                # rating, get_date(date, date_formatted)
            return all_information
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

                        rating = len(f.find("div", class_="_1fkin5c").find_all("span")) # рейтинг

                        date = f.find("div", class_="_4mwq3d").getText() # дата

                        all_data = [name, review]
                        all_information.append(all_data)
                        # rating, get_date(date, date_formatted)
                    return all_information
    except:
        # pyautogui.alert(text='ЧТО-ТО ПОШЛО НЕ ТАК ПРИ ПАРСИНГЕ ЯНДЕКСА, СООБЩИТЕ АДМИНИСТРАТОРУ', title='Ошибка', button='Закрыть')
        exit()


def main():
    all_information = []
    db_info = []
    db_all_info = []
    hrefs = []
    count = 0

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        get_data_from_database(db_info, db_all_info, hrefs)
        for i in hrefs:
            driver.get(i)
            all_information = get_info(driver, all_information)
        all_information = update_data_from_database(db_all_info, db_info, all_information, count) 
    finally:
        driver.quit()

main()