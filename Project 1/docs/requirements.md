# DecodeLabs AI Internship � Project 1 Specification Analysis

**Source:** `Artificial intelligence P1.pdf` (Industrial Training Kit, Batch 2026)

---

## 1. Project Objective

Build a **Rule-Based AI Chatbot** � a deterministic "logic engine" that simulates basic human conversation through explicit programmatic rules, not machine learning.

The project is the **foundation milestone** of the DecodeLabs Artificial Intelligence track. Its purpose is to prove you can design a continuous **Input ? Process ? Output (IPO)** loop that:

- Accepts user text
- Applies transparent, hard-coded decision logic
- Returns predictable, explainable responses

Conceptually, this chatbot represents the **deterministic control layer** ("guardrails") that sits beneath probabilistic AI systems. Before building models that learn or generate unpredictably, you must master **control flow, logic, and structured response mapping**.

Completing Project 1 is **mandatory** to unlock subsequent weekly projects and to earn program verification.

---

## 2. Functional Requirements

### Core goal (explicit)

Create a simple rule-based chatbot that responds to **predefined user inputs**.

### Mandatory logic skeleton (Project 1 Specification slide)

| # | Requirement | Description |
|---|-------------|-------------|
| FR-1 | **Input loop** | Run a continuous `while` loop so the chatbot stays active and repeatedly accepts input. |
| FR-2 | **Sanitization** | Normalize user input (e.g., lowercase + strip whitespace) so casing/spacing variations still match intents. |
| FR-3 | **Knowledge base** | Store **at least 5 intents** in a dictionary mapping user inputs to bot responses. |
| FR-4 | **Fallback** | Return a default response when input does not match any known intent. |
| FR-5 | **Exit strategy** | Support a specific exit command that cleanly breaks the loop and ends the program. |

### Additional stated requirements (summary slide)

| # | Requirement |
|---|-------------|
| FR-6 | Handle **greeting** commands (e.g., hello, hi). |
| FR-7 | Handle **exit** commands. |
| FR-8 | Use **conditional logic** for response selection (if-else or equivalent decision structure). |
| FR-9 | Operate in a **continuous interaction loop**. |

### Recommended implementation pattern (teaching slides)

| # | Requirement |
|---|-------------|
| FR-10 | Prefer **dictionary lookup** (e.g., `responses.get(user_input, fallback)`) over long if-elif chains. |
| FR-11 | Combine lookup + fallback in one atomic operation via `.get()`. |
| FR-12 | Follow the **IPO model**: Input (sanitize) ? Process (intent match) ? Output (generate/display response). |

### Suggested extensions (conclusion slide � not strictly mandatory)

- Expand the bot's vocabulary
- Add nested conditions for smarter routing
- Give the bot a distinct personality

---

## 3. Non-Functional Requirements

| # | Category | Requirement |
|---|----------|-------------|
| NFR-1 | **Determinism** | Same input must always produce the same output. No probabilistic or generative behavior. |
| NFR-2 | **Explainability ("white box")** | Logic must be traceable: Input ? Logic ? Output with no hidden reasoning. |
| NFR-3 | **Safety** | Zero hallucination risk; responses are fully hard-coded. |
| NFR-4 | **Reliability** | Unknown inputs must not crash the program; fallback must always handle them. |
| NFR-5 | **Efficiency awareness** | Intent matching should aim for **O(1)** dictionary lookup rather than **O(n)** linear if-elif scanning at scale. |
| NFR-6 | **Maintainability** | Code should be structured and scalable (avoid fragile "if-elif ladder" anti-patterns). |
| NFR-7 | **Quality** | Submission must meet DecodeLabs verification standards. |
| NFR-8 | **Usability** | Terminal-based interaction should feel continuous and intentional until the user exits. |
| NFR-9 | **Educational clarity** | Implementation should demonstrate foundational AI engineering concepts, not just "make it run." |

---

## 4. Constraints

| Constraint | Detail |
|------------|--------|
| **Technology scope** | Rule-based logic only; **no deep learning / LLM integration** required for Project 1 itself. |
| **Minimum knowledge base size** | At least **5 intents** in the response dictionary. |
| **Interaction model** | Command-line / terminal loop (not a web or GUI app in the core spec). |
| **Program flow** | Must use a persistent loop with an explicit break/exit condition. |
| **Input handling** | Must sanitize/normalize raw user text before matching. |
| **Program gating** | Project 1 must be completed and verified before other projects unlock. |
| **Cohort** | DecodeLabs AI Internship, Batch 2026. |
| **Conceptual boundary** | Hybrid LLM architecture (rule match ? else pass to LLM) is **future context**, not the deliverable for this milestone. |

---

## 5. Inputs

| Input | Description |
|-------|-------------|
| **Raw user text** | Strings entered by the user during each loop iteration (e.g., via `input()`). |
| **Intent keywords** | Predefined keys in the knowledge base (minimum 5), such as greetings, farewells, help, etc. |
| **Exit command** | A specific keyword/command that terminates the session (e.g., `exit`). |
| **Noisy text variants** | Inputs with inconsistent casing, extra spaces, or minor formatting differences � handled via sanitization. |

**Example input flow:**

```
HeLLo   ? sanitized ? hello ? matched intent
unknown ? sanitized ? unknown ? fallback response
exit    ? sanitized ? exit    ? loop termination
```

---

## 6. Outputs

| Output | Description |
|--------|-------------|
| **Matched responses** | Predefined reply strings returned when user input matches a dictionary key/intent. |
| **Fallback response** | Default message when no intent matches (e.g., "I do not understand."). |
| **Session termination** | Clean program exit when the exit command is received. |
| **Continuous feedback loop** | Repeated prompt/response cycles until exit. |

