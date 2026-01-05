import PyPDF2
import google.generativeai as genai


genai.configure(api_key='gemini api key')
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from PDF: {pdf_path}")
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    print(f"Text extraction complete. {len(text)} characters extracted.")
    return text

def correct_text_with_gemini(text):
    print("Correcting text using Gemini...")
    prompt = (
        "The following text was extracted from an old newspaper PDF where text may be "
        "arranged vertically and might have irregular formatting. Please correct any spelling or "
        "grammar errors in the text, maintain the original order of paragraphs, and make sure the "
        "text is coherent and properly structured. If any text appears out of order due to vertical "
        "layout, please rearrange it to make sense within the context. Here's the text:\n\n" + text
    )
    response = model.generate_content(prompt)
    print("API Response:", response)
    if hasattr(response, 'text'):
        corrected_text = response.text
    else:
        corrected_text = "Error: No text returned from API."
    print("Text correction complete.")
    return corrected_text


def text_to_rtf(text):
    print("Converting text to RTF format...")

    rtf = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}\f0\fs24 "
    rtf += text.replace('\n', '\\par ')
    rtf += "}"
    print("Text conversion to RTF complete.")
    return rtf

def convert_to_rtf(text, output_path):
    print(f"Saving RTF content to file: {output_path}")
    rtf_content = text_to_rtf(text)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(rtf_content)
    print(f"File saved successfully to {output_path}")

def main(pdf_path, rtf_output_path):
   
    extracted_text = extract_text_from_pdf(pdf_path)
    
    
    corrected_text = correct_text_with_gemini(extracted_text)
    
  
    convert_to_rtf(corrected_text, rtf_output_path)
    print(f"Conversion complete. Output saved to {rtf_output_path}")

if __name__ == "__main__":
    input_pdf = input("Enter the path to the input PDF file: ")
    output_rtf = input("Enter the path for the output RTF file: ")
    main(input_pdf, output_rtf)
