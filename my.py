from flask import Flask, render_template, request
import pickle as pkl
import numpy as np
import pandas as pd
popolar_book = pd.read_pickle('most-popular-book.pkl')
pv = pd.read_pickle('pivot-tabel.pkl')
with open('similarity.pkl', 'rb') as file:
    similarity = pkl.load(file)
df = pd.read_pickle('books.pkl')


def recommendation(book_name):

    book_name = book_name.strip().lower()
    #
    pv.index = pv.index.str.strip().str.lower()

    if book_name not in pv.index:
        print(f"Book '{book_name}' not found in pivot table index.")
        return []

    index = np.where(pv.index == book_name)[0][0]
    similar_books = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[:5]


    similar_book_names = [pv.index[i[0]] for i in similar_books]


    if book_name not in similar_book_names:
        similar_book_names.insert(0, book_name)

    return similar_book_names[:5]


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book=list(popolar_book['Book-Title'].values),
                           author=list(popolar_book['Book-Author'].values),
                           img=list(popolar_book['Image-URL-M'].values),
                           rating=list(popolar_book['Book-Rating_y'].values))


@app.route('/Recommended')
def book():
    return render_template('Recommended Book.html')


@app.route('/Recommended_Book', methods=['POST'])
def user():
    user_input = request.form.get('user_input')
    print(f"User input: {user_input}")  # Debugging output
    book_list = recommendation(user_input)


    if not book_list:
        return render_template('Recommended Book.html',
                               error="Book not found in the recommendations or database.")

    new_df = df[df['Book-Title'].str.strip().str.lower().isin(book_list)]
    return render_template('Recommended Book.html',
                           book=list(new_df['Book-Title'].values),
                           author=list(new_df['Book-Author'].values),
                           img=list(new_df['Image-URL-M'].values),
                           rating=list(new_df['Book-Rating'].values))


if __name__ == '__main__':
    app.run(debug=True)
