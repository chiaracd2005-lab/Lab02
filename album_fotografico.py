from csv import reader, DictReader

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album={} #inizializzo un dizionario vuoto, avrà come chiavi gli anni e come valori le liste di foto scattate in quell'anno
    try:
        with open(file_path, mode="r", encoding="utf-8") as infile:
            header = infile.readline() #per non leggere la prima riga
            for line in infile:
                line = line.strip() #per ripulire la stringa
                parti = [celle.strip() for celle in line.split(",")] #creo una lista con i singoli elementi della linea
                if len(parti) < 5: #ignora righe con campi mancanti o incomplete
                    continue
                (codice, titolo, autore, mese, anno) = (parti[0], parti[1], parti[2], int(parti[3]), int(parti[4]))#è una tupla
                foto = (codice, titolo, autore, mese, anno) #è una lista
                if anno not in album:
                    album[anno] = [] # se l'anno compare per la prima volta crea una nuova voce nel dizionario album associandole una nuova lista vuota
                album[anno].append(foto) #aggiunge la lista della foto appena creata alla lista dell'anno corrispondente
        return album #restituisce il dizionario completo con tutti gli anni e le relative foto raggruppate
    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if not (1 <= mese <= 12):
        return None

    if cerca_foto(album, codice) is not None:
        return None

    nuova_foto = (codice, titolo, autore, mese, anno)

    try: #scrivo sul file csv
        with open(file_path, mode="a", encoding="utf-8") as infile:
            infile.write(f"{codice},{titolo},{autore},{mese},{anno}")
    except (FileNotFoundError, OSError):
        return None

    if anno not in album: # creo l'anno se non presente e inserisco la foto
        album[anno] = []
    album[anno].append(nuova_foto)

    return nuova_foto


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    #foto è: [codice, titolo, autore, mese, anno]
    for anno, lista_foto in album.items(): # for chiave,valore in dizionario.items() con items() che restituisce tuple
        for foto in lista_foto: # foto è (codice, titolo, autore, mese, anno)
            if foto[0] == codice:
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}" #restituisce una stringa formattata come:'codice, titolo, autore, mese, anno'
    return None #se non trovo la foto

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""

    titoli = [foto[1] for foto in album[anno]] #guardo ogni foto della chiave (l'anno inserito) e considero il titolo (foto[1])
    return sorted(titoli) #restituisce in ordine alfabetico

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:

                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
