import os
import requests
import difflib

# URL der Webseite
url = "https://www.sw-ka.de/de/wohnen/zimmervermittlung/privatzimmer_suchen/?cpage=1"

# Dateinamen für die gespeicherte Version der Webseite
old_filename = "old_page.html"
new_filename = "new_page.html"
cache_filename = "changes.txt"


# Funktion zum Herunterladen und Speichern der Webseite
def download_page(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "w", encoding="utf-8") as file:
            filtered = response.text.split("<table  class=\"std-table data-table shrink _shrink-load-collapsed\">")[1]
            filtered = filtered.split("</table>")[0]
            file.write(filtered)
            print("Webseite erfolgreich heruntergeladen und gespeichert.")
    else:
        print("Fehler beim Herunterladen der Webseite.")


# Funktion zum Vergleichen der alten und neuen Version der Webseite
def compare_pages(old_file, new_file):
    with open(old_file, "r", encoding="utf-8") as old:
        with open(new_file, "r", encoding="utf-8") as new:
            diff = difflib.unified_diff(
                old.readlines(), new.readlines(), fromfile="alte_version", tofile="neue_version"
            )
            diff_text = "\n".join(diff)
            if diff_text:
                with open(cache_filename, "w", encoding="utf-8") as cache:
                    cache.write(diff_text)
                    return True, "Unterschiede gefunden! Siehe " + url + " für Unterschiede.", cache_filename
            else:
                return False, None, None


def check_website():
    # Überprüfen, ob die 'old_page.html'-Datei vorhanden ist
    if not os.path.isfile(old_filename):
        # 'old_page.html'-Datei existiert nicht, herunterladen und speichern der aktuellen Version
        download_page(url, old_filename)

    # 'old_page.html'-Datei existiert, herunterladen und speichern der aktuellen Version
    download_page(url, new_filename)

    compare_result = compare_pages(old_filename, new_filename)

    # Aktualisierte Version als neue alte Version speichern
    download_page(url, old_filename)

    # Vergleichen der alten und neuen Version der Webseite
    return compare_result
