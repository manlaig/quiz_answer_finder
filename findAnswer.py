import requests, json, sys
from bs4 import BeautifulSoup


"""
    sends a search requests to Google and returns the HTML of the response
"""
def googlesearch(searchfor, api_key, search_id):
    link = 'https://www.googleapis.com/customsearch/v1'
    payload = {'key': api_key, 'cx': search_id, 'q': searchfor, 'num': 3}
    response = requests.get(link, params=payload)
    return response.text


"""
    given a HTML content, parse the questions and answers in Quizlet page
"""
def parseQuizlet(htmlContent):
    questions_answers = []
    soup = BeautifulSoup(htmlContent, "html.parser")

    """ each flashcard has question and answer in it """
    all_flashcards = soup.findAll("div", {"class":"SetPage-term"})
    
    for card in all_flashcards:
        question = card.findChildren("span", {"class":"TermText"}, recursive=True)
        questions_answers.append([question[0].contents[0], question[1].contents[0]])

    # consists of [question, answer]
    return questions_answers


"""
    get the percentage match between two strings
"""
def getMatch(string1, string2):
    totalMatch = 0

    str1 = string1.split(" ")
    str2 = string2.split(" ")
    
    for i in str1:
        if i in str2:
            totalMatch += 1
    return round(totalMatch * 100 / len(str1), 1)


"""
    search the web for an answer for a given question
"""
def getAnswer(question, option=0):
    result = googlesearch(question,
                    api_key=api_key,
                    search_id=search_id)
    json_obj = json.loads(result)

    for item in json_obj["items"]:
        link = item["link"]
        
        """ make a GET request and return the content of the HTML """
        contents = requests.get(link).content
        """ contains all the questions with the corresponding answers """
        all_pairs = parseQuizlet(contents)

        bestMatch = 0
        bestAnswer = "not found"

        for i in all_pairs:
            temp = getMatch(question, i[option])
            
            if temp > bestMatch:
                bestMatch = temp
                bestAnswer = i[1 - option]
                
                """ 90% match, so most likely the correct answer """
                if(temp > 90):
                    return (bestAnswer, bestMatch)

    return (bestAnswer, bestMatch)


""" checking for command line arguments """
if(len(sys.argv) == 1):
    question = input("Enter your question: ")
else:
    question = ' '.join(sys.argv[1:])

(answer1, match1) = getAnswer(question)
(answer2, match2) = getAnswer(question, option=1)

print("\nAnswer: " + (answer1 if match1 > match1 else answer2))
print("Match: " + (str(match1) if match1 > match2 else str(match2)) + "%")