import os
import datetime

import dask
import requests

@dask.delayed()  # make this function lazy
def download(base_url, file):
    if file.startswith(("a", "b")):
        os.system(f"wget -nc {base_url}/{file}")
        os.system(f"gunzip {file}")

years = range(1850, datetime.datetime.utcnow().year)
jobs = []
for year in years:
    base_url = f"https://ftp.nhc.noaa.gov/atcf/archive/{year}/"  # base base_url
    resp = requests.get(base_url)  # get listing of base_url

    file_list = [
        line.split(">")[0].strip('"')  # extract the file from the <a href> tag
        for line in resp.content.decode().split("a href=")  # loop through each <a href> tag
        if ".gz" in line # only keep the line if it contains "gz"
    ]

    jobs.extend([download(base_url, file) for file in file_list])  # queue the jobs

dask.compute(jobs, num_workers=4)  # download in parallel

