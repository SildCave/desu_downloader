def main():
    import sys
    import subprocess
    import os
    import argparse
    import time
    import requests
    import threading
    import platform
    import shlex
    from selenium.webdriver.support.ui import Select


    def install(package):
        subprocess.check_output([sys.executable, "-m", "pip", "install", package])

    try:
        import undetected_chromedriver as uc
        
    except ImportError:
        if platform.system() == 'Linux':
            try:
                install("undetected-chromedriver")
                import undetected_chromedriver as uc
            
            except:
                os.system("sudo apt install python3-pip")
                install("undetected-chromedriver")
                import undetected_chromedriver as uc

        else:
            install("undetected-chromedriver")
            import undetected_chromedriver as uc


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

    if not os.path.exists("tools/yt-dlp.exe") or platform.system() == 'Linux':

        r = requests.get("https://github.com/yt-dlp/yt-dlp/releases/download/2022.05.18/yt-dlp.exe")
        open("tools/yt-dlp.exe", 'wb').write(r.content)

    parser = argparse.ArgumentParser()
    parser.add_argument('--link', type=str, required=True, help="link to anime desu")
    parser.add_argument('--path', type=str, required=False, help="path")
    args = parser.parse_args()

    options = uc.ChromeOptions() 
    options.headless = True

    if platform.system() != 'Linux':
        try:
            browser = uc.Chrome(options = options)
        except Exception as e:
            print(f'Download Chrome {e}')
            sys.exit(0)
    else:
        try:
            browser = uc.Chrome(options = options)
        except:
            try:
                os.system('sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
                os.system('sudo sudo dpkg -i google-chrome-stable_current_amd64.deb')
            except Exception as e:
                print(f'Download Chrome {e}')
                sys.exit(0)
            
    if not os.path.exists("tools/yt-dlp.exe") and platform.system() != 'Linux':

        r = requests.get("https://github.com/yt-dlp/yt-dlp/releases/download/2022.05.18/yt-dlp.exe")
        open("tools/yt-dlp.exe", 'wb').write(r.content)

    if platform.system() == 'Linux':
        os.system('sudo apt install python-is-python3')
        if not os.path.exists('/usr/local/bin/youtube-dl'):
            os.system('sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl')
            os.system('sudo chmod a+rx /usr/local/bin/youtube-dl')

    if platform.system() == 'Linux':
        executable = "youtube-dl"
    else:
        executable = "tools/yt-dlp.exe"

    desu_link = args.link
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

    with open('log', 'w') as f:
        f.close()

    def download(link, title, num):
        browser.get(episode_link)
        select = Select(browser.find_element_by_class_name('mirror'))
        select.select_by_visible_text('CDA')
        html_source = browser.page_source
        soup = BS(html_source, features="html.parser")
        iframe_link = soup.find_all('iframe')[0]['src']
        
        with open('log', 'a') as f:
            f.write(f"iframe {iframe_link}\n")
        cda_vid_num = iframe_link.split("/")[4]
        cda_link = f"https://www.cda.pl/video/{cda_vid_num}"
        with open('log', 'a') as f:
            f.write(f"{cda_link}\n")


        def download_yt_dl():
            command = shlex.split(f""""{executable}" -o "{path_to_save}/{str(int(num[0])).zfill(3)}_{title[0]}.%(ext)s" {cda_link}""")
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

    if platform.system() != 'Linux':
        os.system('cls')
    else:
        os.system('clear')
        
    print('DONE')

    os._exit(0)

if __name__ == '__main__':
    main()
