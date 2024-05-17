import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# Configure generative AI 
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = '''
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.

2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.

3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.

4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues. 

2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined' based on the provided image.

3. Disclaimer: Accompany your analysis with the disclaimer: 'Consult with a Doctor before making any decisions'

Please provide me an output response with these 4 headings Detailed analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions
'''

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest", 
                              generation_config=generation_config, 
                              safety_settings=safety_settings)

st.set_page_config(page_title="Image Analytics", page_icon=":robot:")
st.title("Vital Image Analytics")
st.subheader("An application that helps users to identify medical images")

uploaded_file = st.file_uploader("Upload medical image for analysis:", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, width=250, caption="Uploaded medical image")
submit_button = st.button("Generate the analysis")

if submit_button:
    if uploaded_file is not None:
        try:
            # Get the content of the file
            image_data = uploaded_file.getvalue()

            image_parts = [
                {
                    "mime_type": uploaded_file.type,  # Ensure correct MIME type
                    "data": image_data
                },
            ]

            prompt_parts = [
                image_parts[0],
                system_prompt,
            ]

            response = model.generate_content(prompt_parts)
            if response:
                st.title("Here is the analysis based on the image:")
                st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please ensure your API key is correct and has the necessary permissions.")
