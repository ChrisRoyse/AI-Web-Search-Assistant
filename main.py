"""
Main entry point for the AI Web Search Assistant.
"""
import json
from typing import List, Dict
import settings
from deepseek_client import DeepSeekClient
from discovery import SearchDiscovery

class AIWebSearchAssistant:
    def __init__(self):
        """Initialize the AI Web Search Assistant."""
        self.llm = DeepSeekClient()
        self.discovery = SearchDiscovery()
        self.all_results = []

    def interpret_user_query(self, query: str) -> Dict:
        """Interpret and analyze the user's query using DeepSeek."""
        print("\n🤔 Analyzing your query...")
        interpretation = json.loads(self.llm.interpret_query(query))
        
        print("\n📝 Query Analysis:")
        print(f"• Interpreted Intent: {interpretation['interpreted_intent']}")
        print("\n• Suggested Improvements:")
        for improvement in interpretation['suggested_improvements']:
            print(f"  - {improvement}")
        
        return interpretation

    def perform_search_rounds(self, original_query: str, interpretation: Dict) -> List[str]:
        """Perform multiple rounds of searching with refinement."""
        all_results = []
        current_query = original_query

        for round_num in range(1, settings.MAX_SEARCH_ROUNDS + 1):
            print(f"\n🔍 Search Round {round_num}/{settings.MAX_SEARCH_ROUNDS}...")
            
            # Perform search
            round_results = self.discovery.perform_search_round(current_query)
            
            # Add new results to accumulated results
            all_results.extend(round_results)
            self.llm.accumulated_results.extend(round_results)  # Add to LLM's accumulated results
            
            # If not the last round, analyze results and get new queries
            if round_num < settings.MAX_SEARCH_ROUNDS:
                print("🔄 Analyzing all accumulated results and generating new search query...")
                new_queries = self.llm.analyze_search_results(all_results, round_num)
                
                # Use the first suggested query for the next round
                if new_queries:
                    current_query = new_queries[0]
                    print(f"📌 Next round query: {current_query}")
        
        return all_results

    def generate_final_summary(self, query: str, all_results: List[str]) -> str:
        """Generate a comprehensive summary of all findings."""
        print("\n✍️ Generating final summary...")
        return self.llm.generate_final_summary(all_results, query)

    def run(self):
        """Main execution flow of the assistant."""
        print("🔎 Welcome to the AI Web Search Assistant!")
        print("=" * 50)
        
        while True:
            # Get user query
            query = input("\n🤔 Enter your search topic: ").strip()
            
            if not query:
                print("❌ Error: Please enter a valid search query.")
                continue
            
            try:
                # Interpret query
                interpretation = self.interpret_user_query(query)
                
                # Ask if user wants to refine the query
                while True:
                    refine = input("\n🔄 Would you like to add any of these suggested improvements to your query? (yes/no): ").strip().lower()
                    if refine in ['yes', 'y']:
                        print("\n✏️ What would you like to add to your query? (Your original query was:")
                        print(f'"{query}"')
                        additions = input("Additional details: ").strip()
                        if additions:
                            # Combine original query with additions
                            query = f"{query} {additions}"
                            # Re-interpret the refined query
                            interpretation = self.interpret_user_query(query)
                        else:
                            print("❌ No additions provided, using original query.")
                    elif refine in ['no', 'n']:
                        break
                    else:
                        print("❌ Please answer 'yes' or 'no'")
                        continue
                    break
                
                # Perform search rounds
                all_results = self.perform_search_rounds(query, interpretation)
                
                # Generate and display final summary
                summary = self.generate_final_summary(query, all_results)
                
                print("\n📊 Final Summary:")
                print("=" * 50)
                print(summary)
                print("=" * 50)
                
                # Ask if user wants to perform another search
                while True:
                    another = input("\n🔄 Would you like to perform another search? (yes/no): ").strip().lower()
                    if another in ['yes', 'y']:
                        break
                    elif another in ['no', 'n']:
                        print("\n👋 Thank you for using AI Web Search Assistant!")
                        return
                    else:
                        print("❌ Please answer 'yes' or 'no'")
                
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                print("Please try again or contact support if the problem persists.")

def main():
    """Entry point of the program."""
    assistant = AIWebSearchAssistant()
    assistant.run()

if __name__ == "__main__":
    main() 