import os
import sys
import random
from datetime import datetime
from pathlib import Path
import time

from paper_search import PaperSearcher
from duplicate_checker import DuplicateChecker
from review_generator import ReviewGenerator

def main():
    """Main function to generate 10 paper reviews"""
    
    # Configuration
    NUM_REVIEWS = 10
    REVIEWED_FILE = "reviewed_papers.txt"
    
    # Create output directory with today's date
    today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("result") / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting paper review generation...")
    print(f"Output directory: {output_dir}")
    print("-" * 50)
    
    # Initialize components
    searcher = PaperSearcher()
    checker = DuplicateChecker(REVIEWED_FILE)
    
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyDOiNo_lWkMaDbodN8WCj2PBe31hNn375o")
    
    if not api_key:
        print("Warning: No API key found. Using fallback review generation.")
        print("Set GEMINI_API_KEY environment variable for better results.")
        print("-" * 50)
    
    generator = ReviewGenerator(api_key=api_key)
    
    # Search for papers
    print("Searching for LLM safety papers...")
    all_papers = searcher.search_papers(max_results=100)
    
    # Filter out already reviewed papers
    unreviewed_papers = searcher.filter_unreviewed_papers(all_papers, REVIEWED_FILE)
    
    print(f"Found {len(all_papers)} papers total")
    print(f"Found {len(unreviewed_papers)} unreviewed papers")
    print("-" * 50)
    
    if len(unreviewed_papers) < NUM_REVIEWS:
        print(f"Warning: Only {len(unreviewed_papers)} unreviewed papers available.")
        NUM_REVIEWS = len(unreviewed_papers)
    
    # Randomly select papers for review
    papers_to_review = random.sample(unreviewed_papers, min(NUM_REVIEWS, len(unreviewed_papers)))
    
    # Generate reviews
    successful_reviews = 0
    for i, paper in enumerate(papers_to_review, 1):
        print(f"\n[{i}/{NUM_REVIEWS}] Processing: {paper['title'][:80]}...")
        
        try:
            # Generate review
            review_content = generator.generate_review(paper)
            
            # Save review to file
            safe_filename = "".join(c for c in paper['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_filename = safe_filename[:100]  # Limit filename length
            review_file = output_dir / f"{i:02d}_{safe_filename}.md"
            
            with open(review_file, 'w', encoding='utf-8') as f:
                f.write(review_content)
            
            # Mark as reviewed
            checker.mark_as_reviewed(paper['title'])
            
            print(f"  ✓ Review saved: {review_file.name}")
            successful_reviews += 1
            
            # Add a small delay to avoid rate limiting
            if api_key:
                time.sleep(2)
                
        except Exception as e:
            print(f"  ✗ Error generating review: {e}")
            continue
    
    # Summary
    print("\n" + "=" * 50)
    print(f"SUMMARY")
    print(f"Successfully generated {successful_reviews}/{NUM_REVIEWS} reviews")
    print(f"Reviews saved in: {output_dir.absolute()}")
    print(f"Total papers reviewed to date: {checker.get_reviewed_count()}")
    print("=" * 50)

if __name__ == "__main__":
    main()