def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    anni={} #inizializzo un dizionario vuoto, avrà come chiavi gli anni e come valori le liste di foto scattate in quell'anno
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader=csv.DictReader(f) #crea un lettore che interpreta la prima riga del file csv come intestazione delle colonne, ogni riga successiva verrà restituita come dizionario in cui le chiavi sono i nomi delle colonne
        for row in reader: #scorre il csv riga per riga, a ogni iterazione la variabile row contiene i dati di una singola foto
            anno=int(row["anno"]) #estrae il valore della colonna anno della riga corrente e lo converte da stringa a intero
            if anno not in anni: #controlla se l'anno corrente è già tra le chiavi del dizionario
                anni[anno]=[] #crea una nuova voce nel dizionario associandole una nuova lista vuota
            foto= { #è un dizionario e ragruppa le info della singola riga
                "codice":row["codice"].strip(), #.strip() toglie spazi bianchi e caratteri invisibili all'inizio e alla fine dei testi
                "titolo":row["titolo"].strip(),
                "autore":row["autore"].strip(),
                "mese":int(row["mese"].strip()),
                anno:anno
            }
            anni[anno].append(foto) #aggiunge il dizionario della foto appena creato alla lista dell'anno corrispondente
    return anni #restituisce il dizionario completo con tutti gli anni e le relative foto raggruppate

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO

    try:#Validazione del mese (deve essere tra 1 e 12)
        mese = int(mese)
        anno = int(anno)
    except (ValueError, TypeError):
        return None

    if not (1 <= mese <= 12):
        return None
    codice = str(codice).strip()

    for lista_foto in album.values(): #Controllo duplicati: il codice non deve essere già presente in nessun anno dell'album
        for foto in lista_foto:
            if foto["codice"] == codice:
                return None

        nuova_foto = { #Creazione del dizionario della nuova foto
            "codice": codice,
            "titolo": str(titolo).strip(),
            "autore": str(autore).strip(),
            "mese": mese,
            "anno": anno,
        }
        try: # Scrittura su file CSV in fondo (append). Se il file non esiste solleva FileNotFoundError
            with open(file_path, mode="a", encoding="utf-8", newline="") as f:
                fieldnames = ["codice", "titolo", "autore", "mese", "anno"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(nuova_foto)
        except (FileNotFoundError, OSError):
            return None

        if anno not in album: # Se la scrittura su file è andata a buon fine, aggiorna la struttura dati in memoria
            album[anno] = []

        album[anno].append(nuova_foto)
        return nuova_foto # Ritorna il riferimento alla foto appena aggiunta


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO


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
