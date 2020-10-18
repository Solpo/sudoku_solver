# Nyt kaikki ruudut, jotka pystyy vääjäämättä ratkaisemaan, ratkaistaan.
# Seuraava askel: Poistaa mahdollisista kaikki, jotka vääjäämättä menevät muualle.
# Esim: Jos samassa blokissa kaikki mahdolliset tietyn numeron paikat ovat
# samalla rivillä, sitä numeroa ei voi olla samalla rivillä muissa blokeissa.




import time

def ratkaise_sudoku(sisaan_sudoku: list) -> list:
    mahdolliset = alusta_mahdolliset()
    sudoku = alusta_sudoku()
    for y in range(9):
        for x in range(9):
            if sisaan_sudoku[y][x] != 0:
                lisaa_sudokuun(sudoku, y, x, sisaan_sudoku[y][x], mahdolliset)
                for j in range(5):
                    print()
    while True:
        edistysta = 0
        edistysta += tarkasta_vaajaamattomat(sudoku, mahdolliset)
        edistysta += syvatarkasta_blokeista(sudoku, mahdolliset)
        edistysta += syvatarkasta_rivilta(sudoku, mahdolliset)
        edistysta += syvatarkasta_sarakkeesta(sudoku, mahdolliset)
        
        if edistysta == 0:
            print("Järeät käyttöön")
            time.sleep(1)
            alaston_pari_talossa(sudoku, mahdolliset)
            lukitut_kandidaatit_1(sudoku, mahdolliset)
            pass # tänne järeämmät metodit kun ylläolevat helpommat on käytetty
        edistysta = 0
        
        if onko_ratkaistu(sudoku):
            tulosta_sudoku(sudoku)
            return sudoku

def onko_ratkaistu(sudoku: list) -> bool:
    nollia_jaljella = False
    for y in range(9):
            for x in range(9):
                if sudoku[y][x] == 0:
                    return False
    if not nollia_jaljella:
        print("Sudoku ratkaistu:")
        return True

def onko_kelvollinen(sudoku: list) -> bool:
    for nro_talo in range(9):
        blokki = [sudoku[y][x] for (y, x) in blokin_ruudut(nro_talo)]
        rivi = [sudoku[y][x] for (y, x) in rivin_ruudut(nro_talo)]
        sarake = [sudoku[y][x] for (y, x) in sarakkeen_ruudut(nro_talo)]

        for i in range(1,10):
            if blokki.count(i) > 1:
                print(f"Blokissa {nro_talo} virhe: enemmän kuin yksi {i}")
                return False
            if rivi.count(i) > 1:
                print(f"Rivillä {nro_talo} virhe: enemmän kuin yksi {i}")
                time.sleep(2)
                return False
            if sarake.count(i) > 1:
                print(f"Sarakkeessa {nro_talo} virhe: enemmän kuin yksi {i}")
                return False
    
    print("Kelpaa")
    time.sleep(2)
    return True

def tarkasta_vaajaamattomat(sudoku:list, mahdolliset: list) -> int:
    for y in range(9):
        for x in range(9):
            if len(mahdolliset[y][x]) == 1:
                print(f"Nonniih: ruudussa [{y}][{x}] ei voi olla mitään muuta kuin {mahdolliset[y][x][0]}")
                print("lisätään siis luku sudokuun")
                lisaa_sudokuun(sudoku, y, x, mahdolliset[y][x][0], mahdolliset)
                tulosta_sudoku(sudoku)
                return 1
    return 0

def syvatarkasta_blokeista(sudoku:list, mahdolliset: list) -> int:
    for blokki in range(9):
        talon_mahdolliset = []
        for y, x in blokin_ruudut(blokki):
            talon_mahdolliset.append(mahdolliset[y][x][:])
        yhdistetyt_mahdolliset = []
        for i in range(len(talon_mahdolliset)):
            yhdistetyt_mahdolliset.extend(talon_mahdolliset[i])
        for nro in range(1,10):
            if yhdistetyt_mahdolliset.count(nro) == 1:
                for y, x in blokin_ruudut(blokki):
                    if nro in mahdolliset[y][x]:
                        print(f"Nonniih: ruutu [{y}][{x}] on blokin perusteella ainoa ruutu jossa voi olla numero {nro}")
                        print("lisätään siis luku sudokuun")
                        lisaa_sudokuun(sudoku, y, x, nro, mahdolliset)
                        tulosta_sudoku(sudoku)
                        return 1
    return 0

