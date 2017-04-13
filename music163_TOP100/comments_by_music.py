"""
根据歌曲 ID 获得所有的歌曲所对应的评论信息
"""

import requests
import sql
import time
import threading
import pymysql.cursors


class Comments(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '_ntes_nnid=7eced19b27ffae35dad3f8f2bf5885cd,1476521011210; _ntes_nuid=7eced19b27ffae35dad3f8f2bf5885cd; usertrack=c+5+hlgB7TgnsAmACnXtAg==; Province=025; City=025; NTES_PASSPORT=6n9ihXhbWKPi8yAqG.i2kETSCRa.ug06Txh8EMrrRsliVQXFV_orx5HffqhQjuGHkNQrLOIRLLotGohL9s10wcYSPiQfI2wiPacKlJ3nYAXgM; P_INFO=hourui93@163.com|1476523293|1|study|11&12|jis&1476511733&mail163#jis&320100#10#0#0|151889&0|g37_client_check&mailsettings&mail163&study&blog|hourui93@163.com; NTES_SESS=Fa2uk.YZsGoj59AgD6tRjTXGaJ8_1_4YvGfXUkS7C1NwtMe.tG1Vzr255TXM6yj2mKqTZzqFtoEKQrgewi9ZK60ylIqq5puaG6QIaNQ7EK5MTcRgHLOhqttDHfaI_vsBzB4bibfamzx1.fhlpqZh_FcnXUYQFw5F5KIBUmGJg7xdasvGf_EgfICWV; S_INFO=1476597594|1|0&80##|hourui93; NETEASE_AUTH_SOURCE=space; NETEASE_AUTH_USERNAME=hourui93; _ga=GA1.2.1405085820.1476521280; JSESSIONID-WYYY=cbd082d2ce2cffbcd5c085d8bf565a95aee3173ddbbb00bfa270950f93f1d8bb4cb55a56a4049fa8c828373f630c78f4a43d6c3d252c4c44f44b098a9434a7d8fc110670a6e1e9af992c78092936b1e19351435ecff76a181993780035547fa5241a5afb96e8c665182d0d5b911663281967d675ff2658015887a94b3ee1575fa1956a5a%3A1476607977016; _iuqxldmzr_=25; __utma=94650624.1038096298.1476521011.1476595468.1476606177.8; __utmb=94650624.20.10.1476606177; __utmc=94650624; __utmz=94650624.1476521011.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'DNT': '1',
        'Host': 'music.163.com',
        'Pragma': 'no-cache',
        'Referer': 'http://music.163.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }


    params = {
        'csrf_token': ''
    }

    data = {
        'params': 'Ak2s0LoP1GRJYqE3XxJUZVYK9uPEXSTttmAS+8uVLnYRoUt/Xgqdrt/13nr6OYhi75QSTlQ9FcZaWElIwE+oz9qXAu87t2DHj6Auu+2yBJDr+arG+irBbjIvKJGfjgBac+kSm2ePwf4rfuHSKVgQu1cYMdqFVnB+ojBsWopHcexbvLylDIMPulPljAWK6MR8',
        'encSecKey': '8c85d1b6f53bfebaf5258d171f3526c06980cbcaf490d759eac82145ee27198297c152dd95e7ea0f08cfb7281588cdab305946e01b9d84f0b49700f9c2eb6eeced8624b16ce378bccd24341b1b5ad3d84ebd707dbbd18a4f01c2a007cd47de32f28ca395c9715afa134ed9ee321caa7f28ec82b94307d75144f6b5b134a9ce1a'
    }


    
    requests.adapters.DEFAULT_RETRIES = 5
    def get_comments(self, music_id, flag):
        self.headers['Referer'] = 'http://music.163.com/playlist?id=' + str(music_id)
        if flag:
            r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                              headers=self.headers, params=self.params, data=self.data)
        else:
            r = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(music_id),
                              headers=self.headers, params=self.params, data=self.data)
        return r.json()


if __name__ == '__main__':
    my_comment = Comments()


    def save_comments(musics, flag, connection0):
        for i in musics:
            my_music_id = i['MUSIC_ID']
            try:
                comments = my_comment.get_comments(my_music_id, flag)
                if comments['total'] > 0:
                    sql.insert_comments(my_music_id, comments['total'], connection0)
            except Exception as e:
                # 打印错误日志
                print(my_music_id)
                print(e)
                time.sleep(5)


    music_before = sql.get_before_music()
    music_after = sql.get_after_music()

    # pymysql 链接不是线程安全的
    connection1 = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xjj520520ljf',
                                  db='duplicate',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)

    connection2 = pymysql.connect(host='localhost',
                                  user='root',
                                  password='xjj520520ljf',
                                  db='duplicate',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)

    t1 = threading.Thread(target=save_comments, args=(music_before, True, connection1))
    t2 = threading.Thread(target=save_comments, args=(music_after, False, connection2))
    t1.start()
    t2.start()