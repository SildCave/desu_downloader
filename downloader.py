import sys
import subprocess
import os
import argparse
import time
import zipfile
import requests
import threading

def install(package):
    subprocess.check_output([sys.executable, "-m", "pip", "install", package])

try:
    from selenium import webdriver
except ImportError:
    install("selenium")
    from selenium import webdriver
    
try:
    from bs4 import BeautifulSoup as BS
except ImportError:
    install("beautifulsoup4")
    from bs4 import BeautifulSoup as BS

#https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
#https://github.com/yt-dlp/yt-dlp

try:
    os.mkdir('tools')
except FileExistsError:
    pass

if not os.path.exists("tools/msedgedriver.exe"):

    r = requests.get("https://msedgedriver.azureedge.net/102.0.1245.33/edgedriver_win32.zip")
    open("tools/edgedriver_win32.zip", 'wb').write(r.content)

    with zipfile.ZipFile("tools/edgedriver_win32.zip", 'r') as zip_ref:
        zip_ref.extract("msedgedriver.exe", path = "tools")

    os.remove("tools/edgedriver_win32.zip")

if not os.path.exists("tools/yt-dlp.exe"):

    r = requests.get("https://github.com/yt-dlp/yt-dlp/releases/download/2022.05.18/yt-dlp.exe")
    open("tools/yt-dlp.exe", 'wb').write(r.content)

parser = argparse.ArgumentParser()
parser.add_argument('--link', type=str, required=True, help="link to anime desu")
parser.add_argument('--path', type=str, required=False, help="path")
args = parser.parse_args()

executable = "tools/yt-dlp.exe"

op = webdriver.EdgeOptions()
op.add_argument('--headless')

desu_link = args.link

browser = webdriver.Edge(executable_path="tools/msedgedriver.exe", options=op)
browser.get(desu_link)

series_title = desu_link.split('/')[4]

html_source = browser.page_source

soup = BS(html_source, features="html.parser")

episodes = soup.findAll("li", {"data-index" : True})

if args.path:
   path_to_save =  f"{args.path}/{series_title}"
else:
    path_to_save = os.getcwd() + "/" + series_title

try:
    os.mkdir(path_to_save)
except FileExistsError:
    pass

threads = []

def download(link, title, num):
    browser.get(episode_link)
    html_source = browser.page_source
    soup = BS(html_source, features="html.parser")
    iframe_link = soup.find_all('iframe')[0]['src']

    cda_vid_num = iframe_link.split("/")[4]
    cda_link = f"https://www.cda.pl/video/{cda_vid_num}"

    def download_yt_dl():
        command = f""""{executable}" -o "{path_to_save}/{str(int(num[0])).zfill(3)}_{title[0]}.%(ext)s" {cda_link}"""
        process = subprocess.Popen(command, shell=False)
        process.wait()
        sys.exit()


    download_task = threading.Thread(target = download_yt_dl, args = ())
    download_task.start()

    threads.append(download_task)

    

for episode in episodes:

    episode_num = episode.findAll("div")[0].contents
    episode_title = episode.findAll("div")[1].contents
    episode_link = episode.a.get('href')


    download(episode_link, episode_title, episode_num)

    time.sleep(2)

browser.close()
browser.quit()

while not len(episodes) == len(threads):
    pass

for thread in threads:
    thread.join()

os.system('cls')

print('DONE')

os._exit(0)