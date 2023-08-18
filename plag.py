from flask import Flask, request, render_template
import re
import math
from googlesearch import search
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def loadPage():
    return render_template('index.html', query="", output="")

@app.route('/button-click', methods=['POST'])
def button_click():
    try:
        query = request.form.get('query')  # Get the query from the POST request

        x_searches = []
        for x in search(query=query, num=10, stop=10, pause=2.0):
            x_searches.append(x)

        for url in x_searches:
            response = requests.get(url, verify=False)  # Disabling SSL certificate verification
            soup = BeautifulSoup(response.text, 'html.parser')
            all_p = soup.find_all('p')

            for y in range(0, len(all_p)):
                if query in str(all_p[y]):
                    return url

        return "No relevant link found."
    except Exception as e:
        return f"Error occurred: {str(e)}"

@app.route("/", methods=['POST'])
def cosineSimilarity():
    try:
        universalSetOfUniqueWords = []
        matchPercentage = 0

        ####################################################################################################

        inputQuery = request.form['query']
        lowercaseQuery = inputQuery.lower()

        queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()

        for word in queryWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        fd = open("database1.txt", "r")
        database1 = fd.read().lower()

        databaseWordList = re.sub("[^\w]", " ", database1).split()

        for word in databaseWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        ####################################################################################################

        queryTF = []
        databaseTF = []

        for word in universalSetOfUniqueWords:
            queryTfCounter = queryWordList.count(word)
            queryTF.append(queryTfCounter)

            databaseTfCounter = databaseWordList.count(word)
            databaseTF.append(databaseTfCounter)

        dotProduct = sum(queryTF[i] * databaseTF[i] for i in range(len(queryTF)))

        queryVectorMagnitude = math.sqrt(sum(queryTF[i] ** 2 for i in range(len(queryTF))))
        databaseVectorMagnitude = math.sqrt(sum(databaseTF[i] ** 2 for i in range(len(databaseTF))))

        matchPercentage = (dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

        output = "Input query text matches %0.02f%% with database." % matchPercentage

        return render_template('index.html', query=inputQuery, output=output)
    except Exception as e:
        output = "Please Enter Valid Data"
        return render_template('index.html', query=inputQuery, output=output)

if __name__ == '__main__':
    app.run(debug=True)
