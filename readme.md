A program célja

A program egy körökre osztott stratégiai játék, amelyben a játékosok nyersanyagokat gyűjtenek, épületeket vásárolnak és licitálással versenyeznek egymással. A cél minél több arany megszerzése a játék végére, amely 10 körből áll.

Főbb funkciók
1. Új játék indítása

A felhasználó megadhatja a játékosok számát és nevét. A program létrehozza a kezdő játékállást.

2. Mentett játék betöltése

A korábban elmentett játékok bármikor folytathatók. A program automatikusan megkeresi a legutolsó mentést.

3. Játékállás mentése

A program minden kör végén JSON formátumban elmenti az aktuális játékállást.


Használat
A program szerkezete:
hazi/
├── readme.md
├── strat_game/
│   ├── saves/
│   │   ├── epuletek.json
│   │   ├── pattern.json
│   │   ├── mentes/
│   │   ├── ...
│   │   └── mentesx/
│   └── src/
│       └── strat_game.py


A program indítása:
python strat_game/src/strat_game.py

Indítás után választható:
új játék
mentett játék folytatása
 
A menürendszer segítségével a játékos:
licitálhat
megtekintheti nyersanyagait
megtekintheti épületeit
információt kérhet az épületekről
épületet vásárolhat

Mentések
A mentések JSON fájlokként kerülnek eltárolásra a saves mappában.
A program automatikusan létrehozza a szükséges mentési állományokat a körök végén.


Fejlesztési környezet
Python 3.12
Platformfüggetlen működés
Felhasznált library modulok
pathlib
json
random
re
copy

A program kizárólag Python standard könyvtárakat használ.
