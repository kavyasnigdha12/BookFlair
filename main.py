import streamlit as st
import streamlit_option_menu as option_menu

import account
import home
import recommend
import recommend_author
import recommend_genre
import flair_genre
import landing
import pages_ahead

st.set_page_config(
    page_title="𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣!"
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })    

    def run(self):
        with st.sidebar:
            selected_app = option_menu.option_menu(
                menu_title='𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣',
                options=['Home', 'Recommend', 'Author Recommend', 'Genre Recommend', 'Flair Genre', 'Pages Ahead', 'Account'],  # Add Reader Quiz
                icons=['house', 'journal-bookmark-fill', 'book', 'tags', 'stars', 'bookmark-heart', 'person-circle'],  # Add icon for Reader Quiz
                menu_icon='magic',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#BB86FF"},
                    "nav-link-selected": {"background-color": "purple"},
                }
            )

        # Ensure user is logged in to access all sections except Home and Account
        if st.session_state.get('logged_in', False):
            if selected_app == "Home":
                landing.app()  # Show the landing page after login instead of home
            elif selected_app == "Recommend":
                recommend.app()
            elif selected_app == "Author Recommend":
                recommend_author.app()
            elif selected_app == "Genre Recommend":
                recommend_genre.app()
            elif selected_app == "Flair Genre":
                flair_genre.app()
            elif selected_app == "Pages Ahead":  # Handle Reader Quiz selection
                pages_ahead.app()  # Show the Reader Quiz page
            elif selected_app == "Account":
                account.app()
        else:
            if selected_app == "Home":
                home.app()
            elif selected_app == "Account":
                account.app()
            else:
                st.warning("Please log in to access this section.")
                account.app()

# Create an instance of MultiApp
app = MultiApp()

# Add your apps
app.add_app("Home", home.app)
app.add_app("Account", account.app)
app.add_app("Recommend", recommend.app)
app.add_app("Author Recommend", recommend_author.app)
app.add_app("Genre Recommend", recommend_genre.app)
app.add_app("Flair Genre", flair_genre.app)
app.add_app("Reader Quiz", pages_ahead.app)  # Add the Reader Quiz page
app.add_app("Landing", landing.app)  # Add the landing page

# Run the app
app.run()

#########################################################################################
