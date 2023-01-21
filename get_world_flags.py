import requests
from bs4 import BeautifulSoup
from urllib import parse
from threading import Thread
import os


def get_flag_urls():
    html = requests.get("https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags").text

    soup = BeautifulSoup(html, 'html.parser')
    exceptions = {
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Flag_of_Nepal.svg/98px-Flag_of_Nepal.svg.png":
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Flag_of_Nepal.svg/2560px-Flag_of_Nepal.svg.png"
    }
    img_urls = [
        f"https:{img['src'].replace('120', '2560').replace('98', '2560')}"
        for img in soup.find_all("img")
        if "Flag" in img["src"]
    ]

    return img_urls


def save_flag(flag: str):
    try:
        formatted_name = parse.unquote(flag.split("/")[-1]).replace("_", " ").replace("2560px-", "").replace(".svg", "")

        image = requests.get(flag).content
        with open(f"./flags/{formatted_name}", "wb") as f:
            f.write(image)
    except:  # I don't know why but it sometimes errors but doing it again works, and I'm not going to complain
        save_flag(flag)


def save_all():
    if not os.path.exists("./flags/"):
        os.mkdir("./flags/")
    flags = get_flag_urls()

    print(len(flags))

    threads = []
    for flag in flags:
        threads.append(Thread(target=save_flag, args=(flag,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    save_all()
