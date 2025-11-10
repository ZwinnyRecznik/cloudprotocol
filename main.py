# Pobieranie poszczególnych bibliotek
import streamlit as st                                      # Główna biblioteka do tworzenia interfejsów webowych w Pythonie
from datetime import datetime                               # Do generowania daty i godziny (używane w nazwach plików PDF)
import os                                                   # Standardowa biblioteka pythona umożliwiająca pracę z innymi plikami (szukanie, wywoływanie)
from pdf_generator import generuj_pdf                       # Import funkcji generującej plik PDF (z osobnego modułu)
from google_drive_integration import upload_to_drive        # Import funkcji do wysyłania plików na Google Drive

# Kod potrzebny do hostowania aplikacji w Streamlit Cloud
def run_app():

    #  Ustawienia aplikacji - nazwa strony, ikonka, układ aplikacji
    st.set_page_config(page_title="CloudProtocol", page_icon="☁️", layout="centered")

    #  Logo z lokalnej ścieżki
    logo_path = "assets/logo.png"                # Ścieżka do pliku z logo
    if os.path.exists(logo_path):                # Sprawdzenie, czy plik istnieje
        st.image(logo_path, width=180)           # Jeśli tak – wyświetlenie logo w aplikacji
    else:
        st.warning("⚠️ Nie znaleziono pliku logo.png w folderze assets/")  # Jeśli nie – komunikat ostrzegawczy

    st.title("CloudProtocol")                             # Główny tytuł aplikacji
    st.write("Cyfrowy protokół serwisowy")                # Krótki opis pod tytułem

    st.markdown("---")                                    # Linia oddzielająca sekcje
    st.header("Formularz protokołu serwisowego")          # Nagłówek sekcji formularza

    # Pola formularza (interaktywne pola w Streamlit)
    dane_klienta = st.text_input("Dane klienta (Firma, imię i nazwisko, adres, NIP itd...):")
    nazwa_urzadzenia = st.text_input("Nazwa własna/Typ urządzenia:")
    marka = st.text_input("Marka:")
    model = st.text_input("Model:")
    numer_seryjny = st.text_input("Numer seryjny:")
    rok_produkcji = st.text_input("Rok produkcji:")  # Nowe pole na rok produkcji
    stopien_trudnosci = st.selectbox("Stopień trudności serwisu:", ["Łatwy", "Średni", "Trudny"])
    opis_naprawy = st.text_area("Opis naprawy / uwagi:")
    zdjecia = st.file_uploader(
        "Dodaj zdjęcia (opcjonalnie)", type=["jpg", "jpeg", "png"], accept_multiple_files=True
    )
    # Użytkownik może wczytać jedno lub więcej zdjęć, które zostaną dołączone do PDF-a

    # Przycisk generowania PDF
    if st.button("📄 Generuj i zapisz protokół"):                     # Po kliknięciu wywołanie kodu
        # Walidacja pól – sprawdzenie, czy wszystkie pola formularza są wypełnione
        if not all([
            dane_klienta,
            nazwa_urzadzenia,
            marka,
            model,
            numer_seryjny,
            rok_produkcji,
            stopien_trudnosci,
            opis_naprawy
        ]):
            st.error("❗ Proszę wypełnić wszystkie wymagane pola przed kontynuowaniem.")  # Komunikat o błędzie
        else:
            # Tworzymy nazwę pliku PDF i folder, jeśli nie istnieje
            nazwa_pliku = f"protokol_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"     # np. protokol_2025-10-30_21-33-04.pdf
            os.makedirs("protokoly", exist_ok=True)                                    # Tworzy folder „protokoly”, jeśli go jeszcze nie ma
            sciezka_pliku = os.path.join("protokoly", nazwa_pliku)                           # Pełna ścieżka do pliku PDF

            # Tworzenie słownika danych dla PDF (pytanie → odpowiedź)
            dane = {
                "Dane klienta (Firma, imię i nazwisko, adres, NIP itd...)": dane_klienta,
                "Nazwa urządzenia:": nazwa_urzadzenia,
                "Marka:": marka,
                "Model:": model,
                "Numer seryjny:": numer_seryjny,
                "Rok produkcji:": rok_produkcji,
                "Stopień trudności serwisu:": stopien_trudnosci,
                "Opis naprawy / uwagi:": opis_naprawy
            }

            # Generowanie pliku PDF
            generuj_pdf(sciezka_pliku, dane, zdjecia)
            st.session_state["pdf_path"] = sciezka_pliku       # Zapamiętanie ścieżki
            st.session_state["pdf_name"] = nazwa_pliku         # Zapamiętanie nazwy

            # Wysyłka pliku do Google Drive
            try:
                link = upload_to_drive(sciezka_pliku)
                st.session_state["drive_link"] = link          # Zapamiętanie linku
            except Exception as e:
                st.session_state["error"] = str(e)

            st.rerun()  # Odśwież stronę, żeby wyświetlić ramki po zapisaniu

    # ✅ Wyświetlenie trwałych komunikatów po odświeżeniu
    if "pdf_path" in st.session_state:
        st.success(f"✅ Protokół PDF został wygenerowany: **{st.session_state['pdf_name']}**")

    if "drive_link" in st.session_state:
        st.success(f"📂 Plik zapisano w Google Drive: [Otwórz plik]({st.session_state['drive_link']})")

    if "error" in st.session_state:
        st.error(f"❌ Wystąpił błąd podczas wysyłania na Google Drive: {st.session_state['error']}")

    st.markdown("---")                                              # Linia końcowa
    st.caption(                                                     # Stopka aplikacji z podpisem
        "CloudProtocol © 2025 | Aplikacja do tworzenia cyfrowych protokołów serwisowych | Praca Licencjacka studenta Tytusa Szałamachy"
    )
