# Seuraavaksi: naked triples
# äsken tehty: lukitut kandidaatit 2
# Ehkä: Tätä käyttävät lyhyet erikoisversiot ..._mahdollisista_rivilla/sarakkeessa/blokissa
# lskdjflskdjf


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
            edistysta += x_wing(sudoku, mahdolliset)
            edistysta += alaston_pari_talossa(sudoku, mahdolliset)
            edistysta += lukitut_kandidaatit_1(sudoku, mahdolliset)
            edistysta += lukitut_kandidaatit_2(sudoku, mahdolliset)
            if edistysta == 0:
                print("Taitaa olla jumissa")
                time.sleep(0.5)
        edistysta = 0
        
        if onko_ratkaistu(sudoku):
            tulosta_sudoku(sudoku)
            time.sleep(5)
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

def etsi_mahdollisista_talossa(nro: int, tyyppi: str, talo_nro: int, mahdolliset: list) -> int:
    if tyyppi.lower() not in ["r", "s", "b"]:
        raise ValueError("Tyypin oltava r, s tai b")
    tyyppi = tyyppi.lower()
    if tyyppi == "r":
        ruudut = rivin_ruudut(talo_nro)
    elif tyyppi == "s":
        ruudut = sarakkeen_ruudut(talo_nro)
    elif tyyppi == "b":
        ruudut = blokin_ruudut(talo_nro)
    else:
        print("nyt oli väärä talon tyyppi kun koetettiin etsiä ja laskea")
        time.sleep(3)
    
    osumien_koordinaatit = []
    for y, x in ruudut:
        if nro in mahdolliset[y][x]:
            osumien_koordinaatit.append((y, x))
    return (osumien_koordinaatit)

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
    palautettavat_ruudut = [(i, sarake) for i in range(9)]
    return palautettavat_ruudut

def rivin_ruudut(rivi: int) -> list:
    palautettavat_ruudut = [(rivi, i) for i in range(9)]
    return palautettavat_ruudut

