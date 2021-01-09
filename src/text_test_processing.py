import text_processing

t1 = "no to moze odpal Spotify"
t2 = "może teraz zrób screena"
t3 = "uruchom Android Studio"
t4 = "wyszukaj w internecie informacji o II wojnie Światowej"
t5 = "otwórz plik skrypt.pdf"
t6 = 'cyknij zrzut ekranu'

print(text_processing.getTaskAndArgs(t1))
print(text_processing.getTaskAndArgs(t2))
print(text_processing.getTaskAndArgs(t3))
print(text_processing.getTaskAndArgs(t4))
print(text_processing.getTaskAndArgs(t5))
print(text_processing.getTaskAndArgs(t6))
import functions
paths = functions.getListOfApps()
print(len(paths))
print(paths)
