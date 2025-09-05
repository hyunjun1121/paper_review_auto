# Paper Review Automation

Automated paper review generator for LLM Safety research papers.

## Features

- Automatically searches for LLM safety papers from arXiv
- Generates 10 reviews per execution
- Prevents duplicate reviews by tracking reviewed papers
- Saves reviews in markdown format with timestamp-based folders
- Uses Google Gemini 2.5 Pro for high-quality review generation

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your API key:
```bash
# For Google Gemini
export GEMINI_API_KEY="your-api-key-here"
```

Note: The application includes a default API key for testing purposes.

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Search for LLM safety papers from arXiv
2. Filter out previously reviewed papers
3. Generate 10 reviews (or less if fewer unreviewed papers are available)
4. Save reviews in `./result/YYYY-MM-DD_HH-MM-SS/` folder
5. Update the `reviewed_papers.txt` file to track reviewed papers

## Output

Reviews are saved as markdown files in the format:
- `./result/[date]/01_[paper_title].md`
- `./result/[date]/02_[paper_title].md`
- ...

Each review follows the GlitchIQ blog post format with sections for:
- Introduction
- Core Methodology
- Key Strengths & Contributions
- Implications and Future Directions
- Limitations
- Final Verdict

## Files

- `main.py` - Main execution script
- `paper_search.py` - arXiv paper search functionality
- `duplicate_checker.py` - Tracks reviewed papers
- `review_generator.py` - Generates reviews using LLM
- `reviewed_papers.txt` - List of already reviewed papers
- `requirements.txt` - Python dependencies