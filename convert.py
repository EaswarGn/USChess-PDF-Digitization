import PyPDF2
import google.generativeai as genai


genai.configure(api_key='AIzaSyBAlonm5I0MyE7QwBNjYZ5Jl9LMPvUPuAs')
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
        corrected_text = "Error: No text returned from API"
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

def extract_chess_notation_from_rtf(rtf_path):
    print(f"Reading RTF content from file: {rtf_path}")
    with open(rtf_path, 'r', encoding='utf-8') as file:
        rtf_content = file.read()

    print("Extracting chess notation using Gemini...")
    prompt = (
        "The following text contains chess games written in descriptive notation, "
        "but the notation may be scattered across different sections and columns. "
        "Please extract all the descriptive chess notations and combine them into a single, "
        "coherent sequence. Each move should be properly paired, with both a White and Black move "
        "for every turn. Ensure that there should never be a turn that only has one move, meaning each turn must have two moves. Ensure there are no missing or incomplete moves, and correct any such errors. "
        "Format the combined notation as a full game with move numbers. "
        "A small note is that when you first see a chess move, that first move will be the move made by the white pieces"
        "so to find the find the next move played, it will be on the same line (the move the black player played)"
        "keep reading the chess notation like this row by row to get each move, each row will contain a move made by the white player and the corresponding move from the black player."
        "make sure all the move pairs that you output have a move made by the white player and the corresponding move made by the black player."
        "also make sure you thoroughly check the current row to get a white move and then a black move before moving on to the next row."
        "if you don't find a white move and then a black move, then stop."
        "the first example of a chess move pair that you will see in the text is the line where it says 1. P-K4  P-K4"
        "The number one indicates the move number and the first P-K4 indicates the move made by the white player and the second P-K4 indicates the move by the black player"
        "A more complicated example in the text is where it says 3. QxP  and then it leaves the second move blank (move played by the black player)"
        "but if you look carefully, there is some text after the QxP and then there is a line that looks something like this: 3.... Kt-QB3"
        "The .... indicates the move played by white player and the Kt-QB3 indicates the move played by the black player, since there was text in between the .... was necessary"
        "so always look for moves in pairs, considering these examples"
        "another tricky example is where it says 10. KKt-K2 Kt-R4"
        "The move played by the white player is KKt-K2 and the move played by the black player is Kt-R4, never just skip to the next line and replace a missing move with some random move, always look to find the missing move first."
        "Here is the text:\n\n" + rtf_content
    )

    response = model.generate_content(prompt)
    print("API Response:", response)
    if hasattr(response, 'text'):
        full_chess_notation = response.text
    else:
        full_chess_notation = "Error: No text returned from API."
    
    print("Chess notation extraction complete.")
    return full_chess_notation

def main(pdf_path, rtf_output_path):
   
    extracted_text = extract_text_from_pdf(pdf_path)
    
    
    corrected_text = correct_text_with_gemini(extracted_text)
    
  
    convert_to_rtf(corrected_text, rtf_output_path)

    full_chess_notation = extract_chess_notation_from_rtf(rtf_output_path)
    
    print("Final Combined Chess Notation:\n")
    print(full_chess_notation)

if __name__ == "__main__":
    input_pdf = input("Enter the path to the input PDF file: ")
    output_rtf = input("Enter the path for the output RTF file: ")
    main(input_pdf, output_rtf)
