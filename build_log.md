# Build Log & Trade-offs

## Decisions Made
1.	Selection of Option 1 (Enrichment Script): Chosen because it best aligns with the business goal of "reducing time spent triaging." Automatic classification directly speeds up the workflow.

2.	Mock Mode vs. Live API: Implemented a "Mock Mode" using keyword heuristics.
•	Why? Ensures the code is runnable immediately by anyone without needing an OpenAI API key.
•	Trade-off: Accuracy is limited to the quality of my keywords (e.g., might miss subtle "access" issues that don't say "login").

3.	Taxonomy Definitions: Created a strict set of Categories and Teams in the code (CATEGORIES, TEAMS).
•	Why? To prevent "hallucinations" where an LLM might invent teams that don't exist.


## Implementation Details
 File: 'enrichment_tool.py'
 Logic:
    •	Combined request_type, description, and business_impact into a context string.
•	Used conditional logic (If "password" in text -> Category="Access Issue" -> Team="IT Support") to simulate the "Reasoning" step.
•	Outputs a standard CSV compatible with Excel/Sheets.


## Verification
Test Run: Processed 260 rows in <1 second.
Spot Check:
    •	Request: "Users can't log in via SSO"
•	Prediction: Category="Access Issue", Urgency="Critical", Team="IT Support".
•	Result: accurate.
•	Request: "Trial ended earlier than expected"
•	Prediction: Category="Billing/Invoice", Team="Finance".
•	Result: accurate.


## Future Improvements
1.  RAG Integration: Actually index the 'kb_articles.csv' (using TF-IDF or Embeddings) to provide the "specific" Article ID in the 'suggested_action' column.
2.  Feedback Loop: Add a mechanism for users to correct the 'predicted_category' in the UI, and feed that back into few-shot examples.


Timebox Note: This PoC was completed in approximately 4 hours, respecting the constraints.