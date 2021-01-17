<p align="center">
  <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/logo.png">
</p>

## Opis
Projekt zaliczeniowy z przedmiotu "Medyczne Systemy Informacyjne", w którym stworzyłem stronę internetową dla przychodni nazwanej MeetMed, do której dostęp ma pacjent oraz lekarz. W projekcie od zera stworzyłem kilkanaście podstron oraz wiele funkcjonalności. Goście odwiedzający stronę mogą założyć nowe konto oraz się na nie zalogować. Domyślnie każdy nowy użytkownik jest rejestrowany jako pacjent. Z poziomu administratora można zarządzać, aby konto danego użytkownika przekształcić w konto lekarza. Zarówno panel logowania jak i rejestracji posiada walidację danych (niepoprawne dane do logowania, podczas rejestracji niepoprawny format emailu lub niepoprawne powtarzające się hasła). W panelu lekarza można usuwać oraz dodawać nowe wizyty, jednocześnie zapisując pacjentów lub pozostawiać je puste, tak aby pacjenci sami wybrali interesującą ich godzinę wizyty i mieli możliwość zapisania się na nią. Lekarz na swoim koncie może skorzystać z pełnego kalendarza w celu podejrzenia wizyt z miesiąca/tygodnia/dnia, a także zaznaczać wizyty jako zrealizowane. Ma także możliwość uzyskania swoich statystyk tj. liczba wszystkich wizyt, liczba wszystkich obsłużonych pacjentów, godziny pracy, liczba wizyt w danym tygodniu przedstawiona na wykresie. Zrobiłem także możliwość eksportowania do pliku pdf dzisiejszego dnia, taki przykładowy plik znajduje się powyżej w folderze **pdffile**. Dodatkowo lekarz może wyszukać danego pacjenta z bazy wszystkich pacjentów i stworzyć notatki odnoszące się do konkretnej wizyty. Każdy użytkownik także ma możliwość zmiany swoich danych tj. imię, nazwisko, email, hasło, telefon w Ustawieniach konta.

## Funkcjonalności
##### Gość
- strona widoczna tylko dla gości
- panel rejestracji oraz logowania z walidacją danych
#### Lekarz
- możliwość korzystania z kalendarza w trybie widokowym dzień/tydzień/miesiąc (FullCallendar API)
- dodawanie/usuwanie wizyt
- zaznaczanie wizyt jako zrealizowane/niezrealizowane
- podgląd statystyk (ilość wizyt w danym tygodniu, łączna ilość wizyt, łączna ilość pacjentów, ilość przepracowanego czasu)
- eksportowanie dzisiejszego planu dnia lekarza do pliku pdf, w celu późniejszego wydrukowania
- wyszukanie pacjenta z bazy wszystkich pacjentów poprzez filtrowanie danych
- możliwość tworzenia notatek do konkretnej wizyty pacjenta
- zmiana swoich danych personalnych (imię, nazwisko, telefon), a także danych do logowania (e-mail, hasło)
#### Pacjent
- podgląd wszystkich swoich wizyt ze strony pacjenta
- zmiana swoich danych personalnych (imię, nazwisko, telefon), a także danych do logowania (e-mail, hasło)

## Użyte technologie
<p align="center">
  <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/technologies.png">
</p>

## Zdjęcia podglądowe
#### Strona główna
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/homepage.gif">
  </kbd>
</p>

#### Panel logowania oraz rejestracji
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/loginpanel.png">
  </kbd>
</p>
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/registerpanel.png">
  </kbd>
</p>

#### Konto lekarza
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/doctorhome.png">
  </kbd>
</p>
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/doctortoday.png">
  </kbd>
</p>
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/doctorcalendar.gif">
  </kbd>
</p>
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/doctorpanel.png">
  </kbd>
</p>
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/searchpatient.png">
  </kbd>
</p>
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/patientnotes.png">
  </kbd>
</p>
<p align="center">
  <kbd>
    <img src="https://github.com/JakubMakaruk/meetmed-clinicapp/blob/main/readmeimgs/settings.png">
  </kbd>
</p>
