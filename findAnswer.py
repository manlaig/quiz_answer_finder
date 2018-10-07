import requests, json
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
    result = googlesearch('quizlet', 'AIzaSyD7Q20Ts390Ptp-A_y_2EFtESskF4VlPaE', '013798571177656250136:r5mvmy6bpdo')
    json_obj = json.loads(result)
    for i in json_obj["items"]:
        print(i["link"])


all_pairs = parseQuizlet(getWebsiteContent("https://quizlet.com/122037001/chapter-5-understanding-quiz-flash-cards/"))

for item in all_pairs:
    print(item)