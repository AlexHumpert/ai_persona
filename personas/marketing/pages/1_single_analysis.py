import streamlit as st
import base64
from PIL import Image
import io
import warnings

# Filter out the specific deprecation warning
warnings.filterwarnings('ignore', message='.*use_column_width.*')

def create_system_prompt(description: str) -> str:
    """Generates AI system prompt from persona description"""
    prompt = f"""
    You are an AI persona representing a customer with the following characteristics:

    {description}

    Behavioral Guidelines:
    1. Your responses should reflect your environmental awareness level and outdoor activity engagement
    2. Express preferences typical of your activity level and lifestyle
    3. Consider your relationship with the brand values
    4. Show awareness of environmental issues and sustainable practices
    5. Maintain consistent personality traits aligned with your purchase motivations
    6. Reference specific products or initiatives when relevant

    Evaluate any marketing materials or images from the perspective of your environmental 
    concern level, activity needs, and relationship with the brand.
    """
    return prompt.strip()

def analyze_image(image, persona_description):
    """Analyze image from persona's perspective using GPT-4."""
    if st.session_state['openai_client'] is None:
        return "Error: OpenAI API key not configured. Please add your API key in the sidebar."
        
    try:
        # Convert image to RGB mode if needed
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

        response = st.session_state['openai_client'].chat.completions.create(
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

# Page Configuration
st.set_page_config(page_title="Single Image Analysis", page_icon="🖼️")

st.title("🖼️ Single Image Analysis")

if 'persona' not in st.session_state or st.session_state['persona'] is None:
    st.warning("Please generate a persona on the home page first.")
else:
    
    st.header("Upload Image for Analysis")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Analyze Image"):
            if st.session_state['openai_client'] is None:
                st.error("Please configure your OpenAI API key in the sidebar first.")
            else:
                with st.spinner("Analyzing image..."):
                    analysis = analyze_image(image, st.session_state['persona'])
                    st.subheader("Persona's Opinion")
                    st.write(analysis)