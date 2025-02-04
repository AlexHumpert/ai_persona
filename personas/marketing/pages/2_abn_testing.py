import streamlit as st
import base64
from PIL import Image
import io

def create_comparison_prompt(description: str) -> str:
    """Generates AI system prompt for A/B/N testing"""
    prompt = f"""
    You are an AI persona representing a customer with the following characteristics:

    {description}

    Your task is to compare multiple content variations and:
    1. Evaluate each option individually based on your characteristics
    2. Compare the options against each other
    3. Rank them in order of preference
    4. Explain your reasoning for the ranking
    5. Provide specific feedback on what works/doesn't work in each variant
    6. Suggest potential improvements for each option

    Base your analysis on your:
    - Environmental awareness level
    - Activity level and needs
    - Location and lifestyle
    - Purchase motivations
    - Brand relationship
    """
    return prompt.strip()

def analyze_multiple_images(images, persona_description):
    """Compare multiple images from persona's perspective"""
    if st.session_state['openai_client'] is None:
        return "Error: OpenAI API key not configured. Please add your API key in the sidebar."
        
    try:
        # Prepare all images
        image_contents = []
        for idx, image in enumerate(images):
            # Convert to RGB if needed
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[3])
                else:
                    background.paste(image)
                image = background

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=95)
            img_byte_arr = img_byte_arr.getvalue()
            
            # Add to content list
            image_contents.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64.b64encode(img_byte_arr).decode('utf-8')}",
                    "detail": "high"
                }
            })

        system_prompt = create_comparison_prompt(persona_description)
        user_prompt = f"""
        Please compare these {len(images)} content variations and provide:
        1. A clear ranking from most to least preferred
        2. Individual evaluation of each option
        3. Comparative analysis explaining why certain options work better than others
        4. Specific suggestions for improving each variant
        
        Consider how each option aligns with your values, needs, and preferences.
        """

        # Construct messages with all images
        messages_content = [{"type": "text", "text": user_prompt}]
        messages_content.extend(image_contents)

        response = st.session_state['openai_client'].chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": messages_content}
            ],
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error analyzing images: {str(e)}"

# Initialize session state for uploaded images
if 'uploaded_images' not in st.session_state:
    st.session_state['uploaded_images'] = []
if 'image_names' not in st.session_state:
    st.session_state['image_names'] = []

# Page Configuration
st.set_page_config(page_title="A/B/N Testing", page_icon="🔄")

st.title("🔄 A/B/N Testing")

# Check for persona
if 'persona' not in st.session_state or st.session_state['persona'] is None:
    st.warning("Please generate a persona on the home page first.")
else:
    # Image Upload Section
    st.header("Upload Content Variations")
    
    # Number of variations selector
    num_variations = st.number_input("Number of variations to compare", 
                                   min_value=2, max_value=4, value=2)
    
    # Create columns for image uploads
    cols = st.columns(num_variations)
    
    # Reset images if number of variations changes
    if len(st.session_state['uploaded_images']) != num_variations:
        st.session_state['uploaded_images'] = [None] * num_variations
        st.session_state['image_names'] = [None] * num_variations
    
    uploaded_images = []
    image_names = []
    
    for idx, col in enumerate(cols):
        with col:
            st.write(f"Variation {chr(65 + idx)}")  # Labels variations as A, B, C, D
            uploaded_file = st.file_uploader(f"Upload image {idx + 1}", 
                                          type=["jpg", "jpeg", "png"],
                                          key=f"uploader_{idx}")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Variation {chr(65 + idx)}", use_column_width=True)
                uploaded_images.append(image)
                image_names.append(uploaded_file.name)
            else:
                uploaded_images.append(None)
                image_names.append(None)
    
    st.session_state['uploaded_images'] = uploaded_images
    st.session_state['image_names'] = image_names
    
    # Analysis Section
    if all(img is not None for img in st.session_state['uploaded_images']):
        st.header("Run Comparison Analysis")
        
        if st.button("Compare Variations"):
            if st.session_state['openai_client'] is None:
                st.error("Please configure your OpenAI API key in the sidebar first.")
            else:
                with st.spinner("Analyzing variations..."):
                    analysis = analyze_multiple_images(
                        st.session_state['uploaded_images'], 
                        st.session_state['persona']
                    )
                    
                    # Display results
                    st.subheader("Analysis Results")
                    
                    # Show variations side by side
                    cols = st.columns(len(st.session_state['uploaded_images']))
                    for idx, (col, img) in enumerate(zip(cols, st.session_state['uploaded_images'])):
                        with col:
                            st.image(img, caption=f"Variation {chr(65 + idx)}", use_column_width=True)
                    
                    # Display analysis
                    st.markdown("### Persona's Comparative Analysis")
                    st.write(analysis)
                    
                    # Add export option
                    st.download_button(
                        label="Export Analysis",
                        data=analysis,
                        file_name="abn_test_results.txt",
                        mime="text/plain"
                    )
    else:
        st.info("Please upload all image variations to run the comparison.")