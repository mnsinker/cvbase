# Portfolio Parser Test Cases

> Generated from `portfolio_parser_spec.md`
>
> Coverage: Metadata, Section, Subsection, Label, Content, Recursive Nesting, Rule Priority, Edge Cases

---

## Notation

Each test case includes:

- **Scenario** — what is being tested
- **Markdown Input** — the raw markdown fed to the parser
- **Expected Output** — the `{ section, subsection, metadata, blocks }` structure the parser should produce
- **Rationale** — why this behavior is expected

Where the spec is ambiguous, a note flags the uncertainty.

---

## 1. Metadata Rules

### 1.1 — Basic metadata extraction at subsection level

All three metadata keys present immediately after the H2 heading.

```markdown
# Project Alpha

## Overview

Career Spine: software engineer
Advanced Themes: distributed-systems
Excluded Visibility: draft

A paragraph about the project.
```

```json
{
  "section": "Project Alpha",
  "subsection": "Overview",
  "metadata": {
    "career_spine": ["software engineer"],
    "advanced_themes": ["distributed-systems"],
    "excluded_visibility": ["draft"]
  },
  "blocks": [
    {
      "label": "",
      "content": ["A paragraph about the project."]
    }
  ]
}
```

**Rationale:** All three metadata lines are detected by their prefix keys at subsection scope.  
⚠️ **Ambiguity:** The spec does not define how metadata *values* are formatted. Here we assume a single value follows the colon — but comma-separated lists, YAML-style sub-bullets, or space-delimited values are all possible interpretations.

---

### 1.2 — Metadata with multiple values (bullet-list format)

```markdown
# Project Alpha

## Overview

Career Spine:
- software engineer
- tech lead
Advanced Themes:
- distributed-systems
- ml
Excluded Visibility:
- draft

Some content here.
```

```json
{
  "section": "Project Alpha",
  "subsection": "Overview",
  "metadata": {
    "career_spine": ["software engineer", "tech lead"],
    "advanced_themes": ["distributed-systems", "ml"],
    "excluded_visibility": ["draft"]
  },
  "blocks": [
    {
      "label": "",
      "content": ["Some content here."]
    }
  ]
}
```

**Rationale:** Metadata values are lists. The most natural markdown list format follows the key on the next line.  
⚠️ **Ambiguity:** Are indented sub-bullets part of the list? Do blank lines terminate the metadata block?

---

### 1.3 — Metadata with comma-separated inline values

```markdown
## Overview

Career Spine: software engineer, tech lead
Advanced Themes: distributed-systems, ml
Excluded Visibility: draft

Content paragraph.
```

```json
{
  "section": "",
  "subsection": "Overview",
  "metadata": {
    "career_spine": ["software engineer", "tech lead"],
    "advanced_themes": ["distributed-systems", "ml"],
    "excluded_visibility": ["draft"]
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content paragraph."]
    }
  ]
}
```

**Rationale:** Inline comma-separated values are a reasonable interpretation of list values.  
⚠️ **Ambiguity:** The spec does not specify whether comma-separation IS valid, or whether values must be bullet-listed.

---

### 1.4 — No metadata present

```markdown
# Project Beta

## Details

Just a paragraph.

- bullet one
- bullet two
```

```json
{
  "section": "Project Beta",
  "subsection": "Details",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": [
        "Just a paragraph.",
        "bullet one",
        "bullet two"
      ]
    }
  ]
}
```

**Rationale:** Metadata is optional (required: no). When absent, each key defaults to an empty list.

---

### 1.5 — Partial metadata (only one key present)

```markdown
# Project Gamma

## Setup

Excluded Visibility: wip

Content.
```

```json
{
  "section": "Project Gamma",
  "subsection": "Setup",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": ["wip"]
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** Unspecified keys default to `[]`.

---

### 1.6 — Metadata key repeated

What is the parser's behavior when a metadata key appears twice?

```markdown
## Overview

