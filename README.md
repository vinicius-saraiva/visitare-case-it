<div align="center">

# 🏥 Visitare Case — AI Build Midweek

**Dall'idea a un'app online in ~60 minuti, in diretta.**
Costruire *Visitare* — l'app che dà a un Agente Comunitario di Salute (ACS) la lista
e la mappa dei suoi pazienti — partendo da un dataset sanitario reale di Rio de Janeiro.

[![La sfida](https://img.shields.io/badge/📄_La_sfida-SFIDA.md-5436DA?style=for-the-badge)](SFIDA.md)
[![Repo di lavoro](https://img.shields.io/badge/⚙️_Repo_di_lavoro-ai--build--midweek--live-1E3A8A?style=for-the-badge)](https://github.com/vinicius-saraiva/ai-build-midweek-live)
[![App live](https://img.shields.io/badge/🚀_App_live-visitare--rio.vercel.app-E63946?style=for-the-badge)](https://visitare-rio.vercel.app/)

</div>

---

## 🔗 I tre link

| | Cosa | Dove |
|:--|:-----|:-----|
| 📄 | **La sfida** — il caso, il dataset e il dizionario dei dati | [`SFIDA.md`](SFIDA.md) |
| ⚙️ | **Il repo di lavoro** — tutto ciò che abbiamo costruito insieme in diretta (artefatti RePPIT, back-end Supabase, codice dell'app) | [`ai-build-midweek-live`](https://github.com/vinicius-saraiva/ai-build-midweek-live) |
| 🚀 | **L'app funzionante, online** — provala dal telefono | [visitare-rio.vercel.app](https://visitare-rio.vercel.app/) |

> 📝 **Tutti i prompt che ho usato** durante la sessione, in ordine e raggruppati per
> fase, sono qui: [`prompts.md`](https://github.com/vinicius-saraiva/ai-build-midweek-live/blob/main/prompts.md)
> (nel repo di lavoro).

---

## 🧭 Il metodo — RePPIT

> **RePPIT** è un metodo ideato da [Mihail Eric](https://themodernsoftware.dev/).
> Il mio approfondimento: [vinicius.pm/reppit](https://vinicius.pm/reppit).

L'app non è stata costruita chiedendo tutto in un prompt solo. Ogni fase ha lasciato un
**artefatto scritto** che la fase dopo si rilegge come contesto:

| | Fase | Domanda | Artefatto |
|:--|:-----|:--------|:----------|
| **Re** | Research | Cosa abbiamo davvero tra le mani? | `research.md` + `mappa-3d.html` |
| **P** | Propose | Cosa costruiamo, tra le opzioni? | `proposal.md` · `stack-proposal.md` |
| **P** | Plan | In che ordine, cosa si parallelizza? | `plan.md` |
| **I** | Implement | Costruiamolo | `visitare-app/` + back-end Supabase |
| **T** | Test | Funziona davvero, o solo in teoria? | prova a 390 px + deploy |

Trovi tutti questi artefatti nel [repo di lavoro](https://github.com/vinicius-saraiva/ai-build-midweek-live).

---

<div align="center">

**Visitare Case** · AI Build Midweek · Product Heroes · 22 luglio 2026

*Adattamento italiano della sfida del [Claude Impact Lab Rio 2026](https://github.com/prefeitura-rio/claude-impact-lab-saude)
(Anthropic · Prefeitura do Rio de Janeiro).
Progetto vincitore dell'edizione originale: [Visitare](https://github.com/Visitare/visitare) — team ACS Digital.*

</div>
