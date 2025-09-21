# TripTracker
A simple app to log and share travel experiences.

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen matkakuvauksia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään matkakuvauksia.
- Käyttäjä näkee sovellukseen lisätyt matkakuvaukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät matkakuvaukset.
- Käyttäjä pystyy etsimään matkakuvauksia hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä matkakuvauksia.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät matkakuvaukset.
- Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun (esim. kohdemaan, -kaupungin, matkustustapa, matkan ajankohta). Luokat ovat valmiina tietokannassa.
- Käyttäjä pystyy kommentoimaan muiden matkakuvauksia.

## Sovelluksen asennus

Asenna 'flask'-kirjasto:


...
$ pip install Flask
...

Luo tietokannan taulut ja lisää alkutiedot:

...
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < nit.sql
:::

Voit käynnistää sovelluksen näin:

...
$ flask run
...
