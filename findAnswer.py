import requests, json, sys
from bs4 import BeautifulSoup


"""
    sends a search requests to Google and returns the HTML of the response
"""
def googlesearch(searchfor, api_key, search_id):
    link = 'https://www.googleapis.com/customsearch/v1'
    payload = {'key': api_key, 'cx': search_id, 'q': searchfor}
    response = requests.get(link, params=payload)
    return response.text


"""
    make a GET request and return the content of the HTML
"""
def getWebsiteContent(url):
    response = requests.get(url)
    return response.content


"""
    given a HTML content, parse the questions and answers in Quizlet page
"""
def parseQuizlet(htmlContent):
    questions_answers = []
    soup = BeautifulSoup(htmlContent)
    lst = soup.findAll("div", {"class":"SetPage-term"})     #all flashcards (has question answer in it)
    
    for card in lst:
        question = card.findChildren("span", {"class":"TermText"}, recursive=True)
        questions_answers.append([question[0].contents[0], question[1].contents[0]])

    return questions_answers

def getAnswer(question):
    result = googlesearch(question, api, search_id)
    json_obj = json.loads(result)
    link = json_obj["items"][0]["link"]
    all_pairs = parseQuizlet(getWebsiteContent(link))

    for i in all_pairs:
        if i[0] == question:
            return i[1]
        elif i[1] == question:
            return i[2]
    
    return "None"


assert len(sys.argv) != 1, "Enter a question"
question = ' '.join(sys.argv[1:])
print(getAnswer(question))