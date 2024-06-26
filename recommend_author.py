import streamlit as st
import pandas as pd

# Function to get books by author
def get_books_by_author(author_name, data):
    books_by_author = data[data['author'].str.contains(author_name, case=False)]
    if books_by_author.empty:
        st.write(f"No books found by author: **{author_name}**")
        return

    # Displaying books by the specified author
    st.write(f"### Books by author: {author_name}")
    for _, row in books_by_author.iterrows():
        st.markdown("""
            <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 15px; background-color: #333; color: white;">
                <div style="display: flex;">
                    <div style="flex: 3; padding-right: 15px;">
                        <p style="font-size: 26px;"><strong>Title:</strong> {}</p>
                        <p>Average rating : {}</p>
                        <a href="{}" target="_blank">
                            <button style="background-color:#868EFF;color:white;padding:8px;border:none;border-radius:5px;cursor:pointer;">
                                Buy on Amazon
                            </button>
                        </a>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <img src="{}" width="150" style="border-radius: 5px;">
                    </div>
                </div>
            </div>
        """.format(row['title'], row['average_rating'], row['amazon_redirect_link'], row['cover_link']), unsafe_allow_html=True)

def app():
    st.title('Book Search by :violet[Author]')

    # Load book data (assuming it's stored in a variable named 'book_data')
    # You can replace this with your actual method of loading the data
    book_data = pd.read_pickle('book_data.pkl')

    # User input for the author name
    author_input = st.text_input("Enter the name of the author:")
    
    if st.button('Search'):
        if author_input:
            get_books_by_author(author_input, book_data)
        else:
            st.warning("Please enter an author name to search.")

    # Display a few author names from the database
    st.header("Popular Authors", divider='rainbow')
    popular_authors = book_data['author'].value_counts().head(9).index.tolist()
    
    # Display authors in a 3x3 matrix with a border
    cols = st.columns(3)
    for i, author in enumerate(popular_authors):
        with cols[i % 3]:
            author_html = f"""
            <div style="border: 1px solid #ccc; padding: 10px; margin: 5px; border-radius: 5px; text-align: center; background-color: #333; color: white;">
                {author}
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

if __name__ == '__main__':
    app()


# # that layout is not nice
# import streamlit as st
# import pandas as pd

# # Function to get books by author
# def get_books_by_author(author_name, data):
#     books_by_author = data[data['author'] == author_name]
#     if books_by_author.empty:
#         st.write("No books found by author:", author_name)
#         return

#     # Displaying books by the specified author
#     st.write("Books by author:", author_name)
#     for _, row in books_by_author.iterrows():
#         st.write("---")
#         col1, col2 = st.columns([2, 1])
        
#         # Displaying book details in column 1
#         with col1:
#             st.write("Title:", row['title'])
#             st.write("Average rating by users:", row['average_rating'])
#             # Create a button-like link using HTML
#             amazon_button = f"""
#             <a href="{row['amazon_redirect_link']}" target="_blank">
#                 <button style="background-color:#868EFF;color:white;padding:10px;border:none;border-radius:5px;cursor:pointer;">
#                     Buy on Amazon
#                 </button>
#             </a>
#             """
#             st.markdown(amazon_button, unsafe_allow_html=True)
        
#         # Displaying book cover image in column 2
#         with col2:
#             st.image(row['cover_link'], width=150)

# def app():
#     st.title('Book Search by Author')
    
#     # Load book data (assuming it's stored in a variable named 'book_data')
#     # You can replace this with your actual method of loading the data
#     book_data = pd.read_pickle('book_data.pkl')

#     # User input for the author name
#     author_input = st.text_input("Enter the name of the author:")
    
#     if st.button('Search'):
#         get_books_by_author(author_input, book_data)
    
#     # Display a few author names from the database
#     st.title("Popular Authors")
#     popular_authors = book_data['author'].value_counts().head(9).index.tolist()
    
#     # Display authors in a 3x3 matrix with a border
#     cols = st.columns(3)
#     for i, author in enumerate(popular_authors):
#         with cols[i % 3]:
#             author_html = f"""
#             <div style="border: 1px solid white; padding: 10px; margin: 5px; border-radius: 5px; text-align: center;">
#                 {author}
#             </div>
#             """
#             st.markdown(author_html, unsafe_allow_html=True)

# if __name__ == '_main_':
#     app()