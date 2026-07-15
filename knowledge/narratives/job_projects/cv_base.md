---
id: cv_base
experience_fk:
start: 2026/06
end:
---
# Problem Space

Knowledge Is Missing

    Statement: 
        Project files exist.
        Project knowledge does not.
    
    Symptoms: 
        Explicit knowledge does not exist. 
    
        - architecture decisions
        - trade-offs 
        - discoveries
        - capabilities
    
    Root Cause: 
        Project information is captured, but never distilled into reusable knowledge.
    
    Consequence: 
        Every deliverable must be recreated.
    
        Resume → rewrite
        Interview Prep → rewrite
        Portfolio → rewrite
        Blog → rewrite


# Capabilities

## Current Capabilities

Capture Information

    Question: 
        How is information collected?
    
    Flow: 
        Information → Inbox
    
    Examples: 
        * GPT conversations
        * books highlights
        * project notes 
        ---------------
        → Inbox
    
    Benefits: 
        - frictionless capture
        - unified entry point


Distill Information into Knowledge

    Question:
        How does raw information become reusable knowledge?
    
    Flow: 
        Inbox → Narrative
    
    Examples: 
        Question Forge Project → Narrative, containing:
        - problems
        - constraints
        - trade-offs
        - decisions
        - outcomes
    
    Benefits:
        - preserve architectural reasoning
        - reduce repeated analysis
        - accumulate reusable knowledge


Generate Deliverables

    Question: 
        How is knowledge applied to different goals?
    
    Flow: 
        Narrative → Resume
        Narrative → Portfolio
        Narrative → Interview Preparation
    
    Example: 
        One Narrative 
        ↓ 
        Resume / Portfolio / Interview Preparation
    
    Benefits:
        - one source of truth
        - multiple deliverables
        - no repeated rewriting


## Future Capabilities

Extract Concepts

    Question: 
        How can reusable concepts be identified? 
    
    Flow: 
        Narrative → Concept 
        
    Examples: 
        Narratives 
        ↓
        Ownership | Feedback Loop | Policy | Representation
    
    Benefits: 
        - improve retrieval
        - reduce duplicate concepts
        - build a shared vocabulary


Synthesize Insights

    Question: 
        How do higher-level insights synthesized across multiple narratives? 
    
    Flow: 
        Narrative
        + Narrative
        + Narrative 
        ----------------
        → Insight
    
    Example: 
        Question Forge
        + Compiler
        + Decision Engine 
        ----------------------
        → Insight: Representation Is Required Before Computation
    
    Benefits: 
        - discover recurring patterns
        - connect independent narratives
        - generate reusable knowledge


Recommend Actions

    Question
        What should happen next, given current goal? 
    
    Flow
        Insights
        + Current Goal
        + Current Context
        (+ Previous Outcomes)
        ---------------------
        → Recommended Actions
    
    Note
        Implemented through Runtime Policy Generation (See Architecture).
        
    Examples
        - which narrative to emphasize in interview
        - which project deserves further investment
        - which skills should be improved next
    
    Benefits
        - reduce guesswork
        - prioritize high-impact work
        - improve career decisions

Capture Outcomes

    Question: 
        What happened?
    
    Flow:
        Action → Outcome
    
    Examples:
        - capture interview feedback
        - capture application results
           
    Benefits:
        - preserve real-world feedback
        - identify recurring weaknesses
        - reduce repeated mistakes


Learn from Outcomes

    Question: 
        How does the knowledge system continuously improve?
    
    Flow:  
        Outcome → Through Reflection → Updated Narrative → Updated Insight
    
    Examples: 
        Interview Feedback → Updated Narrative → Updated Insight
    
    Benefits:
        - accumulate experience
        - continuously improve knowledge
        - evolve decision quality

# Architecture

The knowledge system consists of three stages:

1. Knowledge Generation
2. Knowledge Consumption
3. Knowledge Evolution

Together they form a continuous learning loop.

## Overall Flow

```json
Information
↓
Inbox
↓
Narrative
↓
Concept
↓
Insight
↓
Runtime Policy
↓
Action
↓
Outcome
↓
Reflection
↓
Updated Narrative
```

The following sections explain each stage of this lifecycle.


## Knowledge Generation 

Question: 

    How does raw information become reusable knowledge?

