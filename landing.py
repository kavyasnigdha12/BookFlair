import streamlit as st
import mysql.connector
import plotly.express as px
import numpy as np
import pickle

from sklearn.svm import LinearSVC
from sklearn.preprocessing import MultiLabelBinarizer

# List of genres
genres = [
    'Academic', 'Action', 'Adult Fiction', 'Adventure', 'American History', 'Animals', 'Anthropology', 'Architecture',
    'Art', 'Asian Literature', 'Autobiography', 'Biography', 'Biology', 'Body', 'Business', 'Cartography', 'Childrens',
    'Cities', 'Classics', 'Comics', 'Computer Science', 'Computers', 'Cooking', 'Crafts', 'Crime', 'Culture',
    'Design', 'Drama', 'Economics', 'Education', 'Engineering', 'English History', 'Environment', 'Epic', 'Fantasy',
    'Feminism', 'Fiction', 'Finance', 'Folk Tales', 'Folklore', 'Food and Drink', 'Football', 'Games', 'Gardening',
    'Gender', 'Graphic Novels', 'Health', 'Heroic Fantasy', 'History', 'Horror', 'How To', 'Humanities', 'Humor', 'India',
    'Inspirational', 'Internet', 'LGBT', 'Language', 'Law', 'Leadership', 'Literature', 'Love', 'Manga', 'Marriage',
    'Medicine', 'Mental Health', 'Military', 'Music', 'Mythology', 'Nature', 'Neuroscience', 'Nonfiction', 'Nursing',
    'Philosophy', 'Plants', 'Plays', 'Poetry', 'Politics', 'Productivity', 'Pseudoscience', 'Psychology', 'Religion',
    'Romance', 'Science', 'Science Fiction', 'Self Help', 'Short Stories', 'Space', 'Spirituality', 'Sports', 'Stone age',
    'Thriller', 'Travel', 'War', 'Womens', 'Young Adult'
]

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bookflair"
    )

def vote_for_genres(selected_genres):
    conn = get_db_connection()
    cursor = conn.cursor()
    for genre in selected_genres:
        cursor.execute("UPDATE votes SET votes = votes + 1 WHERE genre = %s", (genre,))
    conn.commit()
    cursor.close()
    conn.close()

def get_votes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT genre, votes FROM votes")
    votes = cursor.fetchall()
    cursor.close()
    conn.close()
    return {genre: vote for genre, vote in votes}

# Load SVM model, MultiLabelBinarizer, and title_to_genres dictionary for recommendations
with open('svm_model.pkl', 'rb') as file:
    svm = pickle.load(file)

with open('mlb.pkl', 'rb') as file:
    mlb = pickle.load(file)

with open('title_to_genres.pkl', 'rb') as file:
    title_to_genres = pickle.load(file)

def recommend_books(genres):
    encoded_input = mlb.transform([genres])
    decision = svm.decision_function(encoded_input)
    recommended_book_indices = np.argsort(decision, axis=-1, kind='quicksort', order=None)[0][-8:]
    recommended_books = svm.classes_[recommended_book_indices]
    recommendations = []
    for book in recommended_books:
        recommendations.append({
            "Title": book,
            "Genres": ', '.join(title_to_genres[book])
        })
    return recommendations

def update_recommendations():
    user_voted_genres = [genre for genre, votes in get_votes().items() if votes > 0]

    if user_voted_genres:
        recommendations = recommend_books(user_voted_genres)
        return recommendations
    else:
        return []

def app():
    st.title("Welcome to :violet[𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣]!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/wont_be.jpg", width=300)  # Replace with your image path
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.header('Discover Your Next Favorite Book!', divider='rainbow')
        st.subheader("Get personalized recommendations based on your interests!", divider='rainbow')
        st.button("Flair your Reading")

    st.write("")
    st.header("About", divider="rainbow")
    st.write("BookFlair is an online book recommendation system that recommends books based on user interest. It can do this in three ways:\n1. Based on Books\n2. Based on Genre\n3. Based on Authors.")
    st.write("This Webapp is built on Tensorflow, Keras, Streamlit, HTML&CSS and strives for a visually appealing user experience.")

    # Recommendations section
    st.write("")
    st.subheader("Recommendations Based on Flaired Genres", divider='rainbow')

    # Define custom CSS for recommendation cards
    st.markdown("""
        <style>
        .recommendation-card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        .recommendation-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #fff;
        }
        .recommendation-genres {
            font-size: 1.2em;
            color: #999;
        }
        .rainbow-divider {
            width: 100%;
            height: 2px;
            background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
            border: none;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    recommendations = update_recommendations()

    if recommendations:
        for recommendation in recommendations:
            card_html = f"""
            <div class="recommendation-card">
                <div class="recommendation-title">{recommendation['Title']}</div>
                <div class="recommendation-genres">{recommendation['Genres']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.write("No recommendations available. Vote for genres to get recommendations.")

    #button
    # st.write("")
    # st.write("Select the name of your liked book and search it here ( Amazon Search ) :")
    # st.markdown("""
    #     <a href="https://www.amazon.in/books/s?k=books" target="_blank">
    #         <button style="background-color: #333; border: none; color: white; padding: 10px 16px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 3px 2px; cursor: pointer; border-radius: 4px;">Buy  Books</button>
    #     </a>
    # """, unsafe_allow_html=True)

    # Rainbow-colored divider
    st.markdown('<div class="rainbow-divider"></div>', unsafe_allow_html=True)

    # Footer
    st.markdown("<p style='text-align: center; color: white;'> © 2024 𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣. All rights reserved.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Contact us at: support@bookflair.com</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    app()

######################################################################################
# import streamlit as st

# def app():
#     st.title("Welcome to :violet[𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣]!")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         st.image("images/wont_be.jpg", width=300)  # Replace with your image path
#     with col2:
#         st.write("")
#         st.write("")
#         st.write("")
#         st.header('Discover Your Next Favorite Book!', divider='rainbow')
#         st.subheader("Get personalized recommendations based on your interests!",divider='rainbow')
#         st.button("Flair your Reading")

#     st.header("About",divider="rainbow")
#     st.write("BookFlair is an online book recommendation system that recommends books based on user interest. It can do this in three ways:\n1. Based on Books\n2. Based on Genre\n3. Based on Authors.")
#     st.write("This Webapp is built on Tensorflow, Keras, Streamlit, HTML&CSS and strives for a visually appealing user experience. ")
#     #Include Human's Blood, Sweat and Tears.


#     #footer
#     st.write("---")
#     st.markdown("<p style='text-align: center; color: white;'> © 2024 𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣. All rights reserved.</p>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; color: white;'>Contact us at: support@bookflair.com</p>", unsafe_allow_html=True)

###########################################################################################