Career Spine: software engineer
Career Spine: tech lead

Some text.
```

```json
{
  "section": "",
  "subsection": "Overview",
  "metadata": {
    "career_spine": ["software engineer", "tech lead"],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Some text."]
    }
  ]
}
```

**Candidate A — Append:** Values are appended into a single list.  
**Candidate B — Last wins:** Only the last value is kept.  
⚠️ **Ambiguity:** The spec does not describe handling of duplicate metadata keys.

---

### 1.7 — Metadata appearance — NOT at subsection level (top-level)

Metadata appears before any H2 heading.

```markdown
# Project Delta

Career Spine: senior

## Details

Content.
```

```json
{
  "section": "Project Delta",
  "subsection": "Details",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Candidate A — Ignored:** The metadata is silently dropped because it is not at subsection level.  
**Candidate B — Error / Attached to nearest subsection:** Raises an error or attaches to the next subsection.  
⚠️ **Ambiguity:** The constraint says "Metadata is only allowed at subsection level" but does not state the error-handling behavior when violated.

---

### 1.8 — Metadata after some content in the subsection

```markdown
## Overview

Some introductory text.

Career Spine: senior

More text.
```

```json
{
  "section": "",
  "subsection": "Overview",
  "metadata": {
    "career_spine": ["senior"],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Some introductory text.", "More text."]
    }
  ]
}
```

**Candidate A — Metadata still captured:** Metadata lines are detected regardless of position within the subsection, as long as they are under the H2.  
**Candidate B — Only at start of subsection:** Metadata is only detected when it appears immediately after the H2 heading.  
⚠️ **Ambiguity:** The spec says "Metadata is only allowed at subsection level" but not *where* within the subsection it may appear.

---

### 1.9 — Text that looks like metadata but uses wrong casing

```markdown
## Overview

career spine: senior
ADVANCED THEMES: security
Career_Spine: junior

Content.
```

```json
{
  "section": "",
  "subsection": "Overview",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "career spine",
      "content": ["Content."]
    }
  ]
}
```

**Candidate A — Case-sensitive match:** Only exact-case `Career Spine:`, `Advanced Themes:`, `Excluded Visibility:` are recognised.  
**Candidate B — Case-insensitive match:** Lowercase variants are accepted.  
⚠️ **Ambiguity:** The spec lists exact-case detection strings but does not state whether matching is case-sensitive.

---

## 2. Section / Subsection Rules

### 2.1 — Single H1, single H2

```markdown
# Problem Space

## Current Problem

Some text.
```

```json
{
  "section": "Problem Space",
  "subsection": "Current Problem",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Some text."]
    }
  ]
}
```

**Rationale:** Standard case. Section is the H1 text; subsection is the H2 text.

---

### 2.2 — Multiple H1 headings in one document

```markdown
# Section One

## Sub A

Text A.

# Section Two

## Sub B

Text B.
```

```json
{
  "section": "Section One",
  "subsection": "Sub A",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Text A."]
    }
  ]
}
```

**Candidate A — First section wins:** Only the first H1/subsection pair is parsed.  
**Candidate B — Error / Multiple outputs:** Raises an error or produces multiple portfolio entries.  
⚠️ **Ambiguity:** The spec defines a single `{ section, subsection, metadata, blocks }` output. Handling of multiple H1s is unspecified.

---

### 2.3 — No H1 heading (section missing)

Section is `required: yes`.

```markdown
## Orphan Subsection

Content.
```

```json
{
  "section": "",
  "subsection": "Orphan Subsection",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Candidate A — Empty string fallback:** Section defaults to `""`.  
**Candidate B — Error:** Parser raises an error because section is required.  
⚠️ **Ambiguity:** The spec marks section as required but does not define the fallback or error when it's absent.

---

### 2.4 — No H2 heading (subsection missing)

Subsection is `required: yes`.

```markdown
# Section Only

Content.
```

```json
{
  "section": "Section Only",
  "subsection": "",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Candidate A — Empty string fallback:** Subsection defaults to `""`.  
**Candidate B — Error:** Parser raises an error because subsection is required.  
⚠️ **Ambiguity:** Same as section — required field with no defined fallback when absent.

---

### 2.5 — H2 without preceding H1

```markdown
## Standalone Subsection

Content.
```

```json
{
  "section": "",
  "subsection": "Standalone Subsection",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** Section is empty string when no H1 is present; subsection is still populated.

---

### 2.6 — Content between H1 and H2

```markdown
# Problem Space

This is intro content between H1 and H2.

## Details

Actual section content.
```

```json
{
  "section": "Problem Space",
  "subsection": "Details",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Actual section content."]
    }
  ]
}
```

**Candidate A — Inter-H1/H2 content ignored:** Content between H1 and H2 is not part of any subsection, so it is dropped.  
**Candidate B — Attached before first subsection:** Content is attached to the subsection's blocks (pushed to top).  
⚠️ **Ambiguity:** The spec does not address content that falls between H1 and the first H2.

---

### 2.7 — Multiple H2s under one H1

```markdown
# Project

