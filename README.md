
# 🔮 Lenormand LLM Reader
*A structured, narrative-driven Lenormand reading system powered by GPT-based LLMs.*

This project transforms Lenormand card readings into a consistent, interpretable,
and emotionally supportive LLM-powered experience.  
It combines traditional Lenormand logic with modern prompt engineering,
structured outputs, and a modular architecture suitable for future expansion.

---

# 1. Overview

The Lenormand LLM Reader provides:

- Structured multi-card narrative readings  
- Fast single-card YES/NO/MAYBE decisions  
- Bilingual output (EN → KO)  
- Traditional Lenormand techniques (center/mirror/chain) baked into the prompt  
- A modular system that can extend into memory-enabled or persona-driven agents  

This project was initially designed for personal use (Korean UX),  
but the architecture supports multilingual deployment and further productization.

---

# 2. User-facing Service Flow

## 2.1 Multi-card Reading Flow

1. User opens `/reading`
2. Inputs a question (Korean)
3. Selects:
   - category (optional)
   - spread type (PPF, SOA, 3×3, Grand Tableau, etc.)
4. Frontend sends `POST /api/reading`
5. Backend:
   - loads card/spread JSON
   - samples cards
   - builds structured LLM prompt (EN)
   - receives structured JSON reading (EN)
   - converts to Korean
6. Frontend renders:
   - card layout
   - summary / narrative / actions

## 2.2 Single-card YES/NO Flow

1. User enters short question  
2. One card is drawn  
3. System applies YES/NO/MAYBE mapping  
4. Optional LLM explanation  
5. UI shows verdict + short guidance  

## 2.3 Hybrid (Human-in-the-loop) Concept

The system allows human readers to augment LLM outputs via:

- personalized notes  
- interpretation preferences  
- tone/style guidelines  

This can be incorporated through lightweight RAG.

---

# 3. User Flow Diagrams (Mermaid)

## 3.1 Multi-card Reading

```mermaid
flowchart TD
    U[User] -->|Question + Spread| UI[Frontend UI]
    UI -->|POST /api/reading| BE[Backend]

    subgraph S[Backend Processing]
        BE --> CFG[Load cards.json + spreads.json]
        CFG --> DRAW[Sample & shuffle cards]
        DRAW --> PROMPT[Build LLM Prompt]
        PROMPT --> LLM[(LLM)]
        LLM --> EN[English Reading JSON]
        EN --> KO[Korean Translation]
        KO --> RESP[Response JSON]
    end

    RESP --> UI_RENDER[Render Spread + Reading]
    UI_RENDER --> U_R[User Reads Output]
````

## 3.2 Single-card Quick Mode

```mermaid
flowchart TD
    U[User] --> UI[Frontend]
    UI --> BE[Backend API]

    BE --> DRAW[Draw 1 card]
    DRAW --> RULE[YES / NO / MAYBE mapping]

    RULE --> LLM[(LLM – optional)]
    LLM --> TEXT[Short advice]
    RULE --> TEXT

    TEXT --> RESP[Response JSON]
    RESP --> UI_RENDER[Display result]
```

---

# 4. Prompt Design Overview

## 4.1 Card Context Layer

LLM receives structured card data:

```
Position: Card – Short meaning
```

Example:

```
Past: Sun – Success, clarity
Present: Clouds – Doubts
Future: Anchor – Stability
```

## 4.2 Reading Modes

* **Narrative mode** → full multi-card interpretation
* **YES/NO mode** → verdict + short explanation + 3 action items

## 4.3 Lenormand Rule Embedding

The prompt integrates:

* Center card emphasis
* Mirroring pairs
* Chaining (adjacent interactions)

This ensures *relational* interpretation vs. dictionary-style output.

## 4.4 Structured JSON Output

```json
{
  "summary_en": "...",
  "overall_story_en": "...",
  "action_items_en": ["...", "...", "..."]
}
```

## 4.5 Language Handling

* LLM always outputs **EN JSON**
* A separate layer translates to **KO**
* Translation can be turned off for EN-only mode
* UI can add a language toggle with minimal changes

---

# 5. System Architecture

## 5.1 High-level Pipeline

```
User → UI → Backend → LLM → Translation (optional) → UI
```

## 5.2 Component Diagram

```
Frontend (Next.js)
    ↓
Backend (FastAPI)
    - Load cards/spreads
    - Sample cards
    - Build prompt
    - Call LLM
    - Parse JSON
    - Translate (optional)
    ↓
Frontend Rendering
```

Full diagram provided in the architecture section.

## 5.3 Technology Choices

* **Next.js** for UI
* **FastAPI** for backend
* **OpenAI LLMs** for reasoning
* **Static JSON** for card/spread definitions
* **Optional translation layer**

## 5.4 Extensibility

* Multilingual
* Model-swappable
* Persona layers
* RAG integration
* Interactive/streaming agent support

---

# 6. Differentiation & Value Proposition

## 6.1 Structured Reasoning

No random LLM text — consistent, reproducible interpretation grounded in spread logic.

## 6.2 Dual-Mode Experience

Fast single-card vs. deep multi-card storytelling.

## 6.3 Modular Architecture

Card/spread data is external; LLM logic isolated; translation optional.

## 6.4 Multilingual-Ready

EN-first reasoning with KO projection; scalable to JP/CN/others.

## 6.5 Human-in-the-Loop Support

Reader notes or style guidelines can shape model output via RAG.

## 6.6 Safe & Supportive Output

Tone avoids fatalistic or harmful statements.

---

# 7. Demo

(Add screenshots of:

* spread UI
* card display
* sample reading EN/KO
  )

Example fields returned:

```json
{
  "summary_en": "...",
  "summary_ko": "...",
  "overall_story_ko": "...",
  "cards": [...]
}
```

---

# 8. Next Steps & Future Expansion

## 8.1 Integration with AURA (Memory / Knowledge Layer)

AURA is a complementary project providing:

* user/session memory
* RAG-based knowledge retrieval
* persistent persona/world data

Connecting AURA would enable:

* personalized readings
* style consistency
* historical context awareness

Transforming the system into a **memory-enabled AI companion.**

---

## 8.2 VTuber Persona Layer (Character Interaction)

Another related project implements a real-time AI persona layer for VTubing.

Linking it to the reasoning engine enables:

* character-driven readings
* emotional tone control
* live stream interactions
* performative AI agents

---

## 8.3 Toward a Unified AI Agent Framework

```
Reasoning Engine (Lenormand Reader)
+ Memory Layer (AURA)
+ Persona Layer (VTuber AI)
```

This forms the foundation for:

* storytelling agents
* emotionally aware companions
* interactive guidance systems
* creator tools

---

# 9. Repository Structure

```
lenormand-llm-reader/
├── backend/
│   ├── main.py
│   ├── llm_client.py
│   ├── translation_client.py
│   └── data/
│       ├── cards.json
│       └── spreads.json
├── frontend/
│   └── pages/reading.tsx
├── README.md
```

---

# 10. License

MIT (or update depending on your preference)
