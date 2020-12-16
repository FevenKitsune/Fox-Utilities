FROM python:3

# Set work directory to app
WORKDIR /usr/src/app

# Create db directory
RUN mkdir db

# Set database location for Docker
ENV FOXDB=/usr/src/app/db/db.db

# Download latest version of Fox-Utilities
RUN git clone https://github.com/FevenKitsune/Fox-Utilities.git

# Set working directory to newly downloaded repository  
WORKDIR /usr/src/app/Fox-Utilities

# Switch to requested branch
ARG branch
RUN git checkout $branch

# Install required libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py
CMD [ "python", "./main.py" ]
