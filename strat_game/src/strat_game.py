import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import json
import random 
import re

#elérési út
root = Path(__file__).parent.parent
saves = root / "saves"
pattern_path = saves / "pattern.json"
with open(pattern_path) as p:
    pattern_Dict = json.load(p)
epuletek_pattern_path = saves / "epuletek.json"
with open(epuletek_pattern_path) as f:
    epuletek_pattern = json.load(f)
korok = 10
#használt függvények, játékos és épület objektum

multi_licit_menu_text ="Licitet! teszek (1)\nMegnézem milyen épületek vannak a boltban még! (2)\nMegnézem milyen nyersanyagaim vannak! (3)\nMegnézem milyen épületeim vannak! (4)\nMegnézem mit tudnak az épületek! (5)\nVége a körömnek. (6)"
single_licit_menu_text ="Licitet! teszek (1)\nMegnézem milyen nyersanyagaim vannak! (2)\nMegnézem milyen épületeim vannak! (3)\nMegnézem mit tudnak az épületek! (4)\nVége a körömnek. (5)"
draft_menu_text ="Épületet választok (1)\nMegnézem milyen épületek vannak a boltban még! (2)\nMegnézem milyen nyersanyagaim vannak! (3)\nMegnézem milyen épületeim vannak! (4)\nMegnézem mit tudnak az épületek! (5)\nVége a körömnek. (6)"
console_clean ="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

