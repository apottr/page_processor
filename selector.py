import csv
from operator import gt

def load():
    selectors = []
    with open("aff-final.csv") as f:
        reader = csv.DictReader(f,fieldnames=["callsign","lat","lon","website","logo","selectors"])
        reader.__next__()
        for entry in reader:
            selectors.append(entry["selectors"])
    return selectors

def frequency_sel(selectors):
    d = {}
    out = []
    max = ""
    for item in selectors:
        if item in d:
            d[item] += 1
        else:
            d[item] = 1
    for i in range(0,5):
        max = list(d.keys())[0]
        for item in d:
            if gt(d[item],d[max]):
                max = item
        out.append(max)
        del d[max]
    return out

def freq_sel(selectors,top=10):
    uniq = set(selectors)
    d = sorted([(sel, selectors.count(sel)) for sel in uniq],key=lambda k: k[1],reverse=True)
    if top != None:
        return [k[0] for k in d[:(top+1)]]
    else:
        return [k[0] for k in d]

if __name__ == "__main__":
    sel = load()
    print(freq_sel(sel))