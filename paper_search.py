import arxiv
import random
from typing import List, Dict
from datetime import datetime, timedelta

class PaperSearcher:
    def __init__(self):
        self.safety_keywords = [
            "LLM safety", "language model safety", "AI alignment", 
            "jailbreak", "adversarial prompts", "red teaming",
            "constitutional AI", "RLHF", "safety fine-tuning",
            "harmful content detection", "AI safety evaluation",
            "model robustness", "prompt injection", "safety guardrails"
        ]
        
    def search_papers(self, max_results: int = 50) -> List[Dict]:
        """Search for LLM safety related papers from arXiv"""
        papers = []
        
        # Use multiple search queries to get diverse papers
        search_queries = [
            "LLM safety alignment",
            "jailbreak language model",
            "adversarial prompt attack",
            "AI safety evaluation",
            "harmful content detection LLM"
        ]
        
        for query in search_queries:
            search = arxiv.Search(
                query=query,
                max_results=max_results // len(search_queries),
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for paper in search.results():
                # Check if paper is related to LLM safety
                if self._is_safety_related(paper):
                    paper_info = {
                        'title': paper.title,
                        'authors': [author.name for author in paper.authors],
                        'summary': paper.summary,
                        'pdf_url': paper.pdf_url,
                        'published': paper.published,
                        'arxiv_id': paper.entry_id
                    }
                    papers.append(paper_info)
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_papers = []
        for paper in papers:
            if paper['title'] not in seen_titles:
                seen_titles.add(paper['title'])
                unique_papers.append(paper)
        
        return unique_papers
    
    def _is_safety_related(self, paper) -> bool:
        """Check if a paper is related to LLM safety"""
        text_to_check = (paper.title + " " + paper.summary).lower()
        
        # Check for safety-related keywords
        safety_terms = ["safety", "alignment", "harmful", "jailbreak", "adversarial", 
                       "attack", "robust", "secure", "toxic", "bias", "ethics", 
                       "responsible", "risk", "mitigation", "defense", "guardrail"]
        
        llm_terms = ["language model", "llm", "gpt", "chatbot", "transformer", 
                    "bert", "claude", "gemini", "llama", "foundation model"]
        
        has_safety = any(term in text_to_check for term in safety_terms)
        has_llm = any(term in text_to_check for term in llm_terms)
        
        return has_safety and has_llm
    
    def filter_unreviewed_papers(self, papers: List[Dict], reviewed_file: str) -> List[Dict]:
        """Filter out papers that have already been reviewed"""
        try:
            with open(reviewed_file, 'r', encoding='utf-8') as f:
                reviewed_titles = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
        except FileNotFoundError:
            reviewed_titles = set()
        
        unreviewed = [p for p in papers if p['title'] not in reviewed_titles]
        return unreviewed