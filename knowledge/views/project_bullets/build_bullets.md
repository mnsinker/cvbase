---
name: build_bullets
description: Generate candidate resume bullets from project archives.
---
# Purpose

Generate resume bullets from project archives.
Project archives are the source of truth.
Resume bullets are compressed views.
Bullets must remain traceable to evidence contained in the archive.

---

# Parameters

Role

    default_role:
        The first role defined in taxonomy/roles.md

    intended_role:
        Specified in prompt

Project md

    user must specify in prompt

    If not specified:
        throw error immediately

---

# Mode

default: inline

    Generate content according to Format.
    Do not create, modify, or save files.
    Display generated content inline.

---

override: write

    Generate content according to Format.

    Save output to:
        project_bullets/<project_name>_bullets.md

    If file does not exist:
        create file

    If file already exists:
        replace content under matching role section
        preserve content for other roles

---

# Inputs

Required

    taxonomy/roles.md

    projects/<project_name>.md

Optional

    experiences/<experience_name>.md

        Only when:

            - referenced by the project archive
            - requested explicitly

Do not read unrelated files.

---

# Rule - Resume Bullet Lens

A resume bullet is not an architecture summary.

Each bullet should answer:

    What changed?

    Why did it matter?

    What capability or outcome became possible?

Prefer:

    problem
        ↓
    architectural decision
        ↓
    capability or outcome

Over:

    architecture structure
        ↓
    component inventory
        ↓
    generic benefit

A bullet should communicate a claim.

Not a catalog.

---

# Rule - Evidence Extraction

Extract evidence from:

    - Current Capabilities
    - Future Capabilities
    - Architecture
    - Stories

Stories are not the only source of evidence.

Capabilities and architectural discoveries may be equally important.

Future capabilities may be used when:

    - supported by explicit archive evidence
    - partially implemented
    - useful for understanding system direction

Do not present future direction as shipped capability.

---

# Rule - Evidence Selection

Prefer evidence demonstrating:

    - architecture decisions
    - system design
    - abstraction design
    - governance
    - trade-off analysis
    - modeling
    - workflow design
    - systems thinking
    - measurable outcomes

Avoid:

    - implementation details
    - local refactors
    - bug fixes
    - naming cleanups
    - low-level tasks

Unless they changed:

    - architecture
    - abstractions
    - ownership boundaries
    - system direction

---

# Rule - Role Adaptation

Adapt selection according to:

    taxonomy/roles.md

Prefer evidence whose:

    Career Spine

and

    Advanced Themes

align with the target role.

Role alignment influences selection.
Role alignment does not justify inventing evidence.

---

# Rule - Compression

Project archives are the source of truth.

Bullets are compressed views.

Preserve:

    - strongest architectural decisions
    - strongest discoveries
    - strongest capability claims
    - strongest outcomes

Compress:

    - implementation details
    - chronology
    - intermediate steps
    - component inventories
    - layer inventories

Prefer signal over wording.

Do not copy archive text verbatim.

---

# Rule - Cognitive Load

Avoid architecture inventories.

If a bullet contains more than three major architectural nouns:

    compress them into a higher-level concept.

Prefer:

    explicit, reviewable decision workflows

Over:

    context, planning, execution, policy, relationship, traceability layers

Prefer:

    derived dependency relationships

Over:

    tool signatures, registries, mappings, dependency declarations

A reader should understand a bullet after one pass.

---

# Rule - Bullet Set Composition

A bullet set should be MECE.

Bullets should represent different dimensions of the project.

Examples:

    - architecture transformation
    - governance
    - information modeling
    - system direction

Avoid:

    multiple bullets expressing the same discovery.

If two bullets communicate the same higher-level claim:

    merge them.

Example:

    Plan Before Execute

    Validate Before Execute

May be merged into:

    Move Decisions Out Of Runtime

when appropriate.

---

# Rule - Evidence Integrity

Every bullet must be traceable to archive evidence.

Evidence may originate from:

    - Capability
    - Architecture
    - Story

Do not invent:

    - achievements
    - metrics
    - scale
    - impact

Do not introduce facts not present in the archive.

---

# Format

    # <role_name>
    
        - bullet
        - bullet
        - bullet
        - bullet
    
    ## Evidence Mapping
    
    Bullet 1
    
        Sources:
            - Capability: ...
            - Story: ...
    
    Bullet 2
    
        Sources:
            - Capability: ...
            - Architecture: ...
    
    Bullet 3
    
        Sources:
            - Story: ...
    
    Bullet 4
    
        Sources:
            - Capability: ...
            - Story: ...
    
    ---
    
# Writing Style

Emphasize impact: 

    - architecture
    - decision making
    - system thinking

Prefer:
    
    capability 
    ↓
    outcome

Over:

    task
    ↓
    task
    ↓
    task

Prefer:

    architectural discoveries

Over:

    implementation descriptions

Quantify only when supported by evidence.
Use concise resume-style language.

---

# Validation

Before generating bullets, verify:

    - every bullet is supported by archive evidence
    - every bullet aligns with the target role
    - every bullet communicates a meaningful claim
    - no bullet depends on invented facts
    - evidence mapping is complete
    - bullets are not repeating the same discovery
    - bullets are MECE as a set
    - bullets are understandable without project context

If evidence is insufficient:

    omit the bullet

Do not hallucinate.
