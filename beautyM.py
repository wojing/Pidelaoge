import requests
from bs4 import BeautifulSoup

def parse_index():
    url = "http://www.beautylegmm.com"
    respone = requests.get(url)
    soup = BeautifulSoup(respone.text,"html.parser")

    adumlist = soup.find_all(attrs={"class":"post_weidaopic"})
    # for i in Adum:
    #     print(i.a["href"]+'\t'+i.a["title"])

    try:
        nurl = soup.find(attrs={"class":"next"}).a["href"]
    except:
        print("Can't find next")

    res = requests.get(nurl)
    soup = BeautifulSoup(res.text, "html.parser")

    adumlist2 = soup.find_all(attrs={"class": "post_weidaopic"})

    adumlist.extend(adumlist2)

    parse_adum(adumlist[0].a["href"])

def parse_adum(url):
    aurl = url


    respone = requests.get(aurl)
    soup = BeautifulSoup(respone.text,"html.parser")
    print(soup)
    piclist = soup.find_all(has_real_pic)
    # for i in piclist:
    #     print(i)

    next_url=soup.find(attrs={"class":"next"})["href"]


def has_real_pic(tag):
    return tag.has_attr('alt') and tag.has_attr("src") and tag.has_attr("width")

def main():
    url = "http://www.beautylegmm.com"
    ablumlist = []
    piclist = []
    i = 0
    while(i<1):
        list,nurl = parse_ablum(url)
        ablumlist.extend(list)
        if nurl is not None:
            url = nurl
        else:
            break
        i +=1

    for i in ablumlist:
        url = i.a["href"]

        while(True):
            alist,nurl= parse_pic(url)
            piclist.extend(alist)
            if nurl is not None:
                url = nurl
            else:
                break

    print(piclist)


def parse_ablum(url):
    respone = requests.get(url)
    soup = BeautifulSoup(respone.text, "html.parser")
    list = soup.find_all(attrs={"class": "post_weidaopic"})
    nurl =  soup.find(attrs={"class":"next"}).a["href"]
    return  list,nurl


def parse_pic(url):
    respone = requests.get(url)
    soup = BeautifulSoup(respone.text,"html.parser")
    piclist = soup.find_all(has_real_pic)
    next_url = None
    try:
        next_url = soup.find(attrs={"class": "next"})["href"]
    except:
        next_url = None

    return piclist,next_url


if __name__ == '__main__':
    main()