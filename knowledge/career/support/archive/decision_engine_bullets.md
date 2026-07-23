---
project_fk: decision_engine
experience_fk: ""
---
# ai-fde

- Architected a decision engine that transformed fragmented decision logic into explicit, reviewable workflows, making decision behavior observable, testable, and evolvable.

- Separated planning and validation from runtime execution through dependency graphs, execution plans, and pre-execution validation, enabling execution paths and graph correctness to be reviewed before runtime.

- Reduced duplicated system definitions by deriving dependencies from tool signatures and establishing clear ownership boundaries between policy evaluation and execution.

- Explored feedback-driven decision architectures that evolve from static execution toward context-, policy-, and goal-aware decision systems.


## Evidence Mapping

bullet 1:
- Current Problem: Decision Logic Is Fragmented
- Current Capabilities: Decision Context
- Current Capabilities: Decision Traceability
- Architecture: Architectural Goal
- Stories: Core Discovery

bullet 2:
- Current Capabilities: Decision Planning
- Architecture: Dynamic Flow
- Architecture: Static Structure / Planning Layer
- Story: Dependency Discovery — Plan Before Execute
- Story: Dependency Correctness — Validate Before Execute

bullet 3:
- Story: Dependency Definition — Derive Before Duplicate
- Story: Layer Ownership — Separate Policy From Execution
- Architecture: Static Structure / Execution Layer
- Architecture: Static Structure / Policy Layer
- Architecture: Static Structure / Relationship Layer

bullet 4:
- Future Problem: Decision Execution Is Not Enough
- Future Capabilities: Policy Governance
- Future Capabilities: Decision Learning
- Future Capabilities: Decision Coordination
- Architecture: Architectural Goal

# Tech
- LLM
- Tool Calling
- Context Management
- Planning
