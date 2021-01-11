import text_processing
import functions

t1 = "no to moze odpal Spotify"
t2 = "może teraz zrób screena"
t3 = "uruchom Android Studio"
t4 = "wyszukaj w internecie informacje o II wojnie Światowej"
t5 = "otwórz plik test1.pdf"
t6 = 'cyknij zrzut ekranu'
t7 = 'może odpal Visual Studio Code'
t8 = 'pobierz ten filmik'
t9 = 'konwertuj muzyka.mp4'
t10 = 'puść następny utwór'
t11 = 'podgłoś muzykę'

print(text_processing.getTaskAndArgs(t1))
print(text_processing.getTaskAndArgs(t2))
print(text_processing.getTaskAndArgs(t3))
print(text_processing.getTaskAndArgs(t4))
print(text_processing.getTaskAndArgs(t5))
print(text_processing.getTaskAndArgs(t6))
print(text_processing.getTaskAndArgs(t7))
print(text_processing.getTaskAndArgs(t8))
print(text_processing.getTaskAndArgs(t9))
print(text_processing.getTaskAndArgs(t10))
print(text_processing.getTaskAndArgs(t11))
# paths = functions.getListOfApps()
# print(len(paths))
# print(paths)
