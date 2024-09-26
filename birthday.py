import streamlit as st
from streamlit_extras.let_it_rain import rain
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Google Drive API einrichten
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def load_credentials():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return creds

def list_text_files(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='text/plain'",
        fields="files(id, name)"
    ).execute()
    return results.get('files', [])

def read_file_content(file_id):
    request = service.files().get_media(fileId=file_id)
    file_content = request.execute()
    return file_content.decode('utf-8')

st.title("Dyckhome")

st.sidebar.title("Features")
page = st.sidebar.radio("Wähle eine Seite:", ("Startseite", "Fotogalerie", "Quiz", "Rezeptgenerator", "Dycksches-Radio"))

if page == "Startseite":
    st.header("Wilkommen zu deiner kleinen, feinen Website")
    st.write("Hier findest du coole Features, die dir gefallen könnten.")
    st.write("Wähle eine der Optionen in der Seitenleiste, um mehr zu erfahren.")

elif page == "Fotogalerie":
    st.header("Fotogalerie")
    st.write("Hier wird deine Fotogalerie angezeigt.")

    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

elif page == "Quiz":
    st.header("Quiz")
    st.write("Hier wird dein personalisiertes Quiz sein.")

elif page == "Rezeptgenerator":
    st.header("Rezeptgenerator")
    st.write("Hier kannst du Rezepte generieren.")

    folder_id = '1HEC4cAZ6G70v26llUIskK9I5w11paLRv'
    
    if folder_id:
        creds = load_credentials()
        service = build("drive", "v3", credentials=creds)

        files = list_text_files(service, folder_id)

        if files:
            selected_file = st.selectbox("Wähle eine Textdatei aus:", [file['name'] for file in files])
            file_id = next(file['id'] for file in files if file['name'] == selected_file)

            if st.button("Inhalt anzeigen"):
                content = read_file_content(file_id)
                st.text_area("Dateiinhalt:", content, height=300)
        else:
            st.write("Keine Textdateien im angegebenen Ordner gefunden.")


elif page == "Dycksches-Radio":
    st.header("Pick your favourite Playlist")

    col1, col2 = st.columns(2)


    with col1:
        st.write("Arnes Mix")
        spotify_embed_code = """
        <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/65q5bhglITXhDffQzH0MTc?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
        st.markdown(spotify_embed_code, unsafe_allow_html=True)

    with col2:
        st.write("Jules Mix")
        spotify_embed_code2 = """
        <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/59I9uVzvd7rZFYtj9GFb0w?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
        st.markdown(spotify_embed_code2, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col3, col4 = st.columns(2)


    with col3:
        st.write("Karens Mix")
        spotify_embed_code3 = """
        <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/65q5bhglITXhDffQzH0MTc?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
        st.markdown(spotify_embed_code3, unsafe_allow_html=True)

    with col4:
        st.write("HK Mix")
        spotify_embed_code4 = """
        <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/1E2ob6ZfTx4r0YC5Yyryx5?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
        st.markdown(spotify_embed_code4, unsafe_allow_html=True)
