import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
from dotenv import load_dotenv
import os

# Try to load local environment variables, fallback to system environment variables
try:
    dotenv_path = os.path.join(os.path.dirname(__file__), 'configs', '.env')
    load_dotenv(dotenv_path)
except Exception as e:
    st.debug(f"No local .env file found, using system environment variables: {e}")

# Get API key from environment variables (works with both local .env and Cloud Run secrets)
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    st.error("OpenAI API key not found. Please check your environment configuration.")
    st.stop()

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

    Evaluate any marketing materials or images from the perspective of your environmental 
    concern level, activity needs, and relationship with the brand.
    """
    return prompt.strip()

def analyze_image(image, persona_description):
    """Analyze image from persona's perspective using GPT-4o."""
    try:
        # Convert image to RGB mode if it's in RGBA
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[3])
            else:
                background.paste(image)
            image = background

        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr = img_byte_arr.getvalue()
        
        system_prompt = create_system_prompt(persona_description)
        user_prompt = """
        Please evaluate this image and express your opinion about it. Consider:
        1. How well does it align with your environmental values?
        2. Does it authentically represent outdoor activities at your level?
        3. Would this visual content resonate with you and make you engage with the brand?
        4. How effectively does it communicate to your demographic?
        
        Share your perspective based on your characteristics and preferences.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(img_byte_arr).decode('utf-8')}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

# Streamlit UI
st.title("🎯 Persona Pre-Testing Platform")

st.write("""
Test your marketing content against lifelike customer personas before launching your campaigns. 
Synthetic personas simulate real customer responses based on detailed demographic, psychographic, 
and behavioral characteristics.
""")

st.markdown("""
**Common Use Cases:**
- Test campaign messaging across different customer segments
- Validate social media content with target audience personas
- Preview how product descriptions resonate with specific customer types
- Assess marketing visuals across different customer profiles
- Refine email marketing copy for different subscriber segments
""")


# Persona Configuration
st.header("1. Define Target Persona")

# Create columns for better layout
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

# Image Upload and Analysis
if 'persona' in st.session_state:
    st.header("2. Upload Image for Analysis")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                analysis = analyze_image(image, st.session_state['persona'])
                st.subheader("Persona's Opinion")
                st.write(analysis)
else:
    st.info("Please generate a persona first before uploading an image.")