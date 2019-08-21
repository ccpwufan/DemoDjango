import MySQLdb
import pymongo
from movie_base import MovieBase

def test():
    db = MySQLdb.connect("localhost", "python", "python123", "pytestdb", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM MOVIES")
    data = cursor.fetchall()
    print(data)
    db.close()


    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["pytestdb"]
    mycol = mydb["movies"]
    print(mycol.find_one())


def DBfetchallMongoDB(name='', actors=''):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["pytestdb"]
    mycol = mydb["movies"]

    cur = mycol.find()
    movies = []
    for row in cur:
        # print(row)
        mv = MovieBase(no=row['no'], name=row['name'], actors=row['actors'], time=row['time'], score=row['score'])
        movies.append(mv)
    print("return list of movie objects..", movies)
    return movies


if __name__ == '__main__':
    x = DBfetchallMongoDB()
    print(x)
