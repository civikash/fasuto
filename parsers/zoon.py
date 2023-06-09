from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from mysql.connector import connect, Error

all_information = []

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
                select_movies_query = "SELECT id, re_firstname, re_lastname, office, review_text FROM adminc_reviewsemployee WHERE status_id = '1' AND space_id = '4'"
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    #print(row)
                    id = row[0]
                    name = row[1] + " " + (row[2])
                    href = row[3]
                    review = row[4]
                    #print(row)
                    info = [id, name, review, href]
                    rev_info = [name, review]
                    
                    db_all_info.append(info)
                    db_info.append(rev_info)
                    hrefs.append(href)
                    print(hrefs)
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
                print("ALL_INFORMATION", all_information)
                for i in all_information:
                    print("это i", i)
                    if i in db_info:
                        print("Ура!!!")
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
    return all_information


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

    date = date.lstrip()
    date = date.rstrip()
    date = date[:-7]
    date = date.rstrip()
    day, month_str, year = date.split()
    month = months[month_str]
    date_obj = datetime.strptime(f'{day} {month} {year}', '%d %m %Y')
    date_formatted = date_obj.strftime('%d-%m-%y')
    return date_formatted



def get_info(browser, all_information):
    date_formatted = ''

    try:
        zagl2 = BeautifulSoup(browser.page_source, 'lxml')
        all_names = zagl2.find_all("div", class_="comment-container-wrapper")

        for f in all_names:
            name = f.find("a", class_="name").getText() # имя
            if name == "Официальный комментарий заведения":
                pass
            else:
                review_text = f.find("span", class_="js-comment-content").getText() # отзыв
                review_text = review_text.replace("\xa0", " ")
                print('REVIE_TEXT', review_text)

                rating = ((f.find("span", class_="stars-rating-text").getText()).split(','))[0] # рейтинг
                date = f.find("span", class_="z-text--dark-gray").getText() # дата
                # print("data", date)
                all_data = [name, review_text]
                print('ALL_DATA PRINT: ', all_data)
                # rating, get_date(date, date_formatted)
                all_information.append(all_data)
                print('ALL_DATA ВМЕСТЕ С ALL_INFORMATION PRINT: ', all_information)
        print("ALL_INFORMATION PRINT FINAL CHECK: ", all_information)  # добавить эту строку для проверки
    except:
        pass
        print("жорпка")
    return all_information

    

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