**Example outputs:**

- `hello` ? `"Hi there!"`
- `bye` ? `"Goodbye!"`
- `asdfgh` ? `"I do not understand."`
- `exit` ? program ends

---

## 7. User Stories

### Primary user: Intern / developer

| ID | Story |
|----|-------|
| US-1 | As an intern, I want to build a terminal chatbot so I can practice foundational AI logic before advanced ML topics. |
| US-2 | As a developer, I want a continuous input loop so users can have an ongoing conversation until they choose to leave. |
| US-3 | As a developer, I want to sanitize input so `"Hello"`, `" hello "`, and `"HELLO"` behave consistently. |
| US-4 | As a developer, I want a dictionary of intents so adding new responses is simple and maintainable. |
| US-5 | As a developer, I want a fallback response so the bot never fails silently on unknown input. |
| US-6 | As a developer, I want an exit command so the session ends predictably and cleanly. |

### End user: Person chatting in the terminal

| ID | Story |
|----|-------|
| US-7 | As a user, I want to greet the bot and receive a friendly predefined reply. |
| US-8 | As a user, I want to ask simple supported questions/commands and get immediate answers. |
| US-9 | As a user, I want a clear message when the bot doesn't understand my input. |
| US-10 | As a user, I want to type an exit command when I'm done chatting. |

### Program / evaluator

| ID | Story |
|----|-------|
| US-11 | As an evaluator, I want deterministic behavior so outputs are consistent and verifiable. |
| US-12 | As an evaluator, I want traceable logic so I can confirm the bot follows IPO architecture. |

---

## 8. Edge Cases

| Edge case | Expected behavior |
|-----------|---------------------|
| **Empty input** (`""` or whitespace only after strip) | Should not crash; likely no match ? fallback (or treat as empty intent if defined). |
| **Unknown input** | Return fallback response; continue loop. |
| **Case variations** (`"HeLLo"`, `"HELLO"`) | Sanitization should normalize to match greeting intents. |
| **Leading/trailing spaces** | Stripped before matching. |
| **Exit command with different casing** (`"EXIT"`, `"Exit"`) | Should work if sanitization lowercases input and exit key is lowercase. |
| **Exit synonyms** (`"bye"`, `"quit"`) | Only work if explicitly mapped in the knowledge base or exit logic; otherwise treated as normal/fallback input. |
| **Partial matches** (`"hello there"`) | Exact key lookup will **not** match `"hello"` unless substring/multi-word logic is added (out of base spec). |
| **Punctuation attached** (`"hello!"`) | Will likely miss exact match unless sanitization removes punctuation. |
| **Very long input** | Should not crash; falls through to fallback unless explicitly handled. |
| **Special/control characters** | Should be handled safely without breaking the loop. |
| **Repeated exit attempts after break** | N/A � program should already have terminated. |
| **Duplicate keys in dictionary** | Last value wins in Python; avoid duplicates in design. |
| **Only 4 intents defined** | Fails minimum requirement of 5+. |

---

## 9. Evaluation Criteria

### Gate criteria (qualification slide)

- Project 1 is **completed**
- Work passes **DecodeLabs quality verification**
- Completion **unlocks** next week's projects

### Functional checklist (logic skeleton)

| Criterion | Pass condition |
|-----------|----------------|
| Continuous loop | Bot runs until user exits |
| Sanitization | Input normalized before matching |
| Knowledge base | ? 5 intent/response pairs |
| Greeting handling | At least one greeting intent works |
| Exit handling | Dedicated exit command terminates cleanly |
| Fallback | Unknown input returns default message |
| Decision logic | Responses chosen via rules/conditionals or dictionary mapping |
| Determinism | Same input ? same output every time |

### Quality signals (program standards)

- Clean, readable structure aligned with IPO model
- Avoidance of fragile long if-elif chains where dictionary lookup is appropriate
- Evidence of intentional design (not a one-off script)
- Optional bonus: expanded vocabulary, nested logic, personality, logging, OOP structure

### Conceptual understanding (implicit)

- Can explain **deterministic vs probabilistic AI**
- Can explain why rule-based systems are **transparent and safe**
- Understands dictionary lookup as an efficient intent-matching strategy

---

## 10. Skills Being Tested

| Skill area | What the project assesses |
|------------|---------------------------|
| **Control flow** | `while` loops, `break`, conditional branching |
| **Decision-making logic** | Mapping inputs to outputs via rules |
| **Basic AI concepts** | Rule-based systems, intents, deterministic behavior, IPO architecture |
| **Input processing** | Sanitization and normalization |
| **Data structures** | Python dictionaries / hash-map intent lookup |
| **Algorithmic thinking** | O(1) vs O(n) tradeoffs; avoiding if-elif anti-patterns |
| **Software design** | Modular Input ? Process ? Output separation |
| **Error/unknown handling** | Graceful fallback instead of crashes |
| **Explainable AI mindset** | Building "white box" systems with traceable logic |
| **Professional engineering habits** | Maintainable code, quality-ready submission, portfolio thinking |
| **Systems thinking (contextual)** | Understanding guardrails, compliance, and hybrid AI architectures as future direction |

---

## Summary

Project 1 is not about building a smart AI � it is about building a **reliable logic skeleton**: a terminal chatbot that loops continuously, sanitizes input, matches intents from a dictionary of at least five predefined responses, falls back gracefully on unknown input, and exits cleanly on command. Success means demonstrating **control, clarity, and deterministic design** � the foundation for everything that follows in the DecodeLabs AI track.

---

*Analysis based on `Artificial intelligence P1.pdf` in the project workspace.*