## Sub A

Content A.

## Sub B

Content B.
```

```json
{
  "section": "Project",
  "subsection": "Sub A",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content A."]
    }
  ]
}
```

**Candidate A — First subsection only:** Only the first H2 is captured.  
**Candidate B — Multiple output objects:** Parser returns one output per H2.  
⚠️ **Ambiguity:** The single-output contract suggests Candidate A, but the common use-case suggests Candidate B.

---

### 2.8 — H1 with trailing whitespace and special characters

```markdown
#   Problem Space (v2)  

## Setup

Content.
```

```json
{
  "section": "Problem Space (v2)",
  "subsection": "Setup",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** Heading text should be trimmed of leading/trailing whitespace. Special characters in headings are preserved.

---

## 3. Label / Content Rules

### 3.1 — Simple label with paragraph content

```markdown
## Test

Background:

This is the background information.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Background",
      "content": ["This is the background information."]
    }
  ]
}
```

**Rationale:** "Background:" ends with a colon → it is a label. The following paragraph is its content.

---

### 3.2 — Label with bullet list content

```markdown
## Test

Key Points:
- Point one
- Point two
- Point three
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Key Points",
      "content": [
        "Point one",
        "Point two",
        "Point three"
      ]
    }
  ]
}
```

**Rationale:** The bullet items under the label become content items.

---

### 3.3 — Label with mixed content (paragraph + bullets)

```markdown
## Test

Details:

A leading paragraph.

- bullet one
- bullet two
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Details",
      "content": [
        "A leading paragraph.",
        "bullet one",
        "bullet two"
      ]
    }
  ]
}
```

**Rationale:** All content under the label, regardless of type, is collected into the content list.

---

### 3.4 — Multiple consecutive labels

```markdown
## Test

Context:

First paragraph.

Requirements:

- Req A
- Req B

Notes:

Additional info.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Context",
      "content": ["First paragraph."]
    },
    {
      "label": "Requirements",
      "content": ["Req A", "Req B"]
    },
    {
      "label": "Notes",
      "content": ["Additional info."]
    }
  ]
}
```

**Rationale:** Each label starts a new block. Content belongs to the most recent label.

---

### 3.5 — Content without a preceding label

```markdown
## Test

This content has no label.

More content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": [
        "This content has no label.",
        "More content."
      ]
    }
  ]
}
```

**Rationale:** Content without a label gets an empty-string label.

---

### 3.6 — Label with no content (empty content list)

```markdown
## Test

Standalone Label:

Next Section Header
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Standalone Label",
      "content": []
    }
  ]
}
```

**Rationale:** A label with nothing between it and the next block (or end) has an empty content list.  
⚠️ **Note:** "Next Section Header" is not a subsection heading, so it cannot terminate content — it is ambiguous whether "Next Section Header:" could itself be a label.

---

### 3.7 — Text ending with colon that is NOT a label (metadata key)

```markdown
## Overview

Career Spine: senior

Content.
```

See Test 1.1 — `Career Spine:` is metadata, not a label, due to Rule Priority (Metadata > Label).

---

### 3.8 — Text ending with colon inside a paragraph

```markdown
## Test

According to the docs: this is an explanation. Note: it has multiple colons.

Content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": [
        "According to the docs: this is an explanation. Note: it has multiple colons.",
        "Content."
      ]
    }
  ]
}
```

**Candidate A — Only standalone lines ending with colon are labels:** A colon on its own line is a label; colons embedded in a paragraph are not.  
**Candidate B — Any line ending with colon is a label:** The line "According to the docs:" would be parsed as label "According to the docs", splitting the paragraph.  
⚠️ **Ambiguity:** The spec says "Text ending with ':'" for label detection, but does not clarify whether this means a standalone line or any occurrence.

---

### 3.9 — Colon as the only character on a line

```markdown
## Test

:

Content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Candidate A — Label with empty name:** `"label": ""` and `label` field is captured as empty string.  
**Candidate B — Not a valid label:** A single colon is ignored and treated as content.  
⚠️ **Ambiguity:** The spec does not define minimum label content.

---

### 3.10 — Indented paragraph as content

```markdown
## Test

Note:

  This is an indented paragraph.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Note",
      "content": ["This is an indented paragraph."]
    }
  ]
}
```

**Rationale:** Indented paragraphs are also content items (the spec lists "Indented paragraphs" under content detection).

---

### 3.11 — Label with same name appearing multiple times

```markdown
## Test

