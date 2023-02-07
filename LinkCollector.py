from collections import deque
import requests
from bs4 import BeautifulSoup as bs
import xlwt

import Link
import HashTable

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return (int)(start)

#One LinkCollector per 
class LinkCollector:
    def __init__(self,sheetTitle):
        #Workbook
            #creates a new workbook
        self.excelWorkbook = xlwt.Workbook()
            #creates a new sheet with sheetTitle variable as the name
        self.sheet = self.excelWorkbook.add_sheet(sheetTitle, True)
        self.excelWorkbook.save("sheets\\" + sheetTitle + ".xls")
        #Queue
        self.queue = deque()
        #Hash table
        self.myHashTable = HashTable.HashTable()
        #IDNumber
        self.currIDNumber = 0

    #filters out none wikipedia artiles, as well as certain unwanted articles
    def filterOutJunk(self,strLink):
        #searches to make sure its a wiki link
        if(strLink.find("a href=\"/wiki/") == -1):
            return 0
       
        if(strLink.find("cite_note") != -1):
            return 0
        if(strLink.find("cite_ref") != -1):
            return 0
        if(strLink.find("a class=") != -1):
            return 0

      
        return 1

    def findPath(self,startLink, endLink):
        print("Finding path")

        zerothLink = Link.Link("Null", -1, "Null")
        firstLink = Link.Link(startLink, 0, zerothLink)
        self.queue.append(firstLink)
        self.myHashTable.insert(startLink, firstLink)
        
        while(self.queue.__len__() != 0):

            #gets top link in queue
            currLink = self.queue.popleft()
            print(str(currLink.ID) + "       " +   currLink.address)
            
            #gets soup object
            req = requests.get(currLink.address)
            soup = bs(req.text, "html.parser")

            
            
            #gets each wikipedia link within 
            for paragraph in soup.find_all("p"):
                for item in paragraph.find_all("a"):

                    strLink = str(item)
                    #filters out certain junk phrases
                    if(self.filterOutJunk(strLink) == 0):
                        continue
                    
                    #Creates a link from html information
                    indexOfEndOfString = find_nth(strLink, "\"", 2)
                    strLink = strLink[9:indexOfEndOfString] 
                    strLink = "https://en.wikipedia.org" + strLink

                    #checks if link already exists in hash table
                    if(self.myHashTable.find(strLink) != None):
                        continue

                    #adds to hash tables
                    addition = Link.Link(strLink, currLink.ID + 1, currLink)
                    self.myHashTable.insert(strLink, addition)

                    #adds to queue
                    self.queue.append(addition)

                    if(str(strLink) == endLink):
                        print("Match found")

                        print(str(currLink.ID + 1) + "\t" + str(strLink) + "\n")
                        parentLink = currLink
                        
                        while(parentLink.ID != -1):
                            
                            print(str(parentLink.ID) + "\t" + str(parentLink.address) + "\n")
                            parentLink = parentLink.parent
                        
                        
                        return
                
           
            
            
            


    



        