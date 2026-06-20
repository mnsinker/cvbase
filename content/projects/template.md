---
id: template
experience_fk:
start:
end:
---
# Summary

What is this project?
Why does it exist?
What is the core value?
Key capabilities:
- ...
- ...
- ...

# Overall Results

Project-level outcomes.
Current state.
Adoption.
Metrics.
Key accomplishments.

# Architecture

Current architecture.
Major components.
Important relationships.

---

# Stories

## Core Discovery

One sentence.

The recurring architectural discovery that connects all stories.

Examples:

    Observe Before Change

    Decide Before Execute

    Model Before Change

---

## Story

### Title

Format:

    <Problem Domain> — <Architectural Discovery>

Examples:

    Dependency Discovery — Plan Before Execute

    Dependency Correctness — Validate Before Execute

    Dependency Definition — Derive Before Duplicate

    Layer Ownership — Separate Policy From Execution

---

Career Spine:

    - modeling
    - workflow
    - systems

Advanced Themes:

    - automation
    - governance
    - ai-systems

---

### Problem

Before:

    What existed before?

Consequences:

    What problems did it create?

Keep consequences concrete.

Prefer:

    "cannot review execution paths"

over:

    "reduced observability"

---

### Discovery

What understanding changed?

Prefer:

    principle
    realization
    architectural insight

Examples:

    Planning and execution are different concerns.

    Validation is not execution.

    Represent information once. Derive everything else.

Keep this section short.

One to three key insights only.

---

### Outcome

After:

    What emerged?

Examples:

    Planner

    Validator

    Schema Derivation

    Policy Layer

Benefits:

    What became easier, safer, faster, or more predictable?

Benefits should directly address the consequences listed in Problem.

Prefer:

    "review execution paths before runtime"

over:

    "improved predictability"

---

# Writing Rules

Problem:

    Before + Consequences

Discovery:

    New Understanding

Outcome:

    After + Benefits

Do not mix sections.
Do not explain solutions inside Problem.
Do not explain problems inside Outcome.
Do not repeat Discovery inside Outcome.
Keep each section focused on a single responsibility.

---

# Story Selection Rules

Include only stories that changed:

    - architecture
    - ownership boundaries
    - abstractions
    - system direction
    - engineering principles

Exclude:

    - implementation details
    - bug fixes
    - refactors without architectural impact

A story is important only if it changed how the system is understood or built.

