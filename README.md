# 🎯 Synthetic Persona Pre-Test
## Marketing Innovation at Your Fingertips
Transform your marketing campaign testing with AI-powered synthetic personas. Pre-test your marketing content against detailed customer personas before launch, reducing risk and maximizing campaign effectiveness.

🔗 **Live Application**: [AI Persona Marketing](https://ai-persona-marketing-397812137944.europe-west1.run.app)

### Why Use Synthetic Persona Pre-Test?

- Reduce Campaign Risk: Test messaging before investing in full campaign rollouts
- Save Time and Resources: Get instant feedback on campaign materials
- Refine Targeting: Understand how different customer segments respond to your content
- Optimize Content: Fine-tune messaging based on persona-specific insights
- Validate Assumptions: Test your marketing hypotheses with synthetic but realistic customer profiles

### Perfect For:

- Marketing Managers seeking data-driven campaign validation
- Content Creators needing quick feedback on messaging
- Brand Managers wanting to ensure brand consistency
- Digital Marketing Teams optimizing multi-channel content
- Social Media Managers testing content effectiveness

### Key Features

- Customizable persona profiles based on real customer data
- Instant feedback on marketing content
- Visual content analysis capabilities
- Detailed persona-specific insights
- Easy-to-use interface for quick testing

### Repository Structure
```
ai-persona/
├── personas/
│   └── marketing/
│       ├── configs/
│       │   └── .env
│       ├── main.py
│       ├── requirements.txt
│       └── Dockerfile
├── .github/
│   └── workflows/
│       └── deploy-marketing.yml
└── README.md
```

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-persona.git
cd ai-persona/personas/marketing
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
streamlit run main.py
```

### Deployment

The application is automatically deployed to Google Cloud Run using GitHub Actions. The deployment workflow is triggered when changes are pushed to the `main` branch in the `personas/marketing/` directory.

#### Deployment Prerequisites
- Google Cloud Project with Cloud Run and Artifact Registry enabled
- Service account with necessary permissions
- OpenAI API key stored in Google Cloud Secret Manager

#### Key Components
- `main.py`: Main application file containing the Streamlit interface
- `Dockerfile`: Container configuration for Cloud Run deployment
- `requirements.txt`: Python dependencies including:
  - streamlit==1.40.2
  - openai==1.55.1
  - httpx==0.27.2 (pinned for compatibility)
  - Other required packages

#### Environment Configuration
The application uses different environment configurations for local development and production:
- Local: Uses `.env` file in `configs` directory
- Production: Uses Google Cloud Secret Manager

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Troubleshooting
- If you encounter OpenAI client issues, verify the httpx version is pinned to 0.27.2
- For local development issues, ensure your `.env` file is properly configured
- For deployment issues, check the GitHub Actions logs and Cloud Run logs