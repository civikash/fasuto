from mysql.connector import connect, Error
from adminc.models import ReviewsEmployee


def get_data_from_database1(reviews):
    print("Соединение с бд")
    try:
        print("Начато соединение")
        with connect(
            host="localhost",
            user="root",
            password="root",
            database="Mydatabase",
        ) as connection:
            with connection.cursor() as cursor:
                select_movies_query = "SELECT id, re_firstname, re_lastname, office, review_text FROM adminc_reviewsemployee"
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    reviews.append(row[4])
                return reviews
    except Error as e:
        print(e)


def get_data_from_database2(reviews2):
    print("Соединение с бд")
    try:
        print("Начато соединение")
        with connect(
            host="localhost",
            user="root",
            password="root",
            database="Mydatabase",
        ) as connection:
            with connection.cursor() as cursor:
                select_movies_query = "SELECT review_text FROM test_table"
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    reviews2.append(row[0])
                return reviews2
    except Error as e:
        print(e)


def hz(reviews, reviews2):
    print("Соединение с бд")
    try:
        print("Начато соединение")
        with connect(
            host="localhost",
            user="root",
            password="root",
            database="Mydatabase",
        ) as connection:
            with connection.cursor() as cursor:
                for i in reviews:
                    if i in reviews2:
                        # здесь можно сделать вывод на страницу админа для проверки
                        global_check = ReviewsEmployee.objects.filter(id=i.id).update(global_check_review='CHECKING')
                        print(global_check)
    except Error as e:
        print(e)


def main():
    reviews = []
    reviews2 = []
    get_data_from_database1(reviews)
    get_data_from_database2(reviews2)
    hz(reviews, reviews2)
main()