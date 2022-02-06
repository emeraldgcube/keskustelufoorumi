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
- Admin voi lisätä tai yhdistää aihealueita
- Admin voi luoda salatun keskustelualueen, johon vain valituilla käyttäjillä on pääsy

Jokainen foorumin käyttäjä on peruskäyttäjä, moderaattori tai admin.

## Tilanne välipalautuksessa

### [Linkki heroku-sovellukseen](https://topin-foorumi.herokuapp.com/subforum)

- Foorumi on saatu pyörimään 
- Tällä hetkellä käytettävät ominaisuudet vastaavat paljolti esimerkkisovellusta
- Lisäominaisuuksia on aloiteltu
  - Esimerkiksi tulevia tietokantatauluja on jo alustettu ja suunniteltu
   - Esim. Bannit, moderaattorioikeudet yms tulossa
   - Sekä myöskin tarkoituksena mahdollistaa x määrä alafoorumeita
  - Myös seuraava askel asettaa tarkistuksia sivuihin: sivu antanee tällä hetkellä virheitä jos sivuja selaisi kirjautumattomana
  - Yms.