Note:

First note.

Note:

Second note.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Note",
      "content": ["First note."]
    },
    {
      "label": "Note",
      "content": ["Second note."]
    }
  ]
}
```

**Candidate A — Separate blocks:** Duplicate labels produce separate blocks.  
**Candidate B — Merged blocks:** Content is appended to the first matching block.  
⚠️ **Ambiguity:** The spec does not address duplicate labels.

---

### 3.12 — Content that looks like a URL or has special characters

```markdown
## Test

Links:

https://example.com
some@email.com
#hashtag
**bold text**
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Links",
      "content": [
        "https://example.com",
        "some@email.com",
        "#hashtag",
        "**bold text**"
      ]
    }
  ]
}
```

**Rationale:** Content items are raw text; inline markdown formatting is carried verbatim into the content string.

---

### 3.13 — Empty content list after non-label text ending with colon

```markdown
## Test

Version:

Content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Version",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** "Version:" ends with a colon → it is a label. Subsequent text is its content.

---

## 4. Recursive / Nested Block Rules

### 4.1 — Basic nested label (one level)

```markdown
## Test

Section A:

Sub-item A1:

Content under sub-item.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Section A",
      "content": [
        {
          "label": "Sub-item A1",
          "content": ["Content under sub-item."]
        }
      ]
    }
  ]
}
```

**Rationale:** "Nested labels become nested blocks." A label encountered while another label is active becomes a block inside the parent block's content.

---

### 4.2 — Deep nesting (three levels)

```markdown
## Test

Level 1:

Level 2:

Level 3:

Deep content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Level 1",
      "content": [
        {
          "label": "Level 2",
          "content": [
            {
              "label": "Level 3",
              "content": ["Deep content."]
            }
          ]
        }
      ]
    }
  ]
}
```

**Rationale:** Each new label creates a nested block one level deeper.  
⚠️ **Ambiguity:** What triggers nesting depth? Indentation? Sequential labels? The spec says "nested labels become nested blocks" but does not define the nesting *mechanism*.

---

### 4.3 — Nesting with mixed content and labels

