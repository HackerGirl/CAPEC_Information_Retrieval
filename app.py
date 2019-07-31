from flask import Flask,render_template,url_for,request
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

STOPWORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "what", "how", "who", "where", "when", "why", "show","give","tell"]

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():

	# Read data from file '3000.csv' and store relevant information
	index = []
	with open('3000.csv') as file:
		reader = csv.reader(file, delimiter=',')
		next(reader) #skip first row
		for row in reader :
			url = "https://capec.mitre.org/data/definitions/{}.html".format(row[0])
			title = row[1]
			description = row[4]
			data = {'url':url,'title':title,'description':description}
			index.append(data)


	# Initialize the vectorizer 
	# Define our custom stop words to add question words (ie who, what, where, when, why)
	vectorizer = TfidfVectorizer(stop_words=STOPWORDS)

	# Learn model parameters from input files (training)
	tfidf_documents = vectorizer.fit_transform([file['description'] for file in index]) 

	if request.method == 'POST':
		form_data = [request.form['message']]
		# Use learned parameters from vectorizer to transform documents to document-term matrix
		# .A converts sparse matrix to dense matrix (an array/list)
		tfidf_query = vectorizer.transform(form_data).A

		# cosine_similarity computes normalized dot product:
        # tfidf_documents * tfidf_query.T 
		cos_sim = cosine_similarity(tfidf_query, tfidf_documents).flatten()
		results = list(zip(cos_sim.argsort()[::-1], sorted(cos_sim)[::-1]))
		response = [{'title':index[doc]['title'], 'url':index[doc]['url'], 'score':round(score, 3)} for doc,score in results if score>0.1]
	return render_template('result.html',results = response)

	if __name__ == '__main__':
		app.run(debug=True)