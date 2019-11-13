import requests
from bs4 import BeautifulSoup


def getUrlFromUser():
    '''
        get URL from the User wih an input,
        can be replaced by another getter for reusability
    '''
    url = None
    while not checkIfWebsiteURL(url):
        url = input("Enter target URL:")
        if url.lower() == "stop":
            exit()
    print("\nURL obtained.\n")
    return url


def getHtmlFrom(url):
    '''
        get HTML file from the parsed URL,
        if URL not working, returns None
        otherwise returns HTML as a string
    '''
    try:
        response = requests.get(url)
    except Exception:
        print("Could not open {0}".format(url))
        return None #we need to test in main code if URL was succesful
    else:
        return response.text


def getLinksFrom(html):
    '''
        fetches all the link in <a> tags inside the parsed HTML
        returns a list of valid URL-format Sring
    '''
    validLinkList = []
    soup = BeautifulSoup(html, features="html.parser") #HTML made easy to read
    tagList = soup.find_all('a') #BeautifulSoup will give a list of <a> tag
    for tag in tagList:
        link = tag.get('href', None) #extract URL from href parameter
        if checkIfWebsiteURL(link):
            validLinkList.append(link)
    return validLinkList


def checkIfWebsiteURL(toCheck):
    '''
        checks if String is in URL-format for websites
        (i.e if it starts with an HTTP protocol, can be extended)
    '''
    if toCheck == None:
        return False
    targetList = ["https://", "http://"] #more protocols can be added later
    for target in targetList:
        targetLen = len(target)
        if len(toCheck) < targetLen: #check next possible target
            break
        if compareString(toCheck, target, targetLen): #found a match
            return True
    return False #no match found


def compareString(s1, s2, n):
    '''
        compare if two Strings s1 and s2 are identical up to n caracters
        assumes s1 and s2 have at least a length n
    '''
    for i in range(n):
        if s1[i] != s2[i]:
            return False
    return True


if __name__ == "__main__":

    print("Welcome to this basic webCrawler.")
    print("Please input the target URL with the appropriate Protocol.")
    print("Input 'STOP' to exit")
    
    TARGET_COUNT = 100 #desired limit on the number of unique URL
    urlList = [getUrlFromUser()]
    index = 0
    linkCount = 1
    isDone = False
    print("Extracting URL and exploring website...\n")
    # if index catches up with linkCount,
    # we don't have any more URL to explore
    while linkCount > index and not isDone: 
        html = getHtmlFrom(urlList[index])  
        index += 1
        if not html:
            break #skip empty URL
        output = getLinksFrom(html)
        for link in output:
            if link not in urlList:
                urlList.append(link)
                linkCount += 1
                if linkCount == TARGET_COUNT: #exit when TARGET_COUNT reached
                    isDone = True
                    break

    print("\n{0} links found :\n".format(linkCount))
    for link in urlList:
        print(link)
    input("\n\nPlease press enter to terminate.")

