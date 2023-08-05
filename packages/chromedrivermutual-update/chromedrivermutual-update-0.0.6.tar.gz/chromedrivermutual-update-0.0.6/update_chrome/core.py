import os
import ssl, shutil, re, platform
import zipfile
from urllib.request import urlopen
from pathlib import Path
import difflib
import wget


def chrome_driver_url(latest=False):
    def current_chrome_version():
        CHROME_RELEASE_URL = "https://sites.google.com/chromium.org/driver/downloads?authuser=0"
        try:
            response = urlopen(CHROME_RELEASE_URL,context=ssl.SSLContext(ssl.PROTOCOL_TLS)).read()
        except ssl.SSLError:
            response = urlopen(CHROME_RELEASE_URL,).read()

        downloading_version = re.findall(b"ChromeDriver \d{2,3}\.0\.\d{4}\.\d+", response)
        downloading_version = [x.decode().split(" ")[1] for x in downloading_version]
        downloading_version.sort(key=lambda x: [int(i) if i.isdigit() else i for i in x.split('.')])
        downloading_version.reverse()
        osname = platform.system()
        if osname == 'Darwin':
            installpath = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
            verstr = os.popen(f"{installpath} --version").read().strip('Google Chrome ').strip()
            ver_to_download = difflib.get_close_matches(verstr, downloading_version)
            ver_to_download = ver_to_download[0]
            return ver_to_download
        elif osname == 'Windows':
            verstr = os.popen('reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version').read().strip().split(" ")
            verstr = verstr[-1]
            ver_to_download = difflib.get_close_matches(verstr, downloading_version)
            ver_to_download = ver_to_download[0]
            return ver_to_download
        elif osname == 'Linux':
            installpath = "/usr/bin/google-chrome"
            verstr = os.popen(f"{installpath} --version").read().strip('Google Chrome ').strip()
            ver_to_download = difflib.get_close_matches(verstr, downloading_version)
            ver_to_download = ver_to_download[0]
            return ver_to_download
        else:
            raise NotImplemented(f"Unknown OS '{osname}'")

    if latest:
        CHROME_RELEASE_URL = "https://sites.google.com/chromium.org/driver/downloads?authuser=0"
        try:
            response = urlopen(CHROME_RELEASE_URL, context=ssl.SSLContext(ssl.PROTOCOL_TLS)).read()
        except ssl.SSLError:
            response = urlopen(CHROME_RELEASE_URL).read()

        downloading_version = re.findall(b"ChromeDriver \d{2,3}\.0\.\d{4}\.\d+", response)[0].decode().split()[1]
    else:
        downloading_version = current_chrome_version()

    system = platform.system()
    if system == "Windows":
        url = f"https://chromedriver.storage.googleapis.com/{downloading_version}/chromedriver_win32.zip"
    elif system == "Darwin":
        # M1
        if platform.processor() == 'arm':
            url = f"https://chromedriver.storage.googleapis.com/{downloading_version}/chromedriver_mac64_m1.zip"
        else:
            url = f"https://chromedriver.storage.googleapis.com/{downloading_version}/chromedriver_mac64.zip"
    elif system == "Linux":
        url = f"https://chromedriver.storage.googleapis.com/{downloading_version}/chromedriver_linux64.zip"
    return url


def download_chrome_driver(drivers_dir):
    driver_name = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
    if (drivers_dir / driver_name).exists():
            return print("Chrome driver updated already existe")
    url = chrome_driver_url()
    try:
        response = urlopen(url, context=ssl.SSLContext(ssl.PROTOCOL_TLS))  
    except ssl.SSLError:
        response = urlopen(url)  

    zip_file_path = drivers_dir / Path(url).name
    with open(zip_file_path, 'wb') as zip_file:
        while True:
            chunk = response.read(1024)
            if not chunk:
                break
            zip_file.write(chunk)

    extracted_dir = drivers_dir / zip_file_path.stem
    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        zip_file.extractall(extracted_dir)
    os.remove(zip_file_path)

    driver_path = drivers_dir / driver_name
    try:
        (extracted_dir / driver_name).rename(driver_path)

    except FileExistsError:
        (extracted_dir / driver_name).replace(driver_path)

    shutil.rmtree(extracted_dir)
    os.chmod(driver_path, 0o755)


def start_add(location):
    chrome_driver_location = Path(location)
    chrome_driver_location.mkdir(exist_ok=True)
    download_chrome_driver(chrome_driver_location)


if __name__ == "__main__":
    chrome_driver_location = Path("chrome_driver")
    chrome_driver_location.mkdir(exist_ok=True)
    download_chrome_driver(chrome_driver_location)