Flow: 

    ```json
    Information
       │
       │ Capture
       ▼
    Inbox
       │
       │ Distill
       ▼
    Narrative
       │
       │ Extract
       ▼
    Concept
       │
       │ Generate
       ▼
    Insight
    ```

Key Components: 

    Information
        Raw observations captured from books, conversations, projects, and daily work.
    
    Inbox
        A temporary collection layer before knowledge distillation.
    
    Narrative
        The primary knowledge representation for downstream reuse.
      
    Concept
        Semantic indexes extracted from individual narratives for AI retrieval.
    
    Insight
        Higher-level principles synthesized across multiple narratives.

Key Discovery: 

    Knowledge is not captured directly. It is generated through distillation.
    Distillation connects information with: 
        - context
        - constraints
        - trade-offs
        - examples
        - previous experience
    Without these connections: 
        - information remains information.
        - it never becomes knowledge.



## Knowledge Consumption 
Question: 
    How is knowledge transformed into decisions for a specific goal?

Flow: 

```json
Insights + Current Goal + Current Context
  │
  │ inference
  ▼
Runtime Policy
  │
  │ prioritize
  ▼
Recommended Actions
```

Key Components: 

    Insights
        Long-term reusable knowledge, accumulated across narratives.
    
    Current Goal
        The objective the system is trying to achieve.
    
        Examples:
        - Resume
        - Portfolio
        - Interview Preparation
    
    Current Context
        Information relevant to the current situation.
        Examples:
        - target role
        - interview history
        - available projects
    
    Runtime Policy
        A temporary decision policy generated for the current goal and current context.
    
    Recommended Actions
        Concrete next steps produced from the runtime policy.
        Example: 
            - Emphasize Compiler.
            - De-emphasize Product Management.

## Knowledge Evolution

Question: 

    How does the knowledge system continuously improve over time?

Flow: 
```json
Outcome
↓
Reflection
↓
Updated Narrative
↓
Updated Concept
↓
Updated Insight
```

Key Components: 

    Outcome
        Real-world results produced by previous actions.
        Examples: 
            - interview feedback
            - application results
            - portfolio performance
    
    Reflection
        Analyze outcomes to identify
            - what worked
            - what failed
            - why
    
    Updated Narrative
        Record new observations, decisions, and reasoning.
    
    Updated Concept
        Update semantic indexes for future retrieval.
    
    Updated Insight    
        Refine higher-level principles.
    
    Key Discovery
        Feedback alone does not improve knowledge.
        Knowledge evolves only through reflection.
        Outcomes become knowledge only after they are interpreted, connected, and distilled.


## Universal Computation Pattern

Question: 
    Why do
        - CV Base
        - Decision Engine
        - Workflow Engine
        - Graph Engine
    share the same architecture? 

Pattern:
```json
Input
↓
Representation
↓
Transformation
↓
Computation
↓
Output
↓
Feedback
↓
Updated Representation
```



Example 1. Compiler
Flow
```json
Markdown (# Problem Space) 
↓
AST (H1, "Problem Space")
↓
Semantic Analysis (Detect: heading level, parent-child ownership, semantic type)
```

Instance
```json
# Problem Space
↓
H1(Problem Space)
↓
Detect: heading level, parent-child ownership, semantic type
```

Why Representation?

    Without the AST, semantic analysis cannot determine ownership, hierarchy, or semantics.

Example 2. CV Base
Flow
```json
Experience
↓
Narrative
↓
Knowledge Products 
```

Instance
```json
CV Base project experience
↓
Narrative
↓
Resume / Portfolio / Concept / Insight
```

Why Representation?

    Without narratives, knowledge products cannot be generated from project experience. 


Example 3. Question Forge
Flow 
```json
PDF
↓
Question Object
↓
Search / Generation / Personalization
```

Instance
```json
Exam Paper.pdf
↓
Question(stem, diagram, options, difficulty_level)
↓
Question Search | AI Question Generation | Personalized Practice
```
Why Representation?

    Without Question Objects, questions cannot support retrieval, generation, personalization.



Example 4. Decision Engine
Flow 
```json
Context 
↓
State 
↓
Policy Evaluation
```

Instance
```json
User: "I want a refund"
↓
OrderSummary(status="shipped", delivered_days=3)
↓
Refund Allowed
```

