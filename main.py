from pathlib import Path
from functools import partial
import time
from datetime import datetime, date, timedelta
import re

import schedule
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
    return page.text

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

def download_video(url):
    # download will be handled by NGSS camera proxy
    r = requests.get(url, stream = True) 
    print(r.status_code)
    return r.status_code


class NGSS_CLI:
    def __init__(self, ip=None, cfg_file="config.yml"):
        # load from config file
        with open(cfg_file, 'r') as f:
            cfg = yaml.safe_load(f.read())
        self.ip_addr = cfg['ip_addr']
        if ip:
            # overwrite ip address
            self.ip_addr = ip
            print("ip addr: ", self.ip_addr)
        self.root_url = ROOT_URL.format(ip_addr=self.ip_addr)
        self.video_url = partial(VIDEO_URL.format, ip_addr=self.ip_addr)

    def list(self, date=None):
        if not date: # list available dates
            content = get_page_content(self.root_url)
            available_records = glob_dates(content)
            print(tabulate(sorted(available_records.items()), headers=["Date", "URL"]))
        else: # list available videos of a date
            content = get_page_content(self.video_url(date=date))
            available_records = glob_hours(content)
            print(tabulate(sorted(available_records.items()), headers=["Hour", "URL"]))

    def download(self, date):
        # download all video of a date
        content = get_page_content(self.video_url(date=date))
        available_records = glob_hours(content)
        for k, v in available_records.items():
            v = "http://localhost:8080"+v
            print(f"downloading {k} using {v}")
            download_video(v)
            time.sleep(150) #  sleep 2.5 min to download current video
            # speed: 150kb/s, regular filesize is about 25MB

    def auto_download(self):
        # start to download previous day's video
        yesterday = date.today() - timedelta(days=1)
        print("yesterday:", yesterday.strftime("%Y%m%d"))
        
        def download_cur():
            yesterday = date.today() - timedelta(days=1)
            date_str = yesterday.strftime("%Y%m%d")
            print(f"downloading {date_str} at {datetime.now()}")
            self.download(date=date_str)


        # download previous day's video at 2am
        schedule.every().day.at("02:00").do(download_cur)

        while True:
            schedule.run_pending()
            time.sleep(300) # sleep for 5 mins

    def test_glob(self, case="date"):
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

    def test_schedule(self, interval=3):
        sec = 0;
        def hello():
            nonlocal sec
            print(f"hello {sec}")
            sec += interval
        
        schedule.every().second.do(hello)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def test_auto_download(self, date):
        # choose date such that previous date has some recordings
        # e.g. 20220402
        date = str(date)
        pretent_date = datetime.strptime(date, "%Y%m%d")
        yesterday = pretent_date - timedelta(days=1)
        print("yesterday:", yesterday.strftime("%Y%m%d"))
        
        cur_date = yesterday
        def download_cur():
            nonlocal cur_date
            date_str = cur_date.strftime("%Y%m%d")
            print(f"downloading {date_str} at {datetime.now()}")
            status = self.download(date=date_str)
            cur_date = cur_date + timedelta(days=1)
            return status

        # download previous day's video right now + 1min
        delayed_time = datetime.now() + timedelta(minutes=1)
        delayed_time = delayed_time.strftime("%H:%M")
        print(f"start downloading at {delayed_time}")
        schedule.every().day.at(delayed_time).do(download_cur)

        while True:
            schedule.run_pending()
            time.sleep(1) # check every second


if __name__ == "__main__":
    fire.Fire(NGSS_CLI)
