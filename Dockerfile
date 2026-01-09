FROM python:3.11-slim

WORKDIR /app

# Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Port freigeben
EXPOSE 5000

# Flask starten
CMD ["python", "app.py"]