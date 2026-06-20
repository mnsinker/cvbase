# Information Architecture Standard

## Purpose

Define how information should be organized, structured, and communicated.

Applies to:

- project archives
- story archives
- reports
- analyses
- proposals
- documentation
- portfolio content
- resume source material

Unless explicitly overridden.

---

# Principles

## Lead With The Headline

State the conclusion before the explanation.

Good

    Decision Logic Is Fragmented

        Organizations make decisions every day.
        Decision logic is often scattered across:
            - spreadsheets
            - business rules
            - code
            - tribal knowledge

Bad

    Organizations make decisions every day.
    As organizations grow, more tools are introduced.
    Business rules become harder to track.
    Decision Logic Is Fragmented.

---

## One Section, One Responsibility

Each section should answer exactly one question.

Examples

    Problem
        What is wrong?

    Capability
        What can the system do?

    Architecture
        How does the system work?

    Discovery
        What understanding changed?

    Outcome
        What emerged afterwards?

Example

    Problem

        Before:
            Business rules lived inside tools.

        Consequences:
            Policy changes required tool changes.

Counter Example

    Problem

        Before:
            Business rules lived inside tools.

        Policy Layer was introduced.

        Policy changes no longer required tool changes.

---

## Parallel Structure

Items at the same level must belong to the same category.

Good

    Potential Update Targets

        - memory updates
        - context updates
        - policy updates
        - goal updates

Bad

    Potential Updates

        - memory updates
        - policy updates
        - experimentation
        - optimization

---

## Eliminate Redundancy

Each sentence should contribute new information.

Example

    Tool signatures already described:
        - inputs
        - outputs

    Represent information once.
    Derive everything else.

Counter Example

    Dependency definitions existed in multiple places.
    Additional mappings duplicated existing information.
    Metadata was duplicated.

Example

    Consequences

        - graph issues were discovered only after execution began

Counter Example

    Consequences

        - invalid graphs could start execution
        - graph issues were discovered only after execution began

---

# Patterns

## Before → Discovery → After

Use for architectural evolution.

Example

    Problem
        Before:
            Business rules lived inside tools.

    Discovery
        Facts answer:
            What is true?

        Policies answer:
            What should happen?

    Outcome
        After:
            Policy Layer

Counter Example

    Problem
        Old implementation.

    Outcome
        New implementation.

---

## Consequences ↔ Benefits Symmetry

Benefits should directly resolve consequences.

Example

    Consequences

        - execution paths could not be reviewed before runtime

    Benefits

        - review execution paths before runtime

Counter Example

    Consequences

        - execution paths could not be reviewed before runtime

    Benefits

        - cleaner architecture
        - improved scalability

---

# Techniques

## Observation Before Abstraction

Introduce evidence before introducing abstractions.

Example

    Tool Signature
    Tool Registry
    Entity Mapping

    Represent information once.
    Derive everything else.

Counter Example

    Metadata duplication existed.

---

## Prefer Concrete Language

Prefer observable outcomes over abstract labels.

Example

    policy changes required tool changes

Counter Example

    business reasoning remained coupled to execution

Example

    review execution paths before runtime

Counter Example

    improved predictability

---

# Final Check

- Does the first line communicate the headline?
- Does each section answer exactly one question?
- Do all bullets belong to the same category?
- Is any information repeated using different words?
- Does every story follow: Before → Discovery → After
- Do Benefits directly resolve Consequences?
- Can a reader understand the document by scanning only the headlines?