def muut_linjat_blokissa(linja: int) -> tuple:
    if linja < 0 or linja > 8:
        raise ValueError("Pitää olla 0 - 8")
    levea = [i for i in range((linja // 3 * 3), ((linja // 3 * 3) + 3))]
    levea.remove(linja)
    return tuple(levea)

def muiden_kaistojen_linjat(kaista: int) -> list:
    if kaista not in range(3):
        raise ValueError("Kaistan oltava väliltä 0 - 2")
    palautettavat_linjat = []
    siivotut_kaistat = [0, 1, 2]
    siivotut_kaistat.remove(kaista)
    for kaista in siivotut_kaistat:
        palautettavat_linjat += [kaista * 3, kaista * 3 + 1, kaista * 3 + 2]
    return palautettavat_linjat

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
        
def alaston_pari_talossa(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for talon_nro in range(0,9):
        blokin_mahdolliset = [mahdolliset[y][x] for y, x in blokin_ruudut(talon_nro)]
        osumat_blokissa = ()
        for ruudun_mahdolliset in blokin_mahdolliset:
            if blokin_mahdolliset.count(ruudun_mahdolliset) == 2 and len(ruudun_mahdolliset) == 2:
                if len(osumat_blokissa) == 0:
                    osumat_blokissa = (ruudun_mahdolliset)
                    for y, x in blokin_ruudut(talon_nro):
                        if mahdolliset[y][x] != list(osumat_blokissa):
                            if osumat_blokissa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[0])
                                print(f"Mahdollisista poistettu blokin alastoman parein perusteella")
                                eteni += 1
                            if osumat_blokissa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[1])
                                print("Mahdollisista poistettu blokin alastoman parein perusteella")
                                eteni += 1

                elif len(osumat_blokissa) > 0 and ruudun_mahdolliset != osumat_blokissa:
                    print(f"Omg toka alaston pari {ruudun_mahdolliset} samasta blokista {talon_nro}")
                    for y, x in blokin_ruudut(talon_nro):
                        if mahdolliset[y][x] != list(osumat_blokissa):
                            if osumat_blokissa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[0])
                                print("Mahdollisista poistettu blokin tokan alastoman parin perusteella")
                                eteni += 1
                            if osumat_blokissa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_blokissa[1])
                                print("Mahdollisista poistettu blokin tokan alastoman parin perusteella")
                                eteni += 1

        rivin_mahdolliset = [mahdolliset[y][x] for y, x in rivin_ruudut(talon_nro)]
        osumat_rivilla = ()
        for ruudun_mahdolliset in rivin_mahdolliset:
            if rivin_mahdolliset.count(ruudun_mahdolliset) == 2 and len(ruudun_mahdolliset) == 2:
                print(f"omg alaston pari {ruudun_mahdolliset} rivillä {talon_nro}")
                if len(osumat_rivilla) == 0:
                    osumat_rivilla = (ruudun_mahdolliset)
                    for y, x in rivin_ruudut(talon_nro):
                        if mahdolliset[y][x] != list(osumat_rivilla):
                            if osumat_rivilla[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[0])
                                print("Mahdollisista poistettu rivin alastoman parin perusteella")
                                eteni += 1
                            if osumat_rivilla[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[1])
                                print("Mahdollisista poistettu rivin alastoman parin perusteella")
                                eteni += 1

                elif len(osumat_rivilla) > 0 and ruudun_mahdolliset != osumat_rivilla:
                    print(f"Omg toka alaston pari {ruudun_mahdolliset} samalta riviltä {talon_nro}")
                    for y, x in rivin_ruudut(talon_nro):
                        if mahdolliset[y][x] != list(osumat_rivilla):
                            if osumat_rivilla[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[0])
                                print("Mahdollisista poistettu rivin tokan alastoman parin perusteella")
                                eteni += 1
                            if osumat_rivilla[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_rivilla[1])
                                print("Mahdollisista poistettu rivin tokan alastoman parin perusteella")
                                eteni += 1

        sarakkeen_mahdolliset = [mahdolliset[y][x] for y, x in sarakkeen_ruudut(talon_nro)]
        osumat_sarakkeessa = ()
        for ruudun_mahdolliset in sarakkeen_mahdolliset:
            if sarakkeen_mahdolliset.count(ruudun_mahdolliset) == 2 and len(ruudun_mahdolliset) == 2:
                print(f"omg alaston pari {ruudun_mahdolliset} sarakkeessa {talon_nro}")
                if len(osumat_sarakkeessa) == 0:
                    osumat_sarakkeessa = (ruudun_mahdolliset)
                    for y, x in sarakkeen_ruudut(talon_nro):
                        if mahdolliset[y][x] != list(osumat_sarakkeessa):
                            if osumat_sarakkeessa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[0])
                                print("Mahdollisista poistettu sarakkeen alastoman parin perusteella")
                                eteni += 1
                            if osumat_sarakkeessa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[1])
                                print("Mahdollisista poistettu sarakkeen alastoman parin perusteella")
                                eteni += 1
                elif len(osumat_sarakkeessa) > 0 and ruudun_mahdolliset != osumat_sarakkeessa:
                    print(f"Omg toka alaston pari {ruudun_mahdolliset} samassa sarakkeessa {talon_nro}")
                    for y, x in sarakkeen_ruudut(talon_nro):
                        if mahdolliset[y][x] != list(osumat_sarakkeessa):
                            if osumat_sarakkeessa[0] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[0])
                                print("Mahdollisista poistettu sarakkeen tokan alastoman parin perusteella")
                                eteni += 1
                            if osumat_sarakkeessa[1] in mahdolliset[y][x]:
                                mahdolliset[y][x].remove(osumat_sarakkeessa[1])
                                print("Mahdollisista poistettu sarakkeen tokan alastoman parin perusteella")
                                eteni += 1
    return eteni

