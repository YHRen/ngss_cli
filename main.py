from pathlib import Path
from functools import partial
import re
import requests
import yaml 
import fire
from bs4 import BeautifulSoup
from tabulate import tabulate

ROOT_URL = "http://localhost:8080/VIDEO0?translate=xcam&dest-host={ip_addr}"
VIDEO_URL = "http://localhost:8080/VIDEO0/{date}?translate=xcam&dest-host={ip_addr}"
DATE_PTR = re.compile("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


def get_page_content(url):
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    return page.content

def glob_hours(content):
    soup = BeautifulSoup(content, "html.parser")
    ans = {}
    for table_cell in soup.find_all("tr"):
        link = table_cell.find('a')
        if link and link.get('href') and link.text.endswith(".mpg"):
            for td in table_cell.find_all("td"):
                if DATE_PTR.match(td.text):
                    ans[td.text] = link.get('href')
    
    return ans

def glob_dates(content):
    soup = BeautifulSoup(content, "html.parser")
    ans = {}
    for table_cell in soup.find_all("tr"):
        link = table_cell.find('a')
        if link and link.get('href') and link.text.isdigit():
            ans[link.text] = link.get('href')
    
    return ans


class NGSS_CLI:
    def __init__(self, ip=None, cfg_file="config.yml"):
        with open(cfg_file, 'r') as f:
            cfg = yaml.safe_load(f.read())
        self.ip_addr = cfg['ip_addr']
        if ip:
            self.ip_addr = ip
            print("ip addr: ", self.ip_addr)
        self.root_url = ROOT_URL.format(ip_addr=self.ip_addr)
        self.video_url = partial(VIDEO_URL.format, ip_addr=self.ip_addr)

    def list(self, date=None):
        if not date:
            content = get_page_content(self.root_url)
            available_records = glob_dates(content)
            print(tabulate(available_records))
        else:
            content = get_page_content(self.video_url(date=date))
            available_records = glob_hours(content)
            print(tabulate(available_records))

    def test(self, case="date"):
        if case == "date":
            with open(Path("./resources/web_source_video.html"), 'r') as f:
                content = f.read()
            available_records = glob_dates(content)
            print(tabulate(sorted(available_records.items()), headers=["Date", "URL"]))
        elif case == "hour":
            with open(Path("./resources/web_source_day.html"), 'r') as f:
                content = f.read()
            available_records = glob_hours(content)
            print(tabulate(sorted(available_records.items()), headers=["Hour", "URL"]))

        else:
            raise ValueError(f"{case} Not supported")


if __name__ == "__main__":
    fire.Fire(NGSS_CLI)
