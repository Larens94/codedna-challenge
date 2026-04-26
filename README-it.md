> ⚠️ **BOZZA — non ancora aperta.** I task sono in fase di finalizzazione. Segui questo repo per l'annuncio di lancio.

# CodeDNA Challenge

> **CodeDNA migliora il tuo workflow — indipendentemente dallo stack che usi?**

Un benchmark ablativo aperto per ricercatori e sviluppatori. Esegui lo stesso task reale di bug-fix multi-file **due volte con il tuo setup** — una senza annotazioni CodeDNA, una con — e misura il delta in modo oggettivo.

## Premi (simbolici)

| Posizione | Premio |
|-----------|--------|
| 🥇 1° posto | €200 |
| 🥈 2° posto | €100 |
| 🥉 3° posto | €50 |

I premi sono simbolici e finanziati dall'organizzatore. I vincitori vengono annunciati al raggiungimento di almeno 20 submission valide tra tutti i task.

---

## Il design: ablazione within-stack

Questa **non** è "la tua configurazione contro CodeDNA." È uno studio ablativo:

| Run | Cosa cambia |
|-----|-------------|
| **Run A — baseline** | Il tuo tool + il tuo modello + la tua config, *senza* annotazioni CodeDNA |
| **Run B — con CodeDNA** | Stesso tool, modello e config — ma il progetto viene annotato con `codedna init` |

L'unica variabile che cambia tra Run A e Run B è la presenza delle annotazioni CodeDNA nei file sorgente. Tutto il resto rimane costante: stesso bug, stesso modello, stessi file di configurazione, stesso tool.

**Puoi portare qualsiasi stack** (RAG, vector DB, MCP, CLAUDE.md personalizzato, Cursor, Copilot, pipeline multi-agente). L'ablazione funziona in ogni caso — Run A è il tuo stack senza CodeDNA, Run B è il tuo stack con CodeDNA.

### Cosa aggiunge CodeDNA (solo Run B)

| Layer | Cosa aggiunge |
|-------|--------------|
| **L0** — manifest `.codedna` | Mappa dei package a livello di repo, iniettata all'avvio della sessione |
| **L1** — module headers | `exports:` `used_by:` `rules:` `related:` `agent:` `message:` in ogni file |
| **L2** — function Rules: | Vincoli a livello di docstring ad ogni chiamata cross-file |
| **L3** — semantic naming | I nomi delle variabili codificano tipo + origine + dominio |
| **wiki** | Campo `wiki:` + `codedna wiki sync` → project wiki narrativo |

---

## Regole

1. **Numero minimo di partecipanti:** la leaderboard e i premi si attivano quando si raggiungono **almeno 20 submission valide** tra tutti i task. Prima di quella soglia, le submission vengono raccolte ma non classificate.

2. **Validità:** una submission è valida solo se `task_tests_pass: true` E `regression_tests_pass: true` in **entrambe** Run A e Run B, verificato dalla CI. Le submission non valide vengono scartate.

3. **Niente imbrogli:** le submission che hardcodano output attesi, leggono i file ground-truth prima di iniziare, o aggirano in altro modo la vera navigazione dell'agente vengono squalificate. Il giudice (@Larens94) revisiona manualmente tutte le submission.

4. **Mini relazione obbligatoria:** ogni submission deve includere un `report.md` (max 1 pagina) che copre:
   - Quale tool, modello e configurazione hai usato
   - Come l'agente ha approcciato il task in Run A e Run B (strategia di navigazione)
   - Eventuali **casi borderline** — qualsiasi cosa che potrebbe influire sulla validità e dovrebbe essere esaminata prima di essere conteggiata
   - Cosa è cambiato tra Run A e Run B, e cosa ti ha sorpreso

5. **Stack simmetrico:** Run A e Run B devono usare lo stesso tool, modello e file di configurazione. L'unica differenza consentita è la presenza delle annotazioni CodeDNA.

6. **Una submission per task per partecipante.** Puoi ripresentare se la tua submission precedente era invalida (test falliti), ma devi aprire una nuova PR con un nuovo `report.md` che spiega cosa è cambiato.

7. **I risultati sono pubblici.** Tutte le submission — incluse quelle fallite — sono visibili nel repo per trasparenza.

---

## Come partecipare

Ogni submission contiene **due run sullo stesso task**: Run A (senza CodeDNA) e Run B (con CodeDNA). Le esegui entrambe tu. Il confronto è auto-contenuto nella tua PR — il giudice non esegue nulla.

1. **Scegli un task** dalla cartella `tasks/`
2. **Run A — baseline:** esegui il tuo agente sul progetto congelato. Senza annotazioni CodeDNA.
3. **Run B — con CodeDNA:** annota lo stesso progetto congelato con `codedna init`, poi esegui lo stesso agente e config sullo stesso task.
4. **Apri una PR** aggiungendo `submissions/<tuo-username>/`:
   ```
   submissions/<tuo-username>/
   ├── baseline/
   │   ├── results.json     # Run A — senza CodeDNA
   │   └── session.jsonl    # opzionale — session trace (Claude Code, Cursor, ecc.)
   ├── codedna/
   │   ├── results.json     # Run B — con CodeDNA
   │   └── session.jsonl    # opzionale
   ├── config/              # i tuoi file di config (CLAUDE.md, .cursorrules, ecc.)
   └── report.md            # mini relazione su entrambe le run
   ```

