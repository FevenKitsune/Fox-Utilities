FROM python:3

# Set work directory to app
WORKDIR /usr/src/app

# Download latest version of Fox-Utilities
RUN git clone https://github.com/FevenKitsune/Fox-Utilities.git

# Set working directory to newly downloaded repository  
WORKDIR /usr/src/app/Fox-Utilities

# Install required libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py
CMD [ "python", "./main.py" ]
