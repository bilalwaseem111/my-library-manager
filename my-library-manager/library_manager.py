import streamlit as st  # type: ignore
import pandas as pd  # type: ignore

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }

    .stHeader {
        color: #4a4a4a;
        font-family: 'Georgia', serif;
    }

    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }

    .stButton button:hover {
        background-color: #45a049;
    }

    .stTextInput input, .stNumberInput input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 8px;
    }

    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar Footer Styling */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        left: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Arial', sans-serif;
    }

    .sidebar-footer-text {
        font-size: 14px;
        color: #333333;
        font-weight: 600;
    }

    .sidebar-linkedin-logo {
        width: 30px;
        height: 30px;
        transition: transform 0.4s ease, filter 0.4s ease;
        cursor: pointer;
    }

    .sidebar-linkedin-logo:hover {
        transform: scale(1.3);
        filter: drop-shadow(0 0 6px #0077b5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.title("📚 Personal Library Manager")

# Initialize session state to store the library data
if 'library' not in st.session_state:
    # Pre-populated book examples
    st.session_state.library = pd.DataFrame([
        {"Title": "Atomic Habits", "Author": "James Clear", "Genre": "Self-Help", "Year": 2018},
        {"Title": "The Alchemist", "Author": "Paulo Coelho", "Genre": "Fiction", "Year": 1988},
        {"Title": "1984", "Author": "George Orwell", "Genre": "Dystopian", "Year": 1949},
        {"Title": "Sapiens", "Author": "Yuval Noah Harari", "Genre": "History", "Year": 2011},
        {"Title": "The Lean Startup", "Author": "Eric Ries", "Genre": "Business", "Year": 2011}
    ])

# Sidebar for adding a new book
with st.sidebar:
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Year", min_value=1800, max_value=2023, step=1)

    if st.button("Add Book"):
        if title and author and genre and year:
            new_book = pd.DataFrame([[title, author, genre, year]],
                                    columns=["Title", "Author", "Genre", "Year"])
            st.session_state.library = pd.concat([st.session_state.library, new_book], ignore_index=True)
            st.success("✅ Book added successfully!")
            st.balloons()  # Celebration animation
        else:
            st.error("⚠️ Please fill in all fields.")

    # Sidebar footer with LinkedIn link
    st.markdown(
        """
        <div class="sidebar-footer">
            <p class="sidebar-footer-text">Made by Bilal Waseem</p>
            <a href="https://www.linkedin.com/in/bilal-waseem-b44006338" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" class="sidebar-linkedin-logo" alt="LinkedIn Logo">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Display the library
st.header("📚 Your Library")
if not st.session_state.library.empty:
    st.dataframe(st.session_state.library, use_container_width=True)
else:
    st.info("Your library is empty. Add some books!")

# Search Books
st.header("🔍 Search Books")
search_query = st.text_input("Search by Title, Author, or Genre")
if search_query:
    filtered_books = st.session_state.library[
        st.session_state.library["Title"].str.contains(search_query, case=False) |
        st.session_state.library["Author"].str.contains(search_query, case=False) |
        st.session_state.library["Genre"].str.contains(search_query, case=False)
    ]
    if not filtered_books.empty:
        st.dataframe(filtered_books, use_container_width=True)
    else:
        st.info("🚫 No books found matching your search.")
else:
    st.info("Type a search term to filter books.")

# Edit Book Details
st.header("✏️ Edit Book Details")
if not st.session_state.library.empty:
    book_to_edit = st.selectbox("Select a book to edit", st.session_state.library["Title"])
    if book_to_edit:
        book_index = st.session_state.library[st.session_state.library["Title"] == book_to_edit].index[0]
        with st.form(key="edit_form"):
            new_title = st.text_input("Title", value=st.session_state.library.at[book_index, "Title"])
            new_author = st.text_input("Author", value=st.session_state.library.at[book_index, "Author"])
            new_genre = st.text_input("Genre", value=st.session_state.library.at[book_index, "Genre"])
            new_year = st.number_input("Year",
                                       value=st.session_state.library.at[book_index, "Year"],
                                       min_value=1800, max_value=2023, step=1)
            if st.form_submit_button("Update Book"):
                st.session_state.library.at[book_index, "Title"] = new_title
                st.session_state.library.at[book_index, "Author"] = new_author
                st.session_state.library.at[book_index, "Genre"] = new_genre
                st.session_state.library.at[book_index, "Year"] = new_year
                st.success("✅ Book updated successfully!")
                st.snow()  # Snow animation for fun
else:
    st.info("There are no books to edit yet!")

# Delete a Book
st.header("🗑️ Delete a Book")
if not st.session_state.library.empty:
    book_to_delete = st.selectbox("Select a book to delete", st.session_state.library["Title"])
    if st.button("Delete Book"):
        st.session_state.library = st.session_state.library[
            st.session_state.library["Title"] != book_to_delete
        ]
        st.success(f"🗑️ Book '{book_to_delete}' deleted successfully!")
else:
    st.info("No books to delete.")

# Export Library as CSV
st.header("📤 Export Library")
if not st.session_state.library.empty:
    csv = st.session_state.library.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Library as CSV",
        data=csv,
        file_name="my_library.csv",
        mime="text/csv",
    )
else:
    st.info("Add some books to export your library!")
 






























































































 
# 1️⃣ Start wali cheezain
# python
# Copy
# Edit
# import streamlit as st  # type: ignore
# import pandas as pd  # type: ignore
# Ye dono libraries import ki hain.
# streamlit se hum apna web app bana rahe hain.
# pandas se hum table (DataFrame) bana rahe hain jo books ki list rakhti hai.
# 2️⃣ CSS wali decoration 🎨
# python
# Copy
# Edit
# st.markdown(
#     """
#     <style>
#         .....
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# Ye CSS hai, basically style dene ke liye:
# Background color,
# Buttons ka design,
# Text input boxes ka style,
# Dataframe (table) ke liye box-shadow waghera
# Aur sabse important, sidebar mein footer add kiya with LinkedIn logo 💼
# 3️⃣ Title ka kaam
# python
# Copy
# Edit
# st.title("📚 Personal Library Manager")
# Ye upar heading show karta hai app ka naam.
# 4️⃣ Library ka data (books ka list)
# python
# Copy
# Edit
# if 'library' not in st.session_state:
# Yahan hum Streamlit ka session state use kar rahe hain.
# Matlab jab tak app band nahi hota, ye data save rahega.
# Starting mein hum 5 books already diye hain (Atomic Habits, Alchemist... etc).
# 5️⃣ Sidebar ka scene ➕
# python
# Copy
# Edit
# with st.sidebar:
# Left sidebar bana rahe hain.
# Yahan hum nayi book add karne ka form diya hai:
# Title
# Author
# Genre
# Year
# Niche button diya hai "Add Book".
# Jab click karte hain, agar saari fields fill hain to book add kar deta hai.
# Aur sabse end pe:

# python
# Copy
# Edit
# st.markdown(""" <div class="sidebar-footer"> ... </div> """, unsafe_allow_html=True)
# Yahan humne Made by Bilal Waseem likha hai.
# Uske saath LinkedIn ka logo diya hai jisko click karoge to LinkedIn profile pe chala jayega (tera profile 😉).
# 6️⃣ Display karwana library ka data (books ka table) 📚
# python
# Copy
# Edit
# st.header("📚 Your Library")
# Ye page ka main section hai.
# Agar books hain to wo table dikha raha hai, warna bol raha hai "Library empty hai".
# 7️⃣ Search system 🔍
# python
# Copy
# Edit
# search_query = st.text_input("Search by Title, Author, or Genre")
# Upar ek search bar diya hai.
# Tu kuch bhi likhega (title, author, genre), wo books filter karke dikhayega.
# 8️⃣ Edit Book wala kaam ✏️
# python
# Copy
# Edit
# book_to_edit = st.selectbox("Select a book to edit", st.session_state.library["Title"])
# Dropdown hai jahan se tu book choose karega edit karne ke liye.
# Phir wo sari details auto fill ho jayengi.
# Tu update karega, aur phir button dabayega "Update Book" → record update ho jayega!
# 9️⃣ Delete Book ka kaam 🗑️
# python
# Copy
# Edit
# book_to_delete = st.selectbox("Select a book to delete", st.session_state.library["Title"])
# Dropdown se tu choose karega kaunsi book delete karni hai.
# Click karega "Delete Book" → wo book list se delete ho jayegi.
# Aur success message bhi milta hai 👍
# 🔟 Export ka system 📤
# python
# Copy
# Edit
# st.download_button(
#     label="⬇️ Download Library as CSV",
#     data=csv,
#     file_name="my_library.csv",
#     mime="text/csv",
# )
# Ye button se tu pura library ka data CSV file mein download kar sakta hai.
# Matlab apni books ka data tu Excel mein bhi dekh sakta hai!
# 🔧 Sidebar Footer Details
# LinkedIn logo sidebar ke bottom left mein fix hai.
# Hover karoge logo pe to zoom ho jata hai aur glow karta hai!
# Click karte hi LinkedIn profile khul jata hai (tera hi 😎).
# ✅ Tu kya seekha is code se?
# Streamlit ka session state
# Form banake data add/edit/delete karna
# Dataframe show karwana aur filter karna
# Custom CSS aur sidebar footer add karna
# Aur LinkedIn link ke through profile promote karna! 🚀
