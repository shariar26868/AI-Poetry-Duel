import PyPDF2
import io
from docx import Document
from PIL import Image
import pytesseract
import os

class DocumentProcessor:
    """Handles extraction of text from various document formats"""
    
    @staticmethod
    def extract_text(uploaded_file):
        """
        Extract text from uploaded file based on type
        
        Supports: PDF, DOCX, TXT, Images (via OCR)
        
        For Gradio: uploaded_file is a file path string or file object
        """
        if isinstance(uploaded_file, str):
            file_path = uploaded_file
            file_extension = os.path.splitext(file_path)[1].lower()
        else:
            file_path = uploaded_file.name if hasattr(uploaded_file, 'name') else str(uploaded_file)
            file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == ".pdf":
                return DocumentProcessor._extract_from_pdf(file_path)
            elif file_extension in [".docx", ".doc"]:
                return DocumentProcessor._extract_from_docx(file_path)
            elif file_extension == ".txt":
                return DocumentProcessor._extract_from_txt(file_path)
            elif file_extension in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
                return DocumentProcessor._extract_from_image(file_path)
            else:
                return None
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    @staticmethod
    def _extract_from_pdf(file_path):
        """Extract text from PDF"""
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(file_path):
        """Extract text from DOCX"""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    
    @staticmethod
    def _extract_from_txt(file_path):
        """Extract text from TXT"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text.strip()
    
    @staticmethod
    def _extract_from_image(file_path):
        """Extract text from image using OCR"""
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()