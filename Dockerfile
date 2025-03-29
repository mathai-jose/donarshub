

# Use official Python image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy project files to the container
COPY requirements.txt /usr/src/app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

#
COPY . /usr/src/app/

# Expose the application port
EXPOSE 8000

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]