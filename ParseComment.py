# Takes the reddit comment and creates a serch term for YouTube
def createSearch(comment, triggerIndex):
    vtuber = comment[triggerIndex-1]
    search = vtuber + " / " + " ".join(comment[triggerIndex+1:])
    return search
