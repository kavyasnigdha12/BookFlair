import streamlit as st
import pandas as pd
import joblib

# Load the pre-trained models and data
knn = joblib.load('knn_model.pkl')
encoded_train_features = joblib.load('encoded_train_features.pkl')
book_data = pd.read_pickle('book_data.pkl')

# Function to get book recommendations based on genre
def get_books_by_genre(genre_name, data):
    # Finding books by the specified genre
    books_by_genre = data[data['genre_and_votes'].str.contains(genre_name, case=False)]
    return books_by_genre.head(20)  # Limit to 20 books

def app():
    st.title("Search Books by :violet[Genre]")

    # User input for the genre name
    genre_input = st.text_input("Enter the name of the genre:")
    if genre_input:
        genre_books = get_books_by_genre(genre_input, book_data)
        if not genre_books.empty:
            st.write(f"### Books in genre : {genre_input}")
            # CSS style for cards and container with rainbow border
            card_style = """
            <style>
            .card-container {
                display: flex;
                overflow-x: auto;
                padding: 10px;
            }
            .card {
                display: flex;
                background-color: #000000;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                margin: 10px;
                padding: 20px;
                min-width: 350px;
                max-width: 100%;
                font-family: 'Arial', sans-serif;
                align-items: center;
                box-sizing: border-box;
                flex: none;
                border: 2px solid; 
                border-image: dark-grey; 
            }
            .card img {
                border-radius: 10px;
                width: 100px;
                height: 150px;
                margin-left: 20px;
            }
            .card-content {
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding-right: 20px;
                box-sizing: border-box;
            }
            .card h3 {
                font-size: 20px;
                margin: 10px 0;
            }
            .card p {
                color: gray;
                font-size: 18px;
                margin: 5px 0;
            }
            .card a {
                background-color: #868EFF;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
                cursor: pointer;
                margin-top: 10px;
                align-self: start;
            }
            </style>
            """

            # Display the cards
            st.markdown(card_style, unsafe_allow_html=True)
            st.markdown('<div class="card-container">', unsafe_allow_html=True)

            for index, book in genre_books.iterrows():
                card_html = f"""
                <div class="card">
                    <div class="card-content">
                        <h3>{book['title']}</h3>
                        <p>Average Rating: {book['average_rating']}</p>
                        <a href="{book['amazon_redirect_link']}" target="_blank">Amazon Link</a>
                    </div>
                    <img src="{book['cover_link']}" alt="{book['title']}">
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.write("No books found in genre:", genre_input)

    st.header("Popular Genres", divider='rainbow')
    popular_genres = ["Fantasy", "Science Fiction", "Mystery", "Romance", 
                        "Thriller", "Non-Fiction", "Children's", "Biography", "Poetry"]
    
    # Display authors in a 3x3 matrix with a border
    cols = st.columns(3)
    for i, genre in enumerate(popular_genres):
        with cols[i % 3]:
            author_html = f"""
            <div style="border: 1px solid #ccc; padding: 10px; margin: 5px; border-radius: 5px; text-align: center; background-color: #333; color: white;">
                {genre}
            </div>
            """
            st.markdown(author_html, unsafe_allow_html=True)

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

# Run the app
if __name__ == '__main__':
    app()
