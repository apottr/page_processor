import csv,sys,re,requests
from bs4 import BeautifulSoup

def test_selector2(url,sel):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    return r.html.find(sel)

def test_selector(url,sel):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    return [re.sub(r"\s{2,}","",i.text) for i in soup.select(sel)]

def processor(row,index):
    url = row["website"]
    try:
        a = input(f"{url} ({index}/662) : ")
        try:
            print(test_selector(url,a))
        except:
            pass
        b = input("did it work? (Y/n): ")
        if b not in ["Y","y",""]:
            return processor(row,index)
        else:
            return a
    except KeyboardInterrupt:
        sys.exit(0)

def main():
    fn = ["callsign","lat","lon","website","logo"]
    fns = fn+["selector"]
    index = 0
    with open("affiliate.csv","r") as f:
        with open("aff-final.csv","r+") as j:
            w = csv.DictWriter(j,fieldnames=fns)
            r = csv.DictReader(f,fieldnames=fn)
            lastSite = list(reversed(list(csv.DictReader(j,fieldnames=fns))))
            hasHit = False
            r.__next__()
            for line in r:
                index += 1
                if hasHit:
                    if line["website"]:
                        line["selector"] = processor(line,index)
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
