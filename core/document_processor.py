import PyPDF2
import io
from docx import Document
from PIL import Image
import pytesseract
class DocumentProcessor:
    """Handles extraction of text from various document formats"""
    
    @staticmethod
    def extract_text(uploaded_file):
        """
        Extract text from uploaded file based on type
        
        Supports: PDF, DOCX, TXT, Images (via OCR)
        """
        file_type = uploaded_file.type
        
        try:
            if file_type == "application/pdf":
                return DocumentProcessor._extract_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return DocumentProcessor._extract_from_docx(uploaded_file)
            elif file_type == "text/plain":
                return uploaded_file.getvalue().decode("utf-8")
            elif file_type.startswith("image/"):
                return DocumentProcessor._extract_from_image(uploaded_file)
            else:
                return None
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    @staticmethod
    def _extract_from_pdf(file):
        """Extract text from PDF"""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(file):
        """Extract text from DOCX"""
        doc = Document(io.BytesIO(file.getvalue()))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    @staticmethod
    def _extract_from_image(file):
        """Extract text from image using OCR"""
        image = Image.open(io.BytesIO(file.getvalue()))
        text = pytesseract.image_to_string(image)
        return text.strip()