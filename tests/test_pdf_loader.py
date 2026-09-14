from app.pdf_loader import load_pdf


pdf_path = "data/sample.pdf"

try:
    text = load_pdf(pdf_path)

    print("PDF loaded successfully!")
    print("Extracted characters:", len(text))
    print()
    print("First 1000 characters:")
    print(text[:1000])

except FileNotFoundError:
    print("sample.pdf does not exist yet.")
    print("Add a PDF to data/sample.pdf and run this test again.")
