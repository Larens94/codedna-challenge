# CodeDNA Challenge

> **La tua configurazione agente naviga una codebase meglio di CodeDNA — allo stesso livello?**

Un benchmark aperto per ricercatori e sviluppatori. Risolvi gli stessi bug reali multi-file con qualsiasi configurazione — annotazioni CodeDNA, CLAUDE.md personalizzato, .cursorrules, nessuna configurazione — e confronta i risultati in modo oggettivo.

## Premi

| Posizione | Premio |
|-----------|--------|
| 🥇 1° posto | €200 |
| 🥈 2° posto | €100 |
| 🥉 3° posto | €50 |

I vincitori vengono annunciati al raggiungimento del numero minimo di submission valide.
I risultati vengono pubblicati in tempo reale sulla leaderboard.

---

## La regola di fairness: stack simmetrico

CodeDNA è sempre il **control**. Ogni submission viene confrontata con una run CodeDNA allo **stesso livello di stack**.

### Livelli dello stack CodeDNA

CodeDNA v0.9 include più layer — i partecipanti scelgono quali attivare:

| Layer CodeDNA | Cosa aggiunge |
|---------------|--------------|
| **L0** — manifest `.codedna` | Mappa dei package a livello di repo, iniettata all'avvio della sessione |
| **L1** — module headers | `exports:` `used_by:` `rules:` `related:` `agent:` `message:` in ogni file |
| **L2** — function Rules: | Vincoli a livello di docstring ad ogni chiamata cross-file |
| **L3** — semantic naming | I nomi delle variabili codificano tipo + origine + dominio |
| **wiki** — knowledge vault | Campo `wiki:` + `codedna wiki bootstrap/sync` → vault Obsidian + project wiki narrativo |

### Regola di confronto

| La tua submission | Run CodeDNA control richiesta |
|-------------------|-------------------------------|
| Qualsiasi config, nessun extra | CodeDNA L0+L1 |
| La tua config + knowledge base / docs | CodeDNA L0+L1+wiki |
| La tua config + RAG | CodeDNA L0+L1+wiki + stesso setup RAG |
| La tua config + vector DB / MCP / Skills | CodeDNA L0+L1+wiki + stessi extra |

**Puoi portare qualsiasi stack — purché CodeDNA abbia lo stesso stack nel confronto.**

---

## Regole

1. **Numero minimo di partecipanti:** la leaderboard e i premi si attivano quando si raggiungono **almeno 20 submission valide** tra tutti i task. Prima di quella soglia, le submission vengono raccolte ma non classificate.

2. **Validità:** una submission è valida solo se `task_tests_pass: true` E `regression_tests_pass: true`, verificato dalla CI. Le submission non valide o con test falliti vengono scartate.

3. **Niente imbrogli:** le submission che hardcodano output attesi, leggono i file ground-truth prima di iniziare, o aggirano in altro modo la vera navigazione dell'agente vengono squalificate. Il giudice (@Larens94) revisiona manualmente tutte le submission.

4. **Mini relazione obbligatoria:** ogni submission deve includere un `report.md` (max 1 pagina) che copre:
   - Quale configurazione hai usato e perché
   - Come l'agente ha approcciato il task (strategia di navigazione)
   - Eventuali **casi borderline** — annotazioni ambigue, edge case nel task, o qualsiasi cosa che dovrebbe essere esaminata prima di essere conteggiata
   - Qualcosa che ti ha sorpreso (positivo o negativo)

5. **Stack simmetrico:** se aggiungi strumenti oltre al Level 0 (RAG, vector DB, MCP), è richiesta una run CodeDNA corrispondente allo stesso livello di stack.

6. **Una submission per task per partecipante.** Puoi ripresentare se la tua submission precedente era invalida (test falliti), ma devi aprire una nuova PR con un nuovo `report.md` che spiega cosa è cambiato.

7. **I risultati sono pubblici.** Tutte le submission — incluse quelle fallite — sono visibili nel repo per trasparenza.

---

## Come partecipare

Ogni submission contiene **due run sullo stesso task**: una con CodeDNA (il control) e una con la tua configurazione. Il confronto è auto-contenuto nella tua PR — il giudice non esegue nulla.

1. **Scegli un task** dalla cartella `tasks/`
2. **Run 1 — CodeDNA control:** annota il progetto con `codedna init`, poi esegui il tuo agente
3. **Run 2 — la tua configurazione:** esegui lo stesso task con il tuo approccio (CLAUDE.md custom, no-config, RAG, ecc.)
4. **Apri una PR** aggiungendo `submissions/<tuo-username>/`:
   ```
   submissions/<tuo-username>/
   ├── codedna/
   │   ├── results.json     # run con CodeDNA
   │   └── session.jsonl    # opzionale — session trace Claude Code
   ├── challenger/
   │   ├── results.json     # run con la tua configurazione
   │   ├── config/          # i tuoi file di config (CLAUDE.md, .cursorrules, ecc.)
   │   └── session.jsonl    # opzionale
   └── report.md            # mini relazione su entrambe le run
   ```

**Il giudice (@Larens94) revisiona ogni PR per validità e simmetria prima che conti nella classifica.**
La CI verifica che i test passino — le submission invalide vengono scartate.

---

## Metriche

Ogni submission viene valutata su:

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
| `message_adoption_rate` | % di file in cui gli agenti hanno usato `message:` per coordinarsi (solo CodeDNA) |
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

Classifica: `task_tests_pass` + `regression_tests_pass` prima → `f1_localization` DESC → `cost_usd` ASC (tutte le retry sommate).

---

## Generare results.json automaticamente

Se hai usato **Claude Code**, esegui:

```bash
python scripts/report.py \
  --session ~/.claude/projects/<hash>/<session-id>.jsonl \
  --task task_01 \
  --participant tuo-username-github \
  --approach "codedna-v0.9"
```

Questo legge il JSONL della sessione e compila automaticamente tutte le metriche token/costo/tool-call.
Dovrai compilare manualmente `files_touched`.

Per altri strumenti (Cursor, Copilot, OpenCode), compila `results.json` manualmente dalle statistiche d'uso del tuo tool.

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
| task_02 | aperto a proposte | — | — |
| … | fino a 10 task | — | — |

---

## Leaderboard

→ **[Visualizza la leaderboard live](https://larens94.github.io/codedna-challenge)**

---

## Di cosa si tratta questa challenge

Non è un esercizio di marketing. CodeDNA è stato progettato per risolvere un problema specifico: gli agenti AI spendono troppo del loro budget di contesto navigando i file sbagliati. L'ipotesi è che incorporare metadati di navigazione direttamente nei file sorgente — a Level 0, senza infrastruttura esterna — sia sufficiente a migliorare misurabilmente le performance degli agenti.

Abbiamo già dati benchmark su task Django di SWE-bench. Questa challenge invita la community a testare l'ipotesi su progetti diversi, con modelli diversi e configurazioni concorrenti.

Se il tuo approccio batte CodeDNA, è un risultato valido e interessante. Pubblicalo.

---

## Contatti

- GitHub: [@Larens94](https://github.com/Larens94)
- Spec & paper CodeDNA: [github.com/Larens94/codedna](https://github.com/Larens94/codedna)
- Domande: apri una issue in questo repo
