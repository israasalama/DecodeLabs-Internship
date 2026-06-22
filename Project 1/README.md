# Rule-Based AI Chatbot — Logic Engine

A deterministic, terminal-based chatbot built on the **Input → Process
→ Output (IPO)** model. Every response is produced by explicit,
hard-coded rules — there is no machine learning, no randomness, and no
hidden reasoning. The same input always produces the same output.

This is **Project 1** of the DecodeLabs AI Internship track (Batch
2026): the foundation milestone that proves mastery of control flow,
structured response mapping, and "white-box" explainable logic before
moving on to probabilistic/generative AI systems.

---

## Table of Contents

- [Why a Rule-Based Chatbot?](#why-a-rule-based-chatbot)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Example Session](#example-session)
- [Project Structure](#project-structure)
- [Running the Tests](#running-the-tests)
- [Design Documents](#design-documents)
- [Future Enhancements](#future-enhancements)

---

## Why a Rule-Based Chatbot?

Before building AI systems that *learn* or *generate* unpredictably,
the DecodeLabs track requires demonstrating that you can build the
**deterministic control layer** that sits beneath them — the kind of
guardrail logic real production AI systems still rely on today.

| Property | This chatbot |
|---|---|
| Determinism | Same input → same output, always |
| Explainability | Every reply traces back to one rule, with no hidden steps |
| Safety | Zero hallucination risk — every response is hard-coded |
| Lookup strategy | O(1) dictionary lookup, not an O(n) if-elif ladder |

---

## Architecture Overview

The codebase is organized into the same **IPO layers** the design
specifies, with each layer owning exactly one responsibility:

```
INPUT  → reads & sanitizes raw terminal text
PROCESS → classifies the text as EXIT / INTENT / FALLBACK
OUTPUT → renders prompts, replies, and the startup banner
SESSION → owns the continuous while-loop that ties it all together
```

```
src/
├── config/        AppConfig — exit command, fallback text, labels
├── core/           Shared enums (MatchType, SessionState) & data models
├── knowledge/      KnowledgeBase — the intent → response dictionary
├── input/          TerminalInputReader, InputSanitizer
├── process/        ExitDetector, IntentMatcher, ResponseEngine
├── output/         TerminalPresenter, BannerRenderer
├── session/        ChatSession, InteractionLogger
└── main.py         ChatBotApp — wires everything together
```

No class does more than one job. `ChatSession`, for example, owns the
loop but contains **zero** intent-matching rules — that logic lives
only in `process/`. This separation is what makes every individual
piece independently testable.

For the full design rationale, UML, and sequence diagrams, see
[`docs/architecture.md`](docs/architecture.md).

---

## Installation

**Requirements:** Python 3.10 or later (uses the `str | None` union
syntax). No external dependencies are needed to run the chatbot
itself; `pytest` is only required for running the test suite.

```bash
# 1. Clone or download the project, then move into it
cd chatbot_project

# 2. (Optional) create a virtual environment
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. (Optional, for running tests) install pytest
pip install pytest
```

---

## Usage

Run the chatbot as a module from the project root:

```bash
python3 -m src.main
```

You'll see a startup banner, then a `You: ` prompt. Type a message
and press Enter. Type `exit` at any time to end the session cleanly.

### Supported commands (seed knowledge base)

| You type | Bot replies |
|---|---|
| `hello` | Hi there! Welcome to the Logic Engine. |
| `hi` | Hello! How can I help you today? |
| `help` | Supported commands: hello, hi, help, bye, exit. |
| `bye` | Goodbye! Have a great day. |
| `how are you` | I'm running on deterministic logic - always consistent! |
| *(anything else)* | I do not understand. |
| `exit` | Ends the session |

Input is sanitized before matching, so `HELLO`, `  Hello  `, and
`hello` are all treated identically.

---

## Portfolio Upgrades

Beyond the minimum spec, this implementation adds:

| Feature | How it works |
|---|---|
| **More intents** | 14 intents per personality (greetings, `what can you do`, `your name`, `who made you`, `thanks`, `joke`, plus the original 5). |
| **Personality modes** | `mode neutral`, `mode friendly`, `mode professional` — swap the entire response set live, mid-conversation. |
| **Command history** | Type `history` to see your last 5 exchanges and the bot's replies. |
| **Persistent logging** | Every turn is appended to `chatbot_session.log` on disk (in addition to the in-memory trace), so history survives after the program closes. |
| **`clear` command** | Clears the visible terminal output. |
| **Expanded `help`** | Lists every available command, including the new ones. |

These are handled by a new `CommandRouter` (in `src/process/`) that
intercepts meta-commands *before* the normal exit → intent → fallback
pipeline, so the original deterministic logic in `ResponseEngine` and
`IntentMatcher` is completely untouched — the upgrade is purely
additive.

---

## Example Session

```
==================================================
        RULE-BASED AI CHATBOT — LOGIC ENGINE
==================================================
  Deterministic. Explainable. Zero hallucinations.
  Type 'help' to see what I can do, or 'exit' to quit.
==================================================

You: HeLLo
Bot: Hi there! Welcome to the Logic Engine.
You: how are you
Bot: I'm running on deterministic logic - always consistent!
You: asdfgh
Bot: I do not understand.
You: EXIT
Bot: Goodbye! Have a great day.
Bot: Session ended. See you next time!
```

---

## Project Structure

```
chatbot_project/
├── assets/
│   └── banner.txt              Startup ASCII banner
├── docs/
│   ├── architecture.md         Full design doc (UML, sequence diagrams)
│   ├── requirements.md         Original specification analysis
│   └── roadmap.md              Milestone-by-milestone build plan
├── src/
│   ├── config/settings.py      AppConfig
│   ├── core/enums.py           MatchType, SessionState
│   ├── core/models.py          IntentMatch, ProcessResult, InteractionRecord
│   ├── knowledge/knowledge_base.py
│   ├── input/reader.py
│   ├── input/sanitizer.py
│   ├── process/exit_detector.py
│   ├── process/intent_matcher.py
│   ├── process/response_engine.py
│   ├── output/presenter.py
│   ├── output/banner.py
│   ├── session/chat_session.py
│   ├── session/interaction_logger.py
│   └── main.py                 Entry point (ChatBotApp)
├── tests/                      One test file per module
├── pyproject.toml
└── README.md
```

---

## Running the Tests

```bash
python3 -m pytest tests/ -v
```

54 unit tests cover every layer, including the required edge cases:
empty input, whitespace-only input, mixed-case input, exit-command
casing variants, partial/substring matches, special characters, and
very long input. No test depends on live keyboard input — the chat
loop is tested with a mocked input reader.

---

## Design Documents

This implementation was built from a three-phase specification
process, all preserved in `docs/`:

1. **`requirements.md`** — Functional/non-functional requirements,
   constraints, user stories, edge cases, and evaluation criteria.
2. **`architecture.md`** — Class design, module map, UML class
   diagram, sequence diagrams, and data flow.
3. **`roadmap.md`** — The milestone-by-milestone build order this
   code followed (M0 scaffold → M9 full test suite → M10 docs).

---

## Future Enhancements

These are explicitly **out of scope** for Project 1 (per the spec's
"suggested extensions" and the design's "future scalability" section)
but represent natural next steps:

- **Externalized knowledge base** — load intents from JSON/YAML
  instead of a hard-coded dict, so non-developers can edit responses.
- **Intent aliases** — map multiple phrasings (`hi`, `hey`, `yo`) to
  one canonical response without duplicating text.
- **Punctuation-aware sanitization** — strip trailing punctuation so
  `"hello!"` matches `"hello"`.
- **Partial / keyword-in-phrase matching** — handle `"hello there"`
  via token-based rules, still without machine learning.
- **Persistent logging** — write `InteractionRecord`s to a file or
  database instead of only in-memory, for cross-session audit trails.
- **Hybrid router (Project N+)** — when no rule matches, fall through
  to an LLM instead of a static fallback message, combining
  deterministic guardrails with generative AI.
- **Web/API interface** — wrap `ChatSession` behind a REST or
  WebSocket layer, reusing the process layer unchanged.

See `docs/architecture.md` Section 10 for the complete, categorized
roadmap of architectural evolution options.
