import csv,sys,re,requests
from bs4 import BeautifulSoup
from selector import load,freq_sel

selectors = None

def load_webpage(row):
    import urllib3
    urllib3.disable_warnings()
    url = row["website"]
    try:
        r = requests.get(url,headers={"User-Agent": "firefox"},verify=False)
    except Exception as e:
        print(url)
        raise e
    soup = BeautifulSoup(r.text,"html.parser")
    return (soup,url)

def test_selector2(url,sel):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    return r.html.find(sel)

def test_selector(url,sel):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    return [re.sub(r"\s{2,}","",i.text) for i in soup.select(sel)]

def test_selector3(soup,sel):
    return set(filter(lambda x: len(x.split(" ")) > 2 ,[re.sub(r"\s{2,}","",i.text) for i in soup.select(sel)]))

def processor(row,index):
    url = row["website"]
    try:
        a = input(f"{url} ({index}/764) : ")
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

def heuristic_processor(soup,index,nest=""):
    best = ("",[])
    if nest == "":
        for entry in selectors:
            try:
                output = test_selector3(soup[0],entry)
            except Exception as e:
                #output = []
                print(e)
                pass
            if len(output) > len(best[1]):
                best = (entry,output)
        if len(best[1]) > 40:
            return best[0]
        elif len(best[1]) == 0:
            return "skip"
        print(f"{soup[1]} ({index}/764)\nbest selector: {best[0]}\noutput: {best[1]}\nlength: {len(best[1])}")
    if nest == "":
        data = input(f"ENTER to confirm or write new selector to test: ")
    else:
        try:
            d = test_selector3(soup[0],nest)
            print(d,f"length: {len(d)}")
        except Exception as e:
            print(e)
            pass
        data = input(f"did it work? (Y/n): ")
    if data not in "Yy ":
        return heuristic_processor(soup,index,nest=data)
    else:
        if nest:
            return nest
        else:
            return best[0]

def remove_selectors(item):
    item.popitem()
    return item

def main():
    fn = ["callsign","lat","lon","website","logo"]
    fns = fn+["selector"]
    index = 0
    with open("affiliate.csv","r") as f:
        with open("aff-final.csv","r+") as j:
            w = csv.DictWriter(j,fieldnames=fns)
            r = csv.DictReader(f,fieldnames=fn)
            sites = [remove_selectors(item) for item in csv.DictReader(j,fieldnames=fns)]
            r.__next__()
            for line in r:
                index += 1
                if not line in sites:
                    if line["website"]:
                        #line["selector"] = processor(line,index)
                        line["selector"] = heuristic_processor(load_webpage(line),index)
                        w.writerow(line)
                else:
                    continue
                if index % 5:
                    l = load()
                    selectors = freq_sel(l,top=None)
                    del l

if __name__ == "__main__":
    l = load()
    selectors = freq_sel(l,top=None)
    del l
    main()
    #test_selector2("http://www.abc6.com","div.CardList-item-title")