```markdown
## Test

Project:

A project overview.

Phase 1:

First phase tasks.

Phase 2:

Second phase tasks.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Project",
      "content": [
        "A project overview.",
        {
          "label": "Phase 1",
          "content": ["First phase tasks."]
        },
        {
          "label": "Phase 2",
          "content": ["Second phase tasks."]
        }
      ]
    }
  ]
}
```

**Rationale:** A parent label's content array mixes text items and nested block objects.

---

### 4.4 — Two peer labels with nested children

```markdown
## Test

Parent A:

Child A1:

A1 content.

Parent B:

Child B1:

B1 content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Parent A",
      "content": [
        {
          "label": "Child A1",
          "content": ["A1 content."]
        }
      ]
    },
    {
      "label": "Parent B",
      "content": [
        {
          "label": "Child B1",
          "content": ["B1 content."]
        }
      ]
    }
  ]
}
```

**Rationale:** A sibling label at the same nesting level closes the previous parent and starts a new one.  
⚠️ **Ambiguity:** How does the parser know when to close a parent? Does the nesting level reset to 1 when "Parent B:" is seen?

---

### 4.5 — Indentation-driven nesting

```markdown
## Test

Parent:
    Child:
        Grandchild:

Deep content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Parent",
      "content": [
        {
          "label": "Child",
          "content": [
            {
              "label": "Grandchild",
              "content": ["Deep content."]
            }
          ]
        }
      ]
    }
  ]
}
```

**Candidate A — Indentation drives nesting:** Nesting depth is determined by leading whitespace.  
**Candidate B — Sequential labels drive nesting:** Every new label encountered while inside a block is nested, regardless of indentation.  
⚠️ **Ambiguity:** The spec does not clarify what determines nesting depth — indentation or sequential position. "Indented paragraphs" are listed as a content type, but "indented labels" are not discussed for nesting.

---

## 5. Rule Priority

### 5.1 — Metadata > Label (same line, matching metadata key at subsection level)

```markdown
## Overview

Career Spine: senior
```

**Result:** Metadata key, detected as metadata (not label). See 1.1.

---

### 5.2 — Metadata > Label (matching key NOT at subsection level)

```markdown
# Project

Career Spine: senior

## Overview
```

**Result:** In this position `Career Spine:` is NOT at subsection level. Two interpretations:
- If "not at subsection level" means metadata is entirely ignored, can it become a label?
- The spec says Metadata > Label but also says metadata is only allowed at subsection level.

⚠️ **Ambiguity:** If metadata is ignored because it is not at subsection level, does the line then fall through to become a label?

---

### 5.3 — Section > Label (H1 text ending with colon)

```markdown
# Project:

## Details

Content.
```

```json
{
  "section": "Project:",
  "subsection": "Details",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Candidate A — H1 always wins:** `# Project:` is an H1 heading; it is always parsed as a section. The colon is part of the section name.  
**Candidate B — Label detection overrides when rule priority says Section > Label:** This is correct because Section rule has higher priority than Label.  
⚠️ **Note:** The spec says Section > Label in priority, so Candidate A is correct — but it's an edge case worth testing.

---

### 5.4 — Subsection > Label (H2 text ending with colon)

```markdown
# Project

## Overview:

Content.
```

```json
{
  "section": "Project",
  "subsection": "Overview:",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** Subsection > Label in priority. The colon is part of the subsection name.

---

## 6. Edge Cases

### 6.1 — Empty document

```markdown

```

```json
{
  "section": "",
  "subsection": "",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": []
}
```

**Rationale:** An empty document produces empty defaults.

---

### 6.2 — Only whitespace

```markdown
   
   
   
```

```json
{
  "section": "",
  "subsection": "",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": []
}
```

**Rationale:** Whitespace-only content is equivalent to empty.

---

### 6.3 — Only metadata, no content blocks

```markdown
# Project

## Overview

