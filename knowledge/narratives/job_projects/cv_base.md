---
id: cv_base
experience_fk:
start:
end:
---
# Problem Space

## Current Problem

Knowledge Is Missing

    Statement
        Project files exist.
        Project knowledge does not.
    
    Symptoms
        - architecture decisions remain implicit
        - trade-offs remain implicit
        - discoveries remain implicit
        - capabilities remain implicit
    
    Consequence
        Experience exists. 
        Knowledge does not.

        Project → 
           * Resume.doc
           * Interview.doc
           * Portfolio.doc
        Each representation must be recreated.
    

Information Granularity is Fixed

    Statement
        Different situations require different levels of detail.
    
    Symptoms
        Resume:         too compressed
        Interview:      story-level detail
        Project Files:  too detailed
    
    Consequence
        One Representation
            → One Granularity
            → Many Rewrites
        Every new use case starts from scratch.

## Future Problem

Learning Is Missing

    Statement
        Feedback is not captured.
    
    Symptoms
        - application feedback is not captured
        - interview feedback is not captured
        - skill-gap feedback is not captured
    
    Consequence
        Knowledge
            → Action
            → Outcome
            ✕ Feedback
            ✕ Learning
        The loop stops at outcome.


# Capabilities

## Current Capabilities

Knowledge Creation

    Question: What is knowledge?
    Answer: Not facts, but "reusable understanding".

    To be reusable, it must include:
        - problems
        - constraints
        - trade-offs
        - decisions
        - outcomes
    Otherwise, the understanding cannot be reused.
    
    Supports:
        Experience → Knowledge
    
    Benefits:
        - reduce repeated analysis
        - preserve architectural reasoning
        - accelerate future decision making


Knowledge Representation

    Question: How is knowledge reused?
    Answer: Through context-specific representations..
    
    Supports:
        Knowledge → Resume
        Knowledge → Interview
        Knowledge → Portfolio

    Benefits:
        One source of truth, multiple representations.
        No repeated rewriting.


Knowledge Structure

    Question: How does knowledge stay consistent?
    Answer: Through shared structure and standards.

    Including:
        - problem space
        - capabilities
        - architecture
        - stories

        - information architecture
        - writing standards
    
    Benefits:
        - consistent outputs
        - lower maintenance cost
        - easier knowledge reuse


## Future Capabilities

Outcome Capture

    Question: What happens after action? 
    Answer: Capture outcomes.

    Supports:
        Application → Outcome
        Interview → Outcome
        Skill Assessment → Outcome

    Benefits:
        - identify recurring weaknesses
        - reduce repeated mistakes


Action Guidance

    Question: What should happen next?
    Answer: Recommend actions.
    
    Supports:
        Knowledge
        + Feedback
        + Goals
        ------------
        = Recommended Actions
    
    Examples:
        - interview narrative
        - project narratives
        - skill development priorities
    
    Benefits:
        - reduce guesswork
        - focus effort on highest-impact improvements
        - improve career decision making


# Architectural
## Architectural Goal

Build a career knowledge system that can evolve from:

    Experience
        → Resume Documents

toward:

    Experience
        → Knowledge
        → Context
        → Outcomes
        → Reflection
        → New Knowledge


## Dynamic Flow

    Experience
        → Knowledge
        → Context Selection
        → Outcomes 
        → Reflection
        → New Knowledge

## Static Structure
Memory Layer

    Question: What do we know?
    Answer: Store all accumulated knowledge.
    
    CV Base Examples:
        Project Knowledge
            - Problem Space
            - Capabilities
            - Architecture
            - Stories

Context Layer

    Question: What matters right now?
    Answer: Select relevant context for a specific goal.
    
    CV Base Examples:
        - Resume Context
        - Interview Preparation Context
        - Portfolio Context

Policy Layer

    Question: How is output quality controlled?
    Answer: Define standards and constraints.

    CV Base Examples:
        - Information Architecture
        - Writing Format
        - Role Profiles


Outcome Layer (Future)

    Question: What happened?    
    Answer: Capture outcomes from real-world interactions.
    
    CV Base Examples:
        - Application Outcomes
        - Interview Feedback


Decision Layer (Future)

    Question: What should improve next?
    Answer: Recommend future improvements.

    CV Base Examples:
        - which skills deserve investment
        - which experiences deserve emphasis
        - which narratives deserve refinement
        - which content should be removed

# Story: Documents Were Not The Real Problem

Problem

    Strong content became difficult to find.
    Good bullets, stories, and explanations were scattered across resume versions.

Analysis
    Further investigation revealed a deeper chain of problems.

    Document Problem
        Strong content became difficult to find.
    ↓

    Granularity Problem
        Different situations required different levels of detail.
    ↓

    Knowledge Problem
        Facts existed. Reusable understanding did not.
        Trade-offs, constraints, reasoning were never captured explicitly.
    ↓

    Structure Problem
        Knowledge existed. Consistency did not.


Key Discovery

    Experience recorded what happened.
    Knowledge explained why.

Outcome

    From: Experience 
        → Documents

    Toward: Experience 
            → Knowledge 
            → Structured Knowledge 
            → Context-Specific Views

