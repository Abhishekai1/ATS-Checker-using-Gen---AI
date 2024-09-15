import gradio as gr
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # Load all environment variables
genai.configure(api_key="AIzaSyArHkiK3tFLHsTdUiRpJHkEtT-uq8t2iO0")

def get_gemini_response(input_text, jd):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"resume:{input_text}\ndescription:{jd}")
        return response.text
    except Exception as e:
        return f"Error in generating response: {str(e)}"

def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += str(page.extract_text())
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def process_resume(jd, uploaded_file):
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        if "Error" in text:  # Check if there was an error reading the PDF
            return text
        response = get_gemini_response(text, jd)
        return response
    else:
        return "Please upload a PDF resume."

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Smart ATS\nImprove Your Resume ATS")
    
    jd_input = gr.TextArea(label="Paste the Job Description")
    uploaded_file = gr.File(label="Upload Your Resume", type="filepath", file_count="single")
    
    submit_button = gr.Button("Submit")
    output = gr.Textbox(label="Response", interactive=False)

    submit_button.click(process_resume, inputs=[jd_input, uploaded_file], outputs=output)

demo.launch()





