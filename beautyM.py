import requests
import time
from bs4 import BeautifulSoup


def has_real_pic(tag):
    return tag.has_attr('alt') and tag.has_attr("src") and tag.has_attr("width")

def main():
    url = "http://www.beautylegmm.com"
    ablumlist = []
    piclist = []
    i = 1

    while(i):
        list,nurl = parse_ablum(url)
        ablumlist.extend(list)
        if nurl is not None:
            url = nurl
        else:
            break
        i +=1
        print("ablum %d" % i)
    print(time.ctime())

    with open("ablumlist.txt","w") as ablumlist_file:
        ablumlist_file.writelines(["%s\n" % item for item in ablumlist])

    s = 1
    errorPage_list =[]
    for h in ablumlist:
        url = h.a["href"]

        while(True):
            try:
                alist,nurl= parse_pic(url)
                piclist.extend(alist)
                time.sleep(0.5)
                s += 1
                print("pic %d" % s)
            except:
                errorPage_list.extend(url)
                break

            if nurl is not None:
                url = nurl
            else:
                break
    print("end of pic")

    with open("m.txt","w") as f:
        f.writelines(["%s\n" % item for item in piclist])


def parse_ablum(url):
    r = requests.session()
    # r.keep_alive = False
    r.adapters.DEFAULT_RETRIES = 2000
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
        nurl =  soup.find(attrs={"class":"next"}).a["href"]
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


if __name__ == '__main__':
    print("starttime %s" % time.ctime())
    main()
    print("endtime %s " % time.ctime())