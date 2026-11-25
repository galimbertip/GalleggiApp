# GalleggiApp — Cronologia versioni

Schema **V.maggiore.minore.patch**: *maggiore* = cambi di struttura, *minore* = nuove funzioni, *patch* = correzioni.

## v2.5.0 — Benzinai vicino a te che funziona (2026-11-25)
- Ricerca benzinai rifatta: non usa più proxy gratuiti (chiusi o a pagamento, per questo falliva sempre)
- Prezzi ufficiali MIMIT scaricati ogni mattina da GitHub e divisi per zona: l'app scarica solo la tua
- Per Benzina, Diesel, GPL e Metano vedi subito il distributore più vicino e il più economico
- Elenco ordinabile per distanza o prezzo, prezzo self o servito, pulsante 🧭 Vai per la navigazione
- Quanto risparmi su un pieno andando al più economico invece che al più vicino
- Avviso se il prezzo di un distributore non viene aggiornato da più di 3 giorni

## v2.4.1 — Avvio veloce e Firebase più stabile (2026-11-17)
- Avvio molto più veloce: il codice arriva già pronto, non viene più tradotto sul telefono a ogni apertura (tolti 2,7 MB da scaricare)
- Se la memoria locale di Firebase dà un errore interno (bug noto di Firestore), l'app ricarica da sola e per 3 giorni usa la memoria normale
- Avviso "il servizio di accesso non risponde" solo dopo 15 secondi, con stato della connessione
- Errore di lettura dei dati con il dettaglio esatto, un suggerimento e il pulsante Ricarica

## v2.4.0 — Blocco dell'app e ricevute (2026-11-14)
- 🔒 Blocco dell'app con 4 metodi: PIN, sequenza disegnata, impronta, volto
- PIN e sequenza uguali su tutti i dispositivi; impronta e volto si attivano su ogni dispositivo che li ha, con PIN di riserva
- Blocco all'apertura e quando torni dopo 1, 5 o 15 minuti (o subito); 5 errori = attesa di 30 secondi
- "Ho dimenticato il codice": nuovo accesso con Google e blocco disattivato
- Import PDF: riconosce le ricevute di un singolo pagamento (PagoPA, app Telepass, bollettini, fatture) — totale, data anche nel formato "01 06 2025", causale e categoria

## v2.3.0 — Scadenze, ricerca e backup (2026-11-14)
- 🔎 Ricerca nei movimenti su tutti i mesi: descrizione, categoria, trasferta o importo, con totale dei risultati
- 📅 Scadenze in arrivo: le spese fisse dei prossimi 5 giorni in evidenza nel Bilancio (anche quelle scadute)
- 🔁 Riconosce le spese che si ripetono ogni mese (abbonamenti, bollette) e propone di aggiungerle alle fisse
- Corretto: una spesa fissa inserita come spesa normale (a mano, da notifica o PDF) non viene più contata due volte
- 💾 Backup completo in un file (movimenti, bilancio, categorie, lista, Salvadanaio, Benzina) e ripristino senza cancellare niente

## v2.2.1 — Salvadanaio solo per i progetti (2026-11-13)
- Il Salvadanaio resta separato dal risparmio mensile: è per collette e progetti particolari (Quaresima, Avvento, fioretti)
- Tolta l'idea pronta "Fondo emergenze", aggiunta "Raccolta per una causa"

## v2.2.0 — Trasferte e limiti (2026-11-13)
- 🧾 Spese di trasferta da rimborsare: le segni con il nome della trasferta, non contano nel ritmo di spesa
- Filtro "🧾 Rimborsi" in Movimenti: totale in attesa diviso per trasferta e nota spese da condividere o copiare
- "Rimborso arrivato": registra l'entrata e chiude le spese coperte; se elimini il rimborso tornano in attesa
- In Bilancio: quanto aspetti di rimborso e dove arriveresti a fine mese quando arriva
- 🎯 Limiti mensili per categoria in ⚙️, con barre e tacca del punto del mese in Bilancio
- Avviso quando una spesa ti porta all'80% o oltre il limite della categoria

