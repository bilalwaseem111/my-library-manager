import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import os

# ---------- CONFIGURATION ----------
DATA_FILE = 'library_data.csv'  # 📂 File to save your library data

# ---------- LOAD DATA ----------
def load_library():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Year"])

# ---------- SAVE DATA ----------
def save_library(df):
    df.to_csv(DATA_FILE, index=False)

# ---------- INITIALIZE ----------
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    h1, h2, h3 { color: #4CAF50; }
    .stButton button {
        background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px 20px; font-size: 16px;
    }
    .stButton button:hover { background-color: #45a049; }
    .stTextInput input, .stNumberInput input {
        border-radius: 5px; border: 1px solid #ccc; padding: 8px;
    }
    .stDataFrame { border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
    .sidebar-footer {
        position: fixed; bottom: 20px; left: 20px; display: flex; align-items: center; gap: 10px; font-family: 'Arial', sans-serif;
    }
    .sidebar-footer-text { font-size: 14px; color: #333333; font-weight: 600; }
    .sidebar-linkedin-logo {
        width: 30px; height: 30px; transition: transform 0.4s ease, filter 0.4s ease; cursor: pointer;
    }
    .sidebar-linkedin-logo:hover {
        transform: scale(1.3); filter: drop-shadow(0 0 6px #0077b5);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- APP TITLE ----------
st.title("📚 Personal Library Manager")

# ---------- SIDEBAR: ADD BOOK ----------
with st.sidebar:
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Year", min_value=1800, max_value=2025, step=1)

    if st.button("Add Book"):
        if title and author and genre and year:
            new_book = pd.DataFrame([[title, author, genre, year]],
                                    columns=["Title", "Author", "Genre", "Year"])
            st.session_state.library = pd.concat([st.session_state.library, new_book], ignore_index=True)
            save_library(st.session_state.library)  # ✅ Save to CSV
            st.success("✅ Book added successfully!")
            st.balloons()
        else:
            st.error("⚠️ Please fill in all fields.")

    # ---------- SIDEBAR FOOTER ----------
    st.markdown("""
        <div class="sidebar-footer">
            <p class="sidebar-footer-text">Made by Bilal Waseem</p>
            <a href="https://www.linkedin.com/in/bilal-waseem-b44006338" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" class="sidebar-linkedin-logo" alt="LinkedIn Logo">
            </a>
        </div>
    """, unsafe_allow_html=True)

# ---------- DISPLAY LIBRARY ----------
st.header("📚 Your Library")
if not st.session_state.library.empty:
    st.dataframe(st.session_state.library, use_container_width=True)
else:
    st.info("Your library is empty. Add some books!")

# ---------- SEARCH BOOKS ----------
st.header("🔎 Search Books")
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

# ---------- EDIT BOOK ----------
st.header("✏️ Edit Book Details")
if not st.session_state.library.empty:
    book_to_edit = st.selectbox("Select a book to edit", st.session_state.library["Title"])
    if book_to_edit:
        book_index = st.session_state.library[st.session_state.library["Title"] == book_to_edit].index[0]
        with st.form(key="edit_form"):
            new_title = st.text_input("Title", value=st.session_state.library.at[book_index, "Title"])
            new_author = st.text_input("Author", value=st.session_state.library.at[book_index, "Author"])
            new_genre = st.text_input("Genre", value=st.session_state.library.at[book_index, "Genre"])
            new_year = st.number_input("Year", value=int(st.session_state.library.at[book_index, "Year"]),
                                       min_value=1800, max_value=2025, step=1)
            if st.form_submit_button("Update Book"):
                st.session_state.library.at[book_index, "Title"] = new_title
                st.session_state.library.at[book_index, "Author"] = new_author
                st.session_state.library.at[book_index, "Genre"] = new_genre
                st.session_state.library.at[book_index, "Year"] = new_year
                save_library(st.session_state.library)  # ✅ Save to CSV
                st.success("✅ Book updated successfully!")
                st.snow()
else:
    st.info("There are no books to edit yet!")

# ---------- DELETE BOOK ----------
st.header("🗑️ Delete a Book")
if not st.session_state.library.empty:
    book_to_delete = st.selectbox("Select a book to delete", st.session_state.library["Title"])
    if st.button("Delete Book"):
        st.session_state.library = st.session_state.library[st.session_state.library["Title"] != book_to_delete]
        save_library(st.session_state.library)  # ✅ Save to CSV
        st.success(f"🗑️ Book '{book_to_delete}' deleted successfully!")
else:
    st.info("No books to delete.")

# ---------- EXPORT LIBRARY ----------
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