**Il giudice (@Larens94) revisiona ogni PR per validità e simmetria dello stack prima che conti nella classifica.**
La CI verifica che i test passino — le submission invalide vengono scartate.

---

## Metriche

Sia Run A che Run B vengono misurate sullo stesso set di metriche. Il delta tra le due è il segnale principale.

**Correttezza della fix**
| Metrica | Descrizione |
|---------|-------------|
| `task_tests_pass` | I test specifici del task ora passano (il bug è risolto) |
| `regression_tests_pass` | La test suite completa è ancora verde — nessuna regressione introdotta |
| `patch_lines` | Righe modificate nella patch finale (meno = più chirurgico) |
| `failed_edits` | Tentativi di modifica falliti durante la sessione |

**Qualità di navigazione**
| Metrica | Descrizione |
|---------|-------------|
| `f1_localization` | L'agente ha trovato i file giusti? (media armonica di precision + recall sui file ground-truth) |
| `retry_count` | Quante volte hai dovuto ri-invocare l'agente perché la patch era incompleta? |

**Efficienza token**
| Metrica | Descrizione |
|---------|-------------|
| `tokens_input` | Token di input consumati |
| `tokens_output` | Token di output generati |
| `cache_read` | Token cache riutilizzati (costo ridotto) |
| `cost_usd` | Costo totale della sessione in USD (tutte le retry sommate) |
| `tool_calls_total` | Tool call totali — meno = meno spreco di navigazione |

**Multi-agent (opzionale — se usi più di un agente)**
| Metrica | Descrizione |
|---------|-------------|
| `agent_count` | Numero di agenti nella sessione |
| `message_adoption_rate` | % di file in cui gli agenti hanno usato `message:` per coordinarsi (solo Run B) |
| `framework_conflicts` | Conflitti architetturali rilevati (es. due agenti che usano framework diversi) |

**Perché queste metriche contano — dati esistenti CodeDNA:**

| Dimensione | Senza CodeDNA | Con CodeDNA |
|------------|--------------|-------------|
| File corrispondenti alla patch ufficiale (Django #13495, Claude Sonnet) | 6 / 7 | **7 / 7** |
| Edit falliti (stesso task) | 5 | **0** |
| Run ad alto rischio — recall < 50% → patch incompleta (SWE-bench, 3 modelli) | 52% | **25%** |
| Tool call (Gemini 2.5 Pro) | baseline | **−14.3%** |
| Velocità del team (SaaS 5 agenti, DeepSeek R1) | 1× | **1.6×** |

CodeDNA non aiuta solo l'agente a trovare i file giusti — elimina completamente i failed edit sui task con dependency chain. Questa challenge verifica se ciò vale su nuovi progetti e nuovi modelli.

Classifica: `task_tests_pass` + `regression_tests_pass` (entrambe le run) prima → `f1_localization` (Run B) DESC → `cost_usd` (Run B) ASC.

---

## Raccogliere le metriche

**Claude Code** — estrai dal JSONL della sessione in `~/.claude/projects/<hash>/<session-id>.jsonl`:
- Le righe con `"type": "assistant"` contengono `message.usage` con `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`
- Esegui `/cost` all'interno della sessione per un riepilogo in tempo reale

**Altri tool** (Cursor, Copilot, OpenCode) — compila `results.json` manualmente dalle statistiche d'uso del tuo tool.

Vedi `submissions/example/` per il template completo di `results.json`.

---

## Task

I task vengono proposti e validati dalla community di ricerca prima dell'apertura della challenge.

**Requisiti per un task valido:**
- Bug reale da un progetto Python open source (non già in SWE-bench)
- Fix multi-file: la patch tocca 2–6 file
- Test suite deterministica: un test specifico fallisce prima della fix e passa dopo
- Il progetto viene congelato a un commit specifico — tutti lavorano su codice identico

**Per proporre un task:** apri una issue con il label `task-proposal` includendo l'URL della issue GitHub, il commit da congelare e il test che fallisce.

La challenge si apre quando almeno **3 task validati** sono pronti e **20 partecipanti** si sono iscritti.

| Task | Progetto | Difficoltà | File coinvolti |
|------|----------|------------|----------------|
| task_01 | aperto a proposte | — | — |
| … | fino a 10 task | — | — |

---

## Leaderboard

In arrivo — pubblicata al lancio della challenge.

---

## Di cosa si tratta questa challenge

Non è un esercizio di marketing. CodeDNA è stato progettato per risolvere un problema specifico: gli agenti AI spendono troppo del loro budget di contesto navigando i file sbagliati. L'ipotesi è che incorporare metadati di navigazione direttamente nei file sorgente — a Level 0, senza infrastruttura esterna — sia sufficiente a migliorare misurabilmente le performance degli agenti.

Abbiamo già dati benchmark su task Django di SWE-bench. Questa challenge invita la community a testare l'ipotesi su progetti diversi, modelli diversi e stack diversi — e a fornire evidenze controllate a favore o contro.

Se CodeDNA non fa differenza nel tuo stack, è un risultato valido e interessante. Pubblicalo.

---

## Contatti

- GitHub: [@Larens94](https://github.com/Larens94)
- Spec & paper CodeDNA: [github.com/Larens94/codedna](https://github.com/Larens94/codedna)
- Domande o proposte di task: apri una issue in questo repo oppure scrivi a [fabrizio.corpora@gmail.com](mailto:fabrizio.corpora@gmail.com)
