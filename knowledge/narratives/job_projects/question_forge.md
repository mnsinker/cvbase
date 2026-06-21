---
id: question_forge
experience_fk:
start:
end:
---
# Summary

## Current Problem

Educational Content Is Trapped Inside Documents

    Teachers and learning systems rely on questions stored inside PDFs and images.
    Those questions are visible to humans but difficult for machines to locate, parse, audit, and reuse.

    Existing approaches are insufficient because OCR alone can localize text but struggles with mathematical meaning, while VLM-only extraction can understand content but produces unreliable localization.

    Question Forge converts educational documents into structured question assets that can be inspected, evaluated, and exported.

## Future Problem

Question Assets Are Not Enough

    Structured questions solve content extraction, but learning systems also need to decide what should happen next.

    Future users need systems that can represent:
        Student State
        + Learning Goal
        + Question Repository
        ---------------------
        = Next Best Learning Action

    Question Forge is evolving toward AI-native educational systems that connect content understanding, learning context, and decision making.

# Capabilities

## Current Capabilities

Structured Question Generation

    What the system can do:
        Convert educational documents into structured, machine-readable question objects.

    Supports:
        PDF or Image → Question Object

    Includes:
        - question ownership
        - diagram extraction
        - structured parsing
        - export

    Why it matters:
        Questions can be reused by downstream learning, review, and generation systems instead of remaining locked inside documents.

Extraction Observability

    What the system can do:
        Make extraction pipelines inspectable and measurable.

    Supports:
        Pipeline Stage → Audit Artifact → Metrics → Evaluation

    Includes:
        - previews
        - traces
        - cost tracking
        - latency tracking
        - debugging workflows

    Why it matters:
        Extraction quality can be reviewed, measured, and improved instead of treated as a black box.

Relationship Modeling

    What the system can do:
        Represent entities and relationships explicitly.

    Supports:
        Node → Relationship → Node

    Current domain:
        Repository Graph

    Future domains:
        - Student Graph
        - Knowledge Graph
        - Organizational Graph

    Why it matters:
        Ownership, dependency, and learning relationships can be modeled directly instead of inferred from unstructured content.

## Future Capabilities

Educational Knowledge Representation

    What the future system will be able to do:
        Represent relationships between questions, knowledge points, concepts, and curriculum structures.

    Supports:
        Question → Knowledge Point → Concept → Curriculum

    Why it matters:
        Questions can become part of a navigable educational knowledge system.

Learning Context Representation

    What the future system will be able to do:
        Represent student learning state and historical performance.

    Supports:
        Student → Attempts → Performance → Learning State

    Why it matters:
        Learning decisions can be grounded in student context rather than isolated question metadata.

Educational Decision Support

    What the future system will be able to do:
        Recommend the next best learning action from structured content and learning context.

    Supports:
        Student State + Learning Goal + Question Repository → Next Best Learning Action

    Why it matters:
        The system can move from content extraction toward adaptive educational decision making.

Context Compression

    What the future system will be able to do:
        Compress large histories into context that an LLM or decision system can use.

    Supports:
        Student Learning History → Compressed Learning Context

    Why it matters:
        Long-term learning history can influence decisions without overwhelming the reasoning system.

# Architecture

## Architectural Goal

Build a foundation that can evolve from:

    Document → Question Object

toward:

    Question + Student Context + Learning Goal → Next Best Learning Action

The current architecture focuses on educational content understanding. The future architecture expands that foundation into context-aware learning systems.

## Dynamic Flow

    PDF or Image
    → OCR Detection
    → OCR Recognition
    → Question Detection
    → Question Crop
    → VLM Parsing
    → Question Object
    → Export

## Static Structure

Document Layer

    Responsibilities:
        Ingest educational documents and normalize them into processable page or image representations.

    Core components:
        PDF ingestion, image normalization, document representation

Localization Layer

    Responsibilities:
        Locate text regions, question boundaries, and diagram regions.

    Core components:
        OCR Detection, Question Detection, Diagram Detection

