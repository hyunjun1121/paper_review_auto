import os
from typing import Set

class DuplicateChecker:
    def __init__(self, reviewed_file: str = "reviewed_papers.txt"):
        self.reviewed_file = reviewed_file
        self.reviewed_papers = self._load_reviewed_papers()
    
    def _load_reviewed_papers(self) -> Set[str]:
        """Load the list of already reviewed papers"""
        if not os.path.exists(self.reviewed_file):
            return set()
        
        reviewed = set()
        with open(self.reviewed_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    reviewed.add(line)
        return reviewed
    
    def is_reviewed(self, paper_title: str) -> bool:
        """Check if a paper has been reviewed"""
        return paper_title in self.reviewed_papers
    
    def mark_as_reviewed(self, paper_title: str):
        """Mark a paper as reviewed"""
        if paper_title not in self.reviewed_papers:
            self.reviewed_papers.add(paper_title)
            with open(self.reviewed_file, 'a', encoding='utf-8') as f:
                f.write(f"{paper_title}\n")
    
    def get_reviewed_count(self) -> int:
        """Get the number of reviewed papers"""
        return len(self.reviewed_papers)