# Relazione di Submission — [tuo-username] · [task_id]

## Setup

- **Tool:** (es. Claude Code, Cursor, Copilot, …)
- **Modello:** (es. claude-sonnet-4-6, gpt-4o, deepseek-chat, …)
- **Config:** (es. CLAUDE.md personalizzato, .cursorrules, nessuna config, …)
- **Stack extra:** (RAG, vector DB, MCP — oppure "nessuno")
- **Layer CodeDNA attivati (Run B):** (es. L0+L1, L0+L1+wiki, …)

## Run A — baseline (senza CodeDNA)

Descrivi brevemente come l'agente ha approcciato il task senza annotazioni CodeDNA: quali file ha aperto per primo, come è arrivato al bug, quante retry sono state necessarie.

(3–6 frasi sono sufficienti)

## Run B — con CodeDNA

Descrivi lo stesso per la run con le annotazioni CodeDNA presenti. La navigazione è cambiata? L'agente ha usato i campi `used_by:` / `rules:` / `message:`?

## Delta

Cosa è cambiato concretamente tra Run A e Run B? (token count, tool call, failed edit, f1_localization, costo…)

## Perché questa configurazione

Perché hai scelto questo tool e questa config? Cosa ti aspettavi che CodeDNA facesse meglio o peggio con il tuo setup specifico?

## Casi borderline ⚠️

Elenca tutto ciò che potrebbe influire sulla validità della tua submission e che dovrebbe essere esaminato dal giudice prima di essere conteggiato:

- [ ] (nessuno — la submission è lineare)

Esempi di cose da segnalare:
- L'agente ha letto un file che rivela parzialmente la fix
- Un test è passato per il motivo sbagliato
- Hai dovuto intervenire manualmente in qualche punto
- La descrizione del task era ambigua e l'hai interpretata in un modo specifico
- Run A e Run B non sono state eseguite in condizioni strettamente identiche

## Osservazioni

Qualcosa che ti ha sorpreso — positivo o negativo — riguardo al task, al tool o all'effetto delle annotazioni CodeDNA sul tuo workflow.
