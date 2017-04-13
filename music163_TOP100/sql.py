"""
一般 Python 用于连接 MySQL 的工具：pymysql
"""
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='xjj520520ljf',
                             db='duplicate',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# 保存评论
def insert_comments(music_id, comments, connection0):
    with connection0.cursor() as cursor:
        sql = "UPDATE  `musics` SET COMMENTS = %s WHERE MUSIC_ID = %s"
        cursor.execute(sql, (comments, music_id))
    connection0.commit()


# 保存音乐
def insert_music(music_id, music_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `musics` (`MUSIC_ID`, `MUSIC_NAME`) VALUES (%s, %s)"
        cursor.execute(sql, (music_id, music_name))
    connection.commit()



# 保存歌手
def insert_artist(artist_id, artist_name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `artists` (`ARTIST_ID`, `ARTIST_NAME`) VALUES (%s, %s)"
        cursor.execute(sql, (artist_id, artist_name))
    connection.commit()


# 获取所有歌手的 ID
def get_all_artist():
    with connection.cursor() as cursor:
        sql = "SELECT `ARTIST_ID` FROM `artists` ORDER BY ARTIST_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取所有音乐的 ID
def get_all_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取前一半音乐的 ID
def get_before_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 0, 30000000"
        cursor.execute(sql, ())
        return cursor.fetchall()


# 获取后一半音乐的 ID
def get_after_music():
    with connection.cursor() as cursor:
        sql = "SELECT `MUSIC_ID` FROM `musics` ORDER BY MUSIC_ID LIMIT 30000000, 472000000"
        cursor.execute(sql, ())
        return cursor.fetchall()


def dis_connect():
    connection.close()
