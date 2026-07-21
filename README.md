<div align="center">

# 🏥 Claude Impact Lab 2026 | Dataset Salute di Rio

[![Claude](https://img.shields.io/badge/Claude-Impact%20Lab-5436DA?style=for-the-badge&logo=anthropic&logoColor=white)](https://www.anthropic.com)
[![Rio de Janeiro](https://img.shields.io/badge/Prefeitura-Rio%20de%20Janeiro-1E3A8A?style=for-the-badge)](https://prefeitura.rio/)
[![Rocinha](https://img.shields.io/badge/Território-Rocinha-E63946?style=for-the-badge)](https://pt.wikipedia.org/wiki/Rocinha)

</div>

---

## 🎯 La Sfida

## Intelligenza nel Territorio — Ottimizzare la pianificazione delle visite domiciliari degli Agenti Comunitari di Salute

### Il lavoro degli Agenti Comunitari di Salute (ACS)

* Rio ha **6.200 Agenti Comunitari di Salute (ACS)** responsabili di visitare attivamente **4,5 milioni di residenti**.
* Queste visite avvengono soprattutto nei territori più vulnerabili della città: le *favelas*. **La zona di questa sfida è la Rocinha**, la più grande favela del Brasile (~100.000 abitanti su un versante di ~1 km²).
* Oggi la pianificazione delle visite quotidiane dipende ancora molto da:
    * la memoria degli agenti;
    * la carta;
    * la conoscenza informale del territorio.
* Allo stesso tempo, dati clinici e sociali rilevanti restano dispersi e poco utilizzati nei sistemi delle cure primarie.
* La sfida è trasformare questi dati in una risposta pratica e unica ogni mattina:
    * chi visitare;
    * in quale ordine;
    * per quale motivo;
    * sulla base del rischio reale e delle lacune di cura.

### Cosa succede se lo risolviamo

* La presenza quotidiana nel territorio diventa più mirata.
* La cura diventa più preventiva e meno reattiva.
* Le famiglie ad alto rischio vengono raggiunte più rapidamente.
* Le condizioni rilevabili possono essere identificate prima.
* Emergenze e ricoveri evitabili tendono a diminuire.

### Chi beneficia della soluzione

* Direttamente:
    * i **6.200 ACS**, con una giornata di lavoro più chiara, sicura e prioritizzata;
    * i **residenti** seguiti, che vengono visti prima e con maggiore frequenza quando serve.
* Indirettamente:
    * le équipe delle cliniche, che ricevono casi meglio prioritizzati;
    * il sistema sanitario municipale, che può ridurre le emergenze evitabili.

### Com'è fatto il successo

* Ogni ACS inizia la giornata con una lista affidabile di visite basata sul rischio.
* Le famiglie ad alto rischio vengono raggiunte in giorni, non in settimane.
* Agenti ed équipe cliniche restano sincronizzati in tempo reale.
* La città inizia a registrare più famiglie visitate per turno e meno emergenze evitabili.

---

## 📊 Accesso rapido ai dati

<div align="center">

| 🗂️ **Tabella** | 📝 **Descrizione** | 🔗 **File** |
|:---------------|:-------------------|:------------|
| **Pazienti** | Le anagrafiche di migliaia di pazienti, con nome e condizioni cliniche | [📥 pazienti.parquet](assets/parquet/pazienti.parquet) |
| **Eventi Clinici** | Le visite specialistiche prenotate (via *regulação*, da comunicare ai pazienti) e gli accessi in pronto soccorso o ricoveri (che indicano necessità di contatto più stretto) | [📥 eventi_clinici.parquet](assets/parquet/eventi_clinici.parquet) |
| **Visite degli ACS** | Lo storico delle visite degli Agenti Comunitari di Salute | [📥 visite.parquet](assets/parquet/visite.parquet) |
| **Professionisti (ACS)** | L'anagrafica degli Agenti Comunitari di Salute, con nome e équipe di appartenenza | [📥 professionisti.parquet](assets/parquet/professionisti.parquet) |
| **Équipe di Salute** | L'elenco delle équipe e delle unità (UBS), con nome dell'équipe e localizzazione della sede in Rocinha | [📥 equipe.parquet](assets/parquet/equipe.parquet) |

</div>

> I dati sono inclusi nella repo in due formati: **Parquet** in
> [`assets/parquet/`](assets/parquet/) (compatto, pronto per Claude Code) e **CSV**
> completo in [`assets/csv/`](assets/csv/) (leggibile e apribile ovunque).

---

## 📘 Dizionario dei dati

### Modello dei dati

```mermaid
erDiagram
    equipe ||--o{ pazienti : "responsabile di"
    equipe ||--o{ professionisti : "impiega"
    professionisti ||--o{ visite : "effettua"
    pazienti ||--o{ visite : "riceve"
    pazienti ||--o{ eventi_clinici : "ha"

    equipe {
        string equipe_id PK
        string unita_id
        string equipe_nome
        string unita_nome
        float sede_latitudine
        float sede_longitudine
        string area
    }

    professionisti {
        string professionista_id PK
        string nome
        string cognome
        string equipe_id FK
    }

    pazienti {
        string paziente_id PK
        string equipe_id FK
        string unita_id
        string nome
        string cognome
        string fascia_eta
        string sesso
        string razza_colore
        boolean vulnerabilita_sociale
        float latitudine
        float longitudine
        integer quota_m
        boolean iperteso
        boolean diabetico
        boolean gravidanza
    }

    visite {
        string professionista_id FK
        date registrata_il
        integer ordine_visita_giorno
        string paziente_id FK
    }

    eventi_clinici {
        string paziente_id FK
        string tipo
        date data_riferimento
    }
```

### equipe.parquet
Anagrafica delle équipe di salute e delle loro sedi (UBS) in Rocinha. *(49 righe)*

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| `equipe_id` | string | Identificativo univoco dell'équipe (hash) |
| `unita_id` | string | Identificativo dell'unità di salute — UBS (hash) |
| `equipe_nome` | string | Nome dell'équipe, dalla micro-area che copre (es. *Equipe Valão*, *Equipe Alto Vidigal*). Ogni équipe ha un **territorio proprio e contiguo**. Pensato per la visualizzazione nel front-end. |
| `unita_nome` | string | Nome dell'unità. Le **strutture reali** presenti su OpenStreetMap sono usate con il loro nome vero (*Clínica da Família Maria do Socorro*, *Rinaldo de Lamare*, *CMS Albert Sabin*, *CMS Rodolpho Perisse*, *CMS Vila Canoas*); le restanti hanno nome sintetico |
| `sede_latitudine` | float | Latitudine dell'unità, sulla **posizione reale** della struttura dove esiste. Gli ACS partono sempre da qui. |
| `sede_longitudine` | float | Longitudine dell'unità. Gli ACS partono sempre da qui. |
| `area` | string | Comunità servita: `Rocinha`, `Vidigal` o `São Conrado` |

### eventi_clinici.parquet
Registro degli eventi clinici dei pazienti. *(100.503 righe)*

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| `paziente_id` | string | Identificativo univoco del paziente (hash) |
| `tipo` | string | `visita-specialistica-prenotata` = appuntamento da comunicare al paziente; `accesso-ps-o-ricovero` = accesso in urgenza/emergenza o ricovero |
| `data_riferimento` | date | Data di riferimento dell'evento (YYYY-MM-DD) |

### pazienti.parquet
Anagrafica completa dei pazienti con informazioni demografiche e cliniche. *(97.938 righe)*

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| `paziente_id` | string | Identificativo univoco del paziente (hash) |
| `equipe_id` | string | Identificativo dell'équipe responsabile (hash) |
| `unita_id` | string | Identificativo dell'unità di salute — UBS (hash) |
| `nome` | string | Nome del paziente *(sintetico)* |
| `cognome` | string | Cognome del paziente *(sintetico)* |
| `fascia_eta` | string | Fascia d'età (`0-6`, `6-18`, `19-45`, `45-65`, `66+`) |
| `sesso` | string | `Femminile` / `Maschile` |
| `razza_colore` | string | `Bianca` / `Nera` / `Parda` / `Altro` — categoria del censimento brasiliano (IBGE); *Parda* = di carnagione mista |
| `vulnerabilita_sociale` | boolean | Indica se il paziente è in situazione di vulnerabilità sociale |
| `latitudine` | float | Latitudine dell'abitazione *(sintetica)*, ancorata alla rete viaria reale di OpenStreetMap |
| `longitudine` | float | Longitudine dell'abitazione *(sintetica)*, ancorata alla rete viaria reale di OpenStreetMap |
| `quota_m` | integer | Quota altimetrica in metri s.l.m. (SRTM 30 m). Su un versante il costo di uno spostamento è il **dislivello**, non la distanza planare |
| `iperteso` | boolean | Indica se il paziente è iperteso |
| `diabetico` | boolean | Indica se il paziente è diabetico |
| `gravidanza` | boolean | Indica se la paziente è in gravidanza |

### visite.parquet
Registro delle visite domiciliari degli ACS, ordinate come percorso. *(159.599 righe)*

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| `professionista_id` | string | Identificativo univoco del professionista/ACS (hash). Chiave esterna verso `professionisti.parquet` |
| `registrata_il` | date | Data della visita (YYYY-MM-DD). **Solo giorni feriali** |
| `ordine_visita_giorno` | integer | Posizione della visita nel **percorso** della giornata (1 = prima). L'ordine è un vero itinerario: partenza dalla sede, poi vicino-più-vicino tenendo conto del **dislivello** |
| `paziente_id` | string | Identificativo del paziente visitato (hash) |

### professionisti.parquet
Anagrafica degli Agenti Comunitari di Salute (ACS), con l'équipe di appartenenza. *(98 righe)*

Ogni ACS lavora per **una sola équipe** e copre una porzione del suo territorio,
con **8-12 visite al giorno** su giornate feriali.

| Colonna | Tipo | Descrizione |
|---------|------|-------------|
| `professionista_id` | string | Identificativo univoco del professionista/ACS (hash) |
| `nome` | string | Nome dell'ACS *(sintetico)* |
| `cognome` | string | Cognome dell'ACS *(sintetico)* |
| `equipe_id` | string | Identificativo dell'équipe di appartenenza (hash). Chiave esterna verso `equipe.parquet` |

---

## 🇧🇷 Glossario per il pubblico italiano

Termini brasiliani mantenuti nella sfida, con l'equivalente o la spiegazione italiana:

| Termine (BR) | Cosa significa |
|--------------|----------------|
| **ACS** — Agente Comunitário de Saúde | Operatore sanitario di comunità, **assunto dal quartiere in cui vive**. Non è un infermiere: è il ponte tra la clinica e le famiglie del territorio. Non esiste una figura identica in Italia (la più vicina è l'Infermiere di Famiglia e di Comunità, ma con formazione clinica). |
| **Rocinha** | La più grande *favela* del Brasile, sul versante tra São Conrado e Gávea a Rio. ~100.000 abitanti. La zona di questa sfida. |
| **Clínica da Família Maria do Socorro** | L'UBS (unità di cure primarie) reale che ancora la nostra mappa. Da qui partono le équipe ogni mattina. |
| **SUS** — Sistema Único de Saúde | Il servizio sanitario pubblico e universale brasiliano — l'equivalente del nostro **SSN**. |
| **UBS** — Unidade Básica de Saúde / **Clínica da Família** | La struttura delle cure primarie sul territorio, dove ha sede l'équipe. Equivale grosso modo alla **Casa della Comunità**. |
| **Atenção Primária** | Cure primarie / assistenza territoriale. |
| **Regulação** | Il sistema pubblico che assegna e prenota le visite specialistiche. Gli appuntamenti "via regulação" sono quelli che l'ACS deve **comunicare** al paziente. |
| **SMS-Rio / SUBPAV** | La Secretaria Municipal de Saúde di Rio e la sua sottosegreteria per le cure primarie — l'amministrazione che ha fornito i dati. |
| **Favela** | Insediamento urbano informale, i **territori più vulnerabili** dove si concentra il lavoro degli ACS. |
| **Área Programática (AP)** | La suddivisione territoriale della sanità di Rio, simile a un **distretto sanitario**. |
| **Raça/cor (IBGE)** | Categoria del censimento brasiliano (Bianca, Nera, Parda…). In Italia il dato "razza/colore" **non** viene raccolto in sanità: qui è parte del contesto brasiliano. |

---

## 🔒 Processo di anonimizzazione e adattamento

I dati originali della Prefeitura sono anonimizzati con: hash crittografico (SHA256),
campionamento (2.000 pazienti per équipe), *date shifting*, rumore geografico
(~100m), randomizzazione degli indirizzi, generalizzazione (fasce d'età, razza/colore)
e soppressione dei record rari (k-anonymity <5).

**Questo adattamento** aggiunge sopra: traduzione delle colonne in italiano, nomi
sintetici deterministici per pazienti, ACS ed équipe, e **rigenerazione completa
della geografia**. I flag clinici, gli eventi e le visite restano quelli del
dataset reale.

### Come sono costruite le coordinate

Le posizioni originali erano già randomizzate in anonimizzazione, quindi non
esistono più: quelle che trovi qui sono **inventate, ma geograficamente plausibili**.
Sono costruite così:

- **Area**: le tre comunità contigue **Rocinha, Vidigal e São Conrado**, con i
  confini amministrativi reali (OpenStreetMap, *admin_level* 10).
- **Ancoraggio**: ogni abitazione è collocata sulla **rete viaria reale** — becos,
  scalinate, vicoli e strade residenziali — con uno scostamento laterale di pochi
  metri, non su una distribuzione gaussiana.
- **Esclusioni**: nessun punto cade sul versante boscoso del **Parco della Tijuca**,
  sul sedime dell'**Autoestrada Lagoa-Barra**, in acqua, sulle spiagge, sulla roccia
  nuda o su impianti sportivi e aree verdi.
- **Territori**: ogni **équipe ha una micro-area propria e contigua** (partizione
  spaziale bilanciata). La purezza territoriale misurata è del **94%**: i vicini di
  un paziente appartengono quasi sempre alla sua stessa équipe.
- **Densità**: più fitta in Rocinha, intermedia in Vidigal, rada a São Conrado, e
  decrescente con la quota (le parti alte del versante sono più rade).
- **Altimetria**: `quota_m` da modello SRTM 30 m (0-285 m s.l.m.).

Distribuzione della popolazione: Rocinha ~65%, Vidigal ~20%, São Conrado ~15%.

### Come sono ricostruite visite, organico ed eventi

Il dataset anonimizzato di partenza presentava tre artefatti che rendevano la sfida
poco praticabile. Sono stati **ricostruiti**, e i dati che ne risultano sono
**sintetici**:

| Artefatto nell'originale | Ricostruzione |
|:-------------------------|:--------------|
| `ordine_visita_giorno` era stato **rinumerato** dopo il campionamento dei pazienti: le giornate risultavano di 1,99 visite (mediana 1), contro le 8-12 reali, e le rotte non erano ricostruibili | Giornate da **8-12 visite** (media 10,5), ordinate come **itinerario reale**: partenza dalla sede, vicino-più-vicino con penalità di dislivello. Visite consecutive distano in mediana **26 m** |
| L'anagrafica conteneva **3.531 ID**, di cui 2.812 con meno di 10 giorni di attività; i 202 più attivi coprivano fino a 19 équipe, incompatibile con un ACS legato al territorio | **98 ACS**, tutti attivi (mediana 147 giornate/anno), ciascuno legato a **una sola** équipe |
| Il *date shifting* aveva distrutto la struttura settimanale: 27% delle visite nel weekend, accessi in PS piatti | Visite **solo nei feriali**; accessi in **PS con picco nel weekend** (38,6%); appuntamenti specialistici solo nei feriali |

**Perché 98 ACS.** È un vincolo aritmetico, non una scelta estetica: 159.599 visite a
8-12 visite/giorno richiedono ~16.000 giornate-agente, cioè ~98 agenti a tempo pieno
equivalente. Mantenere il volume di visite originale (necessario per preservare le
lacune di cura) implica questo organico. Il rapporto che ne risulta — circa **1.000
assistiti per ACS** — è esattamente il sotto-organico che la sfida deve affrontare.

**Cosa NON è stato toccato.** Il campionamento e la ricalibrazione preservano
esattamente le metriche che descrivono il problema da risolvere:

| Indicatore | Originale | Ricostruito |
|:-----------|----------:|------------:|
| Pazienti mai visitati | 49,9% | **49,9%** |
| Follow-up entro 30 gg da un accesso in PS | 23,7% | **23,9%** |
| Promemoria entro 14 gg da un appuntamento | 30,2% | **29,3%** |
| Visite totali | 159.599 | **159.599** |
| Ipertensione / diabete / gravidanza | 21,5 / 8,3 / 0,7% | **21,5 / 8,3 / 0,7%** |

**Cosa NON rappresenta la realtà:** indicatori assoluti, localizzazione precisa,
popolazione totale, date esatte, nomi. **Cosa è preservato:** la sequenza temporale
degli eventi, le relazioni tra tabelle, le prevalenze cliniche e i principali pattern
di comportamento.

### 📚 Riferimenti tecnici

| Metodologia | Link |
|:------------|:-----|
| 🏥 **HIPAA Safe Harbor Method** | [Documentazione](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html) |
| 🔐 **Differential Privacy** | [Wikipedia](https://en.wikipedia.org/wiki/Differential_privacy) |
| 🛡️ **K-Anonymity** | [Wikipedia](https://en.wikipedia.org/wiki/K-anonymity) |

---

<div align="center">

**AI Build Midweek** · Product Heroes · 22 luglio 2026
*Adattamento italiano della sfida del Claude Impact Lab Rio 2026.
Progetto vincitore: [Visitare](https://github.com/Visitare/visitare) — team ACS Digital.*

</div>
