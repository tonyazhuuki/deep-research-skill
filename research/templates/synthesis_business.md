# Template: Business Synthesis «вывод первым» (company · marketing · macro/finance)

> Added 2026-10-22 after user feedback on a company decision-research: the 12-section v3.10
> synthesis_ru was correct but unreadable («пока дочитаешь до важного — умрёшь»):
> ~17 000 words, 150-word paragraphs with 6 facts each, the answer buried in §1 bullets.
> Fix = Minto pyramid / BLUF: answer → reasons → steps on the first screen, everything
> else one click below. Same idea as Our World in Data topic pages: overview first,
> details on demand.

## When to use

| Research | User-facing `synthesis_[lang].md` |
|---|---|
| **Decision-research in company / marketing / macro** (finance, partners, go/no-go, pricing, deals) | **THIS template** |
| «Понять поле / карта темы» in any domain | `synthesis_longread.md` (unchanged) |
| **Health — any type** | 12-section v3.10 (unchanged) |
| Consensus mode (`consensus_reference*.md`) | unchanged |

**The English `synthesis.md` stays 12-section v3.10.** FACT-CHECKER, ACTION MAPPER, CRITIC and
the other agents keep working on it. Only the reader's document changes shape.

## How it is produced (no content is ever dropped)

1. The full v3.10 translation goes to **`synthesis_[lang]_full.md`** (HUMANIZER, Frontier Radar,
   So What, Read-back — all as usual, applied to this file).
2. The ORCHESTRATOR writes the top layer **`_synthesis_[lang]_top.md`** itself, in one pass
   (structure below), with placeholders where the full text goes.
3. Assemble:
   ```bash
   python3 tools/research_pyramid_build.py <research_folder> --lang ru
   ```
   The tool writes `synthesis_[lang].md` and **refuses (exit 1, nothing written)** if any line of
   the full text is not placed, a placeholder is unknown or repeated, or the `> **Ответ.**` block
   is missing. Fix the top layer and rerun — never delete text to make it pass.

Placeholders: `{{5}}` — numbered section with subsections · `{{5^}}` — only its intro before the
first subsection · `{{So What}}` — unnumbered section by heading start · `{{^}}` — preamble under
the H1. Headings inside placeholders become bold lines (the side TOC shows only the pyramid).
A figure already shown in the top layer is not repeated below. `## Связанные файлы` is appended
automatically.

## Structure of the top layer

```markdown
# <Решение одной фразой: «X: партнёриться или нет»>

## 1. TL;DR — ответ и что делать          ← Telegram берёт весь этот раздел

> **Ответ.** 2–3 sentences: the decision + the one condition that changes it.

### Почему — три причины
1. **<Claim in bold, ≤12 words>.** 1–2 sentences with the deciding number.
2. …
3. …

### Что делать — по порядку
1. **<When/what>:** one action, one sentence why.
… (3–6 steps; first step = what can be done this week)

### <Цифры / Деньги> одной таблицей      ← optional: the numbers the decision rests on
| Вариант | Сколько | Подвох |

## <Вопрос читателя №1, e.g. «Можно ли им верить»>
**Вывод: <one sentence>.**
- **<Bold lead>:** up to 3 bullets, each with a number (conf X.XX, source)
![chart that answers this question](figures/…)   ← charts live up here, not in details

<details markdown="1">
<summary>Подробнее: <what is inside, in plain words></summary>

{{5.1}}

{{6.2}}

</details>

… 3–7 question sections …

## Frontier Radar
**Вывод: <one sentence>.**
<details markdown="1"><summary>Подробнее</summary>

{{Frontier Radar}}

</details>

---

<details markdown="1">
<summary>Приложение: исходный TL;DR, база доказательств, уверенность, глоссарий…</summary>

{{^}}

{{1}}

…every remaining section…

</details>
```

## Hard rules

1. **Sections are reader's questions, not report chapters.** «Можно ли им верить», «Что мне
   можно законно», «Сколько заработаю», «С кем ещё», «Что дальше» — not «Key Findings 5.3».
2. **First screen decides.** Ответ + причины + шаги must be enough to act without opening anything.
   Test: cover everything below the TL;DR — is the decision still clear?
3. **One sentence = one fact, ≤20 words.** No paragraph above 3 sentences in the top layer.
   Numbers go to a table when there are more than three of them.
4. **Every number in the top layer exists in the full text.** The top layer re-orders and compresses;
   it never introduces a figure, name or date that the full text does not contain.
5. **Confidence stays visible:** `(conf 0.85, source)` / `(уверенность 0.85, источник)` after a claim —
   the viewer moves it to the margin.
6. **Plain words.** Same rules as HUMANIZER: no internal codes (C14, DD-2, T3), no invented terms.
7. **Health is out of scope.** Health keeps the 12-section v3.10 even for business-like questions
   (supplement purchases, clinic choice).

## Read it

`tools/view <folder>/synthesis_ru.md` — side TOC lists the question sections, confidence goes
to the margin, «Подробнее» blocks open in place.
