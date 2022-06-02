import re
from urllib.request import urlopen  




def initializer():
    '''
    Reads My Chemical Romance song names from a webpage and gets the relevant lyric page for each song. 
    Cleans the .html file, then returns the lyrics for all the songs as a string. 
    
    Also includes a now-defunct function that stores between which lines of the .txt file each song 
    can be found in a separate .txt file. This can be used in the future to upsample specific songs
    based on user input to generate similar lyrics. 
    
    Returns: 
        all_lyrics (str): A string containing every My Chemical Romance lyric found. 
    '''
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
        lyrics = re.sub("([,!.?]&.*;|\(|\)|\r|<s>|&quot;)", "", lyrics)

        lower_lyrics = lyrics.lower()
        temp1 = len(all_lyrics.split("\n"))
        all_lyrics += lower_lyrics
        temp2 = len(all_lyrics.split("\n"))
        with open("songnames.txt", "a", encoding="utf-8") as f:
            f.write(url + ":" + str(temp1) + ":" + str(temp2) + "\n")

    return all_lyrics


def writer(lyrics, param):
    '''
    Takes a string and a mode parameter as an argument, then writes 
    that string to the lyrics .txt file. 
    
    Parameters: 
        lyrics (str): Text to be written in all_lyrics.txt
        param (str): "w" or "a", the mode to open all_lyrics.txt 
    '''
    with open("all_lyrics.txt", param, encoding="utf-8") as file:
        for line in lyrics:
            file.write(line)
    pass


def importer():
    '''
    Reads the contents of the lyrics .txt file, then adds each line to an array to 
    be used for n-gram generation. Returns the array. 
    Exists mainly to get the lyrics from a local database so as to save time when
    generating n-grams. 
    
    Returns:
        mcr_minicorpus (arr): An array containing the lyrics found in all_lyrics.txt,
        to be used in generating n-grams. 
    '''
    with open("all_lyrics.txt", "r", encoding="utf-8") as file:
        text = file.read()
    raw = re.sub("(\n)+", " </s> <s> ", text)
    raw = "<s> " + raw

    mcr_minicorpus = []
    mcr_minicorpus += raw.split(" ")
    mcr_minicorpus = list(filter(None, mcr_minicorpus))
    return mcr_minicorpus


def main():
    #The following line should be uncommented if all_lyrics.txt does not exist. 
    #writer(initializer(), "w") 
    return importer()