Why Representation?

    Without State, policy evaluation cannot operate on raw context.



Key Takeaway: 

    Structured representations are the prerequisite for computation. 
    Different domains require different representations, but the computational principle remains the same.



# Stories
These stories document the engineering discoveries that emerged while building the CV Base compiler.
They focus on how the system was designed, how modeling decisions were made, and how implementation problems were decomposed.


## Story: Module Design - Design The Compiler Module

Background

    The renderer requires deterministic input.
    LLM-generated structures were not deterministic enough.
    A compiler became the deterministic layer between raw content and rendering.

Module Boundary

```json
Raw Content
      │
      ▼
+----------------+
|    Compiler    |
+----------------+
      │
      ▼
Structured Representation
      │
      ▼
+----------------+
|    Renderer    |
+----------------+
      │
      ▼
  HTML
```

    Why independent compiler? 
    - The compiler should not know anything about portfolios.
    - It should only transform raw content into structured representations.

Design Methodology: 

    Step 1. Identify input and output
        What's the purpose? What should the module produce?
    
    Step 2. Problem Decomposition
        What questions must be answered? 
        In which order should they be answered?
        Those questions define the pipeline.
    
    Step 3. Entities Design
        What entities represent each stage? 
    
    Step 4. Functions Design
        What function transforms one entity into the next? 

Compiler Pipeline

    Markdown                 raw input
        ↓ 
    ParsedLine               what is on each line?
        ↓ 
    Node Tree                who owns whom?
        ↓ 
    Annotated Node Tree      what are the domain semantics?
        ↓ 
    Rewritten Node Tree      how do domain semantics change ownership?
        ↓ 
    Rendered Output          how should it be displayed?

Key Discovery

    Goal
    ↓
    Problems
    ↓
    Entities
    ↓
    Functions
    
    Begin with the end in mind. 
    Design from the destination, not from implementation details.


Coming Next 

    The pipeline defines what representations are needed.
    The next question becomes:
        - How do we decide what deserves its own representation?


## Story: Entity Design - around Value, Not Lifecycle
### Question 1. Does this concept deserve to be name?

Traditional Criteria: 
* has a lifecycle
* has an id
* has its own structure


    Problem: Criterion vs Consequence
    - Lifecycle, IDs, structure are "consequences" of introducing an entity.
    - They are not "criteria" of introducing an entity. 


Real Criteria
* Positive: reused by many places 
* Negative: changing it would require many downstream changes. 


Key Discovery

    Connection determines value. 
    Highly connected concepts deserve their own representation.

Next Question

    Once a concept has been justified, the next question is: 
    - who will use this concept? 


### Question 2. Who will use this concept? 

Why This Question Matters?

    The consumers of an entity determine its abstraction.
    - Designing for only one consumer → overfits the current use case
    - Designing for all intended consumers → produces a reusable abstraction

Before

    Consumers: Portfolio
    ↓
    Chosen Abstraction: Section, Subsection, Metadata 
    ↓
    Consequence: Could not support HTML, book highlights, conversations.
    
    Section
       ├── title
       ├── subsections
       └── metadata

After

    Consumers: Portfolio, HTML, Book Highlights, Conversations
    ↓
    Chosen Abstraction: Node
    ↓
    Outcome: 
        - One abstraction, many consumers. 
        - The compiler remains unchanged, only new renderers are added.
    
    Node
     ├── ast_type
     ├── semantic_type
     ├── content
     └── children

Key Discovery

    Consumers determine entity abstraction.

Next Question

    Once the abstraction is determined, how should it be represented?


### Question 3. how should this concept be represented? 

Why This Question Matters?

    The same concept can be represented in different ways. 
    The chosen representation determines: 
        - how it is used
        - how schema changes are handled

Representation Options

