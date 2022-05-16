import re
from urllib.request import urlopen  




def initializer():
    url_main = "http://www.plyrics.com/m/mychemicalromance.html"
    file = urlopen(url_main)
    landing = file.read().decode('utf-8')
    pattern = "/lyrics/mychemicalromance/(.+)\.html"
    pages = re.findall(pattern, landing)
    urls = []
    all_lyrics = ""

    for i in range(len(pages)):
        urls.append(pages[i])

    for url in urls:
        f = urlopen("http://www.plyrics.com/lyrics/mychemicalromance/" + url + ".html")  
        rawtext = f.read().decode('utf-8')  

        mcr_clean = rawtext.split("lyrics -->")

        lyrics = re.sub("<.*>", "", mcr_clean[1])
        lyrics = re.sub("<.*", "", lyrics)
        lyrics = re.sub("([,!.?]&.*;|\(|\)|\r|<s>)", "", lyrics)

        lower_lyrics = lyrics.lower()
        temp1 = len(all_lyrics.split("\n"))
        all_lyrics += lower_lyrics
        temp2 = len(all_lyrics.split("\n"))
        with open("songnames.txt", "a", encoding="utf-8") as f:
            f.write(url + ":" + str(temp1) + ":" + str(temp2) + "\n")

    return all_lyrics


def writer(lyrics, param):
    with open("all_lyrics.txt", param, encoding="utf-8") as file:
        for line in lyrics:
            file.write(line)
    pass


def importer():
    with open("all_lyrics.txt", "r", encoding="utf-8") as file:
        text = file.read()
    raw = re.sub("(\n)+", " </s> <s> ", text)
    raw = "<s> " + raw

    mcr_minicorpus = []
    mcr_minicorpus += raw.split(" ")
    mcr_minicorpus = list(filter(None, mcr_minicorpus))
    return mcr_minicorpus


def main():
    #writer(initializer(), "w")
    return importer()