def lukitut_kandidaatit_1(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
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
                            eteni += 1
                if esiintymien_sarakkeet_blokissa.count(esiintymien_sarakkeet_blokissa[0]) == len(esiintymien_sarakkeet_blokissa):
                    for y in range(9):
                        if (y, absoluuttiset_koordinaatit[0][1]) not in absoluuttiset_koordinaatit and \
                            nro in mahdolliset[y][absoluuttiset_koordinaatit[0][1]]:
                            mahdolliset[y][absoluuttiset_koordinaatit[0][1]].remove(nro)
                            print(f"Sarakkeessa {absoluuttiset_koordinaatit[0][1]}: on blokin {blokki} kaikki {nro}:n esiintymät" + \
                                f"poistetaan siis se mahdollisista kohdasta {mahdolliset[absoluuttiset_koordinaatit[0][0]][x]}")
                            eteni += 1
                    
                print("Lukitut kandidaatit kertaalleen laskettu")
    return eteni

def lukitut_kandidaatit_2(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for nro in range(7, 8):
        for rivi in range(0,9):
            mahdollisen_paikat_rivilla = []
            for ruutu in rivin_ruudut(rivi):
                if nro in mahdolliset[ruutu[0]][ruutu[1]]:
                    mahdollisen_paikat_rivilla.append(ruutu)
            if len(mahdollisen_paikat_rivilla) > 1:
                osumien_sarakkeet = []
                for osuma in mahdollisen_paikat_rivilla:
                    osumien_sarakkeet.append(osuma[1])
                osumien_kaistat = [sarake // 3 for sarake in osumien_sarakkeet]
                if len(set(osumien_kaistat)) == 1:
                    siivottava_blokki = ruudun_blokki(mahdollisen_paikat_rivilla[0][0], mahdollisen_paikat_rivilla[0][1])
                    for y, x in blokin_ruudut(siivottava_blokki):
                        if (y, x) not in mahdollisen_paikat_rivilla and nro in mahdolliset[y][x]:
                            mahdolliset[y][x].remove(nro)
                            print(f"Poistettu {nro} mahdollisista ruudussa {y},{x} (lukitut kandidaatit 2)")
                            time.sleep(1)

        for sarake in range(0,9):
            mahdollisen_paikat_sarakkeessa = []
            for ruutu in sarakkeen_ruudut(sarake):
                if nro in mahdolliset[ruutu[0]][ruutu[1]]:
                    mahdollisen_paikat_sarakkeessa.append(ruutu)
            if len(mahdollisen_paikat_sarakkeessa) > 1:
                osumien_rivit = []
                for osuma in mahdollisen_paikat_sarakkeessa:
                    osumien_rivit.append(osuma[0])
                osumien_kaistat = [rivi // 3 for rivi in osumien_rivit]
                if len(set(osumien_kaistat)) == 1:
                    siivottava_blokki = ruudun_blokki(mahdollisen_paikat_sarakkeessa[0][0], mahdollisen_paikat_sarakkeessa[0][1])
                    for y, x in blokin_ruudut(siivottava_blokki):
                        if (y, x) not in mahdollisen_paikat_sarakkeessa and nro in mahdolliset[y][x]:
                            mahdolliset[y][x].remove(nro)
                            print(f"Poistettu {nro} mahdollisista ruudussa {y},{x} (lukitut kandidaatit 2)")
                            time.sleep(1)
    return eteni

def x_wing(sudoku: list, mahdolliset: list) -> int:
    eteni = 0
    for nro in range(1,10):
        # rivi
        for talon_nro in range(9):
            pari = etsi_mahdollisista_talossa(nro, "r", talon_nro, mahdolliset)
            if len(pari) == 2:
                parin_sarakkeet = (pari[0][1], pari[1][1])
                for toka_talon_nro in range(talon_nro + 1, 9):
                    toka_pari = etsi_mahdollisista_talossa(nro, "r", toka_talon_nro, mahdolliset)
                    if len(toka_pari) == 2 and (toka_pari[0][1], toka_pari[1][1]) == parin_sarakkeet:
                        print(f"Löytyi X-wingin pari numerolla {nro}, riveiltä {pari[0][0]} ja {toka_pari[0][0]}, sarakkeista {pari[0][1]} ja {pari[1][1]}.")
                        print(f"Numero löytyy riveittäin hakiessa täsmälleen kohdista {pari} ja {toka_pari}")
                        for poiston_rivi in range(9):
                            if poiston_rivi != pari[0][0] and poiston_rivi != toka_pari[0][0]:
                                for poiston_sarake in parin_sarakkeet:
                                    if nro in mahdolliset[poiston_rivi][poiston_sarake]:
                                        mahdolliset[poiston_rivi][poiston_sarake].remove(nro)
                                        print(f"X-wingin perusteella poistettu {nro} ruudun [{poiston_rivi}, {poiston_sarake}] mahdollisista.")
                                        eteni += 1
        # sarake
        for talon_nro in range(9):
            pari = etsi_mahdollisista_talossa(nro, "s", talon_nro, mahdolliset)
            if len(pari) == 2:
                parin_rivit = (pari[0][0], pari[1][0])
                for toka_talon_nro in range(talon_nro + 1, 9):
                    toka_pari = etsi_mahdollisista_talossa(nro, "s", toka_talon_nro, mahdolliset)
                    if len(toka_pari) == 2 and (toka_pari[0][0], toka_pari[1][0]) == parin_rivit:
                        print(f"Löytyi X-wingin pari numerolla {nro}, sarakkeista {pari[0][1]} ja {toka_pari[0][1]}, riveiltä {pari[0][0]} ja {pari[1][0]}.")
                        print(f"Numero löytyy sarakkeitain hakiessa täsmälleen kohdista {pari} ja {toka_pari}")
                        for poiston_sarake in range(9):
                            if poiston_sarake != pari[0][1] and poiston_sarake != toka_pari[0][1]:
                                for poiston_rivi in parin_rivit:
                                    if nro in mahdolliset[poiston_rivi][poiston_sarake]:
                                        mahdolliset[poiston_rivi][poiston_sarake].remove(nro)
                                        print(f"X-wingin perusteella poistettu {nro} ruudun [{poiston_rivi}, {poiston_sarake}] mahdollisista.")
                                        eteni += 1
    return eteni
     
def poista_mahdollisista_rivilla(numero: int, rivi: int, mahdolliset: list): 
    for mahdollisten_rivi, mahdollisten_ruutu in rivin_ruudut(rivi):
        if numero in mahdolliset[mahdollisten_rivi][mahdollisten_ruutu]:
            mahdolliset[mahdollisten_rivi][mahdollisten_ruutu].remove(numero)

def poista_mahdollisista_sarakkeessa(numero: int, sarake: int, mahdolliset: list): 
    for mahdollisten_rivi, mahdollisten_ruutu in sarakkeen_ruudut(sarake):
        if numero in mahdolliset[mahdollisten_rivi][mahdollisten_ruutu]:
            mahdolliset[mahdollisten_rivi][mahdollisten_ruutu].remove(numero)

def poista_mahdollisista_blokissa(numero: int, blokki: int, mahdolliset: list): 
    for mahdollisten_rivi, mahdollisten_ruutu in blokin_ruudut(blokki):
        if numero in mahdolliset[mahdollisten_rivi][mahdollisten_ruutu]:
            mahdolliset[mahdollisten_rivi][mahdollisten_ruutu].remove(numero)

def lisaa_sudokuun(sudoku: list, rivi: int, sarake: int, numero: int, mahdolliset: list):
    sudoku[rivi][sarake] = numero
    poista_mahdollisista_rivilla(numero, rivi, mahdolliset)
    poista_mahdollisista_sarakkeessa(numero, sarake, mahdolliset)
    poista_mahdollisista_blokissa(numero, ruudun_blokki(rivi, sarake), mahdolliset)
    mahdolliset[rivi][sarake] = []

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
                if not onko_kelvollinen_sudoku(palautettava):
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

def ota_rivi(rivinro: int) -> list:
    while True:
        try:
            syote = input(f"Syötä rivi #{rivinro} numeroita, erottimena välilyönti.\n{'# ' * 3}{'* ' * 3}# # #\n")
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

def onko_kelvollinen_sudoku(sudoku: list) -> bool:
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

if __name__ == "__main__":
    
    # sudoku = ota_sudoku()
    # if onko_kelvollinen_sudoku(sudoku):
    #     nimi = input("Anna sudokullesi nimi: ")
    #     with open("sudokut.txt", "a") as tiedosto:
    #         tiedosto.write(f"{nimi} = {sudoku}\n")
    #     time.sleep(2)
    #     ratkaise_sudoku(sudoku)

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
    # tähän asti ratkaistu:
    # https://www.extremesudoku.info/index.html?pos=--2--6--5-7-59--8-15-2-736-2--1-54---15-7289-7-39-8--1--7--9--8-2--5--4-5--7--6--
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
    # ei ole vielä ratkennut

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

    # Evil 19.10.
    # evil_1910 = [
    #     [0, 0, 4, 2, 0, 0, 0, 0, 8], 
    #     [0, 6, 0, 0, 9, 0, 0, 4, 0], 
    #     [3, 0, 5, 0, 4, 0, 1, 0, 0], 
    #     [9, 0, 0, 0, 0, 7, 0, 0, 0], 
    #     [0, 3, 6, 0, 5, 0, 4, 2, 0], 
    #     [0, 0, 0, 4, 0, 0, 0, 0, 1], 
    #     [0, 0, 2, 0, 1, 0, 8, 0, 6], 
    #     [0, 1, 0, 0, 6, 0, 0, 9, 0], 
    #     [6, 0, 0, 0, 0, 2, 3, 0, 0]
    #     ]
    # print("Evil sudoku 19.10.")
    # ratkaise_sudoku(evil_1910)
    
    # sudoku_x_wing = [
    #     [0, 0, 3, 8, 0, 0, 5, 1, 0], 
    #     [0, 0, 8, 7, 0, 0, 9, 3, 0], 
    #     [1, 0, 0, 3, 0, 5, 7, 2, 8], 
    #     [0, 0, 0, 2, 0, 0, 8, 4, 9], 
    #     [8, 0, 1, 9, 0, 6, 2, 5, 7], 
    #     [0, 0, 0, 5, 0, 0, 1, 6, 3], 
    #     [9, 6, 4, 1, 2, 7, 3, 8, 5], 
    #     [3, 8, 2, 6, 5, 9, 4, 7, 1], 
    #     [0, 1, 0, 4, 0, 0, 6, 9, 2]]
    # ratkaise_sudoku(sudoku_x_wing)
    # # ei ratkea vielä

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