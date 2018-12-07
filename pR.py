# # pagerank function where we take an index of pages, a dictionary of rankings, a constant, and a num of pages
# # we calculate the new rankings based on the old rankings and how many nodes each page connects to
# # and then return the new dictionary to be iterated over again
import os, json


home = os.getcwd()
os.chdir("IU-folder")

def pageRank(pageRanks, p, n):
    # equation
    # rj = (p/n) + (1-p) x sum(ri/di)

    # random probability of being clicked on
    randomProb = p / n

    # 1-p in the equation
    minusConstant = 1 - p

    # for every page in our pageranks dictionary
    for page in pageRanks:
        linkedPages = outlinks[page]
        if len(linkedPages) == 0:
            pageRanks[page] = randomProb

        else:
            pageRankssum = []
            for item in linkedPages:
                pageRank = pageRanks[item]

                indivRank = pageRank / len(inlinks[item])


                pageRankssum.append(indivRank)
            newRank = randomProb + (minusConstant * (sum(pageRankssum)))
            pageRanks[page] = newRank


    return pageRanks


# open text file and read in the lines, splitting and stripping them into a list
with open("pageRank.txt") as textFile:
    contents = textFile.readlines()


# crete a set of all the pages, even if they don't link to anything
outlinks = {}
inlinks = {}
#keeping track of how many pages there are
pages= []

for i in range(len(contents)):
    #stripping and cleaning the file and creating a dictionary
    #0 : [1,23]

    contents[i] = contents[i].strip().split("\t")
    contents[i][0] = int(contents[i][0])
    contents[i][1] = int(contents[i][1])
    if contents[i][1] not in inlinks:
        inlinks[contents[i][1]] = [contents[i][0]]
        pages.append(contents[i][1])

    else:
        inlinks[contents[i][1]].append(contents[i][0])
        pages.append(contents[i][1])


    if contents[i][0] not in outlinks:
        outlinks[contents[i][0]] = [contents[i][1]]
        pages.append(contents[i][0])
    else:
        outlinks[contents[i][0]].append(contents[i][1])
        pages.append(contents[i][0])




pages = list(set(pages))

#print("inlinks", inlinks)

p = 0.05
n = len(pages)


pageRanks = {}
for page in pages:
    pageRanks[page] = 1 / len(pages)
    if page not in outlinks:
        outlinks[page] = []
 
#print("outlinks", outlinks)


#pageRanks = {}
#for page in pages:
#    pageRanks[page] = 1 / len(pages)


previousSum = 0
#
# # how many iterations of page rank has happened
count = 0

pageRanks = pageRank(pageRanks, p, n)
#
#
# # while loop so that we run pagerank until the results stop changing
while True:
    # keep track of how many iterations
    count += 1

    # keep track of the new previous sum
    previousSum = sum(pageRanks.values())

    # update the pageranks with another iteration
    pageRanks = pageRank(pageRanks, p, n)

    # print out the new ranks, the sum of the ranks, and how many iterations
    #print("Current page ranks",pageRanks)

#    print("Sum of page ranks", sum(pageRanks.values()))
#
#    print("Num of rank cycles", count)

    # if our current sum and previous sum are the same
    # then we break our loop as the values have stabilized
    if previousSum == sum(pageRanks.values()):
        print(count)
        break


#
#print(pageRanks)
print(sum(pageRanks.values()))
os.chdir(home)
with open("pageRanks.dat", "w") as file:
    file.write(json.dumps(pageRanks))