Semantic Extraction Layer

    Responsibilities:
        Convert localized content into structured educational meaning.

    Core components:
        VLM Parsing, Question Object Generation

Observability Layer

    Responsibilities:
        Make extraction behavior visible, measurable, and debuggable.

    Core components:
        Audit Artifacts, Preview Generation, Metrics, Cost Tracking, Latency Tracking

Relationship Layer

    Responsibilities:
        Represent ownership, dependency, and domain relationships.

    Core components:
        Entity Registry, Dependency Mapping, Graph Runtime

Decision Layer (Future)

    Responsibilities:
        Select learning actions from student context, learning goals, and available question assets.

    Core components:
        Student State, Learning Goal, Question Repository, Next Best Action

# Stories

## Core Discovery

Model Boundaries Before Understanding

    The recurring architectural discovery was that extraction quality depends on explicit boundaries:
        - tool boundaries between localization and semantic understanding
        - ownership boundaries between questions and diagrams
        - domain boundaries between content, context, goals, and decisions

## Story: OCR Extraction — Separate Localization From Understanding

Career Spine: information-modeling, systems
Advanced Themes: automation, ai-systems

Problem

    Before:
        OCR was expected to power the extraction pipeline end to end.

    Consequences:
        - question ownership across pages remained difficult to resolve
        - mathematical notation could not be reliably converted into structured expressions
        - recognition costs increased even when the system only needed location
        - recognition latency slowed the pipeline

Discovery

    Localization and understanding are different concerns.
    OCR Detection can answer where content is.
    OCR Recognition should be used only when recognized text is required.

Outcome

    After:
        OCR became primarily a localization capability.

    Benefits:
        - resolve many ownership problems through coordinates
        - avoid recognition cost when localization is sufficient
        - reduce latency in stages that do not require full text recognition
        - create a foundation for hybrid extraction

---

## Story: VLM Extraction — Assign Tools By Capability Boundary

Career Spine: information-modeling, systems
Advanced Themes: ai-systems

Problem

    Before:
        VLMs were tested as a replacement for localization and semantic extraction.

    Consequences:
        - full-page understanding was inconsistent
        - generated bounding boxes were difficult to trust
        - question localization remained unstable
        - diagram localization could not be governed reliably

Discovery

    VLMs are stronger at semantic understanding than deterministic localization.
    Tool selection should follow capability boundaries rather than preference for one model family.

Outcome

    After:
        VLMs became responsible for semantic extraction.
        Localization responsibilities moved to more deterministic stages.

    Benefits:
        - preserve VLM strengths for question meaning and structure
        - improve trust in location-sensitive outputs
        - make extraction behavior easier to audit

---

## Story: Diagram Ownership — Model Relationships Before Cropping

Career Spine: information-modeling, workflow
Advanced Themes: automation, ai-systems

Problem

    Before:
        Diagram extraction was treated as a standalone detection problem.

    Consequences:
        - diagrams could be detected without clear question ownership
        - crops could be correct locally but ambiguous in the question object
        - downstream outputs could not reliably attach diagrams to the right question

Discovery

    Diagram ownership is not only a diagram problem.
    Ownership originates from question boundaries and relationships between extracted entities.

Outcome

    After:
        Diagram extraction became part of relationship modeling between questions and owned assets.

    Benefits:
        - attach diagrams to the correct question
        - evaluate extraction quality at the question-object level
        - reduce ambiguity in exported assets

---

## Story: Learning Direction — Move From Question Objects To Decisions

Career Spine: information-modeling, systems
Advanced Themes: ai-systems

Problem

    Before:
        The project focused on producing structured question assets.

    Consequences:
        - extracted questions did not explain what a student should do next
        - learning history was not represented as decision context
        - learning goals were not connected to available questions

Discovery

    Question structure is a foundation, not the final decision.
    Learning systems require explicit representations of state, goals, options, and feedback.

Outcome

    After:
        The project direction expanded from content extraction toward educational decision support.

    Benefits:
        - connect questions to learning goals
        - use student state as decision context
        - prepare the architecture for next-best-action recommendations
