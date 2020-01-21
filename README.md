# Information Retrieval for Common Attack Pattern Enumeration and Classification -
In this lesson, you will learn learn how to build a basic information retrieval app to search for common attack patterns found on the MITRE CAPEC database. Through this lesson, you will learn about attack patterns employed by adversaries, and natural language processing fundamentals.

### HackerGirl Skills Learned
* Security: Become familar with common attack patterns used by adversaries
* Machine Learning: Learn modern Machine Learning techniques: Natural Language Processing (NLP) and Information Retrieval (IR)
* Coding: Web Development with Python

## Background
**CAPEC:**
* Understanding how an adversary operates is essential to an effective cyber security engineer. [CAPEC™](https://capec.mitre.org/) provides a publicly available catalog of common attack patterns that helps users understand how adversaries exploit weaknesses in applications and other cyber-enabled capabilities. CAPEC™ is used by analysts, developers, testers, and educators to advance community understanding of exploits and enhance security defenses against exploits. 
* "Attack Patterns" are descriptions of the common attributes and approaches employed by adversaries to exploit known weaknesses in cyber-enabled capabilities. Attack patterns define the challenges that an adversary may face and how they go about solving it. Attack Patterns are derviced from analyizing patterns in real-world exploits and help those developing applications, or administrating cyber-enabled capabilities to better understand the specific elements of an attack and how to stop them from succeeding.

**Information Retrieval:**
* Information Retrieval is the task of gathering resources that are revelant to a user's information needs. We use NLP to process documents and extract information. IR is used everywhere - from question/answering systems to information routing and filtering to IBM Watson on Jeopardy! 
* In this lesson, we will be building a document retrieval system that matches user queries with documents in the CAPEC database. 
* There are many different design decisions that comprise an information retrieval system. Two key factors are *document representation* and *document similarity*. 


## Document Representation and Similarity

**Vector Space Model**
* How the heck do we teach computers to understand human language in documents?! There are many methods that draw from the *vector space model*, which represents queries and documents as vectors in a common vector space.
* The vector space model is a V-dimensional space, where V is the vocabulary (set of all words used in documents). Each term in the vocabulary is an axis of the space. In order to compute document similarity, we will project our documents and the user query in the vector space, then calculate which documents are closest to the query. See *Diagram 1*.
  - [More Notes on Vector Space Model](https://ils.unc.edu/courses/2013_spring/inls509_001/lectures/06-VectorSpaceModel.pdf)
* Each document, *d* has a position in the vector space that is determined by the words and their frequencies found in *d*. Again, how we choose to compute documents' positions in the vector space is a key design decision. For this lesson, we will implement tf-idf, but I encourage you to explore other vectorization options, such as [doc2vec](https://cs.stanford.edu/~quocle/paragraph_vector.pdf), and decide which works best for your data domain. 

**TF-IDF Weighting**
* To start, we will use a *bag of words (BoW) model*, a vector representation that ignores word ordering in a document.
  - [More Notes on Bag of Words](https://medium.com/greyatom/an-introduction-to-bag-of-words-in-nlp-ac967d43b428)
* In order to transform our documents into the vector space, we can convert a collection of text documents to a matrix of token counts, with dimensions *D x V*, where V is the number of words in the vocabulary and D is the number of documents. Each document, *d* is represented as a count vector, meaning it contains the number of times each word in V appears in *d*. *Diagram 2* shows the count vectors for each document.
* TF-IDF is a weighting scheme that we apply to the term-document count matrix to reflect "how important" a word is to a document in a collection. Term frequency (tf) is the number of times a term, *t* appears in document *d*, and inverse document frequency (idf) is the inverse of the number of documents that contain *t*. Word importance increases proportionally to the number of times a word appears in the document, but it is offset by the frequency of the word in the corpus.TF-IDF weighting modifies the count vector values found in *Diagram 2* to more accurately represent word importance in a document. 
  - [More Notes on TF-IDF](https://web.stanford.edu/class/cs276/handouts/lecture6-tfidf-handout-1-per.pdf)
* In my source code, I use the TfidfVectorizer from Scikit-Learn. I also recommend using Gensim for TF-IDF models, or Word2Vec/Doc2Vec models. 

<div>
<img src="https://github.com/rachelbari/CAPEC-Information-Retrieval/blob/master/static/vsm-diagram.png" width="375" height="375"> <img src="https://github.com/rachelbari/CAPEC-Information-Retrieval/blob/master/static/count-matrix-diagram.png" width="425" height="375">
</div>
<br>
<br>

**Measuring Similarity**
* Once we project our documents into the vector space model, we can find how similar two documents are.
* Depending on your objective, there are a variety of document similarity measures you may choose from. For this project, we will use cosine distance, but I encourage you to check out [Jaccard distance](https://www.statisticshowto.datasciencecentral.com/jaccard-index/) and [Euclidean distance](http://rosalind.info/glossary/euclidean-distance/) as well. 
* *Cosine similarity* computes the dot product for normalized vectors. Our document corpus is represented as a *D x V* matrix, and our query document is represented as a *1 x V* matrix, so we can find the cosine similarity between the query document and each document in our corpus to find which documents match our query! See *Document 1* for a visual representation of cosine similarity. 

## Project Directions:

### Steps:
1. Download ```3000.csv``` from S3 Bucket
2. Create a web app using Flask (or a micro-framework of your choice). Create routes and html templates for a home page and a search results page. Check out the source code, [Flask Quickstart](http://flask.pocoo.org/docs/1.0/quickstart/), or [Getting Started Tutorial](https://medium.com/techkylabs/getting-started-with-python-flask-framework-part-1-a4931ce0ea13) to get started.
3. Create a form on your home page where a user can submit a search query
4. Load the ```3000.csv``` file and save relevant data. I used *description* to train the TFIDF model, *id* to build a url to CAPEC's online database, and *title* to share with users on the results page. 
5. Implement TFIDF using Scikit-learn or Gensim - or build your own vectorizer from scratch!
6. Compute document similarity between your TFIDF-transformed document matrix and query document
7. Return relevant documents by returning the top-n similar documents, some minimum threshold score, or a combination of both. In the source code, we return the top 3 documents and use a minimum threshold score of 0.1.



