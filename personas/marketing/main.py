import streamlit as st
from openai import OpenAI
import warnings

# Filter out the specific deprecation warning
warnings.filterwarnings('ignore', message='.*use_column_width.*')

# Initialize session state
if 'openai_client' not in st.session_state:
    st.session_state['openai_client'] = None
if 'persona' not in st.session_state:
    st.session_state['persona'] = None

def initialize_openai_client(api_key: str) -> None:
    """Initialize OpenAI client with provided API key"""
    try:
        st.session_state['openai_client'] = OpenAI(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return False

def generate_persona_description(activity_level: str, environmental_concern: str, 
                               age_range: tuple, location: str, purchase_motivation: str) -> str:
    """Creates a structured Patagonia customer persona description"""
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
    
    # Define location characteristics
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

# Page Configuration
st.set_page_config(page_title="AI Persona Platform", page_icon="🎯")

# Sidebar Configuration
st.sidebar.header("📝 API Configuration")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API key",
    type="password",
    help="You can find your API key at https://platform.openai.com/api-keys"
)

if api_key and st.sidebar.button("Initialize API"):
    if initialize_openai_client(api_key):
        st.sidebar.success("API key successfully configured!")

# Main Content
st.title("🎯 Persona Pre-Testing Platform")

st.write("""
Test your marketing content against lifelike customer personas before launching your campaigns. 
Synthetic personas simulate real customer responses based on detailed demographic, psychographic, 
and behavioral characteristics.
""")

st.markdown("""
**Available Features:**
- Persona Customization: Create detailed customer profiles for targeted feedback
- Single Image Analysis: Get detailed feedback on individual marketing visuals
- A/B/N Testing: Compare multiple content variations to identify the most effective options


**Common Use Cases:**
- Test campaign messaging and content across different customer segments
- Preview how product descriptions resonate with specific customer types
- Assess marketing visuals across different customer profiles and segments
""")

# Persona Configuration
st.header("Define Your Target Persona")

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
    st.success("Persona generated! You can now use the Single Analysis or A/B/N Testing pages.")