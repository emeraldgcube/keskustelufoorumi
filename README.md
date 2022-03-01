# keskustelufoorumisovellus
hy:n tietokantasovellus-kurssille tehtävä keskustelufoorumisovellus

## Perusidea
Tarkoituksena on tehdä chat-esimerkkisovelluksen kaltainen foorumisovellus, hieman laajamittaisempana. 
Ominaisuuksia ovat:
- Foorumilla on erilaisia keskustelualueita, jotka voidaan sektioida aiheittensa mukaisesti ryppäisiin
- Käyttäjät voivat luoda foorumeille uusia keskusteluja/topicceja sekä kirjoittaa niihin viestejä
- Kirjoittamiseen/keskustelun aloittamiseen tarvitaan käyttäjätunnus
- Käyttäjä voi muokata luomansa keskustelun tai viestin otsikkoa tai sisältöä
- Käyttäjä voi etsiä tietyn sanan sisältäviä tai tietyn käyttäjän kirjoittamia viestejä
- Moderaattori voi poistaa viestejä
- Admin voi luoda salatun keskustelualueen, johon vain valituilla käyttäjillä on pääsy

Jokainen foorumin käyttäjä on peruskäyttäjä, moderaattori tai admin.

## Tilanne välipalautuksessa

### [Linkki heroku-sovellukseen](https://topin-foorumi.herokuapp.com/subforum)

## Tilanne välipalautus 2:sessa

- Foorumi on harmillisesti hieman rikkinäinen tällä hetkellä, tietokantoja on juuri muutettu ja siirrytty useaan foorumiin ja topicceihin yhden viestipalstan sijaan.
- Topic sivu ei myöskään toimi halutulla tavalla tällä hetkellä, vaan näyttää kaikki foorumin viestit. Ratkaisua etsiessä...
- Toiminnallisuudet ovat laajentuneet, tietokannat ovat pitkälti lopullisessa muodossaan
- Viime välipalautuksesta on otettu huomioon mm. pitkät syötteet, bugi session clearaamisessa, committien kieli (ainakin yritetty :D) yms.
- Ulkomuoto saatu jo tyydyttäväksi
- Koodia refaktoroitu ja laajennettu

Toiminnallisuudessa pyritään ennen viimeistä palautusta pääsemään yllä mainittuihin kriteereihin

