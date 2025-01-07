"""
DeepSeek LLM client for query interpretation and result analysis.
"""
from openai import OpenAI
from typing import List, Dict, Any
import settings

class DeepSeekClient:
    def __init__(self):
        """Initialize the DeepSeek client with API configuration."""
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            default_headers={"Content-Type": "application/json"}
        )
        self.previous_queries = []  # Track all previous queries
        self.accumulated_results = []  # Track all search results
        self.original_query = ""  # Store the original query

    def interpret_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze the user's query to understand intent and suggest improvements.
        """
        # Store the original query
        self.original_query = query
        self.previous_queries = []  # Reset for new search
        self.accumulated_results = []  # Reset for new search
        
        messages = [
            {"role": "system", "content": "You are an expert at understanding search queries and suggesting improvements."},
            {"role": "user", "content": f"Analyze this search query and suggest improvements: '{query}'\n\n"
                                      f"Return a JSON with these fields:\n"
                                      f"- original_query: the original query\n"
                                      f"- interpreted_intent: what you think the user wants to know\n"
                                      f"- suggested_improvements: list of ways to improve the query\n"
                                      f"- search_keywords: list of important keywords to focus on"}
        ]
        
        response = self.client.chat.completions.create(
            model=settings.DEEPSEEK_MODEL,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return response.choices[0].message.content

    def get_diverse_queries(self, current_results: List[str], previous_queries: List[str]) -> List[str]:
        """
        Get new search queries ensuring they are diverse and not too similar to previous ones.
        """
        messages = [
            {"role": "system", "content": "You are an expert at analyzing search results and suggesting diverse follow-up queries. "
                                        "Return exactly 3 search queries, one per line, without any additional text or explanation. "
                                        "Each query MUST stay within the user's core requirements (e.g., if they want breeder puppies, "
                                        "ONLY search for breeder-related information, NEVER suggest alternatives like adoption). "
                                        "Focus on different aspects of their specific request, such as different breeders, different "
                                        "locations within their area, or different aspects of their requirements."},
            {"role": "user", "content": f"Based on these search results, suggest 3 NEW and DIFFERENT search queries that would help gather more specific "
                                      f"information while strictly adhering to the user's core requirements. Each query should focus on a different aspect "
                                      f"but NEVER deviate from the core requirements (e.g., if they want breeder puppies, don't suggest adoption).\n\n"
                                      f"Previous queries that you should NOT repeat or be too similar to:\n"
                                      f"{previous_queries}\n\n"
                                      f"Current search results:\n{current_results}"}
        ]
        
        response = self.client.chat.completions.create(
            model=settings.DEEPSEEK_MODEL,
            messages=messages,
            temperature=0.7
        )
        
        # Split response into lines and clean up
        queries = [q.strip() for q in response.choices[0].message.content.split('\n') if q.strip()]
        return queries[:3]

    def check_query_similarity(self, new_queries: List[str], previous_queries: List[str]) -> List[bool]:
        """
        Check if new queries are too similar to previous ones.
        Returns a list of booleans indicating which queries are unique enough.
        """
        if not previous_queries:
            return [True] * len(new_queries)

        messages = [
            {"role": "system", "content": "You are an expert at analyzing query similarity. For each new query, respond with 'true' if it explores a sufficiently different aspect than all previous queries, or 'false' if it's too similar to any previous query. Respond with exactly one true/false per line."},
            {"role": "user", "content": f"Previous queries:\n{previous_queries}\n\nNew queries to check:\n{new_queries}"}
        ]

        response = self.client.chat.completions.create(
            model=settings.DEEPSEEK_MODEL,
            messages=messages,
            temperature=0.1  # Low temperature for consistent judgments
        )

        # Parse response into boolean list
        similarity_checks = [
            line.strip().lower() == 'true'
            for line in response.choices[0].message.content.split('\n')
            if line.strip().lower() in ['true', 'false']
        ]
        return similarity_checks[:len(new_queries)]

    def analyze_search_results(self, current_results: List[str], round_number: int) -> List[str]:
        """
        Analyze all accumulated search results and suggest new search queries for the next round.
        Ensures queries are diverse, build on what we've learned, and stay focused on the original goal.
        """
        max_attempts = 3
        for attempt in range(max_attempts):
            messages = [
                {"role": "system", "content": "You are an expert at analyzing search results and suggesting strategic follow-up queries. "
                                            "Based on ALL accumulated data so far, suggest a NEW search query that: \n"
                                            "1. Addresses gaps in the current information\n"
                                            "2. Builds on what we've already learned\n"
                                            "3. Stays focused on the original search goal\n"
                                            "4. Is significantly different from previous queries\n"
                                            "Return exactly ONE search query without any additional text or explanation."},
                {"role": "user", "content": f"Original search goal: {self.original_query}\n\n"
                                          f"Previous queries that you should NOT repeat or be similar to:\n"
                                          f"{self.previous_queries}\n\n"
                                          f"ALL accumulated search results so far:\n"
                                          f"{self.accumulated_results}\n\n"
                                          f"Based on this data, what's the most strategic NEW search query to help answer "
                                          f"the original question while exploring uncovered aspects?"}
            ]
            
            response = self.client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=messages,
                temperature=0.7
            )
            
            # Get the new query
            new_query = response.choices[0].message.content.strip()
            
            # Check if it's similar to previous queries
            similarity_check = self.check_query_similarity([new_query], self.previous_queries)
            
            if similarity_check[0]:  # If the query is unique enough
                self.previous_queries.append(new_query)
                return [new_query]
            
            if attempt == max_attempts - 1:
                print("⚠️ Note: Could not find a completely unique query, using best available option.")
                self.previous_queries.append(new_query)
                return [new_query]
        
        return []

    def generate_final_summary(self, all_results: List[str], original_query: str) -> str:
        """
        Generate a comprehensive summary of all search results.
        """
        messages = [
            {"role": "system", "content": "You are an expert at synthesizing information and creating comprehensive summaries."},
            {"role": "user", "content": f"Create a detailed summary answering this query: '{original_query}'\n\n"
                                      f"Based on all these search results:\n\n{all_results}"}
        ]
        
        response = self.client.chat.completions.create(
            model=settings.DEEPSEEK_MODEL,
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content 