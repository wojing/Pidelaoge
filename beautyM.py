import requests
import time
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wojing', db='work',charset='utf8')

def has_real_pic(tag):
    return tag.has_attr('alt') and tag.has_attr("src") and tag.has_attr("width")




def main():

    cur = conn.cursor()
    cur.execute("truncate  bl_ablum_list")
    cur.execute("truncate  bl_ablum_detail")

    url = "http://www.beautylegmm.com"
    ablumlist = []
    piclist = []
    i = 1

    while(i<2):
        list,nurl = parse_ablum(url)
        import_ablum(cur,list)
        ablumlist.extend(list)
        time.sleep(0.1)
        if nurl is not None:
            url = nurl
        else:
            break
        i +=1
        print("ablum %d" % i)
    print(time.ctime())

    # with open("ablumlist.txt","w") as ablumlist_file:
    #     ablumlist_file.writelines(["%s\n" % item for item in ablumlist])


    ablum_new = getNewAblum(cur,ablumlist)



    print("ablum_new num is %s"  % len(ablum_new))


    s = 1
    errorPage_list =[]
    for h in ablum_new:
        url = h.a["href"]

        while(True):
            try:
                alist,nurl= parse_pic(url)
                import_pic(cur,alist)
                # piclist.extend(alist)
                time.sleep(0.1)
                s += 1
                print("pic %d" % s)
            except:
                errorPage_list.extend(url)
                break

            if nurl is not None:
                url = nurl
            else:
                break
    print("end of normal")

    print("error page num is %d" % len(errorPage_list) )

    err = 0


    errorPage_final_list=[]

    for e in errorPage_list:
        url = e
        while(True):
            try:
                alist, nurl = parse_pic(url)
                import_pic(cur, alist)
                # piclist.extend(alist)
                time.sleep(0.1)
                err += 1
                print("pic_err %d" % err)
            except:
                 errorPage_final_list.extend(url)
                 break

            if nurl is not None:
                url = nurl
            else:
                break

    print("error page handled num is %d" % len(errorPage_final_list) )


    cur.close()
    conn.close()


def parse_ablum(url):
    r = requests.session()
    # r.keep_alive = False
    r.adapters.DEFAULT_RETRIES = 200
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    respone = r.get(url,headers = header)
    soup = BeautifulSoup(respone.text, "html.parser")
    list = soup.find_all(attrs={"class": "post_weidaopic"})
    # nurl = None
    try:
        nurl = soup.find(attrs={"class":"next"}).a["href"]
    except:
        nurl = None
    r.close()
    return  list,nurl


def parse_pic(url):
    r = requests.session()
    # r.keep_alive = False
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    r.adapters.DEFAULT_RETRIES = 10
    respone = r.get(url,headers = header)
    soup = BeautifulSoup(respone.text,"html.parser")
    piclist = soup.find_all(has_real_pic)
    next_url = None
    try:
        next_url = soup.find(attrs={"class": "next"})["href"]
    except:
        next_url = None
    r.close()
    return piclist,next_url


def import_ablum(cur,list):
    for i in list:
        ablum_url = i.div.a['href']
        ablum_name = i.div.a.text.replace("'","\\'")

        ablum_no = ablum_name.split(" ")[2]

        print(ablum_name)
        print(ablum_url)
        print(ablum_no)

        cur.execute("insert into bl_ablum_list values( '%s', '%s', '%s')" % ( ablum_name, ablum_url, ablum_no ) )
    conn.commit()

def import_pic(cur,list):
    for i in list:
        pic_url =  i["src"]
        pic_name = i["alt"].replace("'","\\'")
        pic_no = pic_name.split(" ")[2]
        sql = "insert into bl_ablum_detail values('%s','%s','%s') " % (pic_name,pic_url,pic_no )
        cur.execute(sql )
    conn.commit()


def import_errorPage(cur,list):
    for i in list:
        sql = "insert into "
    pass


def getNewAblum(cur,list):
    ablum_new =[]
    for i in list:
        no = i.div.a.text.replace("'","\\'").split(" ")[2]
        sql =("select * from bl_ablum_list where ablum_no = '%s' " % no)
        row_count = cur.execute(sql)
        if row_count == 0 :
           ablum_new.extend(i)

    return ablum_new





if __name__ == '__main__':
    print("starttime %s" % time.ctime())
    main()

    print("endtime %s " % time.ctime())