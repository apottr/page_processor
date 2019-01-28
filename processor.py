import requests

def runner(url):
    r = requests.get(url)
    print(r.text)