import ssl,  urllib.request, tools, time, os, sys
from bs4 import BeautifulSoup
import urllib.robotparser
from collections import deque


crawledLinks = []
urlLinks = deque([])
links = []
bigURl = {}


def createUrlDict(start, end):
    urlDict = {}
    for i in range(start,end):
        urlDict[i] = urlLinks[i]
    return urlDict


def createPageRank(number,urlDict):
    for key, value in urlDict.items():
        for i in range(len(crawledLinks)):
            if value == crawledLinks[i]:
                if value in bigURl:
                    key = bigURl[value]
                
        with open("pageRank.txt", "a") as file:
            file.write(str(number) + "\t" + str(key) + "\n")


def get_links(url, count):
    global links

    context = ssl._create_unverified_context()
    try:
             #identifying myself as a IU user to the webpage 
        req = urllib.request.Request(url, headers={'User-Agent': 'IUB-I427-ayeffron'})

        fileobj = urllib.request.urlopen(req, context = context)


        domain = url.split("//")[-1].split("/")[0]
        crawledLinks.append(url)

        

        #opening the link and getting the contents of the page, also saving the file to the directory 
       # page = urllib.request.urlopen(url, context = context)
        contents = fileobj.read().decode(errors="replace")
        fileobj.close()
        

        
        with open("index-"+str(count)+".html", "w") as file:
            file.write(contents)
        with open("index.dat", "a") as file2:
            file2.write(str(count) +"\t"+ url +"\n")
        
 
        domain = url.split("//")[-1].split("/")[0]


    except:
        print("not a link")
        return urlLinks
    else:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url("https://" + domain+ "/robots.txt")
        rp.read()
        

        soup = BeautifulSoup(contents, 'html.parser')
    
        for link in soup.find_all('a', href=True):
            link = tools.relativeLink(domain, link["href"])
            if ".jpg" not in link and ".svg" not in link and ".pdf" not in link and ".png" not in link and rp.can_fetch("*", link) and "https" in link:
                links.append(link)
      
        links = list(set(links))
        
        for link in links:
            if link not in crawledLinks:
                urlLinks.appendleft(link)
                
    
    return urlLinks


#Main
    

#creating the directory where the files will sit
directory = tools.createFolder("IU-folder")

#changing our directory to the new directory folder 
home = os.getcwd()
os.chdir(directory)

count = 1

urlDict = {}
urlLinks.appendleft("https://news.iu.edu/iu-bloomington/index.html")

bigURl["https://news.iu.edu/iu-bloomington/index.html"] = 1
seed_tuple = urlLinks.pop()



urlLinks = get_links(seed_tuple, count)
#with open("index.dat", "a") as file:
#    file.write(str(count) + "\t"+ seed_tuple + "\n")
    
    
urlDict = createUrlDict(1, len(urlLinks))
for item in urlDict:
    if urlDict[item] not in bigURl:
        bigURl[urlDict[item]] = item
createPageRank(count, urlDict)

    
while True:
    time.sleep(1) 
    count += 1 
    #DPS and BFS are the same for the pop
    old = len(urlLinks)

    next_link = urlLinks.pop()
    while next_link in crawledLinks or "facebook" in next_link:
        next_link = urlLinks.pop()




    #print(next_link)
    print(count, next_link)
#    with open("index.dat", "a") as file:
#        file.write(str(count) +"\t"+ next_link +"\n")

    

  
    if len(crawledLinks) == 200:
        print("Crawler done")
        break
    
    else:

        urlLinks = get_links(next_link,count)
        new = len(urlLinks)
        urlDict = createUrlDict(old, new)
        for item in urlDict:
            if urlDict[item] not in bigURl:
                bigURl[urlDict[item]] = item
        createPageRank(count, urlDict)

        

#how to get this to run on terminal