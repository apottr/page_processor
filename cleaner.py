import csv
#from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup

def test_selector2(url,sel):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    return r.html.find(sel)

def test_selector(url,sel):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    return [i.text for i in soup.select(sel)]

def processor(row):
    url = row["website"]
    a = input(f"{url} : ")
    try:
        print(test_selector(url,a))
    except:
        pass
    b = input("did it work? (Y/n): ")
    if b not in ["Y","y",""]:
        return processor(row)
    else:
        return a

def main():
    fn = ["callsign","lat","lon","website","logo"]
    fns = fn+["selector"]
    with open("affiliate.csv","r") as f:
        with open("aff-final.csv","r+") as j:
            w = csv.DictWriter(j,fieldnames=fns)
            r = csv.DictReader(f,fieldnames=fn)
            lastSite = list(reversed(list(csv.DictReader(j,fieldnames=fns))))
            hasHit = False
            r.__next__()
            for line in r:
                if hasHit:
                    if line["website"]:
                        line["selector"] = processor(line)
                        w.writerow(line)
                elif line["website"] == lastSite[0]["website"]:
                    hasHit = True
                    del lastSite
                    continue
                else:
                    continue

if __name__ == "__main__":
    main()
    #test_selector2("http://www.abc6.com","div.CardList-item-title")