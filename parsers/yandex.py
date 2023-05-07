from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pyautogui
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
                select_movies_query = "SELECT id, re_firstname, re_lastname, office, review_text FROM adminc_reviewsemployee WHERE status_id = '1' AND space_id = '2'"
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    # print(row)
                    id = row[0]
                    name = row[1] + " " + (row[2])
                    href = row[3]
                    review = row[4]
                    print(row)
                    info = [id, name, review, href]
                    rev_info = [name, review]
                    
                    db_all_info.append(info)
                    db_info.append(rev_info)
                    hrefs.append(href)
                    # print(hrefs)
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
                    # print("это i", i)
                    if i in db_info:
                        # print("Ура!!!")
                        d = (db_all_info[count])
                        # print(d)
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

    if date[-4] == '2':
        date_str = date
    else:
        date_str = date + ' ' +str(datetime.today().year)
    day, month_str, year = date_str.split()
    month = months[month_str]
    date_obj = datetime.strptime(f'{day} {month} {year}', '%d %m %Y')
    date_formatted = date_obj.strftime('%d-%m-%y')
    return date_formatted


def get_info(browser, all_information):
    date_formatted = ''
    try:   
        print("должно работать")
        BS_body = BeautifulSoup(browser.page_source, 'lxml')
        all_info = BS_body.find_all("div", class_="business-review-view")

        for f in all_info:
            name = f.find("div", class_="business-review-view__author").find("span").getText() # имя
            # print(name)
            review = f.find("span", class_="business-review-view__body-text").getText() # текст отзыва
            # print(review)
            rating = len(f.find_all("span", class_="_full")) # рейтинг
            
            date = f.find("span", class_="business-review-view__date").find("span").getText() # дата
            # дата берется в формате "3 марта", если год прошлый, то "3 марта 2022"
            all_inform = [name, review]
            # print(all_inform)
            #, rating, get_date(date, date_formatted)
            all_information.append(all_inform)
            print("все ок")
        return all_information
    except:
        pyautogui.alert(text='ЧТО-ТО ПОШЛО НЕ ТАК ПРИ ПАРСИНГЕ ЯНДЕКСА, СООБЩИТЕ АДМИНИСТРАТОРУ', title='Ошибка', button='Закрыть')
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