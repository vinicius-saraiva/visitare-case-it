"""
Adattamento leggero del dataset reale del Claude Impact Lab Rio 2026.

Parte dai 4 parquet ANONIMIZZATI reali della Prefeitura do Rio e li trasforma
in modo che:
  1. le colonne siano tradotte in italiano (leggibili dal pubblico);
  2. ogni paziente riceva un nome/cognome brasiliano sintetico (deterministico);
  3. tutti i punti GPS siano riposizionati nella Favela da Rocinha, attorno alla
     Clínica da Família Maria do Socorro Silva e Souza (-22.9893451, -43.255015).

I DATI CLINICI REALI (ipertensione, diabete, gravidanza, vulnerabilità, eventi,
visite) e le loro RELAZIONI sono preservati: cambiano solo l'etichetta delle
colonne, i nomi (che nell'originale erano anonimizzati) e le coordinate (che
nell'originale erano già randomizzate come rumore).

Contesto brasiliano mantenuto: ACS, UBS, Rio, Rocinha.
"""

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

SRC = Path(__file__).parent.parent / "dataset-italia" / "original"
OUT = Path(__file__).parent / "assets" / "parquet"
PREVIEW = Path(__file__).parent / "assets" / "anteprima"
OUT.mkdir(parents=True, exist_ok=True)
PREVIEW.mkdir(parents=True, exist_ok=True)

# --- Rocinha: ancora e area di dispersione ----------------------------------
CLINICA_LAT, CLINICA_LON = -22.9893451, -43.255015
# bounding box approssimativo della favela (in gradi)
LAT_MIN, LAT_MAX = -22.9955, -22.9835
LON_MIN, LON_MAX = -43.2600, -43.2470


def short_id(h: str) -> str:
    """Accorcia l'hash a 12 caratteri per la leggibilità a schermo."""
    return h[:12]


def clip(lat, lon):
    return (float(np.clip(lat, LAT_MIN, LAT_MAX)),
            float(np.clip(lon, LON_MIN, LON_MAX)))


# ---------------------------------------------------------------------------
# 1. EQUIPE — riposiziona le sedi (le UBS) dentro Rocinha
# ---------------------------------------------------------------------------
eq = pd.read_parquet(SRC / "equipes_anonimizadas.parquet")

# le coordinate originali distinte = le distinte unità di salute (UBS)
sedi_orig = eq[["endereco_latitude", "endereco_longitude"]].drop_duplicates().reset_index(drop=True)
n_unita = len(sedi_orig)

# genera n_unita punti-sede dentro Rocinha; il primo = la Clínica Maria do Socorro
sede_lat = [CLINICA_LAT]
sede_lon = [CLINICA_LON]
for _ in range(n_unita - 1):
    sede_lat.append(float(rng.uniform(LAT_MIN + 0.001, LAT_MAX - 0.001)))
    sede_lon.append(float(rng.uniform(LON_MIN + 0.001, LON_MAX - 0.001)))

nomi_unita = ["Clínica da Família Maria do Socorro Silva e Souza"] + \
             [f"UBS Rocinha {i:02d}" for i in range(2, n_unita + 1)]

sedi_orig["_key"] = sedi_orig["endereco_latitude"].round(6).astype(str) + "|" + \
                    sedi_orig["endereco_longitude"].round(6).astype(str)
sedi_orig["unita_id"] = [short_id(hashlib.sha256(f"unita{i}".encode()).hexdigest()) for i in range(n_unita)]
sedi_orig["unita_nome"] = nomi_unita
sedi_orig["sede_latitudine"] = np.round(sede_lat, 6)
sedi_orig["sede_longitudine"] = np.round(sede_lon, 6)

key2sede = sedi_orig.set_index("_key")[["unita_id", "unita_nome", "sede_latitudine", "sede_longitudine"]]

eq["_key"] = eq["endereco_latitude"].round(6).astype(str) + "|" + eq["endereco_longitude"].round(6).astype(str)
eq = eq.merge(key2sede, left_on="_key", right_index=True, how="left")
equipe = pd.DataFrame({
    "equipe_id": eq["equipe_id"].map(short_id),
    "unita_id": eq["unita_id"],
    "unita_nome": eq["unita_nome"],
    "sede_latitudine": eq["sede_latitudine"],
    "sede_longitudine": eq["sede_longitudine"],
})
# mappa equipe_id(originale) -> sede, per posizionare i pazienti
eqorig2sede = eq.set_index("equipe_id")[["sede_latitudine", "sede_longitudine"]].to_dict("index")

# ---------------------------------------------------------------------------
# 2. PAZIENTI — traduci colonne, aggiungi nomi, riposiziona in Rocinha
# ---------------------------------------------------------------------------
pac = pd.read_parquet(SRC / "pacientes_anonimizados.parquet")

SESSO = {"Feminino": "Femminile", "Masculino": "Maschile"}
RAZZA = {"Branca": "Bianca", "Preta": "Nera", "Parda": "Parda", "Outros": "Altro"}

# --- pool di nomi brasiliani ---
FEM = ["Maria", "Ana", "Francisca", "Antônia", "Adriana", "Juliana", "Márcia",
       "Fernanda", "Patrícia", "Aline", "Sandra", "Camila", "Amanda", "Bruna",
       "Jéssica", "Letícia", "Vanessa", "Débora", "Luciana", "Cláudia",
       "Rosângela", "Vera", "Cristiane", "Simone", "Regina"]
FEM_IDOSA = ["Maria", "Conceição", "Terezinha", "Aparecida", "Francisca",
             "Benedita", "Sebastiana", "Rita", "Josefa", "Lourdes", "Neusa"]