## v2.1.0 — Numero di versione (2026-11-13)
- Numero di versione (V.maggiore.minore.patch) sempre visibile in fondo e in ⚙️
- Schermata "Novità" con la cronologia completa degli aggiornamenti
- Avviso una volta sola quando l'app si aggiorna

## v2.0.0 — Tutto in un'app (2026-11-13)
- ⛽ BenzinApp integrata come sezione Benzina: dashboard, statistiche, storico, garage, import/export CSV, Google Drive, benzinaio più economico — stessi dati di prima
- Da una notifica di pagamento al distributore: "Registra come rifornimento" con importo già scritto
- Carburante del mese in corso mostrato nella sezione Benzina
- Categorie di spesa ed entrata personalizzate (＋ Nuova categoria), gestibili in ⚙️
- Lista: nel dubbio ti chiedo il reparto, puoi crearne di nuovi e me lo ricordo
- Salvadanaio: collette di Avvento Romano e Ambrosiano e idee pronte per le collette libere
- Dati salvati anche in locale: niente perso se ricarichi o manca la rete, poi si sincronizza
- Opzioni spostate sull'icona ⚙️ in alto
- Corretto: "busta per vestiti" finiva in Frutta e verdura ("per" letto come "pere")

## v1.6.0 — Salvadanaio (2026-11-13)
- 🐷 Salvadanaio integrato (ex QuaresimApp): collette di Quaresima Romana/Ambrosiana e libere, importi rapidi, storico, riepilogo
- Obiettivo in € per le collette
- "Ho consegnato il salvadanaio" registra il totale nel bilancio
- Import dei vecchi dati dal browser o dal backup JSON, ora salvati nel cloud
- Confronto con le app di budget più diffuse

## v1.5.0 — Calcolo di fine mese corretto (2026-11-13)
- Spese straordinarie (es. meccanico): tolte dal disponibile ma non proiettate sul ritmo di spesa
- Saldo iniziale se il bilancio parte a metà mese (non si inventa più lo stipendio)
- "Ti restano" e "Budget al giorno" chiari, nuovo stato "Soldi del mese finiti"
- "Come lo calcolo?" con tutti i passaggi
- Avviso se il giorno di paga impostato non coincide con lo stipendio

## v1.4.0 — Lista della spesa (2026-11-05)
- 🛒 Lista con reparti automatici e "Compri spesso"
- Prezzi indicativi e stima del totale
- Condivisione della lista
- "Ho finito la spesa" registra lo scontrino nel bilancio

## v1.3.0 — Spese dalle notifiche (2026-11-02)
- Pagamenti da notifiche di Wallet/banca tramite MacroDroid
- Modulo precompilato con importo, esercente e categoria
- Avviso per i distributori di carburante

## v1.2.0 — Inizio del bilancio (2026-11-01)
- Data di inizio: gli anni di benzina precedenti non mandano più i mesi in rosso
- Statistiche e ritmo di spesa solo sui giorni tracciati

## v1.1.0 — Inserimento e import PDF (2026-10-31)
- Pulsanti − Spesa / + Entrata / 📄 Da PDF ben visibili
- Modifica dei movimenti con un tocco
- Import da PDF: busta paga, Telepass, documenti generici, con anteprima e anti-doppioni

## v1.0.2 — Correzione accesso (2026-10-31)
- Corretto il blocco su "Caricamento" all'avvio
- Messaggi chiari se l'accesso Google non è configurato

## v1.0.1 — GalleggiApp (2026-10-30)
- Nuovo nome GalleggiApp (era FineMese) e nuova icona

## v1.0.0 — Prima versione (2026-10-30)
- Bilancio da stipendio a stipendio: "ce la fai ad arrivare a fine mese?"
- Entrate, spese e spese fisse
- Benzina letta in automatico da BenzinApp
- Statistiche mensili, export CSV, accesso con Google
