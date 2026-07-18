# Purpose

Convert canonical project markdown content
into Portfolio JSON.

---

# Part 1 — Source Normalization

Normalize source markdown into canonical project content.

## Rule 1 Formatting Repair
Normalization may repair
- list formatting
- paragraph formatting

Examples:
Malformed Ordered Lists

    1.Structured Question Generation
    ↓
    1. Structured Question Generation

Pseudo Paragraphs

        Educational content is trapped inside documents.
    ↓
    Educational content is trapped inside documents.


## Rule 2 Content Preservation
Normalization must not: 
- invent content
- rewrite content
- summarize content
- remove content


## Rule 3 Label Detection

When a line ends with ":", text before ":" → label

Example 

    Before:
        OCR was expected...
    
    ↓
    
    {
      "label": "Before",
      "content": [
        "OCR was expected..."
      ]
    }

## Rule 4 Recursive Label Conversion

When a line ends with “:” 
- text before “:” becomes Block.label
- following content becomes Block.content[]

This rule applies recursively at every nesting level.
- Bullet lists become content[] items inside the current Block.
- Paragraphs become content[] items inside the current Block.
- Label detection takes precedence over plain content.
- Colon-terminated labels are structural boundaries, not literal content.


---

# Part 2 — Apply Visibility

Remove content excluded from portfolio output.
Visibility metadata attached to a heading applies to the entire heading subtree.

Example

    ## Research Problems
    excluded_visibility: portfolio
    ...

    ↓

    Remove:
    - Research Problems
    - all descendants

---

# Part 3 — Portfolio Structure

## Section Contract

Reusable Content Blocks define reusable Portfolio JSON structures.
Reusable Content Blocks may appear inside any Section Contract.
```json
    {
      "section": "",
      "title": "",
      "metadata":{},
      "blocks": []
    }
```

Rules

- section required
- title required
- blocks required
- blocks is array

All section content must be represented through blocks.
Sections do not define custom fields.
Section-specific meaning belongs in block labels, not JSON keys.

Example 

    {
      "section": "capabilities",
      "title": "Current Capabilities",
      "blocks": []
    }


## Block Contract
inside a block, it should be:
```json
    {
      "label": "",
      "content": []
    }
```

Rule:
- label optional
- content required and must be an array
- content items may contain nested blocks
- nested blocks follow the same Block Contract recursively

Do not generate section-specific fields.
Examples of prohibited fields:
- supports
- includes
- description
- responsibilities
- core_components
- project_response
- frames
These must be represented as blocks.


Example

    Section Label
        Child Label A:
            ...
        Child Label B:
            ...

    ↓

    {
      "label": "Section Label",
      "content": [
        {
          "label": "Child Label A",
          "content": ["..."]
        },
        {
          "label": "Child Label B",
          "content": ["..."]
        }
      ]
    }   


---

# Part 4 — Allowed Sections
Allowed section values only.
They do not define additional JSON structures.
All section content must follow the Section Contract and Block Contract.

Allowed `section` values
- problem_space
- capabilities
- architecture
- stories


