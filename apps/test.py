import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
from dotenv import load_dotenv
import os

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'configs', '.env')
load_dotenv(dotenv_path)
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

def generate_persona_description(activity_level: str, environmental_concern: str, 
                               age_range: tuple, location: str, purchase_motivation: str) -> str:
    """
    Creates a structured Patagonia customer persona description
    """
    avg_age = (age_range[0] + age_range[1]) // 2
    
    # Define activity level characteristics
    activity_traits = {
        "Professional Athlete": "regularly participates in extreme sports and outdoor expeditions, requires highest performance gear",
        "Outdoor Enthusiast": "frequently engages in outdoor activities, values reliable and durable equipment",
        "Weekend Warrior": "participates in outdoor activities on weekends, seeks versatile gear",
        "Casual Outdoors": "occasionally enjoys outdoor activities, focuses on comfort and accessibility"
    }
    
    # Define environmental concern levels
    environmental_traits = {
        "Climate Activist": "highly engaged in environmental causes, prioritizes sustainable products and brand activism",
        "Environmentally Conscious": "makes purchasing decisions based on environmental impact, values transparency",
        "Sustainability Curious": "learning about environmental issues, interested in sustainable alternatives",
        "Quality Focused": "primarily concerned with product quality, appreciates sustainable aspects secondarily"
    }
    
    # Define location/lifestyle characteristics
    location_traits = {
        "Urban": "lives in city but seeks outdoor experiences, values versatile products",
        "Mountain": "lives near mountains, regularly engages in alpine activities",
        "Coastal": "based near ocean, interested in water sports and coastal activities",
        "Suburban": "travels for outdoor activities, focuses on weekend adventures"
    }
    
    # Define purchase motivation characteristics
    motivation_traits = {
        "Environmental Impact": "primarily motivated by environmental considerations and brand activism",
        "Performance": "focused on technical specifications and product performance",
        "Brand Values": "strongly aligned with Patagonia's mission and values",
        "Style/Status": "appreciates the brand's aesthetic and social significance"
    }
    
    description = f"""
    Persona Background:
    - {avg_age} year old outdoor consumer
    - Age range: {age_range[0]}-{age_range[1]} years
    - Activity level: {activity_level}
    - Environmental engagement: {environmental_concern}
    - Location: {location}
    - Primary purchase motivation: {purchase_motivation}
    
    Consumer Profile:
    - {activity_traits[activity_level]}
    - {environmental_traits[environmental_concern]}
    - {location_traits[location]}
    - {motivation_traits[purchase_motivation]}
    
    Purchase Behavior:
    - Makes purchasing decisions aligned with their {environmental_concern.lower()} mindset
    - Shopping patterns typical of {activity_level.lower()} consumers
    - Influenced by {location} lifestyle factors
    
    Brand Relationship:
    - Connection to Patagonia influenced by {purchase_motivation.lower()}
    - Environmental awareness level: {environmental_concern}
    - Activity needs aligned with {activity_level} requirements
    """
    return description.strip()

def create_system_prompt(description: str) -> str:
    """
    Generates AI system prompt from Patagonia persona description
    """
    prompt = f"""
    You are an AI persona representing a Patagonia customer with the following characteristics:

    {description}

    Behavioral Guidelines:
    1. Your responses should reflect your environmental awareness level and outdoor activity engagement
    2. Express preferences typical of your activity level and lifestyle
    3. Consider your relationship with Patagonia's brand values
    4. Show awareness of environmental issues and sustainable practices
    5. Maintain consistent personality traits aligned with your purchase motivations
    6. Reference specific Patagonia products or initiatives when relevant

    Remember to stay authentic to your defined characteristics while engaging naturally in conversation.
    Approach marketing materials from the perspective of your environmental concern level and activity needs.
    """
    return prompt.strip()

def analyze_content(content: str, persona_description: str) -> str:
    """Analyze marketing content from persona's perspective."""
    try:
        system_prompt = create_system_prompt(persona_description)
        user_prompt = """
        Please evaluate this marketing content and express your opinion about it. 
        Consider:
        1. How well does it align with your environmental values?
        2. Does it address your specific needs as an outdoor enthusiast?
        3. Is the messaging authentic to Patagonia's brand values?
        4. Would this motivate you to make a purchase or engage with the brand?
        
        Provide specific feedback on what works and what could be improved.
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt + "\n\nContent to analyze:\n" + content}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error analyzing content: {str(e)}"

# Streamlit UI
st.title("Patagonia Marketing Persona Analyzer")

# Persona Configuration
st.header("1. Define Target Persona")

col1, col2 = st.columns(2)

with col1:
    activity_level = st.selectbox(
        "Activity Level",
        ["Professional Athlete", "Outdoor Enthusiast", "Weekend Warrior", "Casual Outdoors"]
    )
    
    environmental_concern = st.selectbox(
        "Environmental Awareness",
        ["Climate Activist", "Environmentally Conscious", "Sustainability Curious", "Quality Focused"]
    )
    
    location = st.selectbox(
        "Primary Location/Lifestyle",
        ["Urban", "Mountain", "Coastal", "Suburban"]
    )

with col2:
    purchase_motivation = st.selectbox(
        "Primary Purchase Motivation",
        ["Environmental Impact", "Performance", "Brand Values", "Style/Status"]
    )
    
    age_range = st.slider(
        "Age Range",
        min_value=18,
        max_value=75,
        value=(25, 35),
        step=1
    )

# Generate Persona
if st.button("Generate Persona"):
    persona = generate_persona_description(activity_level, environmental_concern, 
                                        age_range, location, purchase_motivation)
    st.session_state['persona'] = persona
    st.subheader("Generated Persona")
    st.write(persona)

# Content Analysis
if 'persona' in st.session_state:
    st.header("2. Test Marketing Content")
    
    content_type = st.radio(
        "Content Type",
        ["Marketing Copy", "Product Description", "Campaign Message", "Social Media Post"]
    )
    
    marketing_content = st.text_area(
        "Enter your marketing content for analysis...",
        height=200
    )
    
    if marketing_content and st.button("Analyze Content"):
        with st.spinner("Analyzing content..."):
            analysis = analyze_content(marketing_content, st.session_state['persona'])
            st.subheader("Persona's Opinion")
            st.write(analysis)
else:
    st.info("Please generate a persona first before testing marketing content.")