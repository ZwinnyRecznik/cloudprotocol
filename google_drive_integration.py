# Pobieranie poszczególnych bibliotek ze zbioru bibliotek pydrive2
from pydrive2.auth import GoogleAuth                  # Import klasy do autoryzacji w Google
from pydrive2.drive import GoogleDrive                # Import klasy do komunikacji z Google Drive
import os                                             # Standardowa biblioteka pythona umożliwiająca pracę z innymi plikami (szukanie, wywoływanie)


# Definicja funkcji, która wysyła plik na Google Drive
def upload_to_drive(sciezka_pliku):
    gauth = GoogleAuth()                              # Tworzy obiekt autoryzacji Google
    gauth.LocalWebserverAuth()                        # Uruchamia lokalny serwer do logowania użytkownika (otwiera przeglądarkę)
    drive = GoogleDrive(gauth)                        # Tworzy obiekt Google Drive po udanej autoryzacji

    # ID folderu docelowego na Dysku Google (pobrane z linku w przeglądarce)
    folder_id = "1YWitIFmvWL_vS3Yji0LPOpJR7D0MCyTv"

    # Tworzy nowy plik w Google Drive z określonym tytułem i folderem nadrzędnym
    plik_drive = drive.CreateFile({
        "title": os.path.basename(sciezka_pliku),        # Nazwa pliku (bez pełnej ścieżki)
        "parents": [{"id": folder_id}]                   # Umiejscowienie pliku w określonym folderze
    })

    plik_drive.SetContentFile(sciezka_pliku)               # Ustawia zawartość pliku lokalnego jako treść pliku w chmurze
    plik_drive.Upload()                                    # Wysyła  plik na Google Drive (upload)

    # Zwraca link do udostępnionego pliku, który można otworzyć w przeglądarce
    return f"https://drive.google.com/file/d/{plik_drive['id']}/view?usp=sharing"