MASC = ["José", "João", "Antônio", "Francisco", "Carlos", "Paulo", "Pedro",
        "Lucas", "Luiz", "Marcos", "Gabriel", "Rafael", "Daniel", "Marcelo",
        "Bruno", "Eduardo", "Felipe", "Rodrigo", "Rafael", "Gustavo", "Thiago",
        "Leonardo", "Fernando", "Márcio", "Wesley"]
MASC_IDOSO = ["José", "Antônio", "Sebastião", "Benedito", "Raimundo", "Geraldo",
              "Manoel", "Severino", "Waldir", "Osvaldo", "Djalma"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira",
              "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins",
              "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira",
              "Barbosa", "Rocha", "Dias", "Nunes", "Moreira", "Cardoso",
              "Teixeira", "Correia", "Mendes", "Nascimento", "Araújo"]


def nome_per(pid: str, sesso: str, faixa: str):
    r = np.random.default_rng(int(hashlib.sha256(pid.encode()).hexdigest()[:8], 16))
    idoso = faixa == "66+"
    if sesso == "Femminile":
        pool = FEM_IDOSA if idoso else FEM
    else:
        pool = MASC_IDOSO if idoso else MASC
    nome = pool[r.integers(len(pool))]
    sob = f"{SOBRENOMES[r.integers(len(SOBRENOMES))]} {SOBRENOMES[r.integers(len(SOBRENOMES))]}"
    return nome, sob


sesso_it = pac["sexo"].map(SESSO)
nomi = [nome_per(pid, s, f) for pid, s, f in zip(pac["paciente_id"], sesso_it, pac["faixa_etaria"])]

# coordinate: attorno alla sede della propria equipe (le orig. dei pazienti erano rumore)
base = pac["equipe_id"].map(lambda e: eqorig2sede.get(e, {"sede_latitudine": CLINICA_LAT, "sede_longitudine": CLINICA_LON}))
base_lat = base.map(lambda d: d["sede_latitudine"]).to_numpy()
base_lon = base.map(lambda d: d["sede_longitudine"]).to_numpy()
jit_lat = rng.normal(0, 0.0013, len(pac))
jit_lon = rng.normal(0, 0.0016, len(pac))
new_coords = [clip(la + jla, lo + jlo) for la, lo, jla, jlo in zip(base_lat, base_lon, jit_lat, jit_lon)]

pazienti = pd.DataFrame({
    "paziente_id": pac["paciente_id"].map(short_id),
    "equipe_id": pac["equipe_id"].map(short_id),
    "unita_id": pac["unidade_id"].map(short_id),
    "nome": [n for n, _ in nomi],
    "cognome": [s for _, s in nomi],
    "fascia_eta": pac["faixa_etaria"],
    "sesso": sesso_it,
    "razza_colore": pac["raca_cor"].map(RAZZA),
    "vulnerabilita_sociale": pac["situacao_vulnerabilidade"],
    "latitudine": [round(la, 6) for la, _ in new_coords],
    "longitudine": [round(lo, 6) for _, lo in new_coords],
    "iperteso": pac["hipertenso"],
    "diabetico": pac["diabetico"],
    "gravidanza": pac["gestacao"],
})

# ---------------------------------------------------------------------------
# 3. EVENTI CLINICI — traduci colonne e valori
# ---------------------------------------------------------------------------
ev = pd.read_parquet(SRC / "eventos_clinicos_anonimizados.parquet")
TIPO = {
    "agendamento": "visita-specialistica-prenotata",
    "urgencia-emergencia-ou-internacao": "accesso-ps-o-ricovero",
}
eventi = pd.DataFrame({
    "paziente_id": ev["paciente_id"].map(short_id),
    "tipo": ev["tipo"].map(TIPO),
    "data_riferimento": ev["data_referencia"],
})

# ---------------------------------------------------------------------------
# 4. VISITE — traduci colonne
# ---------------------------------------------------------------------------
vis = pd.read_parquet(SRC / "visitas_anonimizadas.parquet")
visite = pd.DataFrame({
    "professionista_id": vis["profissional_id"].map(short_id),
    "registrata_il": vis["registrados_em"],
    "ordine_visita_giorno": vis["ordem_visita_dia"],
    "paziente_id": vis["paciente_id"].map(short_id),
})

# ---------------------------------------------------------------------------
# Salvataggio
# ---------------------------------------------------------------------------
tabelle = {
    "equipe": equipe,
    "pazienti": pazienti,
    "eventi_clinici": eventi,
    "visite": visite,
}
for nome, df in tabelle.items():
    df.to_parquet(OUT / f"{nome}.parquet", index=False)
    df.head(200).to_csv(PREVIEW / f"{nome}_anteprima.csv", index=False)
    print(f"{nome:16s} {df.shape[0]:>7,} righe  -> {nome}.parquet  {list(df.columns)}")

# rimuovi i vecchi parquet con nomi portoghesi
for vecchio in ["pacientes", "eventos_clinicos", "visitas", "equipes"]:
    p = OUT / f"{vecchio}.parquet"
    if p.exists():
        p.unlink()
        print(f"rimosso {vecchio}.parquet (versione originale non tradotta)")

print(f"\nCoordinate: lat [{pazienti.latitudine.min():.4f}, {pazienti.latitudine.max():.4f}] "
      f"lon [{pazienti.longitudine.min():.4f}, {pazienti.longitudine.max():.4f}]")
print(f"Clínica Maria do Socorro: {CLINICA_LAT}, {CLINICA_LON}")
