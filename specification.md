# Természetes nyelvi és szemantikus technológiák kurzus
## HÁZI FELADAT
### RDF modellezés
**2024. november**  
**Készítette: Strausz György**

Készítsen szemantikus web technológiákat alkalmazó az információ keresést támogató modellt szabályozás jellegű dokumentumokhoz!  
A megoldásnak tartalmaznia kell egy minimum 3-5 bekezdést (10-15 mondat) szövegrészlet nyelvtechnológia elemzését, RDF modell (RDF adatfájl) elkészítését és a modell lekérdezését támogató 3-5 SparQL lekérdezés elkészítését.  
A megoldásnak nem kell integrált megvalósítása, több részfeladatot megoldó szolgáltatás alkalmazása is megfelelő.  

### A feladat részletezése
1. **Válasszon az alábbi lehetőségek közül egy dokumentumot és annak megfelelő részletét:**
   - Tanulmányi és vizsgaszabályzat (TVSZ) - [Link](https://kth.bme.hu/hallgatoknak/szabalyzatok/)
   - Közúti közlekedés szabályai (KRESZ) - [Link](https://net.jogtar.hu/jogszabaly?docid=97500001.kpm)
   - Családi otthonteremtés támogatása - [Link](https://net.jogtar.hu/jogszabaly?docid=A1600017.KOR)

2. **Készítsen nyelvtechnológia elemzőt, amely a szövegből RDF hármasokká alakítható egyszerű állításokat hozz létre!**  
   Ügyeljen rá, hogy a kötőszavakon kívül minden az eredeti mondat értelmezéséhez szükséges lényeges elemet tartalmazzon! A felesleges (stop) szavak eltávolítására, szótövesítésre, a mondat nyelvtani elemzésére használhatja a félév első felében felhasznált vagy elkészített megoldásokat.

3. **Készítsen egy RDF adatbázisba betöltető XML, n3 dokumentumot (adatfájlt), amely tartalmaz minden állítását a választott szövegrésznek!**

4. **Töltse be az adatmodelljét egy RDF adatbázisba és készítsen lekérdezéseket, amely a modell tartalmát eléri, bemutatja!**

5. **(Opcionális) Készítsen integrált megoldást, amely egy szövegrészlet alapján automatikusan létrehoz és futtat egy RDF adatbázist és egy egyszerű szöveges felületen lehetővé tesz SparQL lekérdezések beírását és futtatását!**  
   A megoldás elkészítéséhez segíthetnek a következő dokumentációk:
   - [RDF4J Rest API Documentation](https://rdf4j.org/documentation/reference/rest-api/)
   - [RDF4J 2.0 Release Review](https://projects.eclipse.org/projects/technology.rdf4j/releases/2.0/review)

6. **(Opcionális) Készítsen az előző pontban specifikált megoldáshoz webes GUI felületet, amelyen a modell tartalma lekérdezhető intuitív módon (SparQL ismerete nélkül)!**

### Követelmények
A feladatok megoldását tetszőleges technológiával el lehet végezni. Dolgozhat saját eszközön vagy az egyetemi NIIF felhőben található virtuális gépeken.  
Adatbázisként az órákon is használt az NIIF felhő virtuális gépein is elérhető RDF4J vagy a regisztráció után szabadon letölthető GraphDB ([Link](https://graphdb.ontotext.com/)) vagy a Neo4J ([Link](https://neo4j.com/)) javasolt.

**Leadandó:**  
Egy zip fájlban tömörítve az elkészített vagy felhasznált eszközök (saját fejlesztés esetén forráskóddal együtt), az elkészített adatbázist tartalmazó dokumentum és egy dokumentáció, amely tartalmazza a fejlesztés és a megoldás elemeit, az elkészített lekérdezéseket és a futtatási eredmények dokumentációját.  

### Az értékelés menete:
Az elfogadáshoz szükséges az 1-4. pontokban felsorolt feladatok elvégzése és dokumentálása, a megoldás minősége szerint ezért 0-4 vizsgapont szerezhető.  
Az integrált megoldás (5. feladat) elkészítéséért 5-7 vizsgapont szerezhető.  
Webes GUI felülettel rendelkező megoldás megvalósításáért 8-10 vizsgapont jár.