def syvatarkasta_rivilta(sudoku:list, mahdolliset: list) -> int:
    for rivi in range(9):
        talon_mahdolliset = []
        for y, x in rivin_ruudut(rivi):
            talon_mahdolliset.append(mahdolliset[y][x][:])
        yhdistetyt_mahdolliset = []
        for i in range(len(talon_mahdolliset)):
            yhdistetyt_mahdolliset.extend(talon_mahdolliset[i])
        for nro in range(1,10):
            if yhdistetyt_mahdolliset.count(nro) == 1:
                for y, x in rivin_ruudut(rivi):
                    if nro in mahdolliset[y][x]:
                        print(f"Nonniih: ruutu [{y}][{x}] on rivin perusteella ainoa ruutu jossa voi olla numero {nro}")
                        print("lisätään siis luku sudokuun")
                        lisaa_sudokuun(sudoku, y, x, nro, mahdolliset)
                        tulosta_sudoku(sudoku)
                        return 1
    return 0

def syvatarkasta_sarakkeesta(sudoku:list, mahdolliset: list) -> int:
    for sarake in range(9):
        talon_mahdolliset = []
        for y, x in sarakkeen_ruudut(sarake):
            talon_mahdolliset.append(mahdolliset[y][x][:])
        yhdistetyt_mahdolliset = []
        for i in range(len(talon_mahdolliset)):
            yhdistetyt_mahdolliset.extend(talon_mahdolliset[i])
        for nro in range(1,10):
            if yhdistetyt_mahdolliset.count(nro) == 1:
                for y, x in sarakkeen_ruudut(sarake):
                    if nro in mahdolliset[y][x]:
                        print(f"Nonniih: ruutu [{y}][{x}] on sarakkeen perusteella ainoa ruutu jossa voi olla numero {nro}")
                        print("lisätään siis luku sudokuun")
                        lisaa_sudokuun(sudoku, y, x, nro, mahdolliset)
                        tulosta_sudoku(sudoku)
                        return 1
    return 0
        
# def lukitut_ehdokkaat_1():
#     pass

def alusta_sudoku() -> list:
    palautettava = []    
    for i in range(9):
        palautettava.append([])
        for j in range(9):
            palautettava[i].append(0)
    return palautettava