jatekosok = {} #jatekos objektum elemeinek behívására
class Jatekos:
    def __init__(self, nev, arany, fa, ko, vas, epuletek):
        self.nev = nev
        self.arany = arany
        self.fa = fa
        self.ko = ko
        self.vas = vas
        self.licit = -1
        self.epuletek = epuletek

    def meg_tudja_adni_a_licitet(self):
        if self.licit <= self.arany:
            return True
        else:
            print("Maximum annyit licitálhatsz ahány aranyad van!")
            return False        

    def licitalas(self):
            self.arany -= self.licit

    def termeles(self):
        epuletek = self.epuletek
        print("Termelés kezdete")
        print(self.epuletek.keys())
        for epulet in self.epuletek.keys():
            print(epulet)
            szamitas_mod = epuletek_pattern[epulet]["Termeles"]["Arany"]["type"]
            if szamitas_mod == "const":
                self.arany += epuletek_pattern[epulet]["Termeles"]["Arany"]["value"]*self.epuletek[epulet]
                print('Arany konstanssal változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Arany"]["value"])
            elif szamitas_mod == "formula":
                self.arany += eval(epuletek_pattern[epulet]["Termeles"]["Arany"]["expr"])*self.epuletek[epulet]
                print('Arany változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Arany"]["expr"])

            szamitas_mod = epuletek_pattern[epulet]["Termeles"]["Fa"]["type"]
            if szamitas_mod == "const":
                self.fa += epuletek_pattern[epulet]["Termeles"]["Fa"]["value"]*self.epuletek[epulet]
                print('Fa konstanssal változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Fa"]["value"])
            elif szamitas_mod == "formula":
                self.fa += eval(epuletek_pattern[epulet]["Termeles"]["Fa"]["expr"])*self.epuletek[epulet]
                print('Fa változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Fa"]["expr"])

            szamitas_mod = epuletek_pattern[epulet]["Termeles"]["Ko"]["type"]
            if szamitas_mod == "const":
                self.ko += epuletek_pattern[epulet]["Termeles"]["Ko"]["value"]*self.epuletek[epulet]
                print('Ko konstanssal változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Ko"]["value"])
            elif szamitas_mod == "formula":
                self.ko += eval(epuletek_pattern[epulet]["Termeles"]["Ko"]["expr"])*self.epuletek[epulet]
                print('Ko változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Ko"]["expr"])

            szamitas_mod = epuletek_pattern[epulet]["Termeles"]["Vas"]["type"]
            if szamitas_mod == "const":
                self.vas += epuletek_pattern[epulet]["Termeles"]["Vas"]["value"]*self.epuletek[epulet]
                print('Vas konstanssal változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Vas"]["value"])
            elif szamitas_mod == "formula":
                self.vas += eval(epuletek_pattern[epulet]["Termeles"]["Vas"]["expr"])*self.epuletek[epulet]
                print('Vas változik:')
                print(epuletek_pattern[epulet]["Termeles"]["Vas"]["expr"])
            print("-------")

    def megveheti_epulet(self,epulet):
        if (self.arany >= epuletek_pattern[epulet]["Ar"]["Arany"]) and (self.fa >= epuletek_pattern[epulet]["Ar"]["Fa"]) and (self.ko >= epuletek_pattern[epulet]["Ar"]["Ko"]) and (self.vas > epuletek_pattern[epulet]["Ar"]["Vas"]):
            return True
        else:
            return False

    def epulet_vasarlas(self,epulet):
        self.arany -= epuletek_pattern[epulet]["Ar"]["Arany"]
        self.fa -= epuletek_pattern[epulet]["Ar"]["Fa"]
        self.ko -= epuletek_pattern[epulet]["Ar"]["Ko"]
        self.vas -= epuletek_pattern[epulet]["Ar"]["Vas"]
        self.epuletek[epulet] += 1
        print("Sikeres épület vásárlás")

    def epulet_refund(self,epulet):
        self.arany += epuletek_pattern[epulet]["Ar"]["Arany"]
        self.fa += epuletek_pattern[epulet]["Ar"]["Fa"]
        self.ko += epuletek_pattern[epulet]["Ar"]["Ko"]
        self.vas += epuletek_pattern[epulet]["Ar"]["Vas"]
        print("Nem volt elég nyersanyagod, választott épület eladva")

    def mennyi_nyersanyaga_van(self):
        print(str(self.arany)+" darab aranyad van.\n"+str(self.fa)+" fád van.\n"+str(self.ko)+" köved van.\n"+str(self.vas)+" vasad van.")
    
    def milyen_epuletei_vannak(self):
        for epulet in self.epuletek.keys():
            if self.epuletek[epulet] > 0:
                print(str(self.epuletek[epulet])+" darab "+epulet+" van a birtokodon.")

def szam_lett_megadva(szam):
    try:
        szam = int(szam)
    except ValueError:
        print("Pozitív egész számot adj meg!")
        return False
    if int(szam) < 0:
        print("Pozitív egész számot adj meg!")
        return False
    return True

def epulet_printout():
    uzenet = "A lehetséges épületek: "
    epuletek_list = []
    for epulet in epuletek_pattern.keys():
        uzenet += epulet+", "
        epuletek_list.append(epulet)
    print(uzenet)
    kereses = input("Melyik épületet szeretnéd részletesen megnézni (írj be bármit ha már nem szeretnél több épületet megnézni)")
    while kereses in epuletek_list:
        print("A(z) "+kereses+" tulajdonságai:\n")
        print("Ár:\nArany: "+str(epuletek_pattern[kereses]["Ar"]["Arany"])+"\nFa: "+str(epuletek_pattern[kereses]["Ar"]["Fa"])+"\nKő: "+str(epuletek_pattern[kereses]["Ar"]["Ko"])+"\nVas: "+str(epuletek_pattern[kereses]["Ar"]["Vas"]))
        print("\nTermelés:")
        nyersanyagok = ["Arany","Fa","Ko","Vas"]
        for nyersanyag in nyersanyagok:
            if epuletek_pattern[kereses]["Termeles"][nyersanyag]["type"] == "const":
                print(nyersanyag+": "+str(epuletek_pattern[kereses]["Termeles"][nyersanyag]["value"]))
            else:
                print(nyersanyag+": "+epuletek_pattern[kereses]["Termeles"][nyersanyag]["string"])
        kereses = input("Melyik épületet szeretnéd részletesen megnézni (írj be bármit ha már nem szeretnél több épületet megnézni)")

def mentes():
    print("Mentés")
    kovkor_fajlnev_json = fajlnev +"_"+ str(kor) + ".json"
    kovkor_fajl_path = mappa_path / kovkor_fajlnev_json
    Path(kovkor_fajlnev_json).touch()
    for jatekos in jatekosok.keys():
        jatek_mentes_Dict[jatekos]["arany"] = jatekosok[jatekos].arany
        jatek_mentes_Dict[jatekos]["fa"] = jatekosok[jatekos].fa
        jatek_mentes_Dict[jatekos]["ko"] = jatekosok[jatekos].ko
        jatek_mentes_Dict[jatekos]["vas"] = jatekosok[jatekos].vas
        jatek_mentes_Dict[jatekos]["epuletek"] = jatekosok[jatekos].epuletek
    with open(kovkor_fajl_path, "w", encoding="utf-8") as f:
        json.dump(jatek_mentes_Dict, f, ensure_ascii=False, indent=4)
        print("Mentés kész")
   
#kezdeti játékállás beolvasása / létrehozása
helyes_nev = False
while helyes_nev == False:
    jatekkezdes = input("Új játékot szeretnél kezdeni (írd be hogy új), vagy mentett játékot folytatni (írd be, hogy mentett)?")
    if jatekkezdes == "új":
        fajlnev = input("Mi legyen a mentés neve?")
        mappa_path = saves / fajlnev
        Path(mappa_path).mkdir(exist_ok=True)
        fajlnev_json = fajlnev+"_0.json"
        fajl_path = mappa_path / fajlnev_json
        Path(fajl_path).touch()
        helyes_nev = True
    elif jatekkezdes =="mentett":
        fajlnev = input("Mi a mentés neve?")
        mappa_path = saves / fajlnev
        if mappa_path.exists():
            helyes_nev = True
        else:
            print("Adj meg egy létező mentés nevet")
            continue
        max_index = -1        
        for fajl in mappa_path.glob("*.json"):
            match = re.search(r"_(\d+)\.json$", fajl.name)
            if match:
                index = int(match.group(1))
                if index > max_index:
                    max_index = index
        aktualis_kor = max_index
        fajlnev_json = fajlnev+"_"+str(aktualis_kor)+".json"
        fajl_path = mappa_path / fajlnev_json
        kovkor_fajlnev_json = fajlnev+"_"+str(aktualis_kor+1)+".json"
        kovkor_fajl_path = mappa_path / kovkor_fajlnev_json
    else:
        print("új vagy mentett szöveget írj be!")
        continue

#jatekosszám és játékmód meghatározása
if jatekkezdes == "új": #új játék kezdésénél adatok beolvasása objektumba, első körös DF létrehozása
    aktualis_kor = 0
    jatek_mentes_Dict = {}
    jatekos_szam_input = input("Hány játékos legyen?")
    while szam_lett_megadva(jatekos_szam_input) == False:
        jatekos_szam_input = input("Hány játékos legyen?")
    jatekos_szam_int = int(jatekos_szam_input)

    for sorszam in range(jatekos_szam_int): #Játékos nevek bekérése, dataframe és objektum adatainak megtöltése
        valid_jatekos_nev = False
        while valid_jatekos_nev == False:
            jatekos_nev = input("Mi legyen az "+str(sorszam+1)+". játékos neve?")
            if jatekos_nev in jatek_mentes_Dict.keys(): #TODO Nem működik
                print("Olyan nevet adj meg ami még nem lett használva")
            else:
                valid_jatekos_nev = True
        
        jatek_mentes_Dict[jatekos_nev] = pattern_Dict["jatekos"]
        for epulet in epuletek_pattern.keys():
            jatek_mentes_Dict[jatekos_nev]["epuletek"][epulet] = 0
        jatekosok[jatekos_nev] = Jatekos(jatekos_nev,jatek_mentes_Dict[jatekos_nev]["arany"],jatek_mentes_Dict[jatekos_nev]["fa"],jatek_mentes_Dict[jatekos_nev]["ko"],jatek_mentes_Dict[jatekos_nev]["vas"],jatek_mentes_Dict[jatekos_nev]["epuletek"])

    with open(fajl_path, "w", encoding="utf-8") as f:
        json.dump(jatek_mentes_Dict, f, ensure_ascii=False, indent=4)

    print(jatekos_szam_int)
    print(aktualis_kor)
else: #mentett játék beolvasása objektumba
    with open(fajl_path) as f:
        jatek_mentes_Dict = json.load(f)
    jatekos_szam_int = 0
    for jatekos_nev in jatek_mentes_Dict.keys():
        jatekosok[jatekos_nev] = Jatekos(jatekos_nev,jatek_mentes_Dict[jatekos_nev]["arany"],jatek_mentes_Dict[jatekos_nev]["fa"],jatek_mentes_Dict[jatekos_nev]["ko"],jatek_mentes_Dict[jatekos_nev]["vas"],jatek_mentes_Dict[jatekos_nev]["epuletek"])
        jatekos_szam_int += 1
    print(jatekos_szam_int)
    print(aktualis_kor)
"""
jatekosok = {}
jatekosok["test"] = Jatekos("test",5,5,5,5)
jatekosok["test2"] = Jatekos("test2",5,5,5,5)
jatekosok["test3"] = Jatekos("test3",5,5,5,5)

for key in epuletek_pattern.keys():
    jatekosok["test"].epuletek[key] = 0

if jatekosok["test"].megveheti_epulet("Fureszmalom"):
    jatekosok["test"].epulet_vasarlas("Fureszmalom")

for jatekos in jatekosok.keys():
    print(jatekosok[jatekos].nev)
    print(jatek_mentes_Dict[jatekos])
"""

felhozatal = [] #játékban lévő épületek
for epulet in epuletek_pattern.keys():
    felhozatal.append(epulet)
if jatekos_szam_int == "1":
    
    #egyjátékos
    print("még nincs")
    for kor in range(aktualis_kor+1,korok+1):
        #print(console_clean) TODO
        print("A "+str(kor)+". kör következik")
        jatekos = jatekosok.keys()[0]

        #licit
        #print(console_clean) TODO

        valid_kor = False
        while valid_kor == False:
            dontes = input(single_licit_menu_text)
            if dontes == "1":
                print("Összesen "+str(jatekosok[jatekos].arany)+" aranyad van.")
                licit = input("Mennyit licitálsz? (Még)")
                while szam_lett_megadva(licit) == False:
                    licit = input("Mennyit licitálsz? (Még)")
                jatekosok[jatekos].licit = int(licit)

                while jatekosok[jatekos].meg_tudja_adni_a_licitet() == False:
                    licit = input("Mennyit licitálsz (Még)?")
                    while szam_lett_megadva(licit) == False:
                        licit = input("Mennyit licitálsz? (Még)")
                    jatekosok[jatekos].licit = int(licit)
                jatekosok[jatekos].licitalas()    
            elif dontes == "2":
                jatekosok[jatekos].mennyi_nyersanyaga_van()
                input("Üss egy entert hogy visszalépj")
            elif dontes == "3":
                jatekosok[jatekos].milyen_epuletei_vannak()
                input("Üss egy entert hogy visszalépj")
            elif dontes == "4":
                epulet_printout()
                input("Üss egy entert hogy visszalépj")
            elif dontes =="5" and jatekosok[jatekos].licit >= 0:
                valid_kor = True
            else:
                print("Rossz input, vagy adj meg licitet, hogy tovább léphessen a kör!")

        epulet_kinalat = []
        for sorszam in range(jatekosok[jatekos].licit+1):
            epulet = random.choice(felhozatal)
            epulet_kinalat.append(epulet)
        #épület draftolás
    
        valid_kor = False
        vasarlas_volt = False
        while valid_kor == False:
            dontes = input(draft_menu_text)

            if dontes == "1" and not(vasarlas_volt): #épület vásárlás
                index = 0
                for epulet in epulet_kinalat:
                    print("Az "+str(index+1)+". épület: "+epulet)
                    index += 1
                draft = input("Melyik épületet szeretnéd elvinni?\nHelytelen index megadásával vissza tudsz lépni a menübe")
                while szam_lett_megadva(draft) == False:
                    draft = input("Melyik épületet szeretnéd elvinni?\nHelytelen index megadásával vissza tudsz lépni a menübe")
                draft = int(draft)
                if 0<draft<index+1: #helyes index lett megadva
                    valasztott_epulet = epulet_kinalat[draft-1]
                    del epulet_kinalat[draft-1]
                    if jatekosok[jatekos].megveheti_epulet(valasztott_epulet):
                        jatekosok[jatekos].epulet_vasarlas(valasztott_epulet)
                    else:
                        jatekosok[jatekos].epulet_refund(valasztott_epulet)
                    vasarlas_volt = True

            elif dontes == "1" and vasarlas_volt:
                print("Már vásároltál")

            elif dontes == "2": #bolt kínálat kiírás
                uzenet = "A boltban: "
                for epulet in epulet_kinalat:
                    uzenet += epulet
                    uzenet += ", "
                uzenet += "van még."
                print(uzenet)
                input("Üss egy entert hogy visszalépj")    

            elif dontes == "3":
                jatekosok[jatekos].mennyi_nyersanyaga_van()
                input("Üss egy entert hogy visszalépj")

            elif dontes == "4":
                jatekosok[jatekos].milyen_epuletei_vannak()
                input("Üss egy entert hogy visszalépj")

            elif dontes == "5":
                epulet_printout()
                input("Üss egy entert hogy visszalépj")

            elif dontes =="6" and vasarlas_volt == True:
                valid_kor = True
            else:
                print("Rossz input, vagy vegyél ki épületet, hogy tovább léphessen a kör!")
        jatekosok[jatekos].termeles()

        #jatekállás kimentése
        mentes()

else:
    #többjátékos
    for kor in range(aktualis_kor+1,korok+1):
        #print(console_clean) TODO
        print("A "+str(kor)+". kör következik")
        epulet_kinalat = []
        for sorszam in range(int(jatekos_szam_int)+1):
            epulet = random.choice(felhozatal)
            epulet_kinalat.append(epulet)
        
        #licit
        for jatekos in jatekosok.keys():
            #print(console_clean) TODO
            print(str(jatekos)+" játékos következik!")

            valid_kor = False
            while valid_kor == False:
                dontes = input(multi_licit_menu_text)
                if dontes == "1":
                    print("Összesen "+str(jatekosok[jatekos].arany)+" aranyad van.")
                    licit = input("Mennyit licitálsz? (Még)")
                    while szam_lett_megadva(licit) == False:
                        licit = input("Mennyit licitálsz? (Még)")
                    jatekosok[jatekos].licit = int(licit)

                    while jatekosok[jatekos].meg_tudja_adni_a_licitet() == False:
                        licit = input("Mennyit licitálsz (Még)?")
                        while szam_lett_megadva(licit) == False:
                            licit = input("Mennyit licitálsz? (Még)")
                        jatekosok[jatekos].licit = int(licit)
                    jatekosok[jatekos].licitalas()
                elif dontes == "2":
                    uzenet = "A boltban: "
                    for epulet in epulet_kinalat:
                        uzenet += epulet
                        uzenet += ", "
                    uzenet += "van még."
                    print(uzenet)
                    input("Üss egy entert hogy visszalépj")      
                elif dontes == "3":
                    jatekosok[jatekos].mennyi_nyersanyaga_van()
                    input("Üss egy entert hogy visszalépj")
                elif dontes == "4":
                    jatekosok[jatekos].milyen_epuletei_vannak()
                    input("Üss egy entert hogy visszalépj")
                elif dontes == "5":
                    epulet_printout()
                    input("Üss egy entert hogy visszalépj")
                elif dontes =="6" and jatekosok[jatekos].licit >= 0:
                    valid_kor = True
                else:
                    print("Rossz input, vagy adj meg licitet, hogy tovább léphessen a kör!")

        #jatékos sorrend létrehozása
        sorrend = []
        for jatekos in jatekosok.keys():
            sorrend.append((jatekosok[jatekos].nev,jatekosok[jatekos].licit))
            jatekosok[jatekos].licit = -1 #következő kör kezdetére resetel
        sorrend.sort(key=lambda x: (-x[1], random.random()))
        print(sorrend)

        #épület draftolás
        for jatekos_tuple in sorrend:
            jatekos = jatekos_tuple[0]
            #print(console_clean) TODO
            print(str(jatekos)+" játékos következik!")

            valid_kor = False
            vasarlas_volt = False
            while valid_kor == False:
                dontes = input(draft_menu_text)

                if dontes == "1" and not(vasarlas_volt): #épület vásárlás
                    index = 0
                    for epulet in epulet_kinalat:
                        print("Az "+str(index+1)+". épület: "+epulet)
                        index += 1
                    draft = input("Melyik épületet szeretnéd elvinni?\nHelytelen index megadásával vissza tudsz lépni a menübe")
                    while szam_lett_megadva(draft) == False:
                        draft = input("Melyik épületet szeretnéd elvinni?\nHelytelen index megadásával vissza tudsz lépni a menübe")
                    draft = int(draft)
                    if 0<draft<index+1: #helyes index lett megadva
                        valasztott_epulet = epulet_kinalat[draft-1]
                        del epulet_kinalat[draft-1]
                        if jatekosok[jatekos].megveheti_epulet(valasztott_epulet):
                            jatekosok[jatekos].epulet_vasarlas(valasztott_epulet)
                        else:
                            jatekosok[jatekos].epulet_refund(valasztott_epulet)
                        vasarlas_volt = True

                elif dontes == "1" and vasarlas_volt:
                    print("Már vásároltál")

                elif dontes == "2": #bolt kínálat kiírás
                    uzenet = "A boltban: "
                    for epulet in epulet_kinalat:
                        uzenet += epulet
                        uzenet += ", "
                    uzenet += "van még."
                    print(uzenet)
                    input("Üss egy entert hogy visszalépj")    

                elif dontes == "3":
                    jatekosok[jatekos].mennyi_nyersanyaga_van()
                    input("Üss egy entert hogy visszalépj")

                elif dontes == "4":
                    jatekosok[jatekos].milyen_epuletei_vannak()
                    input("Üss egy entert hogy visszalépj")

                elif dontes == "5":
                    epulet_printout()
                    input("Üss egy entert hogy visszalépj")

                elif dontes =="6" and vasarlas_volt == True:
                    valid_kor = True
                else:
                    print("Rossz input, vagy vegyél ki épületet, hogy tovább léphessen a kör!")
            jatekosok[jatekos].termeles()

        #jatekállás kimentése
        mentes()

#scores
pontszamok = []
for jatekos in jatekosok.keys():
    pontszamok.append((jatekosok[jatekos].nev,jatekosok[jatekos].arany))
pontszamok.sort(key=lambda x:x[1], reverse=True)
helyezes = 1
for jatekos_tuple in pontszamok:
    print("Az"+str(helyezes)+". helyezett: "+jatekos_tuple[0]+", "+jatekos_tuple[1]+" darab arannyal")
    helyezes += 1



    






            


            
        



