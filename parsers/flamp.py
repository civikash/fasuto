import undetected_chromedriver
import time
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from datetime import datetime

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
    print(date)
    date = date.lstrip()
    date = date.rstrip()
    print(date)
    if date[-4] == '2':
        date = date
    else:
        date = (date[:-7]) + ' ' +str(datetime.today().year)
    print(date)
    day, month_str, year = date.split()
    month = months[month_str]
    date_obj = datetime.strptime(f'{day} {month} {year}', '%d %m %Y')
    date_formatted = date_obj.strftime('%d-%m-%y')
    return date_formatted


def scrolling(browser, names, rev_numbers, all_info):
    info = ()
    date_formatted = ''

    browser.refresh()
    browser.implicitly_wait(30)
    while True:
        # Проматываем страницу вниз
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-cat-elements-button--next")))
        except Exception as e:
            continue  # Не нашли элемент, попробуем на следующей итерации
        actions = ActionChains(browser)
        actions.move_to_element(element).perform()

        try:
            time.sleep(3)
            all_page = BeautifulSoup(browser.page_source, 'lxml')
            try:
                rev_number = int(all_page.find("section", class_="ugc-feed").find("div", class_="hg-row__side").getText())
                # количество отзывов на странице
            except:
                pass
            all_names = all_page.find_all("li", class_="ugc-list__item")
            for f in all_names:
                name = f.find("a", class_="name").getText() # имя
                name = name[3:-2]

                rating = f.find("li", class_="review-estimation__item--checked").getText() # оценка в отзыве
                
                review = f.find("div", class_="js-ugc-item-text-full").find("p", class_="t-rich-text__p").getText() # текст отзыва
            
                if name not in names:
                    review = review[7:-6]
                    review = review.replace("\t", "")
                    rating = rating[5:-4]
                    date = f.find("a", class_="ugc-date").getText()

                    names.append(name)
                    info = (name, rating, review)
                    all_info.append(info)
                
            
            element.click()
        except WebDriverException:
            rev_numbers.append(rev_number)
            # print(info)
            return names, rev_numbers, all_info

def main():
    names = []
    rev_numbers = []
    all_info = []

    options = webdriver.ChromeOptions()
    options.headless = True
    browser = undetected_chromedriver.Chrome(options)
    browser.get("https://barnaul.flamp.ru/firm/yurist_dlya_lyudejj_ooo-70000001059119138")
    browser.implicitly_wait(30)

    scrolling(browser, names, rev_numbers, all_info)
    print(all_info)

    while True:
        if len(names) == rev_numbers[0]:
            print("Все сработано правильно")
            break
        else:
            print("Что-то сломалось")
            break
            # scrolling(browser, names, rev_numbers)

    browser.close()
    browser.quit()

main()