def alusta_mahdolliset() -> list:
    mahdolliset = []
    for i in range(9):
        mahdolliset.append([])
        for j in range(9):
            mahdolliset[i].append([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return mahdolliset

def tulosta_sudoku(sudoku: list):
    for i in range(9):
        for j in range(0, len(sudoku[i]), 3):
            print(viivan_tulostus(sudoku[i][j]), end=" ")
            print(viivan_tulostus(sudoku[i][j + 1]), end=" ")
            print(viivan_tulostus(sudoku[i][j + 2]), end="  ")
        print()
        if (i) % 3 == 2:
            print()
    # time.sleep(0.5)
			
def viivan_tulostus(i: int):
    if i == 0:
        return "_"
    else:
        return i

def ruudun_blokki(rivi: int, sarake: int) -> int:
    if rivi <= 2:
        if sarake <= 2:
            return 0
        elif sarake <= 5:
            return 1
        elif sarake <= 8:
            return 2
    elif rivi <= 5:
        if sarake <= 2:
            return 3
        elif sarake <= 5:
            return 4
        elif sarake <= 8:
            return 5
    elif rivi <= 8:
        if sarake <= 2:
            return 6
        elif sarake <= 5:
            return 7
        elif sarake <= 8:
            return 8
        
def blokin_ruudut(blokki: int) -> list:
    i = blokki // 3 * 3
    j = blokki % 3 * 3
    palautettavat_ruudut = []
    for rivi in range(i, i + 3):
        for sarake in range(j, j + 3):
            palautettavat_ruudut.append((rivi, sarake))
    return palautettavat_ruudut

def sarakkeen_ruudut(sarake: int) -> list:
    palautettavat_ruudut = []
    for i in range(9):
        palautettavat_ruudut.append((i, sarake))
    return palautettavat_ruudut

def rivin_ruudut(rivi: int) -> list:
    palautettavat_ruudut = []
    for i in range(9):
        palautettavat_ruudut.append((rivi, i))
    return palautettavat_ruudut

def muut_linjat_blokissa(linja: int) -> tuple:
    if linja < 0 or linja > 8:
        raise ValueError("Pitää olla 0 - 8")
    levea = [i for i in range((linja // 3 * 3), ((linja // 3 * 3) + 3))]
    levea.remove(linja)
    return tuple(levea)

def alaston_pari_talossa(sudoku: list, mahdolliset: list):
    for i in range(0,9):
        blokin_mahdolliset = [mahdolliset[y][x] for y, x in blokin_ruudut(i)]
        osumat_blokissa = ()
        for j in blokin_mahdolliset:
            if blokin_mahdolliset.count(j) == 2 and len(j) == 2:
                if len(osumat_blokissa) == 0:
                    osumat_blokissa = (j)
                    time.sleep(1)
                    for y, x in blokin_ruudut(i):
                        if mahdolliset[y][x] != list(osumat_blokissa):
                            if osumat_blokissa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[0])
                                print("Mahdollisista poistettu blokin alastoman parein perusteella")
                                time.sleep(1)
                            if osumat_blokissa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[1])
                                print("Mahdollisista poistettu blokin alastoman parein perusteella")
                                time.sleep(1)

                elif len(osumat_blokissa) > 0 and j != osumat_blokissa:
                    print(f"Omg toka alaston pari {j} samasta blokista {i}")
                    for y, x in blokin_ruudut(i):
                        if mahdolliset[y][x] != list(osumat_blokissa):
                            if osumat_blokissa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[0])
                                print("Mahdollisista poistettu blokin tokan alastoman parin perusteella")
                                time.sleep(1)
                            if osumat_blokissa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[1])
                                print("Mahdollisista poistettu blokin tokan alastoman parin perusteella")
                                time.sleep(1)

        rivin_mahdolliset = [mahdolliset[y][x] for y, x in rivin_ruudut(i)]
        osumat_rivilla = ()
        for j in rivin_mahdolliset:
            if rivin_mahdolliset.count(j) == 2 and len(j) == 2:
                print(f"omg alaston pari {j} rivillä {i}")
                if len(osumat_rivilla) == 0:
                    osumat_rivilla = (j)
                    for y, x in rivin_ruudut(i):
                        if mahdolliset[y][x] != list(osumat_rivilla):
                            if osumat_rivilla[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[0])
                                print("Mahdollisista poistettu rivin alastoman parin perusteella")
                                time.sleep(1)
                            if osumat_rivilla[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[1])
                                print("Mahdollisista poistettu rivin alastoman parin perusteella")
                                time.sleep(1)

                elif len(osumat_rivilla) > 0 and j != osumat_rivilla:
                    print(f"Omg toka alaston pari {j} samalta riviltä {i}")
                    for y, x in rivin_ruudut(i):
                        if mahdolliset[y][x] != list(osumat_rivilla):
                            if osumat_rivilla[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[0])
                                print("Mahdollisista poistettu rivin tokan alastoman parin perusteella")
                                time.sleep(1)
                            if osumat_rivilla[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[1])
                                print("Mahdollisista poistettu rivin tokan alastoman parin perusteella")
                                time.sleep(1)

        sarakkeen_mahdolliset = [mahdolliset[y][x] for y, x in sarakkeen_ruudut(i)]
        osumat_sarakkeessa = ()
        for j in sarakkeen_mahdolliset:
            if sarakkeen_mahdolliset.count(j) == 2 and len(j) == 2:
                print(f"omg alaston pari {j} sarakkeessa {i}")
                if len(osumat_sarakkeessa) == 0:
                    osumat_sarakkeessa = (j)
                    for y, x in sarakkeen_ruudut(i):
                        if mahdolliset[y][x] != list(osumat_sarakkeessa):
                            if osumat_sarakkeessa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[0])
                                print("Mahdollisista poistettu sarakkeen alastoman parin perusteella")
                                time.sleep(1)
                            if osumat_sarakkeessa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[1])
                                print("Mahdollisista poistettu sarakkeen alastoman parin perusteella")
                                time.sleep(1)
                elif len(osumat_sarakkeessa) > 0 and j != osumat_sarakkeessa:
                    print(f"Omg toka alaston pari {j} samassa sarakkeessa {i}")
                    for y, x in sarakkeen_ruudut(i):
                        if mahdolliset[y][x] != list(osumat_sarakkeessa):
                            if osumat_sarakkeessa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[0])
                                print("Mahdollisista poistettu sarakkeen tokan alastoman parin perusteella")
                                time.sleep(1)
                            if osumat_sarakkeessa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[1])
                                print("Mahdollisista poistettu sarakkeen tokan alastoman parin perusteella")
                                time.sleep(1)

