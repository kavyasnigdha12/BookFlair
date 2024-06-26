##########################################################################################
import streamlit as st

def app():
    st.title("Discover What to :violet[Read Next]")
    st.write("Let's discover your next favorite genre based on your reading preferences.")
    st.write("Note: Please answer in upper case")
    # Rainbow-colored divider
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
    st.markdown('<div class="rainbow-divider"></div>', unsafe_allow_html=True)

    # Part 1: Reading Habits
    st.header("Part 1: Reading Habits")
    reading_habits_questions = [
        ("How often do you find yourself in a reading slump?",
         ["Rarely, I can always find something to keep me engaged.",
          "Occasionally, but I usually bounce back quickly.",
          "Frequently, I struggle to find books that hold my attention."]),

        ("When choosing a book, what factors influence you the most? (Choose two)",
         ["Genre recommendations from friends or online communities.",
          "Awards and critical acclaim.",
          "Blurb or synopsis that piques my curiosity.",
          "Eye-catching cover art or intriguing title."]),

        ("Do you prefer standalone novels or series?",
         ["Standalone novels - I enjoy a complete story in one book.",
          "Series - I love getting invested in characters and a world over multiple books."])
    ]

    answers_part1 = []
    for idx, (question, options) in enumerate(reading_habits_questions):
        st.subheader(f"{idx + 1}. {question}")
        for opt_idx, option in enumerate(options):
            st.write(f"    {chr(65 + opt_idx)}. {option}")
        if idx == 1:
            answer = st.text_input(f"Your answer (choose two, e.g., AB): ", key=f"part1_{idx}").upper()
        else:
            answer = st.text_input(f"Your answer (A/B/C): ", key=f"part1_{idx}").upper()
        answers_part1.append(answer)

    # Part 2: Favorite Books & Genres
    st.write("")
    st.header("\n\nPart 2: Favorite Books & Genres")
    favorite_books_questions = [
        ("Think of a book you absolutely loved. What genre was it?",
         ["Mystery/Thriller",
          "Fantasy/Sci-Fi",
          "Romance",
          "Historical Fiction/Non-Fiction",
          "Literary Fiction/Classics"]),

        ("What element did you enjoy most about that book?",
         ["The suspenseful plot and unexpected twists.",
          "The immersive world-building and fantastical elements.",
          "The heartwarming love story and character development.",
          "The historical accuracy or insightful exploration of real-world issues.",
          "The beautiful prose style and exploration of complex themes."]),

        ("Have you ever tried a genre outside your comfort zone?",
         ["Yes, and I enjoyed it!",
          "Maybe once or twice, but it wasn't for me.",
          "No, I prefer sticking to genres I know I like."])
    ]

    answers_part2 = []
    for idx, (question, options) in enumerate(favorite_books_questions):
        st.subheader(f"{idx + 1}. {question}")
        for opt_idx, option in enumerate(options):
            st.write(f"    {chr(65 + opt_idx)}. {option}")
        answer = st.text_input("Your answer (A/B/C/D/E): ", key=f"part2_{idx}").upper()
        answers_part2.append(answer)

    # Part 3: Literary Interests
    st.write("")
    st.header("\n\nPart 3: Literary Interests")
    literary_interests_questions = [
        ("Imagine yourself on a grand adventure. What setting would most excite you?",
         ["A bustling metropolis filled with secrets and hidden clues.",
          "A mystical land with powerful magic and mythical creatures.",
          "A charming seaside town or a grand historical palace.",
          "A time period vastly different from our own, filled with historical intrigue.",
          "A quiet retreat in nature where complex human emotions unfold."]),

        ("What kind of characters do you find most compelling?",
         ["The brilliant detective or resourceful protagonist facing a dangerous challenge.",
          "The powerful mage or brave warrior on an epic quest.",
          "The passionate lovers or charming characters navigating relationships.",
          "The historical figure or social reformer making a difference in the world.",
          "The deeply flawed protagonist grappling with existential questions."]),

        ("What kind of ending leaves you feeling satisfied?",
         ["A shocking revelation and a sense of justice prevailing.",
          "A stunning victory for good against evil, or a satisfying world-changing discovery.",
          "A heartwarming resolution or a couple finding their happily ever after.",
          "A thought-provoking conclusion that leaves you pondering the bigger picture.",
          "A poignant or bittersweet ending that resonates on an emotional level."])
    ]

    answers_part3 = []
    for idx, (question, options) in enumerate(literary_interests_questions):
        st.subheader(f"{idx + 1}. {question}")
        for opt_idx, option in enumerate(options):
            st.write(f"    {chr(65 + opt_idx)}. {option}")
        answer = st.text_input("Your answer (A/B/C/D/E): ", key=f"part3_{idx}").upper()
        answers_part3.append(answer)

    if st.button("Submit"):
        # Validate if all questions are answered
        if not all(answers_part1) or not all(answers_part2) or not all(answers_part3):
            st.error("Please answer all questions before submitting.")
        else:
            # Process answers and provide genre recommendations
            answer_list = answers_part1 + answers_part2 + answers_part3
            count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

            for ans in answer_list:
                for letter in ans:
                    if letter in count:
                        count[letter] += 1

            max_genre = max(count, key=count.get)

            genre_recommendations = {
                'A': "Dive into a thrilling Mystery, Detective Fiction, or Crime novel next! "
                     "You might love authors like Agatha Christie, Gillian Flynn, or Lee Child.",
                'B': "Unleash your imagination with Fantasy, Sci-Fi, or Dystopian Fiction! "
                     "Check out works by J.R.R. Tolkien, Margaret Atwood, or N.K. Jemisin.",
                'C': "Let your heart melt with a captivating Romance novel. Explore authors like Jane Austen, "
                     "Nicholas Sparks, or Talia Hibbert.",
                'D': "Embark on a journey through time with Historical Fiction or delve into Non-Fiction based "
                     "on a period or topic that interests you. Consider Hilary Mantel, Yuval Noah Harari, or authors "
                     "specializing in your preferred historical era.",
                'E': "Get lost in the beautiful prose and profound themes of Literary Fiction or delve into classic works. "
                     "Explore authors like Toni Morrison, Virginia Woolf, or your favorite classic writer."
            }

            book_recommendations = {
                'A': ("Agatha Christie:\n"
                      "- Murder on the Orient Express\n"
                      "- The Murder of Roger Ackroyd\n"
                      "- And Then There Were None\n"
                      "- Death on the Nile\n"
                      "- The A.B.C. Murders\n\n"
                      "Gillian Flynn:\n"
                      "- Gone Girl\n"
                      "- Sharp Objects\n"
                      "- Dark Places\n"
                      "- The Grownup\n"
                      "- Broken (in the anthology \"Rogues\")\n\n"
                      "Lee Child:\n"
                      "- Killing Floor\n"
                      "- Die Trying\n"
                      "- Tripwire\n"
                      "- Running Blind\n"
                      "- Echo Burning"),

                'B': ("J.R.R. Tolkien:\n"
                      "- The Hobbit\n"
                      "- The Fellowship of the Ring\n"
                      "- The Two Towers\n"
                      "- The Return of the King\n"
                      "- The Silmarillion\n\n"
                      "Margaret Atwood:\n"
                      "- The Handmaid's Tale\n"
                      "- Oryx and Crake\n"
                      "- The Year of the Flood\n"
                      "- MaddAddam\n"
                      "- Alias Grace\n\n"
                      "N.K. Jemisin:\n"
                      "- The Fifth Season\n"
                      "- The Obelisk Gate\n"
                      "- The Stone Sky\n"
                      "- The City We Became\n"
                      "- The Killing Moon"),

                'C': ("Jane Austen:\n"
                      "- Pride and Prejudice\n"
                      "- Sense and Sensibility\n"
                      "- Emma\n"
                      "- Mansfield Park\n"
                      "- Persuasion\n\n"
                      "Nicholas Sparks:\n"
                      "- The Notebook\n"
                      "- A Walk to Remember\n"
                      "- Dear John\n"
                      "- The Last Song\n"
                      "- Safe Haven\n\n"
                      "Talia Hibbert:\n"
                      "- Get a Life, Chloe Brown\n"
                      "- Take a Hint, Dani Brown\n"
                      "- Act Your Age, Eve Brown\n"
                      "- The Princess Trap\n"
                      "- A Girl Like Her"),

                'D': ("Hilary Mantel:\n"
                      "- Wolf Hall\n"
                      "- Bring Up the Bodies\n"
                      "- The Mirror and the Light\n"
                      "- A Place of Greater Safety\n"
                      "- Beyond Black\n\n"
                      "Yuval Noah Harari:\n"
                      "- Sapiens: A Brief History of Humankind\n"
                      "- Homo Deus: A Brief History of Tomorrow\n"
                      "- 21 Lessons for the 21st Century\n"
                      "- Money: The True Story of a Made-Up Thing\n"
                      "- The Ultimate Experience\n\n"
                      "Other Authors:\n"
                      "- Ken Follett: The Pillars of the Earth\n"
                      "- Philippa Gregory: The Other Boleyn Girl\n"
                      "- Colson Whitehead: The Underground Railroad\n"
                      "- Anthony Doerr: All the Light We Cannot See\n"
                      "- Erik Larson: The Devil in the White City"),

                'E': ("Toni Morrison:\n"
                      "- Beloved\n"
                      "- Song of Solomon\n"
                      "- The Bluest Eye\n"
                      "- Sula\n"
                      "- Jazz\n\n"
                      "Virginia Woolf:\n"
                      "- Mrs. Dalloway\n"
                      "- To the Lighthouse\n"
                      "- Orlando\n"
                      "- A Room of One's Own\n"
                      "- The Waves\n\n"
                      "Other Classic Authors:\n"
                      "- Leo Tolstoy: War and Peace\n"
                      "- Fyodor Dostoevsky: Crime and Punishment\n"
                      "- James Joyce: Ulysses\n"
                      "- Gabriel Garcia Marquez: One Hundred Years of Solitude\n"
                      "- Herman Melville: Moby-Dick")
            }

            st.write("\nBased on your answers, you might enjoy exploring the following genres:")
            st.write(genre_recommendations[max_genre])
            st.write("\nHere are some book recommendations for you:")
            st.write(book_recommendations[max_genre])

            # Rainbow-colored divider
    st.markdown('<div class="rainbow-divider"></div>', unsafe_allow_html=True)
    # Footer
    st.markdown("<p style='text-align: center; color: white;'> © 2024 𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣. All rights reserved.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Contact us at: support@bookflair.com</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()
