FROM python:3

# Set work directory to app
WORKDIR /usr/src/app

# Copy the repository into the image
COPY . .

# Install required libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py
CMD [ "python", "./main.py" ]