def lukitut_kandidaatit_1(sudoku: list, mahdolliset: list):
    print("Mennään lukittuihin kandidaatteihin #1")
    for blokki in range(0,9):
        blokin_mahdolliset = [mahdolliset[y][x] for y, x in blokin_ruudut(blokki)]
        for nro in range(1, 10):
            esiintymia = 0
            for solun_mahdolliset in blokin_mahdolliset:
                if nro in solun_mahdolliset:
                    esiintymia += 1
            if esiintymia > 0 and esiintymia <= 3 :
                esiintymien_indeksit = []
                esiintymien_hakukohta = 0
                while len(esiintymien_indeksit) < esiintymia:
                    if nro in blokin_mahdolliset[esiintymien_hakukohta]:
                        esiintymien_indeksit.append(esiintymien_hakukohta)
                    esiintymien_hakukohta += 1
                esiintymien_rivit_blokissa = [i // 3 for i in esiintymien_indeksit]
                esiintymien_sarakkeet_blokissa = [i % 3 for i in esiintymien_indeksit]
                
                absoluuttiset_koordinaatit = []
                for j in range(esiintymia):
                    absoluuttiset_koordinaatit.append(((blokki // 3) * 3 + esiintymien_rivit_blokissa[j], (blokki % 3) * 3 + esiintymien_sarakkeet_blokissa[j]))
                if esiintymien_rivit_blokissa.count(esiintymien_rivit_blokissa[0]) == len(esiintymien_rivit_blokissa):
                    for x in range(9):
                        if (absoluuttiset_koordinaatit[0][0], x) not in absoluuttiset_koordinaatit and \
                            nro in mahdolliset[absoluuttiset_koordinaatit[0][0]][x]:
                            mahdolliset[absoluuttiset_koordinaatit[0][0]][x].remove(nro)
                            print(f"Rivillä {absoluuttiset_koordinaatit[0][0]}: on blokin {blokki} kaikki {nro}:n esiintymät" + \
                                f"poistetaan siis se mahdollisista kohdasta {mahdolliset[absoluuttiset_koordinaatit[0][0]][x]}")
                            time.sleep(1)
                if esiintymien_sarakkeet_blokissa.count(esiintymien_sarakkeet_blokissa[0]) == len(esiintymien_sarakkeet_blokissa):
                    for y in range(9):
                        if (y, absoluuttiset_koordinaatit[0][1]) not in absoluuttiset_koordinaatit and \
                            nro in mahdolliset[y][absoluuttiset_koordinaatit[0][1]]:
                            mahdolliset[y][absoluuttiset_koordinaatit[0][1]].remove(nro)
                            print(f"Sarakkeessa {absoluuttiset_koordinaatit[0][1]}: on blokin {blokki} kaikki {nro}:n esiintymät" + \
                                f"poistetaan siis se mahdollisista kohdasta {mahdolliset[absoluuttiset_koordinaatit[0][0]][x]}")
                            time.sleep(1)
                    
                print("Lukitut kandidaatit kertaalleen laskettu")



def poista_mahdollisista_rivilla(mahdolliset: list, rivi: int, numero: int): 
    for mahdollisten_rivi, mahdollisten_ruutu in rivin_ruudut(rivi):
        if numero in mahdolliset[mahdollisten_rivi][mahdollisten_ruutu]:
            mahdolliset[mahdollisten_rivi][mahdollisten_ruutu].remove(numero)

def poista_mahdollisista_sarakkeessa(mahdolliset: list, sarake: int, numero: int): 
    for mahdollisten_rivi, mahdollisten_ruutu in sarakkeen_ruudut(sarake):
        if numero in mahdolliset[mahdollisten_rivi][mahdollisten_ruutu]:
            mahdolliset[mahdollisten_rivi][mahdollisten_ruutu].remove(numero)

def poista_mahdollisista_blokissa(mahdolliset: list, blokki: int, numero: int): 
    for mahdollisten_rivi, mahdollisten_ruutu in blokin_ruudut(blokki):
        if numero in mahdolliset[mahdollisten_rivi][mahdollisten_ruutu]:
            mahdolliset[mahdollisten_rivi][mahdollisten_ruutu].remove(numero)

def lisaa_sudokuun(sudoku: list, rivi: int, sarake: int, numero: int, mahdolliset: list):
    sudoku[rivi][sarake] = numero
    poista_mahdollisista_rivilla(mahdolliset, rivi, numero)
    poista_mahdollisista_sarakkeessa(mahdolliset, sarake, numero)
    poista_mahdollisista_blokissa(mahdolliset, ruudun_blokki(rivi, sarake), numero)
    mahdolliset[rivi][sarake] = []

def ota_rivi(rivinro: int) -> list:
    while True:
        try:
            syote = input(f"Syötä rivi #{rivinro} numeroita, erottimena välilyönti.\n{'# ' * 8}#\n")
            if len(syote) > 17:
                syote = syote[:17]
            if len(syote) < 17:
                syote += " " * (17 - len(syote))
            for i in range(0, 18, 2):
                if syote[i] == " ":
                    syote = syote[:i] + "0" + syote[i+1:]
                if syote[i] not in "0123456789":
                    syote = syote[:i] + "0" + syote[i+1:]
            for i in range(1, 17, 2):
                if syote[i] != " ":
                    syote = syote[:i] + " " + syote[i+1:]
            rivi = syote.strip().split(" ")
            rivi = [int(i) for i in rivi]
            for i in rivi:
                if i != 0 and rivi.count(i) != 1:
                    raise ValueError
                if i < 0 or i > 9:
                    raise ValueError
            print("Siivottu rivi:")
            for i in rivi:
                print(i, end=" ")
            print("\n\n")

            return rivi
        except (KeyError, ValueError, IndexError):
            print()
            print("Virheellinen rivi")
            print()
            continue

def ota_sudoku():
    palautettava = []
    rivinro = 0
    while True:    
        while len(palautettava) < 9:
            palautettava.append(ota_rivi(rivinro))
            rivinro = len(palautettava)
        print("Sudokusi alla. Jos olet tyytyväinen, paina Enter, muuten anna korjattavan rivin numero (0 - 8)")
        print("Käskyllä i# sijoitetaan riville # uusi rivi ja siirretään muita 1 alaspäin")
        tulosta_sudoku(palautettava)
        print()
        try:
            komento = input("Korjattavan rivin numero tai tyhjä = OK: ")
            if komento == "":
                print("\n")
                if not onko_kelvollinen(palautettava):
                    continue
                return palautettava
            
            elif komento[0].lower() == "i":
                rivinro = int(komento[1])
                if rivinro > 8 or rivinro < 0:
                    raise ValueError
                elif rivinro == 8:
                    palautettava[8] = ota_rivi(rivinro)
                else:
                    for i in range(7, rivinro - 1, -1):
                        palautettava[i+1] = palautettava[i]
                    palautettava[rivinro] = ota_rivi(rivinro)

            else:
                rivinro = int(komento)
                if rivinro < 0 or rivinro > 8:
                    print()
                    print("Rivinumeron oltava väliltä 0 - 8")
                    raise ValueError
                palautettava[rivinro] = ota_rivi(rivinro)
                continue
        except (KeyError, ValueError):
            continue

if __name__ == "__main__":
    pass
    
    # sudoku = ota_sudoku()
    # print("Ok, lähdetään ratkaisemaan")
    # print("Annettu sudoku")
    # tulosta_sudoku(sudoku)
    # ratkaise_sudoku(sudoku)

    # sudoku_keskitaso = [
    #     [6, 0, 9, 0, 4, 0, 0, 0, 1],
    #     [7, 1, 0, 5, 0, 9, 6, 0, 0],
    #     [0, 5, 0, 0, 0, 0, 0, 0, 0],
    #     [2, 0, 7, 0, 8, 0, 0, 9, 0],
    #     [0, 0, 0, 0, 6, 0, 0, 2, 4],
    #     [0, 6, 0, 9, 0, 0, 0, 0, 8],
    #     [0, 0, 8, 0, 0, 0, 3, 0, 0],
    #     [0, 0, 0, 4, 0, 0, 0, 0, 7],
    #     [0, 0, 0, 0, 5, 0, 0, 0, 0]]
    # print("Lähtötilanne")
    # tulosta_sudoku(sudoku_keskitaso)
    # time.sleep(3)
    # ratkaistu = ratkaise_sudoku(sudoku_keskitaso)
 
    # sudoku_vaikea = [
    #     [8, 5, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 3, 0, 0, 0, 0],
    #     [4, 0, 0, 0, 0, 0, 0, 9, 5],
    #     [0, 2, 0, 9, 0, 8, 0, 0, 0],
    #     [5, 8, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 7, 0, 6],
    #     [0, 0, 7, 0, 0, 1, 8, 0, 0],
    #     [0, 0, 0, 8, 0, 9, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 2, 1, 3]]
    # # ratkeaa
    # print("Vaikea sudoku: ")
    # tulosta_sudoku(sudoku_vaikea)
    # time.sleep(1)
    # vaikean_ratkaisu = ratkaise_sudoku(sudoku_vaikea)

    # sudoku_extreme = [
    #     [0, 0, 2, 0, 0, 6, 0, 0, 5],
    #     [0, 7, 0, 0, 9, 0, 0, 8, 0],
    #     [1, 0, 0, 2, 0, 0, 3, 0, 0],
    #     [2, 0, 0, 1, 0, 0, 4, 0, 0],
    #     [0, 1, 0, 0, 7, 0, 0, 9, 0],
    #     [0, 0, 3, 0, 0, 8, 0, 0, 1],
    #     [0, 0, 7, 0, 0, 9, 0, 0, 8],
    #     [0, 2, 0, 0, 5, 0, 0, 4, 0],
    #     [5, 0, 0, 7, 0, 0, 6, 0, 0]]
    
    
    # print("Extreme sudoku: ")
    # tulosta_sudoku(sudoku_extreme)
    # time.sleep(3)
    # extremen_ratkaisu = ratkaise_sudoku(sudoku_extreme)
    # tulosta_sudoku(extremen_ratkaisu)
    # # ei ratkea... vielä!
    # sudoku_egregious = [
    #     [0, 9, 0, 0, 1, 0, 0, 6, 0],
    #     [8, 0, 0, 0, 0, 9, 0, 0, 3],
    #     [0, 0, 0, 7, 0, 2, 0, 0, 0],
    #     [0, 3, 8, 0, 0, 0, 9, 0, 0],
    #     [9, 0, 0, 0, 0, 0, 0, 0, 7],
    #     [0, 0, 5, 0, 0, 0, 6, 1, 0],
    #     [0, 0, 0, 5, 0, 8, 0, 0, 0],
    #     [3, 0, 0, 9, 0, 0, 0, 0, 4],
    #     [0, 6, 0, 0, 7, 0, 0, 2, 0]
    # ]
    # print("Sudoku egregious")
    # time.sleep(3)
    # ratkaise_sudoku(sudoku_egregious)
    # # ei ole vielä ratkennut

    # sudoku_evil = [
    #         [0, 0, 2, 6, 0, 0, 0, 0, 0],
    #         [0, 6, 0, 4, 0, 5, 0, 8, 0],
    #         [0, 0, 0, 9, 0, 0, 0, 0, 2],
    #         [0, 8, 0, 0, 0, 0, 7, 5, 6],
    #         [0, 0, 0, 0, 3, 0, 0, 0, 0],
    #         [7, 2, 5, 0, 0, 0, 0, 3, 0],
    #         [6, 0, 0, 0, 0, 8, 0, 0, 0],
    #         [0, 1, 0, 3, 0, 6, 0, 4, 0],
    #         [0, 0, 0, 0, 0, 9, 3, 0, 0]
    #     ]
    # print("Sudoku evil")
    # time.sleep(3)
    # ratkaise_sudoku(sudoku_evil)
    # # ei ole vielä ratkennut

    naked_pair_rivi_5 = [
            [1, 6, 7, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0],

            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 8, 2, 3],
            [0, 3, 4, 0, 8, 0, 0, 0, 9],

            [0, 0, 0, 8, 6, 0, 9, 0, 0],
            [5, 0, 0, 0, 9, 1, 0, 0, 4],
            [7, 0, 0, 0, 0, 5, 3, 0, 0]
        ]
    print(naked_pair_rivi_5)
    if onko_kelvollinen(naked_pair_rivi_5):
        ratkaise_sudoku(naked_pair_rivi_5)
    # # Ratkesi kun naked pairit oli implementoitu

    # sudoku_forkids = [
    #     [8, 0, 6, 0, 0, 0, 0, 0, 0], 
    #     [0, 0, 0, 6, 0, 0, 0, 0, 0], 
    #     [0, 0, 0, 9, 0, 3, 2, 0, 0], 
    #     [9, 3, 0, 2, 0, 0, 0, 1, 0], 
    #     [0, 0, 0, 0, 0, 0, 0, 2, 6], 
    #     [0, 0, 0, 3, 4, 0, 5, 0, 0], 
    #     [1, 0, 0, 0, 8, 0, 0, 0, 0], 
    #     [3, 0, 0, 0, 0, 7, 0, 0, 4], 
    #     [0, 0, 4, 0, 0, 0, 0, 0, 0]
    #     ]
    # # ratkeaa
    # sudoku_tyhja = [
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],

    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],

    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #     ]