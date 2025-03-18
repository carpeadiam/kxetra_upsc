import json
from fpdf import FPDF
from flask import Blueprint

qp_pdf = Blueprint('qp_pdf', __name__)
# Path to the JSON file
json_file_path = "response_data.json"  # Replace with the actual file path

# Read JSON data from the file
with open(json_file_path, "r") as file:
    data = json.load(file)

try:
    req_data = data['candidates'][0]['content']['parts'][0]
    print("Extracted req_data:", req_data)  # Debugging print
except (KeyError, IndexError) as e:
    print("Error: Missing expected keys in JSON:", e)
    exit()

# Extract the text value which contains the JSON code block
text_value = req_data["text"]

# Remove markdown code block formatting if present
if text_value.startswith("```json"):
    # Split the string into lines
    lines = text_value.splitlines()
    # Remove the first line (which should be "```json")
    if lines[0].startswith("```json"):
        lines = lines[1:]
    # Remove the last line if it's just "```"
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    # Join the remaining lines into a single JSON string
    json_str = "\n".join(lines)
else:
    json_str = text_value

# Parse the extracted JSON string
try:
    parsed_json = json.loads(json_str)
except json.JSONDecodeError as e:
    print("Error: Could not parse JSON from the extracted text:", e)
    exit()

# Create a PDF instance
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)
# this is a section that would be seen for a case where the unicode font translation of a greek symbol is not available in a subject like math or physics
# pdf.add_font("DejaVu", "", "dejavu-fonts-ttf-2.37\ttf\DejaVuSans.ttf", uni=True)
# pdf.set_font("DejaVu", size=12)

# Add a title
pdf.set_font("Arial", style="B", size=16)
pdf.cell(200, 10, "UPSC Practice Question Paper", ln=True, align='C')
pdf.ln(10)

# Add questions from the parsed JSON
pdf.set_font("Arial", size=12)
for idx, item in enumerate(parsed_json["questions"], start=1):
    pdf.multi_cell(0, 10, f"{idx}. {item['question']}")
    pdf.ln(5)
    for statement_idx, statement in enumerate(item['statements'], start=1):
        pdf.cell(0, 10, f"   {statement_idx}. {statement}", ln=True)
    pdf.ln(5)
    for opt_key, opt_val in item['options'].items():
        pdf.cell(0, 10, f"   {opt_key}. {opt_val}", ln=True)
    pdf.ln(5)

# Save PDF
pdf_output_path = "question_paper/paper1.pdf"
pdf.output(pdf_output_path)
print(f"Question paper saved as {pdf_output_path}")
