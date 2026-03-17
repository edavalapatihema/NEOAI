import pandas as pd
import argparse
import os
import json
from tqdm import tqdm
import random
from typing import Dict, List, Optional


CATEGORIES = [
    "Access Issue",
    "Hardware",
    "Software/Bug",
    "Data Integrity",
    "Feature Request",
    "How-to/Guidance",
    "Billing/Invoice"
]

URGENCY_LEVELS = ["Low", "Medium", "High", "Critical"]

TEAMS = [
    "IT Support",
    "Engineering - Core Platform",
    "Engineering - Data",
    "HR Operations",
    "Finance",
    "Customer Success"
]

class EnrichmentTool:
    def __init__(self, requests_path: str, kb_path: str, output_path: str, use_mock: bool = True):
        self.requests_path = requests_path
        self.kb_path = kb_path
        self.output_path = output_path
        self.use_mock = use_mock
        
        
        print(f"Loading data from {requests_path}...")
        self.df_requests = pd.read_csv(requests_path)
        print(f"Loaded {len(self.df_requests)} requests.")
        
        if os.path.exists(kb_path):
            self.df_kb = pd.read_csv(kb_path)
            print(f"Loaded {len(self.df_kb)} KB articles.")
        else:
            self.df_kb = pd.DataFrame()
            print("Warning: KB articles file not found.")

    def run(self):
        """Main execution loop."""
        print("Starting enrichment process...")
        
        
        new_cols = ['predicted_category', 'predicted_urgency', 'recommended_team', 'suggested_action']
        for col in new_cols:
            if col not in self.df_requests.columns:
                self.df_requests[col] = None

       
        results = []
        for index, row in tqdm(self.df_requests.iterrows(), total=len(self.df_requests)):
            context = self._prepare_context(row)
            
            if self.use_mock:
                enrichment = self._mock_inference(context)
            else:
                enrichment = self._llm_inference(context)
            
            results.append(enrichment)

        
        enriched_df = pd.DataFrame(results)
        for col in new_cols:
            self.df_requests[col] = enriched_df[col]

       
        print(f"Saving enriched data to {self.output_path}...")
        self.df_requests.to_csv(self.output_path, index=False)
        print("Done!")

    def _prepare_context(self, row) -> str:
        
       
        return f"Subject: {row.get('request_type', 'N/A')}\nDescription: {row.get('description', '')}\nImpact: {row.get('business_impact', '')}"

    def _mock_inference(self, context: str) -> Dict[str, str]:
        
        
        lower_context = context.lower()
        
        
        if "password" in lower_context or "login" in lower_context or "sso" in lower_context:
            category = "Access Issue"
        elif "invoice" in lower_context or "billing" in lower_context:
            category = "Billing/Invoice"
        elif "error" in lower_context or "bug" in lower_context or "fail" in lower_context:
            category = "Software/Bug"
        elif "data" in lower_context or "import" in lower_context:
            category = "Data Integrity"
        elif "how to" in lower_context or "guidance" in lower_context:
            category = "How-to/Guidance"
        else:
            category = "Feature Request"

       
        if "critical" in lower_context or "deadline" in lower_context or "outage" in lower_context:
            urgency = "Critical"
        elif "high" in lower_context or "unable to" in lower_context:
            urgency = "High"
        else:
            urgency = "Medium"

       
        if category == "Access Issue":
            team = "IT Support"
        elif category == "Billing/Invoice":
            team = "Finance"
        elif category == "Software/Bug":
            team = "Engineering - Core Platform"
        elif category == "Data Integrity":
            team = "Engineering - Data"
        else:
            team = "Customer Success"

       
        if category == "Access Issue":
            action = "Reset MFA and verify IdP logs."
        elif category == "Billing/Invoice":
            action = "Check contract SKU limit and validity."
        elif category == "Software/Bug":
            action = "Check logs for stack traces and known regressions."
        else:
            action = "Review KB articles and escalate if needed."

        return {
            'predicted_category': category,
            'predicted_urgency': urgency,
            'recommended_team': team,
            'suggested_action': action
        }

    def _llm_inference(self, context: str) -> Dict[str, str]:
       
        
       
        return self._mock_inference(context) 

    def chat_mode(self):
        
        print("\n" + "="*50)
        print("🤖 AI Triage Assistant (CLI Chat)")
        print("Type 'exit' to quit.")
        print("="*50 + "\n")

        # Ensure we have enriched data in memory (run enrichment if needed, or load existing)
        if 'predicted_category' not in self.df_requests.columns:
            print("Enriching data first...")
            self.run() 

        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue

                if self.use_mock:
                    response = self._mock_chat_response(user_input)
                else:
                    response = self._llm_chat_response(user_input)
                
                print(f"Bot: {response}\n")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

    def _mock_chat_response(self, query: str) -> str:
        
        query = query.lower()
        
        
        if "how many" in query or "count" in query:
            if "critical" in query:
                count = len(self.df_requests[self.df_requests['predicted_urgency'] == 'Critical'])
                return f"There are {count} Critical requests currently."
            elif "access" in query:
                count = len(self.df_requests[self.df_requests['predicted_category'] == 'Access Issue'])
                return f"There are {count} Access Issues reported."
            else:
                return f"I have {len(self.df_requests)} total requests in the queue."

        
        if "finance" in query:
            count = len(self.df_requests[self.df_requests['recommended_team'] == 'Finance'])
            
            sample = self.df_requests[self.df_requests['recommended_team'] == 'Finance'].iloc[0]['description'][:50]
            return f"The Finance team has {count} assigned tickets. Example: '{sample}...'"
        
        if "it support" in query:
            count = len(self.df_requests[self.df_requests['recommended_team'] == 'IT Support'])
            return f"IT Support has {count} assigned tickets."

        
        if "login" in query or "sso" in query:
            return "For login issues, I usually recommend resetting MFA or checking IdP logs. Do you want to list the active tickets?"

       
        keywords = [w for w in query.split() if len(w) > 3] 
        if not keywords:
             return "Please ask a more specific question about the support tickets."

        # Look for any keyword match
        mask = self.df_requests['description'].str.contains('|'.join(keywords), case=False, na=False)
        matches = self.df_requests[mask]

        if not matches.empty:
            count = len(matches)
            top = matches.head(3)
            summary = "\n".join([f"- {row['request_id']} ({row['predicted_category']}): {row['description'][:60]}..." for _, row in top.iterrows()])
            return f"I found {count} tickets related to your query:\n{summary}\n..."
        
        return "I'm a mock AI engine. I didn't find those keywords in the dataset. Try asking about 'slow', 'invoice', 'error', etc."

    def _llm_chat_response(self, query: str) -> str:
        """Placeholder for real Chat completion."""
        
        return self._mock_chat_response(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enrich support requests using AI (or Mock AI).")
    parser.add_argument("--input", default="requests.csv", help="Path to input CSV")
    parser.add_argument("--kb", default="kb_articles.csv", help="Path to KB CSV")
    parser.add_argument("--output", default="requests_enriched.csv", help="Path to output CSV")
    parser.add_argument("--real-ai", action="store_true", help="Use real LLM instead of mock heuristics")
    parser.add_argument("--chat", action="store_true", help="Start in conversational CLI mode")
    
    args = parser.parse_args()
    
    tool = EnrichmentTool(
        requests_path=args.input,
        kb_path=args.kb,
        output_path=args.output,
        use_mock=not args.real_ai
    )

    if args.chat:
        tool.chat_mode()
    else:
        tool.run()