| Representation | Typical Usage                     |
|----------------|-----------------------------------|
| Primitive      | Local variables inside a function |
| Dictionary     | Concepts with evolving schemas    |
| DataClass      | Concepts with stable schemas      |


    Dictionary
    
        How it is used: 
            - No instance needs to be created. 
            - Adding a new field does not affect existing code.
    
        Example 1: 
            T1. metadata = {"A": ...}
            T2. metadata["A"]
            T3. metadata = {"A": ..., "B": ... }
            --------------------------------
            Existing code (T2) still works.
    
        Example 2: Metadata
            Chosen Representation: Dictionary
            Reason: Metadata schema might change in the future.



    DataClass
    
        How it is used: 
            - Objects must be instantiated.
            - Schema changes immediately expose affected instance creation code.
                    
        Example 1:
            T1. class Metadata (A)
            T2. Metadata(A)
            T3. class Metadata (A,B)
            -------------------------
            Existing code (T2) is immediately identified by the IDE. 
    
        Example 2. Node
            Chosen Representation: DataClass
            Reason: Stable schema.


Guideline

- If the schema is still evolving, prefer Dictionary.
- If the schema is stabilized, prefer DataClass.


## Story: Function Design - Separate Problems Before Writing Logic
<a id="funtion-design-separate-problems"></a>

### Question 1: How to design functions?

Goal

    Transform a flat list of parsed lines into a node tree.
    
    Example
        Parsed Lines: 
            H1  Problem Space
            H2  Current Problem
            H2  Future Work
        ↓
        Node Tree: 
            Problem Space
            ├── Current Problem
            └── Future Work

Before

    The implementation started immediately. 
    The function gradually became: 
    
        if  
        while
        update_tree()
        update_stack()
        ...
    
    Every new case introduced another branch.
    The implementation became hard to understand and extend.


Step Back & Think

    Start from the goal. 
    ↓
    Focus on a single node.
    ↓
    Ask: what must happen before this node can appear in the final tree? 
    ↓
    Discovery: the node must find its parent first.

After 

    Goal
    ↓
    Find Parent
    ↓
    Update Tree
    ↓
    Update Stack
    ↓
    for node in nodes: 
        parent = find_parent()
        update_tree()
        update_stack()

Key insight

    Start with the goal.
    ↓
    Focus on one instance.
    ↓
    Identify the missing steps.
    ↓
    Each missing step becomes a function.


### Question 2: How to design rules? 

Background

    A rule system determines which outcome should be chosen, given a particular input.
    Examples: 
        - Compiler: Who is the parent?
        - Decision Engine: Should the refund be approved?
        - Workflow Engine: What should happen next?

Case Study

    In the compiler, the rule system answers following question:
    
        Previous Lines: 
            H1 Problem Space
            H2 Future Work
        Current Line: 
            H2  Current Problem
        ------------------
        → Who is the parent? 

Methodology

    Definition
    ↓
    Hypotheses
    ↓
    Evaluation
    ↓
    Decision 
    (repeat) 
    ---------------
    Final Design


Case Study Walkthrough

    Hypothesis 1. Heading has the highest priority.
        Evaluation: 
            Example: Heading > indent / paragraph / everything? 🟢Yes
        Decision: 
            Keep. | Reason: Heading has a strict ordering.
    
    ↓
    
    Hypothesis 2. Can the remaining node types be ordered by one global priority?
        Evaluation: 
            Example: Paragraph > Bullet?    🟡︎Sometimes
            Example: Bullet > Paragraph?    🟡︎Sometimes
        Decision: 
            Reject. | Reason: No strict ordering exists.
    
    The remaining nodes require another explanation.
    
    ↓
    
    Hypothesis 3. Indentation determines ownership for the remaining nodes.
        Evaluation: 
            Example:      🟢Yes
                Paragraph
                    Bullet 
            Example:      🟢Yes
                Bullet
                    Bullet 
            Example:      🔴No
                Paragraph
                - Bullet
        Decision: 
            - General Rule: Indentation.
            - Exception: Bullet Rule.
    
    ↓
    
    Final Design
        Heading
        ↓
        Indentation
        ↓
        Bullet

Key Discovery

    General Rules
    ↓ 
    Specific Rules
    ↓
    Exceptions
    
    ⭐️ Each new rule handles what previous rules cannot.


# Appendix 
excluded visibility: true

Markown 

Block Nodes
- Heading
- Paragraph
- Bullet
- Ordered List
- Quote Block (todo)
- Code Fence
- Front Matter
- Table (todo)
- Horizontal Rule
- HTML Block
- Math Block
- Reference Link (todo)
- Wiki Link (todo)

Inline Nodes
- Strong
- Italic
- Inline Code
- Link
- Image
- Emoji（todo）
- Footnote（todo）