Career Spine: senior
Advanced Themes: security
```

```json
{
  "section": "Project",
  "subsection": "Overview",
  "metadata": {
    "career_spine": ["senior"],
    "advanced_themes": ["security"],
    "excluded_visibility": []
  },
  "blocks": []
}
```

**Rationale:** Metadata is captured. With no label or content lines, blocks is an empty list.

---

### 6.4 — Horizontal rule (`---`)

```markdown
## Test

Before.

---

After.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Before.", "After."]
    }
  ]
}
```

**Candidate A — HR is ignored (not a block):** Horizontal rules are skipped during parsing.  
**Candidate B — HR terminates current label's content:** Acts as a separator.  
⚠️ **Ambiguity:** The spec does not address thematic breaks (HRs).

---

### 6.5 — Fenced code block

```markdown
## Test

Code:

```
def hello():
    print("world")
```
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Code",
      "content": [
        "def hello():",
        "    print(\"world\")"
      ]
    }
  ]
}
```

**Candidate A — Code fenced content is treated as paragraphs:** Each line inside backticks is a content item.  
**Candidate B — Code block is a single content item:** The entire fenced block is one string (with internal newlines).  
⚠️ **Ambiguity:** The spec does not address fenced code blocks.

---

### 6.6 — Multi-line indented content

```markdown
## Test

Note:
    First indented paragraph.

    Second indented paragraph (separated by blank line).
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Note",
      "content": [
        "First indented paragraph.",
        "Second indented paragraph (separated by blank line)."
      ]
    }
  ]
}
```

**Rationale:** Blank-line-separated indented paragraphs are distinct content items.

---

### 6.7 — Unicode and special characters in content

```markdown
## Test

Symbols:

© 2025 — All rights reserved
Café résumé ñoño
π ≈ 3.14159
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Symbols",
      "content": [
        "© 2025 — All rights reserved",
        "Café résumé ñoño",
        "π ≈ 3.14159"
      ]
    }
  ]
}
```

**Rationale:** Unicode characters are preserved verbatim.

---

### 6.8 — Line starting with a single colon not matching label pattern

```markdown
## Test

:not a label

Content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": [
        ":not a label",
        "Content."
      ]
    }
  ]
}
```

**Rationale:** `:not a label` does not end with a colon (the colon is at the start), so it is not a label. It is content.  
⚠️ **Edge case for detection logic:** The detection pattern `text ending with ":"` must ensure the colon is at the end, not the start.

---

### 6.9 — Unrecognised metadata key (extra text looking like metadata)

```markdown
## Overview

Random Key: value

Content.
```

```json
{
  "section": "",
  "subsection": "Overview",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Random Key",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** "Random Key:" is not one of the three recognised metadata keys. It falls through to label detection.

---

### 6.10 — Bullet list without preceding label

```markdown
## Test

- Item one
- Item two
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Item one", "Item two"]
    }
  ]
}
```

**Rationale:** Content without a label → `"label": ""`.

---

### 6.11 — Tab indentation vs space indentation

```markdown
## Test

List:
	Tab-indented paragraph.
    Four-space indented paragraph.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "List",
      "content": [
        "Tab-indented paragraph.",
        "Four-space indented paragraph."
      ]
    }
  ]
}
```

**Rationale:** Both tabs and spaces are acceptable indentation for indented paragraphs.  
⚠️ **Ambiguity:** Mixed indentation types may cause inconsistent nesting depth detection.

---

### 6.12 — Overly long label name

```markdown
## Test

A label that is intentionally extremely long and goes well beyond typical line length limits to test buffer handling and string capacity:

Content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "A label that is intentionally extremely long and goes well beyond typical line length limits to test buffer handling and string capacity",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** Long labels are captured in full.

---

### 6.13 — HTML comments in markdown

```markdown
## Test

<!-- This is a comment -->

Visible content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Visible content."]
    }
  ]
}
```

**Candidate A — HTML comments are stripped:** Comments are removed before parsing.  
**Candidate B — HTML comments become content items:** They are treated as paragraph content.  
⚠️ **Ambiguity:** The spec does not address HTML comments.

---

### 6.14 — Link syntax in content

```markdown
## Test

