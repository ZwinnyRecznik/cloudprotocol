# Pobieranie poszczególnych bibliotek ze zbioru bibliotek ReportLab
from reportlab.pdfgen import canvas             # biblioteka umożliwiająca graficzną obróbkę dokumentu PDF
from reportlab.lib.pagesizes import A4          # biblioteka definiująca rozmiar A4 dla generowanego dokumentu
from reportlab.lib.utils import ImageReader     # biblioteka umożliwiająca wstawianie i wczytywanie obrazów do dokumentu
from reportlab.pdfbase import pdfmetrics        # biblioteka umożliwiająca rejestrowanie i używanie własnych czcionek
from reportlab.pdfbase.ttfonts import TTFont    # jak wyżej
import os                                       # standardowa biblioteka pythona umożliwiająca pracę z innymi plikami (szukanie, wywoływanie)

# Ścieżki do czcionek
FONT_PATH_REGULAR = os.path.join("assets", "DejaVuSans.ttf")
FONT_PATH_BOLD = os.path.join("assets", "DejaVuSans-Bold.ttf")

# Rejestracja czcionek
pdfmetrics.registerFont(TTFont("DejaVu", FONT_PATH_REGULAR))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_PATH_BOLD))


def generuj_pdf(plik_wyjscia, dane, zdjecia=None):          # Zdefiniowanie funkcji generującej dokument PDF
    """
    Generuje PDF protokołu serwisowego.
    - plik_wyjscia: ścieżka do pliku PDF
    - dane: słownik danych (pytanie -> odpowiedź, którą wpisuje użytkownik i jest zapisywana)
    - zdjecia: lista plików zdjęć (opcjonalnie)

    """

    c = canvas.Canvas(plik_wyjscia, pagesize=A4)              # Tworzy nowy pusty dokument PDF w formacie A4
    szerokosc, wysokosc = A4                                  # Pobiera szerokość i wysokość strony (potrzebne do rozmieszczenia elementów)

    # --- Nagłówek / znak wodny ---
    c.setFont("DejaVu", 10)                    # Ustawia czcionkę DejaVu o rozmiarze 10
    c.setFillGray(0.6)                                        # Ustawia kolor tekstu na jasnoszary (0=czarny, 1=biały)
    c.drawRightString(szerokosc - 40, wysokosc - 40,          # Umieszcza tekst w prawym górnym rogu
                      "Wygenerowano za pomocą aplikacji CloudProtocol")

    # --- Tytuł dokumentu ---
    c.setFont("DejaVu-Bold", 28)               # Ustawia pogrubioną czcionkę o rozmiarze 28
    c.setFillGray(0)                                           # Ustawia kolor tekstu na czarny
    c.drawCentredString(szerokosc / 2, 760,                 # Umieszcza tytuł wyśrodkowany na górze strony
                        "Protokół Serwisowy")

    # --- Dane serwisowe ---
    y = 700                                                   # Pozycja pionowa (y) od której zaczyna się treść formularza
    for pytanie, odpowiedz in dane.items():                   # Dopasowuje (iteruje) wszystkie pytania i odpowiedzi w słowniku danych

        #  popraw tekst pytania, jeśli to „Nazwa urządzenia”
        if pytanie.strip().startswith("Nazwa urządzenia"):             # Fragment kodu dodany ze względu na błąd niepojawiania się znaku ":"
            pytanie = "Nazwa własna/Typ urządzenia:"

        pytanie = pytanie.strip()                                      # Usuwa spacje z początku i końca tekstu
        if not pytanie.endswith(":"):                                  # Jeśli pytanie nie kończy się dwukropkiem
            pytanie += ":"                                             # ...to go dodaj

        # nagłówek dla opisu naprawy (pogrubiony)
        if pytanie.startswith("Opis naprawy"):                             # Jeśli pytanie dotyczy opisu naprawy
            c.setFont("DejaVu", 18)                        # Ustaw większą czcionkę (Opis jest szczcegłonie ważny i powinien być wyróżniony)
        else:
            c.setFont("DejaVu", 12)                        # W przeciwnym razie czcionka standardowa
        c.drawString(50, y, pytanie)                                    # Rysuje tekst pytania na stronie w pozycji (x=50, y)

        # odpowiedź pogrubiona
        c.setFont("DejaVu-Bold", 14)                    # Ustawia pogrubioną czcionkę dla odpowiedzi
        text = c.beginText(70, y - 18)                               # Tworzy obiekt tekstu, zaczynający się nieco niżej
        text.textLines(str(odpowiedz))                                  # Wstawia odpowiedź (obsługuje również teksty wieloliniowe)
        c.drawText(text)                                                # Rysuje odpowiedź na PDF
        y -= 50 + len(str(odpowiedz).splitlines()) * 14                 # Przesuwa wskaźnik "y" w dół w zależności od długości tekstu

        # przejście na nową stronę jeśli zabraknie miejsca
        if y < 100:                                                     # Jeśli zostało mało miejsca na stronie
            c.showPage()                                                # Tworzy nową stronę
            c.setFont("DejaVu", 10)                     # Ustawia czcionkę dla nagłówka na nowej stronie
            c.setFillGray(0.6)
            c.drawRightString(szerokosc - 40, wysokosc - 40,
                              "Wygenerowano za pomocą aplikacji CloudProtocol")
            y = 750                                                     # Resetuje pozycję tekstu na nowej stronie

    # --- Stopka informacyjna ---
    c.setFont("DejaVu", 10)                              # Ustawia małą czcionkę dla stopki
    c.setFillGray(0.5)                                                  # Kolor jasnoszary

    if zdjecia:                                                         # Jeśli użytkownik dodał zdjęcia
        c.drawRightString(szerokosc - 50, 40,                         # Umieszcza mały napis w stopce
                          "Zdjęcia na następnej stronie")
        c.showPage()                                                      # Przechodzi do nowej strony (będzie strona ze zdjęciami)

        # --- Strona 2 i kolejne: zdjęcia ---
        c.setFont("DejaVu", 12)
        y_pos = 750                                                         # Pozycja startowa dla pierwszego zdjęcia
        licznik = 1                                                         # Numeracja zdjęć
        for zdj in zdjecia:                                                 # Dopasowuje wszystkie dodane zdjęcia (iteracja)
            obraz = ImageReader(zdj)                                        # Wczytuje obraz jako obiekt ReportLab
            c.drawImage(obraz, 50, y_pos - 150,                          # Rysuje obraz w PDF (x=50, y=y_pos-150)
                         width=200, height=150)                             # Ustalony rozmiar zdjęcia
            c.drawString(50, y_pos - 160, f"zdj. {licznik}")        # Dodaje podpis pod zdjęciem
            y_pos -= 200                                                    # Przesuwa pozycję w dół dla kolejnego zdjęcia
            licznik += 1                                                    # Zwiększa numer zdjęcia

            if y_pos < 100:                                                 # Jeśli zabraknie miejsca na stronie
                c.showPage()                                                # Tworzy nową stronę
                c.setFont("DejaVu", 10)
                c.setFillGray(0.6)
                c.drawRightString(szerokosc - 40, wysokosc - 40,
                                  "Wygenerowano za pomocą aplikacji CloudProtocol")
                y_pos = 750                                                 # Resetuje pozycję na nowej stronie
    else:
        # jeśli brak zdjęć → tylko mały szary napis w stopce
        c.drawRightString(szerokosc - 50, 40,                            # Napis w prawym dolnym rogu
                          "Protokół nie zawiera zdjęć")

    c.save()                                                                # Zapisuje i finalizuje dokument PDF

