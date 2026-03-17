# Analysis & Scoping Notes

## Goal: Reduce triage time by enriching incoming support requests.
 1.Questions I'd Ask Stakeholders (Clarify & Scope)
To ensure the solution fits the wider ecosystem, I'd ask:

Q1 Impact: How do we quantify "high impact" recurring issues? Is it by volume, revenue at risk, or customer tier?

Q2 Ecosystem: What upstream/downstream applications are used? (e.g., JIRA, Salesforce, Slack).

Q3 SLAs: Are there defined SLAs or TATs for high-priority tickets we must adhere to?

Q4 Tooling: Is there a centralized CRM taking care of assignment/routing, or are we aggregating multiple channels?

Q5 Personas: Who oversees these metrics? (VP of Support? Engineering Leads?).

Q6 Process: How does current routing work? Is there roster management or manual dispatch?

Q7 Incentives: How is the support team encouraged? (Resolution time? CSAT?).

Q8 Feedback: Is there an NPS mechanism in place we can correlate with?

 ## 2. Assumptions I Made
•	Environment: I assume there is a centralized CRM that handles the actual routing/assignment. My tool acts as an enrichment layer feeding into that.

•  Immediate Value: As an immediate "AI Infusion," I assumed a Conversational AI / Chatbot capability (simulated in my PoC) is the highest value add to ask questions against KB articles and history.

•	Long Term: Eventually, we will look at automating downstream actions using a combination of AI and RPA tools.

•	Data: requests.csv is anonymized, but in production, we'd need RBAC and PII masking.

## 3. Proposed Solution Architecture

While the PoC uses a heuristic "Mock Mode," the target architecture is:

1.	Vector Embeddings: For all structured/unstructured data (Requests + KB), create vector embeddings using OpenAI models.
2.	RAG Implementation: Implement Retrieval Augmented Generation (RAG) to support the Conversational AI. This allows the bot to "cite" specific KB articles.
3.	Roadmap: Move toward a custom SLM (Small Language Model) for specific domain tasks if costs scale too high.
Reliability, Privacy & Evaluation
•	Hallucination Control: Use RAG and Cosine Similarity to score response accuracy. Reconcile AI predictions with actual resolution status and user feedback.
•	Privacy: Mask PII/PHI data and implement RBAC-based guardrails before sending context to the model.
•	Evaluation: continuously monitor response accuracy and improve prompt engineering based on channel, role, and business impact.

## 4. PoC Implementation Details
For this specific casestudy  deliverables:
•	Batch Processing: I implemented the enrichment_tool.py to tag incoming CSV data.

•	Bonus Chatbot: I included a CLI Chat interface to demonstrate the "Conversation AI" direction mentioned in my assumptions.





