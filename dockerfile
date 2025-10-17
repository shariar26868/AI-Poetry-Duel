FROM python:3.10-slim-bullseye

# Set up working directory
WORKDIR /home/user/app

# Update package sources to include main, contrib, and non-free
RUN echo "deb http://deb.debian.org/debian bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bullseye-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list

# Install system packages
COPY packages.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        git-lfs \
        ffmpeg \
        libsm6 \
        libxext6 \
        cmake \
        rsync \
        libgl1 \
        curl \
        tesseract-ocr \
        tesseract-ocr-eng \
        poppler-utils \
    && rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY config/ ./config/
COPY core/ ./core/
COPY utils/ ./utils/
COPY app.py .
COPY .env .
COPY .streamlit/ ./.streamlit/

# Expose Gradio port
EXPOSE 7860

# Run as non-root user
USER 1000

# Start the application
CMD ["python3", "app.py"]