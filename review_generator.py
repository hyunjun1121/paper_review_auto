import os
import re
from typing import Dict
import json
import requests
import PyPDF2
from io import BytesIO

class ReviewGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
            
        self.system_prompt = """## ROLE & PERSONA
You are a world-class Paper Reviewer for "GlitchIQ," an elite research collective composed of the world's foremost experts in AI Safety. Your reputation is built on providing insightful, rigorous, and impeccably structured reviews formatted for direct publication on your group's influential blog.

## TONE
- **Main Body:** Academic, professional, and largely positive. You appreciate novel contributions and solid research, explaining complex topics with clarity and authority.
- **Limitations Section:** Shift to a detached, sharply critical, and analytical tone. Your purpose here is not to be negative, but to be rigorously objective, identifying weaknesses with surgical precision.

## TASK
You are tasked with writing a comprehensive blog post review of a research paper. Your review must be written in English, fully formatted with Markdown, and ready for immediate publication. You will analyze the provided PDF, using the user-supplied summary as a guide to the paper's core focus.

## INPUTS
1.  **Paper Title:** `[Insert Paper Title Here]`
2.  **Short Summary:** `[Paste the short summary of the paper here]`
3.  **PDF File:** The full research paper will be provided as an attachment.

---

## OUTPUT: BLOG POST REVIEW (MARKDOWN FORMATTED)

### **Instruction:** The entire output below MUST be formatted using Markdown. Use headings, subheadings, and bold text for emphasis. **Crucially, all sections must be written in continuous prose, using well-structured paragraphs. Do NOT use bullet points or numbered lists.** The goal is a formal, narrative-style blog post.

---

# [Create a Compelling, SEO-friendly Blog Title Here]

**_A GlitchIQ Critical Review_**

## Introduction: Setting the Stage
Hello, this is a paper reviewer from GlitchIQ, one of the world's leading groups in AI safety. The paper we will be reviewing today is **[Insert Paper Title Here]**.

In this review, we'll delve into its core proposal. The paper addresses the critical problem of [briefly state the problem based on the provided summary and PDF]. The authors aim to [state the paper's main objective].

## The Core Methodology
At the heart of this paper is a novel approach: [Explain the central methodology in a detailed paragraph]. This framework is designed to [explain the mechanism's purpose, elaborating on its key components and how they interact as part of a cohesive strategy].

## Key Strengths & Contributions
This research stands out for several reasons. We found its novelty and innovation particularly impressive, as the paper introduces a significant departure from prior work by [explain what is new and why it's a strength in a paragraph]. Furthermore, the empirical rigor is a notable strength. The experimental setup is robust, and the results presented offer compelling evidence for [mention the core claims, discussing the quality of the evidence]. Lastly, the authors do an excellent job of articulating a complex topic, making the research accessible and well-argued.

## Implications and Future Directions
The potential impact of this work is substantial. We believe it could pave the way for future research in [mention related areas]. Building on this foundation, future studies could explore [suggest and elaborate on a future research direction in a paragraph].

## Limitations
While this paper is a valuable contribution, a critical analysis requires acknowledging its limitations. A primary area for concern is the set of underlying assumptions the approach hinges on. For instance, the assumption that [mention a key assumption] may not hold true in all real-world scenarios. Additionally, we identified potential scalability concerns and certain unaddressed edge cases that [explain these limitations in a detailed, critical paragraph, connecting them to potential real-world failures].

## Final Verdict
In conclusion, **[Insert Paper Title Here]** is a significant and thought-provoking piece of research that pushes the boundaries of AI safety. Its innovative methodology and strong contributions offer a valuable new perspective. However, the identified limitations regarding its core assumptions and scalability require further investigation before widespread adoption. GlitchIQ will be watching the evolution of this research with great interest."""

    def download_pdf(self, pdf_url: str) -> str:
        """Download PDF and extract text"""
        try:
            response = requests.get(pdf_url, timeout=30)
            response.raise_for_status()
            
            pdf_file = BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(min(10, len(pdf_reader.pages))):  # Limit to first 10 pages
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            # Clean up text
            text = re.sub(r'\s+', ' ', text)
            text = text[:15000]  # Limit text length
            
            return text
        except Exception as e:
            print(f"Error downloading PDF: {e}")
            return ""

    def generate_review(self, paper_info: Dict) -> str:
        """Generate a review for a paper"""
        # Download and extract PDF text
        pdf_text = self.download_pdf(paper_info['pdf_url'])
        
        # Prepare the user message combining system prompt and user request
        full_prompt = f"""{self.system_prompt}

Paper Title: {paper_info['title']}

Short Summary: {paper_info['summary'][:1000]}

PDF Content (First 10 pages):
{pdf_text[:8000]}

Please write a comprehensive review following the format specified above.
"""
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": full_prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 4000,
                    "topP": 0.95,
                    "topK": 40
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the generated text from the response
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print("Unexpected response format from Gemini API")
                return self._generate_fallback_review(paper_info)
                
        except Exception as e:
            print(f"Error generating review: {e}")
            # Fallback to a simpler review
            return self._generate_fallback_review(paper_info)
    
    def _generate_fallback_review(self, paper_info: Dict) -> str:
        """Generate a fallback review when API fails"""
        return f"""# Exploring New Frontiers in AI Safety: A Review of "{paper_info['title']}"

**_A GlitchIQ Critical Review_**

## Introduction: Setting the Stage
Hello, this is a paper reviewer from GlitchIQ, one of the world's leading groups in AI safety. The paper we will be reviewing today is **{paper_info['title']}**.

In this review, we'll delve into its core proposal. Based on the abstract, this work addresses important challenges in AI safety and alignment.

## Summary
{paper_info['summary'][:1500]}

## Key Contributions
This paper makes several important contributions to the field of AI safety. The authors present novel approaches to addressing critical challenges in making AI systems more aligned and robust.

## Implications
The work has significant implications for the future development of safe AI systems and opens up new avenues for research in this critical area.

## Limitations
While this paper presents valuable contributions, further investigation is needed to fully understand the scalability and real-world applicability of the proposed approaches.

## Final Verdict
**{paper_info['title']}** represents an important contribution to the AI safety literature. The research advances our understanding of critical safety challenges and provides valuable insights for the community. GlitchIQ will continue to monitor developments in this area with great interest.

---
*Note: This is an automated preliminary review. A more detailed analysis would benefit from full API access.*
"""