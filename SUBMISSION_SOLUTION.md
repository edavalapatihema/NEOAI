# Automation PoC: Support Triage Tool

## Context
For this assessment, I focused on Option 1 (Automated Enrichment)because accurate tagging is the upstream bottleneck that affects everything else (routing, reporting, and resolution time).

My goal was to build a tool that could immediately start reducing triage time without needing complex infrastructure.

## What's Included
1.  **enrichment_tool.py**: The script I wrote to process the CSVs.
2.  **requests_enriched.csv**: The output file with my added tags (Category, Urgency, Team, Action).
3.  **analysis.md**: My initial notes on scoping and design choices.
4.  **build_log.md**: A quick log of decisions I made while coding.

## Quick Start
I've included a **requirements.txt**, but really you just need "pandas"  and "tqdm" .

1.  **Install**:
    in Terminal
    pip install pandas tqdm openai
    
2.  **Run the processing**:
    in Terminal
    python enrichment_tool.py
    
    This reads **requests.csv** and outputs **requests_enriched.csv**.
    Note: It runs in a "Mock Mode" by default using keyword logic I wrote, so you don't need an API key to test it.

3.  **Run the Chat Bot (Bonus)**:
    in Terminal
    python enrichment_tool.py --chat
    
    I added this CLI feature out of personal curiosity to demonstrate how the future-state "Conversational AI" would feel. It allows you to query the dataset naturally.

## My Approach
I initially considered using a full LLM for everything, but for a potentially high-volume triage system, cost and latency are real concerns.

**Why Mock Mode?** I wanted this code to be runnable by anyone reviewing it, immediately. I designed the architecture so the "inference" step is isolated—right now it uses regex/keywords, but it's one function change to swap in GPT-4 or Claude.

**Structure:** I enforced a strict list of Categories and Teams. One risk with LLMs is they "invent" teams (e.g. "Engineering , Login Team"). My script forces the output to match the company's org chart.

## Trade-offs
**Accuracy vs. Complexity:** The current keyword logic is fast but misses nuance. A real LLM implementation would be better at catching "implied" urgency.
**Chat:** The chat is a simple keyword search right now. In a real production version, I'd throw the ticket embeddings into a vector store (like Pinecone) for semantic search.
