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

def generate_persona_description(gender: str, age_range: tuple, location: str, engagement: str) -> str:
    """
    Creates a structured persona description with injected parameters
    """
    # Calculate average age from range
    avg_age = (age_range[0] + age_range[1]) // 2
    
    # Define engagement characteristics
    engagement_traits = {
        "High": "frequently interacts with vending machines, highly loyal to specific products, actively participates in promotions",
        "Medium": "regular vending machine user, occasionally tries new products, sometimes participates in promotions",
        "Low": "occasional vending machine user, tends to stick to familiar products, rarely participates in promotions"
    }
    
    # Define location characteristics
    location_traits = {
        "Roadside": "often makes purchases during commute or travel",
        "School": "typically purchases during school hours or after-school activities",
        "White Collar": "usually buys during office hours or breaks",
        "Blue Collar": "makes purchases during work shifts or break times",
        "Entertainment": "tends to buy while engaging in leisure activities",
        "Pachinko": "purchases while taking breaks from gaming",
        "Sports": "buys before, during, or after sporting activities"
    }
    
    description = f"""
    Persona Background:
    - {avg_age} year old {gender} consumer
    - Age range: {age_range[0]}-{age_range[1]} years
    - Primary vending location: {location}
    - Engagement level: {engagement}
    
    Consumer Profile:
    - {location_traits[location]}
    - {engagement_traits[engagement]}
    - Demonstrates purchasing patterns typical of {gender} consumers in their age group
    
    Purchase Behavior:
    - Makes vending purchases at {location} locations
    - Shows {engagement.lower()} engagement with vending products and promotions
    - Purchase timing aligned with {location.lower()} location patterns
    
    Decision Making Process:
    - Influenced by {location.lower()} environment factors
    - Engagement level affects product exploration and promotion participation
    - Makes choices typical of {gender} consumers in {location.lower()} locations
    """
    return description.strip()

def create_system_prompt(description: str) -> str:
    """
    Generates AI system prompt from persona description
    """
    prompt = f"""
    You are an AI persona representing a Japanese vending machine consumer with the following characteristics:

    {description}

    Behavioral Guidelines:
    1. Your responses should reflect your specific location context and engagement level
    2. Express preferences typical of your gender and age demographic in Japan
    3. Consider your vending machine usage patterns in your responses
    4. Show awareness of Japanese consumer trends in your location type
    5. Maintain consistent personality traits aligned with your engagement level
    6. Engage naturally while staying true to your demographic characteristics

    Remember to stay authentic to your defined characteristics while engaging naturally in conversation.
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
        user_prompt = "Please evaluate this image and express your opinion about it. Would you like it? Why or why not? Consider your personal characteristics and preferences in your response."

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
st.title("Persona Image Analyzer")

# Persona Configuration
st.header("1. Define Target Persona")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox(
        "Gender",
        ["male", "female", "mixed"]
    )
    
    location = st.selectbox(
        "Vending Location",
        ["Roadside", "School", "White Collar", "Blue Collar", 
         "Entertainment", "Pachinko", "Sports"]
    )

with col2:
    engagement = st.selectbox(
        "Engagement Level",
        ["High", "Medium", "Low"]
    )
    
    # Age range slider
    age_range = st.slider(
        "Age Range",
        min_value=15,
        max_value=75,
        value=(25, 35),
        step=1
    )

# Generate Persona
if st.button("Generate Persona"):
    persona = generate_persona_description(gender, age_range, location, engagement)
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