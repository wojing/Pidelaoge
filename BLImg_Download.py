import sys
import os
import threading
import pymysql
import time
import requests
import queue

host = "http://www.beautylegmm.com"
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wojing', db='work',charset='utf8')
blpath = "E:\python project\\bl"

cur = conn.cursor()

def imgDownload(item):
    url = host+ item[1]
    name = item[1].split('/')[-1]
    bldir = blpath+'\\'+item[0].split(' - ')[0]
    file_name = bldir + '\\'+name

    if not os.path.exists(bldir):
        os.makedirs(bldir)

    r = requests.session()
    r.adapters.DEFAULT_RETRIES = 200
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    ### download with requets

    if not os.path.exists(file_name):
        r = requests.get(url, headers= header , stream= True)
        with open(file_name,'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            print("File %s is downloaded." % file_name)
            f.close()

    ### download with curl TODO


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wojing', db='work', charset='utf8')


class TaskQueue():
    def __init__(self,ablum_list):
        self.cur = conn.connect()
        sql = "select * from bl_ablum_detail where ablum_no in ( %s ) " % ablum_list
        cur.execute(sql)

        self.queue = queue.Queue()
        self.flag = False
        self.addTask()


    def addTask(self,num =100000):

        for i in range(num):
            row = cur.fetchone()
            if row is None:
                self.flag = True
                break
            else:
                self.queue.put(row)

        return self.flag


class ImgDownload(threading.Thread):
    def __init__(self,TaskQueue):
        threading.Thread.__init__(self)
        self.queue = TaskQueue

    def run(self):
        while(True):
            if self.queue.queue.empty():
                self.queue.queue.task_done()
                break
            item = self.queue.queue.get()
            try:
                imgDownload(item)
            except:
                print("Unexpected error:", sys.exc_info())
                pass
            finally:
                self.queue.queue.task_done()

def main():
    ts = time.time()
    queue = TaskQueue()
    for x in range(8):
        downloader = ImgDownload(queue)
        downloader.daemon=True
        downloader.start()

    queue.queue.join()


    # print('Took {}s'.format(time.time() - ts))

				#flag = self.queue.addTask()
                #if flag:
                    #self.queue.queue.task_done()
                    #break
if __name__ == '__main__':
    main()