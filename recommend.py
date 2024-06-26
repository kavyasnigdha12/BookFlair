import streamlit as st
import joblib
import pandas as pd
from tensorflow.keras.models import load_model

# Function to get book recommendations
def get_book_recommendations(book_title, data, knn, encoded_train_features):
    # Finding the index of the book in the DataFrame
    try:
        sample_book_index = data[data['title'] == book_title].index[0]
    except IndexError:
        st.write("Book not found in dataset.")
        return

    # Display information about the sample book
    st.markdown(
        f"""
        <style>
        .rainbow-border {{
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 2px solid;
            border-image: linear-gradient(to right, violet, indigo, blue, green, yellow, orange, red);
            border-image-slice: 1;
        }}
        </style>
        <div class='rainbow-border'>
            <h3>{data.loc[sample_book_index, 'title']}</h3>
            <p>Author: {data.loc[sample_book_index, 'author']}</p>
            <p>Genres: {", ".join(data.loc[sample_book_index, 'genre_and_votes'].split(";")[:4])}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Finding nearest neighbors
    distances, indices = knn.kneighbors(encoded_train_features[sample_book_index].reshape(1, -1))

    # HTML and CSS for styling cards
    card_html = """
        <style>
            .card-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 10px;
                flex-wrap: wrap;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 10px;
                width: 300px;
                height: auto;
                padding: 20px;
                margin: 10px;
                text-align: center;
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            .card:hover {{
                transform: scale(1.05);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                color: #BB86FF;
            }}
            .card img {{
                width: 100%;
                max-height: 300px;
                border-radius: 10px;
                margin-bottom: 10px;
            }}
        </style>
        <div class="card-container">
            {cards}
        </div>
    """

    card_template = """
        <div class="card">
            <img src="{image}" alt="{title} Image">
            <h3>{title}</h3>
            <p>Author: {author}</p>
            <p>Genres: {genres}</p>
            <p>Average rating: {rating}</p>
            <a href="{link}" target="_blank"><button style="background-color: #868EFF; color: white; border: none; border-radius: 5px; padding: 10px 15px; cursor: pointer;">Amazon Link</button></a>
        </div>
    """

    # Generating cards for similar books, limiting to 8 recommendations
    cards = ""
    for i in indices.flatten()[1:7]:
        title = data.iloc[i]['title']
        author = data.iloc[i]['author']
        genres = data.iloc[i]['genre_and_votes'].split(";")[:4]
        rating = data.iloc[i]['average_rating']
        link = data.iloc[i]['amazon_redirect_link']
        image = data.iloc[i]['cover_link']

        card = card_template.format(
            title=title,
            author=author,
            genres=", ".join(genres),
            rating=rating,
            link=link,
            image=image
        )
        cards += card

    st.markdown(card_html.format(cards=cards), unsafe_allow_html=True)

# Define the main app function
def app():
    st.title("Recommendations On :violet[Books]")

    # Load the saved models and data
    knn = joblib.load('knn_model.pkl')
    encoded_train_features = joblib.load('encoded_train_features.pkl')
    book_data = pd.read_pickle('book_data.pkl')

    # User input for the book title
    user_input = st.text_input("Enter the title of the book for recommendations:")

    if user_input:
        get_book_recommendations(user_input, book_data, knn, encoded_train_features)

    # Display a few book titles from the dataset
    st.header("Popular Books", divider="rainbow")
    popular_books = ["Inner Circle", "After Ever After", "10th Grade", "Nancy Drew: #1-64", "Crooked House", "The Long Mars", "Ten Thousand Skies Above You", "The Inexplicable Logic of My Life", "The Neutronium Alchemist: Consolidation"]
    
    # Display popular book titles in a 3x3 grid with styled borders
    cols = st.columns(3)
    for i, title in enumerate(popular_books):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; padding: 10px; margin: 5px; border-radius: 5px; text-align: center; background-color: #333; color: white;">
                    {title}
                </div>
                """,
                unsafe_allow_html=True
            )

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
