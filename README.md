# 🎯 Synthetic Persona Pre-Test
## Marketing Innovation at Your Fingertips
Transform your marketing campaign testing with AI-powered synthetic personas. Pre-test your marketing content against detailed customer personas before launch, reducing risk and maximizing campaign effectiveness.

Why Use Synthetic Persona Pre-Test?

- Reduce Campaign Risk: Test messaging before investing in full campaign rollouts
- Save Time and Resources: Get instant feedback on campaign materials
- Refine Targeting: Understand how different customer segments respond to your content
- Optimize Content: Fine-tune messaging based on persona-specific insights
- Validate Assumptions: Test your marketing hypotheses with synthetic but realistic customer profiles

Perfect For:

- Marketing Managers seeking data-driven campaign validation
- Content Creators needing quick feedback on messaging
- Brand Managers wanting to ensure brand consistency
- Digital Marketing Teams optimizing multi-channel content
- Social Media Managers testing content effectiveness

Key Features

- Customizable persona profiles based on real customer data
- Instant feedback on marketing content
- Visual content analysis capabilities
- Detailed persona-specific insights
- Easy-to-use interface for quick testing

### Project Structure
```
AI_PERSONA/
├── apps/
│   ├── ai_persona.py
│   └── test.py
├── configs/
│   └── .env
├── images/
│   └── do_not_buy.png
├── .gitignore
└── requirements.txt
```

### Setup and Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI_PERSONA.git
cd AI_PERSONA
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the `configs` directory with:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run apps/ai_persona.py
```

### Key Components
- `apps/ai_persona.py`: Main application file containing the Streamlit interface
- `apps/test.py`: Test suite for application functionality
- `configs/.env`: Configuration file for environment variables
- `images/`: Directory for storing test images and assets

