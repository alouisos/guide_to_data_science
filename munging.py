# this is like a notebook of my code during data munging and is not a complete code to follow
# will soon create a ipython notebook and upload it here for you to be able to follow the recipes of my process



data = pd.read_csv('data.csv')

#clean minutes 
dirty = '142 mins.'
number, text = dirty.split(' ')
clean = int(number)
print number


data.genres = data.genres.str.replace('[', '').str.replace(']','')

genres = set()
for m in data.genres: 
	genres.update(k for k in m.split(','))
genres = sorted(genres) 

for genre in genres: 
	data[genre] = [genre in movie.split(',') for movie in data.genres]

movie_genres = data.iloc[:, 8:]
#dummify the movie genres 
movie_genres = movie_genres.applymap(lamdba x: 1 if x else 0)
data.drop('genres', axis = 1, inplace=True)
data = pd.concat([data, movie_genres], axis = 1)

# take numerical values and explore them for outliers 
data[['runtime', 'rating']].describe() 
data[['director', 'first_actor', 'second_actor']].describe() 

plt.hist(data.rating, bins = 50, color = '#A3C1AD' )
plt.xlabel("Movie Rating")

plt.hist(data.runtime, bins =50, color = '#A3C1AD')
plt.xlabel('Movie Runtime in mins')
plt.xlim(0,300)

plt.scatter(data.runtime, data.rating, lw=0, alpha=.075, color='k')

# take surnames to create a word cloud 
surnames = [x.split(' ')[-1] for x in data.director]
surnames.to_csv('director_surnames.csv', sep=',') 

# use a wordcloud generator like http://www.jasondavies.com/wordcloud/ or www.wordle.net


#stratify actors according to rating 
        print rating, subset[subset.rating==subset.rating.max()].first_actor.values


#reduce dimensions for directors - stratify them according to mean rating 
data_for_model =  data.get(['director', 'first_actor', 'second_actor', 'title', 'rating_class'])
 data_for_model = data_for_model.sort('director')
g = data.groupby('director')
directors_stratified = pd.DataFrame(g.rating_class.aggregate(np.mean))
directors_stratified = directors_stratified// 1

values = [directors_stratified.ix[director][0] for director in data_for_model.director]
data_for_model['avg_rating_director'] = values 


#actual prediction 
features = data.iloc[:, 1:-1]
X = features.values
classes = data.iloc[:, -1]
y = classes.values

from sklearn import metrics 
from sklearn.cross_validation import train_test_split

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=0)
 
from sklearn.tree import DecisionTreeClassifier 
clf = DecisionTreeClassifier(max_depth= 5) 
clf.fit(Xtrain, y train)
ypred = clf.predict(Xtest)
print metrics.classification_report(ytest, ypred)



