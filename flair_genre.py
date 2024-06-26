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
    st.title("Flair for Your :violet[Favorite Genre]")

    # Include CSS for hover effect
    st.markdown("""
        <style>
        .genre-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            height: 150px;
            text-align: center;
            margin-bottom: 10px;
            transition: transform 0.2s; /* Animation */
        }
        .genre-card:hover {
            transform: scale(1.05); /* (105% zoom) */
            border-color: #868EFF;
            border-width: 2px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Form to select genres and vote
    with st.form(key='vote_form'):
        selected_genres = st.multiselect("Select genres", genres)
        submit_button = st.form_submit_button(label='Vote')

    # Increment the vote count
    if submit_button:
        if selected_genres:
            vote_for_genres(selected_genres)
            st.success(f"Thank you for voting for: {', '.join(selected_genres)}!")
        else:
            st.warning("Please select at least one genre to vote.")

    # Display the votes using styled cards with hover effect
    st.write("")
    st.write("")
    st.subheader("Current Votes", divider='rainbow')
    votes = get_votes()
    cols = st.columns(3)  # Create 3 columns for the grid

    for i, genre in enumerate(genres):
        with cols[i % 3]:  # Distribute genres evenly across the columns
            genre_html = f"""
            <div class="genre-card">
                <h3>{genre}</h3>
                <p>{votes.get(genre, 0)} votes</p>
            </div>
            """
            st.markdown(genre_html, unsafe_allow_html=True)

    # Display a bar chart of the votes
    st.write("")
    st.write("")
    st.subheader("Votes Distribution", divider='rainbow')
    df = {"Genre": list(votes.keys()), "Votes": list(votes.values())}
    fig = px.bar(df, x="Genre", y="Votes", title="Votes per Genre")
    st.plotly_chart(fig)

    # footer CSS        
    st.markdown("""
        <style>
        .rainbow-divider {
            width: 100%;
            height: 2px;
            background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
            border: none;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    # Rainbow-colored divider
    st.markdown('<div class="rainbow-divider"></div>', unsafe_allow_html=True)
    # Footer
    st.markdown("<p style='text-align: center; color: white;'> © 2024 𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣. All rights reserved.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Contact us at: support@bookflair.com</p>", unsafe_allow_html=True)

    # Recommendations based on user-voted genres
    # st.write("")
    # st.write("")
    # st.subheader("Recommendations Based on Your Voted Genres")
    # recommendations = update_recommendations()

    # if recommendations:
    #     for recommendation in recommendations:
    #         st.write(f"*Title:* {recommendation['Title']}")
    #         st.write(f"*Genres:* {recommendation['Genres']}")
    # else:
    #     st.write("No recommendations available. Vote for genres to get recommendations.")

if __name__ == '__main__':
    app()

##########################################################################################
# #LITTLE ADVANCDED _ SHOWS RECOM ONLY WHEN USER SELECTS THE VOTES
# import streamlit as st
# import numpy as np
# import pandas as pd
# import mysql.connector
# import plotly.express as px
# import pickle

# from sklearn.svm import LinearSVC
# from sklearn.preprocessing import MultiLabelBinarizer
# from sklearn.model_selection import train_test_split

# # Load SVM model, MultiLabelBinarizer, and title_to_genres dictionary
# with open('svm_model.pkl', 'rb') as file:
#     svm = pickle.load(file)

# with open('mlb.pkl', 'rb') as file:
#     mlb = pickle.load(file)

# with open('title_to_genres.pkl', 'rb') as file:
#     title_to_genres = pickle.load(file)

# # Other code from your stats page
# genres = [
#     'Academic', 'Action', 'Adult Fiction', 'Adventure', 'American History', 'Animals', 'Anthropology', 'Architecture',
#     'Art', 'Asian Literature', 'Autobiography', 'Biography', 'Biology', 'Body', 'Business', 'Cartography', 'Childrens',
#     'Cities', 'Classics', 'Comics', 'Computer Science', 'Computers', 'Cooking', 'Crafts', 'Crime', 'Culture', 'Dc Comics',
#     'Design', 'Drama', 'Economics', 'Education', 'Engineering', 'English History', 'Environment', 'Epic', 'Fantasy',
#     'Feminism', 'Fiction', 'Finance', 'Folk Tales', 'Folklore', 'Food and Drink', 'Football', 'Games', 'Gardening',
#     'Gender', 'Graphic Novels', 'Health', 'Heroic Fantasy', 'History', 'Horror', 'How To', 'Humanities', 'Humor', 'India',
#     'Inspirational', 'Internet', 'LGBT', 'Language', 'Law', 'Leadership', 'Literature', 'Love', 'Manga', 'Marriage',
#     'Medicine', 'Mental Health', 'Military', 'Music', 'Mythology', 'Nature', 'Neuroscience', 'Nonfiction', 'Nursing',
#     'Philosophy', 'Plants', 'Plays', 'Poetry', 'Politics', 'Productivity', 'Pseudoscience', 'Psychology', 'Religion',
#     'Romance', 'Science', 'Science Fiction', 'Self Help', 'Short Stories', 'Space', 'Spirituality', 'Sports', 'Stone age',
#     'Thriller', 'Travel', 'War', 'Womens', 'Young Adult'
# ]

# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="bookflair"
#     )

# def get_votes():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT genre, votes FROM votes")
#     votes = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return {genre: vote for genre, vote in votes}

# def recommend_books(genres):
#     encoded_input = mlb.transform([genres])
#     decision = svm.decision_function(encoded_input)
#     recommended_book_indices = np.argsort(decision, axis=-1, kind='quicksort', order=None)[0][-4:]
#     recommended_books = svm.classes_[recommended_book_indices]
#     recommendations = []
#     for book in recommended_books:
#         recommendations.append({
#             "Title": book,
#             "Genres": ', '.join(title_to_genres[book])
#         })
#     return recommendations

#     # Function to increment vote count
# def vote_for_genres(selected_genres):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     for genre in selected_genres:
#         cursor.execute("UPDATE votes SET votes = votes + 1 WHERE genre = %s", (genre,))
#     conn.commit()
#     cursor.close()
#     conn.close()

# # Function to get current votes
# def get_votes():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT genre, votes FROM votes")
#     votes = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return {genre: vote for genre, vote in votes}

# def app():
#     st.title("Flair for Your Favorite Genre")
    
#     # Your existing code for voting and displaying votes
#     # Include CSS for hover effect
#     st.markdown("""
#         <style>
#         .genre-card {
#             border: 1px solid #ddd;
#             border-radius: 5px;
#             padding: 10px;
#             height: 150px;
#             text-align: center;
#             margin-bottom: 10px;
#             transition: transform 0.2s; /* Animation */
#         }
#         .genre-card:hover {
#             transform: scale(1.05); /* (105% zoom) */
#             border-color: #868EFF;
#             border-width: 2px;
#         }
#         </style>
#         """, unsafe_allow_html=True)

#     # Form to select genres
#     with st.form(key='vote_form'):
#         selected_genres = st.multiselect("Select genres", genres)
#         submit_button = st.form_submit_button(label='Vote')

#     # Increment the vote count
#     if submit_button:
#         if selected_genres:
#             vote_for_genres(selected_genres)
#             st.success(f"Thank you for voting for: {', '.join(selected_genres)}!")
#         else:
#             st.warning("Please select at least one genre to vote.")

#     # Display the votes using styled cards with hover effect
#     st.write("")
#     st.write("")
#     st.subheader("Current Votes", divider='rainbow')
#     votes = get_votes()
#     # Display genres in a 3x3 grid
#     cols = st.columns(3)  # Create 3 columns for the grid

#     for i, genre in enumerate(genres):
#         with cols[i % 3]:  # Distribute genres evenly across the columns
#             genre_html = f"""
#             <div class="genre-card">
#                 <h3>{genre}</h3>
#                 <p>{votes.get(genre, 0)} votes</p>
#             </div>
#             """
#             st.markdown(genre_html, unsafe_allow_html=True)

#     # Display a bar chart of the votes
#     st.write("")
#     st.write("")
#     st.subheader("Votes Distribution", divider='rainbow')
#     df = {"Genre": list(votes.keys()), "Votes": list(votes.values())}
#     fig = px.bar(df, x="Genre", y="Votes", title="Votes per Genre")
#     st.plotly_chart(fig)

#     #new code    
#     st.subheader("Recommendations Based on Your Voted Genres")
#     user_voted_genres = []  # Collect voted genres here
#     for genre, votes in get_votes().items():
#         if votes > 0:
#             user_voted_genres.append(genre)
#     if user_voted_genres:
#         recommendations = recommend_books(user_voted_genres)
#         for recommendation in recommendations:
#             st.write(f"*Title:* {recommendation['Title']}")
#             st.write(f"*Genres:* {recommendation['Genres']}")
#     else:
#         st.write("No recommendations available. Vote for genres to get recommendations.")

# if __name__ == '_main_':
#     app()

##########################################################################################
#BASIC
# import streamlit as st
# import mysql.connector
# import plotly.express as px

# # List of genres
# genres = [
#     'Academic', 'Action','Adult Fiction', 'Adventure', 'American History','Animals', 'Anthropology', 'Architecture', 'Art', 'Asian Literature', 'Autobiography', 'Biography','Biology', 'Body', 'Business', 'Cartography','Childrens', 'Cities', 'Classics', 'Comics', 'Computer Science','Computers','Cooking','Crafts', 'Crime', 'Culture', 'Dc Comics', 'Design', 'Drama', 'Economics', 'Education', 'Engineering', 'English History', 'Environment', 'Epic', 'Fantasy', 'Feminism', 'Fiction', 'Finance','Folk Tales', 'Folklore', 'Food and Drink', 'Football', 'Games', 'Gardening', 'Gender', 'Graphic Novels', 'Health', 'Heroic Fantasy', 'History', 'Horror', 'How To', 'Humanities', 'Humor', 'India', 'Inspirational', 'Internet', 'LGBT','Language', 'Law', 'Leadership', 'Literature', 'Love', 'Manga', 'Marriage', 'Medicine', 'Mental Health', 'Military', 'Music', 'Mythology', 'Nature', 'Neuroscience', 'Nonfiction', 'Nursing', 'Philosophy', 'Plants', 'Plays', 'Poetry', 'Politics', 'Productivity', 'Pseudoscience', 'Psychology','Religion', 'Romance', 'Science', 'Science Fiction','Self Help', 'Short Stories', 'Space', 'Spirituality', 'Sports', 'Stone age', 'Thriller', 'Travel', 'War', 'Womens','Young Adult'
# ]

# # Database connection
# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",         # Replace with your host
#         user="root",     # Replace with your MySQL username
#         password="", # Replace with your MySQL password
#         database="bookflair"    # Database name
#     )

# # Function to increment vote count
# def vote_for_genres(selected_genres):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     for genre in selected_genres:
#         cursor.execute("UPDATE votes SET votes = votes + 1 WHERE genre = %s", (genre,))
#     conn.commit()
#     cursor.close()
#     conn.close()

# # Function to get current votes
# def get_votes():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT genre, votes FROM votes")
#     votes = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return {genre: vote for genre, vote in votes}

# # Streamlit app function
# def app():
#     st.title("Flair for Your :violet[Favorite Genre]")

    # # Include CSS for hover effect
    # st.markdown("""
    #     <style>
    #     .genre-card {
    #         border: 1px solid #ddd;
    #         border-radius: 5px;
    #         padding: 10px;
    #         height: 150px;
    #         text-align: center;
    #         margin-bottom: 10px;
    #         transition: transform 0.2s; /* Animation */
    #     }
    #     .genre-card:hover {
    #         transform: scale(1.05); /* (105% zoom) */
    #         border-color: #868EFF;
    #         border-width: 2px;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)

    # # Form to select genres
    # with st.form(key='vote_form'):
    #     selected_genres = st.multiselect("Select genres", genres)
    #     submit_button = st.form_submit_button(label='Vote')

    # # Increment the vote count
    # if submit_button:
    #     if selected_genres:
    #         vote_for_genres(selected_genres)
    #         st.success(f"Thank you for voting for: {', '.join(selected_genres)}!")
    #     else:
    #         st.warning("Please select at least one genre to vote.")

    # # Display the votes using styled cards with hover effect
    # st.write("")
    # st.write("")
    # st.subheader("Current Votes", divider='rainbow')
    # votes = get_votes()
    # # Display genres in a 3x3 grid
    # cols = st.columns(3)  # Create 3 columns for the grid

    # for i, genre in enumerate(genres):
    #     with cols[i % 3]:  # Distribute genres evenly across the columns
    #         genre_html = f"""
    #         <div class="genre-card">
    #             <h3>{genre}</h3>
    #             <p>{votes.get(genre, 0)} votes</p>
    #         </div>
    #         """
    #         st.markdown(genre_html, unsafe_allow_html=True)

    # # Display a bar chart of the votes
    # st.write("")
    # st.write("")
    # st.subheader("Votes Distribution", divider='rainbow')
    # df = {"Genre": list(votes.keys()), "Votes": list(votes.values())}
    # fig = px.bar(df, x="Genre", y="Votes", title="Votes per Genre")
    # st.plotly_chart(fig)

# if __name__ == '_main_':
#     app()