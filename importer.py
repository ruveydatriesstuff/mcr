import re
from urllib.request import urlopen  # for reading websites

hassetup = False



def initializer():
    url_main = "http://www.plyrics.com/m/mychemicalromance.html"
    file = urlopen(url_main)
    landing = file.read().decode('utf-8')
    pattern = "/lyrics/mychemicalromance/(.+)\.html"
    deneme2 = re.findall(pattern, landing)
    urls = []
    all_lyrics = ""

    for i in range(len(deneme2)):
        urls.append(deneme2[i])

    for url in urls:
        f = urlopen("http://www.plyrics.com/lyrics/mychemicalromance/" + url + ".html")  #
        mcr_deneme = f.read().decode('utf-8')  # read the file with (utf-8) encoding

        mcr_clean = mcr_deneme.split("lyrics -->")

        lyrics = re.sub("<.*>", "", mcr_clean[1])
        lyrics = re.sub("<.*", "", lyrics)
        lyrics = re.sub("([,!.?]|&.*;|\r)", "", lyrics)

        lower_lyrics = lyrics.lower()
        temp1 = len(all_lyrics.split("\n"))
        all_lyrics += lower_lyrics
        temp2 = len(all_lyrics.split("\n"))
        with open("songnames.txt", "a", encoding="utf-8") as f:
            f.write(url + ":" + str(temp1) + ":" + str(temp2) + "\n")

    return all_lyrics


def writer(deneme, param):
    with open("all_lyrics.txt", param, encoding="utf-8") as file:
        for line in deneme:
            file.write(line)
    pass


def importer():
    with open("all_lyrics.txt", "r", encoding="utf-8") as file:
        text = file.read()
    deneme = re.sub("(\n)+", " </s> <s> ", text)
    deneme = "<s> " + deneme

    mcr_minicorpus = []
    mcr_minicorpus += deneme.split(" ")

    # list_lyrics = lower_lyrics.split("\n")

    # mcr_minicorpus = ["<s> "+line+" </s>" for line in list_lyrics]
    # print(mcr_minicorpus)

    mcr_minicorpus = list(filter(None, mcr_minicorpus))
    return mcr_minicorpus


def upsampler(songnames, coeff):
    urls = []
    ups_lyrics = ""
    for i in range(len(songnames)):
        urls.append("http://www.plyrics.com/lyrics/mychemicalromance/" + songnames[i] + ".html")
    for url in urls:
        f = urlopen(url)  #
        ups_deneme = f.read().decode('utf-8')  # read the file with (utf-8) encoding

        ups_clean = ups_deneme.split("lyrics -->")

        lyrics = re.sub("<.*>", "", ups_clean[1])
        lyrics = re.sub("<.*", "", lyrics)
        lyrics = re.sub("([,!.?]|&.*;|\r)", "", lyrics)

        lower_lyrics = lyrics.lower()
        ups_lyrics += lower_lyrics
    for i in range(coeff):
        writer(ups_lyrics, "a")

    pass


def index():
    places = {}
    with open("songnames.txt", "r", encoding="utf-8") as f:
        for line in f:
            thruple = line.split(":")
            places[thruple[0]] = (thruple[1], thruple[2][0:-1])

    return places


def upsample_dict(places, songnames, coeff):
    with open("all_lyrics.txt", "r", encoding="utf-8") as f:
        lyrics = f.readlines()
    with open("all_lyrics.txt", "a", encoding="utf-8") as fw:
        for song in songnames:
            lines = ""
            i1 = int(places.get(song)[0])
            i2 = int(places.get(song)[1])
            while i1 != i2:
                lines += lyrics[i1]
                i1 += 1
            for i in range(coeff):
                fw.write(lines)
    pass


def upsample_worker(songnames, coeff):
    upsample_dict(index(), songnames, coeff)
    pass


def main():
    # global hassetup
    # if hassetup is False:
    #writer(initializer(), "w")
    #   hassetup = True
    return importer()
