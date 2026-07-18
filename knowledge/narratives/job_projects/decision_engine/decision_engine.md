---
id: decision_engine
experience_fk:
start:
end:
links: 
  - label: Project Page
    url: 
  - label: Live Demo
---
# Problem Space

## Current Problem

Decision Logic Is Fragmented

    Organizations make decisions every day. However, the logic behind those decisions is often scattered across:
        - excel spreadsheets
        - slide decks
        - business rules
        - code
        - tribal knowledge
    As a result, decisions become difficult to understand, govern, test, and improve.

AI Decision Engine: turns decision logic from an implicit process into an explicit system.



## Future Problem

Decision Execution Is Not Enough

    Making decisions is only the first step. Organizations must also determine:
       	 Context + Policies + Goals → Next Best Action
    and continuously learn from the outcomes.

The long-term objective: a decision system capable of planning, executing, evaluating, and improving decisions over time.

------

# Capabilities

## Current Capabilities

Decision Context
    Define the information required for a decision.

    Supports: OrderSummary → CouponEligibility → CouponDecision
    Makes decision inputs explicit.

Decision Planning
    Derive execution order from dependency relationships.

    Supports: Target Entity → Dependency Graph → Execution Plan
    Including:
        planning
        validation
        dependency management

Decision Traceability
    Make decision behavior observable and explainable.

    Supports: Execution Plan → Execution Trace → Review
    Including:
        dependency graphs
        execution traces
        runtime outputs
    Enables debugging and governance of decision systems.


## Future Capabilities

Policy Governance
    Support policy ownership, lifecycle management, approval, and versioning.

    Supports: Policy → Version → Approval → Deployment


Decision Learning
    Turn decision outcomes into reusable knowledge.

    Supports: Decision → Outcome → Feedback → Policy Updates
    Potential update targets may include:
        - memory updates
        - context updates
        - policy updates
        - goal review
    Potential mechanisms: 
        - evaluation
        - experimentation
        - optimization

Decision Coordination
    Coordinate decisions across multiple contexts, policies and domains.

    Supports: Contexts + Policies + Goals → Coordinated Actions
    Potential implementations:
        Single-Agent Coordination
        Multi-Agent Coordination


# Architecture

## Architectural Goal

Build a foundation that can evolve from:

    Context → Decision

toward:

    Context + Memory + Policies + Goals → Next Best Action


The architecture is designed to make decision making observable, testable, and evolvable.


## Dynamic Flow

    Request 
    → Target Entity 
    → Planner 
    → Execution Plan 
    → Runtime 
    → Entity Production 
    → Policy Evaluation 
    → Decision

## Static Structure

Context Layer

    Responsibilities: define the information required for decisions
    Core components: Entities

Planning Layer

    Responsibilities: derive execution order from dependencies
    Core components: Planner, Validator

Execution Layer

    Responsibilities: execute decision workflows and produce entities
    Core components: Runtime, Tools

Policy Layer
    
    Responsibilities: evaluate business rules and generate decisions
    Core components: Policies

Relationship Layer
    
    Responsibilities: model dependencies between entities
    Core components: Dependency Graph

Traceability Layer

    Responsibilities: make decision behavior observable and explainable
    Core components: Execution Plans, Execution Traces, Runtime Outputs

# Stories

## Core Discovery

Decide Before Execute

    The architecture evolved by progressively moving decisions out of runtime.
    Examples: 
        * Dependency Discovery — Plan Before Execute
        * Dependency Correctness — Validate Before Execute
        * Dependency Definition — Derive Before Duplicate
        * Layer Ownership — Separate Policy From Execution


## Story: Dependency Discovery — Plan Before Execute

Career Spine: workflow, systems
Advanced Themes: automation, ai-systems

Problem
    
    Before: Execution path did not exist before runtime.
            while loop: 
               - discover dependency
               - insert step

    Consequences: Pipeline Black Box
        * execution paths could not be reviewed before execution
        * dependency issues could only be discovered during execution

Discovery

    Planning and execution are different concerns.
        - Planning answers: What should happen?
        - Execution answers: Make it happen.

Outcome

    After: Dependency Graph
         → Planner 
         → Execution Plan
    Runtime consumed an execution plan, instead of constructing one
    
    Benefits: 
        - catch dependency issues before runtime
        - review execution paths before runtime

---

## Story: Dependency Correctness — Validate Before Execute

Career Spine: systems
Advanced Themes: governance

Problem

    Before:
        Dependency Graph existed, correctness was still checked during execution.
        Examples:
            - cycle detection
            - missing producers
    
    Consequences:
        - graph issues were discovered only after execution began

Discovery

    Validation is not execution.    
        - Planning answers: What should run?
        - Validation answers: Can it run safely?
    
    Execution should: assume correctness.
    Validation should: establish correctness.

Outcome

    After:
        Validator
    
    Benefits:
        - detect graph issues before execution


---

## Story: Dependency Definition — Derive Before Duplicate

Career Spine: information-modeling, systems
Advanced Themes: governance

Problem

    Before:
        Dependency definitions existed in multiple places.
        Examples:
            Tool Signature
            Tool Registry
            Entity Mapping

    Consequences:
        - the same information required multiple updates
        - dependency definitions could drift out of sync

Discovery

    Tool signatures already described:
        - inputs
        - outputs

    Represent information once. Derive everything else.

Outcome

    After:
        Tool Signature → Derived Dependencies

    Benefits:
        - dependency definitions exist in one place
        - graph relationships no longer require manual synchronization

---

## Story: Layer Ownership — Separate Policy From Execution

Career Spine: systems
Advanced Themes: governance, ai-systems

Problem

    Before: Business rules lived inside tools.
    Consequences: policy changes required tool changes

Discovery

    Facts answer: What is true?
    Policies answer: What should happen?

    Facts and decisions evolve at different rates. They require different ownership boundaries.

Outcome

    After: Policy Layer
    Benefits: policy changes no longer require tool changes