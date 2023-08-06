from main import Downloader
import time

if __name__ == '__main__':
    d = Downloader()
    url = "https://gamedownloads.rockstargames.com/public/installer/Rockstar-Games-Launcher.exe"
    d.start(url, "r.exe",2,retries=2)
    # time.sleep(2)  
    # d.stop()
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,block=False,multithread=False)
    # time.sleep(2)  
    # d.stop()
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,block=False)
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,block=False,multithread=False)
    # time.sleep(2)  
    # d.stop()
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,block=False)
    # time.sleep(2)
    # d.start(url, "r.exe",2,retries=2,block=False,multithread=False)