Links:

[Example](https://example.com)
[Reference-style][ref]
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "Links",
      "content": [
        "[Example](https://example.com)",
        "[Reference-style][ref]"
      ]
    }
  ]
}
```

**Rationale:** Markdown link syntax is carried verbatim.

---

### 6.15 — Very deeply nested labels (stack limit test)

```markdown
## Test

L1:
L2:
L3:
L4:
L5:
L6:
L7:
L8:
L9:
L10:

Bottom content.
```

```json
{
  "section": "",
  "subsection": "Test",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "L1",
      "content": [
        {
          "label": "L2",
          "content": [
            {
              "label": "L3",
              "content": [
                {
                  "label": "L4",
                  "content": [
                    {
                      "label": "L5",
                      "content": [
                        {
                          "label": "L6",
                          "content": [
                            {
                              "label": "L7",
                              "content": [
                                {
                                  "label": "L8",
                                  "content": [
                                    {
                                      "label": "L9",
                                      "content": [
                                        {
                                          "label": "L10",
                                          "content": ["Bottom content."]
                                        }
                                      ]
                                    }
                                  ]
                                }
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Rationale:** Deeply nested labels produce deeply nested blocks. Implementation should guard against stack overflow with a recursion limit.  
⚠️ **Missing rule:** The spec should define a maximum nesting depth.

---

## 7. Ambiguous / Conflict Test Cases

### 7.1 — Metadata key text used as content text at top level

```markdown
# Career Spine

## Overview

Content.
```

```json
{
  "section": "Career Spine",
  "subsection": "Overview",
  "metadata": {
    "career_spine": [],
    "advanced_themes": [],
    "excluded_visibility": []
  },
  "blocks": [
    {
      "label": "",
      "content": ["Content."]
    }
  ]
}
```

**Rationale:** "Career Spine" as H1 text is a section heading, not metadata. No ambiguity — Section > Metadata in priority.  
⚠️ **Edge case for UX:** A user might reasonably expect `# Career Spine` to set metadata, but the spec says only the exact string `Career Spine:` (with colon) triggers metadata detection, and only at subsection level.

---

### 7.2 — Text that is both a valid label AND looks like metadata (wrong level)

```markdown
# Project

Career Spine: senior is the central theme

## Overview

Content.
```

**Question:** Is "Career Spine: senior is the central theme" a metadata line (ignored because not at subsection level) or a label?

⚠️ **Conflict:** The spec says metadata detection is "Career Spine:" — exact match? Starts-with? The example value `senior` suggests the format `Key: value`. But if the line is `Career Spine: senior is the central theme`, does the trailing text after "senior" matter? Is it a single metadata value, or not metadata at all because it doesn't match a simple pattern?

---

### 7.3 — Metadata value that looks like a colon-terminated label

```markdown
## Overview

Career Spine:
- senior
- tech lead

Another label:

Content.
```

**Question:** Is `Career Spine:` a metadata key (with bullet-list values) or a label?

The spec says Metadata > Label at subsection level, so it should be metadata. But if metadata matching is exact string match (`"Career Spine:"`), then the line uniquely identifies as metadata.

---

### 7.4 — Content followed by metadata in same subsection

```markdown
## Overview

Some content paragraph.

Career Spine: senior

More content.
```

See 1.8 — Spec does not clarify whether metadata must appear before any content.

---

## Spec Improvement Suggestions

### A. Unclear Rules

| ID | Rule | Issue |
|---|---|---|
| A1 | Metadata value format | The spec shows metadata as `list[string]` with an empty-list default, but does not specify how values are written in markdown. Are they comma-separated inline (`Career Spine: a, b`)? Bullet-listed on following lines? Space-delimited? A single example is needed. |
| A2 | Label detection: standalone vs embedded | "Text ending with ':'" could mean any line whose last character is a colon (e.g., `According to the docs: this is an explanation.` would be split). Clarify that label detection only applies to *standalone lines* (not embedded in paragraphs). |
| A3 | Nesting mechanism | "Nested labels become nested blocks" does not explain *how* nesting works. Is it indentation-driven? Sequential proximity? Does every new label after another label automatically nest? Must nesting be explicitly indicated via whitespace? |
| A4 | Indentation unit | "Indented paragraphs" are a content type but the spec does not define the indentation unit (2 spaces? 4 spaces? tabs? any? mixed?). How does indentation interact with nesting depth? |
| A5 | Bullet detection | The spec lists "Bullets" as content but does not specify supported bullet characters (`-`, `*`, `+`, numbered `1.`). |
| A6 | Paragraph boundary | The term "Paragraphs" is not defined. Is a paragraph a single line, or text separated by blank lines? |
| A7 | Metadata key matching | Is metadata key detection an exact string match (e.g., `Career Spine:` only) or a prefix/starts-with match? What about case sensitivity? |
| A8 | Content item termination | What *ends* a content collection under a label? Another label? A heading? The end of the subsection? A blank line? |

### B. Conflicts / Contradictions

| ID | Conflict | Explanation |
|---|---|---|
| B1 | Metadata priority outside subsection | Rule Priority says Metadata > Label. Constraint says metadata "only allowed at subsection level". If metadata text appears *outside* subsection level, does the line fall through to become a label (Metadata rule doesn't apply), or is Metadata > Label still in effect (line is ignored as invalid metadata)? These two rules contradict each other for lines matched by metadata keys but not at subsection level. |
| B2 | Section is required, but no fallback defined | The spec says `section` is `required: yes` but does not define what happens when no H1 exists. Same for `subsection`. Both need explicit fallback (empty string? error?). |
| B3 | Single output contract vs. multiple H2s | The output contract shows a single `{ section, subsection, metadata, blocks }` object, but a realistic portfolio document may have multiple H2 subsections. The spec does not address whether the parser processes only the first subsection, returns multiple objects, or merges them. |

### C. Missing Rules

| ID | Missing Rule | Why Needed |
|---|---|---|
| C1 | Maximum recursion / nesting depth | Without a defined limit, deeply nested labels could cause stack overflow in implementation. |
| C2 | Empty document behavior | What should the parser produce for an empty markdown document? |
| C3 | Unknown markdown features | Spec says nothing about: fenced code blocks, HTML comments, horizontal rules (`---`), blockquotes (`>`), tables, images, or inline HTML. Should these be ignored, treated as content, or raise errors? |
| C4 | Duplicate metadata keys | Not addressed. Should the last value win, values be appended, or duplicate keys cause an error? |
| C5 | Duplicate labels | Not addressed. Should identical labels merge content or create separate blocks? |
| C6 | Content between H1 and first H2 | Not addressed. Should it be dropped, attached to the first subsection, or attached to all subsections? |
| C7 | Whitespace handling | Not addressed. Should heading text and content be trimmed? Are blank lines between blocks significant? |
| C8 | Metadata position within subsection | Not addressed. Must metadata appear immediately after the H2 heading, or can it appear anywhere within the subsection? |
| C9 | Content types: granularity | The three content detection types (paragraphs, bullets, indented paragraphs) are vague. What counts as one "paragraph"? Is a blank line the delimiter? What about a single word followed by a newline? |
| C10 | Error handling philosophy | The spec never mentions error states. What happens with malformed input? Does the parser silently recover, raise exceptions, or produce best-effort output? A set of invariants ("parser never crashes", "parser always returns valid JSON") would guide implementation. |
