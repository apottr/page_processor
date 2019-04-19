import requests,re
import geopandas as gp
import pandas as pd
from shapely.geometry import Point
from bs4 import BeautifulSoup

def load_csv():
    df = pd.read_csv("aff-final.csv",sep=",")
    df["geometry"] = df.apply(lambda z: Point(z.lon,z.lat),axis=1)
    return gp.GeoDataFrame(df)

def grabber(url,sel):
    r = requests.get(url,headers={"User-Agent": "firefox"},verify=False)
    soup = BeautifulSoup(r.text,"html.parser")
    return list(filter(lambda x: len(x.split(" ")) > 2 ,[re.sub(r"\s{2,}","",i.text) for i in soup.select(sel)]))

def bbox_intersects(gdf,bbox):
    nw,se = bbox["nw"],bbox["se"]
    return gdf.cx[nw[0]:se[0],nw[1]:se[1]]

def get_points_from_bbox(bbox):
    df = load_csv()
    d = bbox_intersects(df,bbox)
    out = []
    for row in d.itertuples():
        out.append(renderer(row))
    return out


def renderer(row):
    return {
        "callsign": getattr(row,"callsign"),
        "geo": {"lat": getattr(row,"lat"), "lon": getattr(row,"lon")},
        "url": getattr(row,"website"),
        "thumbnail": getattr(row,"logo"),
        "headlines": grabber(getattr(row,"website"),getattr(row,"selectors"))
    }

if __name__ == "__main__":
    bounds = {"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }
    #bounds = {"nw":[-114.8184,31.3322],"se": [-109.0452,37.0043] }
    print(get_points_from_bbox(bounds))