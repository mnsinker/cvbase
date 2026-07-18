# LangGraph

## Definition

LangGraph is a framework for building stateful, graph-based LLM workflows.

## Why It Exists

普通 chain 更适合固定线性流程；
复杂 Agent 需要分支、循环、状态、恢复和人工审批。

## Core Abstractions

- State
- Node
- Edge
- Conditional Edge
- Checkpoint
- Interrupt
- Subgraph

## Essential Nature

LangGraph is essentially:

State + State Transition + Runtime Control

## Key Characteristics

- Explicit state
- Conditional routing
- Cycles
- Persistence
- Human-in-the-loop
- Failure recovery
- Observability

## Related Concepts

- State Machine
- Workflow Engine
- Agent Runtime
- Event-driven System
- Durable Execution

## Interview Questions

- Why use LangGraph instead of a normal Python function?
- How does LangGraph manage state?
- When should you not use LangGraph?
- What is the difference between LangGraph and LangChain?