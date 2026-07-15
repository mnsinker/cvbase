# Purpose

Convert Portfolio Markdown into deterministic Portfolio JSON.

# Output Contract

```json
{
  "section": "",
  "subsection": "",
  "metadata": {},
  "blocks": []
}
```

## Section Contract

Field:
    section

Datatype:
    string

Required:
    yes

Detection:
    H1 heading

Example:
    # Problem Space

## Subsection Contract

Field:
    subsection

Datatype:
    string

Required:
    yes

Detection:
    H2 heading

Example:
    ## Current Problem

## Metadata Contract
```json
{
  "career_spine": [],
  "advanced_themes": [],
  "excluded_visibility": []
}
```
Allowed Keys:
    career_spine
    advanced_themes
    excluded_visibility

Datatype:
    list[string]

Required:
    no

Detection:
    Career Spine:
    Advanced Themes:
    Excluded Visibility: 

Constraint: 
    Metadata is only allowed at subsection level.


## Block Contract
```json
{
  "label": "",
  "content": []
}
```

### Label Contract

Field:
    label

Datatype:
    string

Required:
    no

Detection:
    Text ending with ":"

Example:
    Before:


### Content Contract

Field:
    content

Datatype:
    list

Required:
    yes

Detection:
    Paragraphs
    Bullets
    Indented paragraphs

Example:
    Paragraph / bullets     
    ↓
    content item

### Recursive Block Contract
Nested labels become nested blocks.


# Rule Priority

Metadata > Section > Subsection > Label > Content

    Content Detection is applied only when no higher-priority rule matches.
