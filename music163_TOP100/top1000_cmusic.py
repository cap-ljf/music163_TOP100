import pymysql.cursors
import sql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='xjj520520ljf',
                             db='duplicate',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def output_music():
	with connection.cursor() as cursor:
		sql1 = 'select distinct * from musics order by COMMENTS desc'
		cursor.execute(sql1)
		comments = cursor.fetchmany(100)
	with open('T100_music.txt','w') as f:
		for i in comments:
			f.write('%s\n'%str(i))
			print(i)
	


if __name__ == '__main__':

	output_music()
	connection.close()