 HEY BUDDIES , THIS IS THE SMALL POC WHICH I WORKED , TRY TO UNDERSTAND THE POC , THEN CLONE IT  

Collabs are always welcome

Context
-------
You have joined an internal AI Solutions Engineering function supporting an operations/support organization.
A stakeholder says: "Here’s our dataset. I need to pull information from it and make it useful."
Your task is to take an ambiguous ask and deliver a scoped, usable outcome.

Data Provided
-------------
- requests.csv      : 260 anonymized support/ops requests with structured + unstructured fields
- kb_articles.csv   : anonymized knowledge base articles (optional to use for retrieval/RAG)
- data_dictionary.csv : definitions of all fields

Business goals (intentionally broad)
-----------------------------------
The stakeholder wants to:
1) Reduce time spent routing and triaging incoming requests,
2) Identify high-impact recurring issues and automation opportunities,
3) Produce a weekly executive-ready summary that highlights trends, risks, and actions.

Your tasks
----------
A) Clarify and scope:
   - List the questions you would ask.
   - If answers are not available, state assumptions.

B) Propose a solution:
   - Provide an architecture/workflow that uses AI where appropriate.
   - Address reliability (hallucination control), privacy, and evaluation.

C) Build a working proof-of-concept (choose one):
   Option 1: A script/notebook that enriches requests.csv with:
     - category (your taxonomy), urgency, recommended owner team, and a short "next best action"
   Option 2: A lightweight app or CLI that supports:
     - ad-hoc question answering over requests + KB
   Option 3: A dashboard-style report (can be a markdown/pdf) with:
     - top drivers, trend analysis, and clear recommendations

D) Show your work:
   - Include a short build log (iterations, failures, decisions, evaluation approach).
   - Include prompt versions if you use LLMs.

Constraints
-----------
- Do not use any real customer data; only the provided anonymized data.
- You may use any tools, but you must be able to explain and defend your approach.
- Prioritize repeatability: another engineer should be able to re-run your workflow.



This is designed to be completable in ~3–6 hours. If you choose to go further, explain what you would do next and why.

Good luck.
