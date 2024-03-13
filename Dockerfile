# Base image with system dependencies
FROM ubuntu:20.04

# Update package lists
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    festival \
    festival-dev \
    libfestivalclient-dev \
    speech-dispatcher \
    espeak

# Install additional TTS engines (optional)
# You can comment out or uncomment engines based on your needs and availability
# Be aware of licensing restrictions for some engines
# - MaryTTS (https://marytts.sourceforge.io/)
RUN git clone https://github.com/marytts/marytts.git /opt/marytts
RUN cd /opt/marytts && ./configure && make && make install

# - Cepstral (https://cepstral.com/) (commercial, requires license)
# RUN wget https://... (download Cepstral installer) && sh ... (install script)

# Install Python libraries
# RUN pip3 install fastapi pycountry

# Copy application code
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

# Expose port (adjust if needed)
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]