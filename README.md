# Basis App – Flask mit Docker

Diese Basis‑Applikation ist eine **sehr einfache Flask Web App**, die in einem
**Docker Container** läuft.  
Sie dient als **Grundlage** für spätere Erweiterungen mit **Docker Compose**,
**Kubernetes** und **Minikube**.

---

## Funktionalität

Die App stellt zwei HTTP Endpoints bereit:

| Endpoint | Beschreibung |
|--------|--------------|
| `/` | Gibt eine einfache HTML‑Begrüßung zurück |
| `/health` | Health Check für Docker / Kubernetes |

Beispiel:
```
GET /
→ Hallo aus Docker!

GET /health
→ { "status": "healthy" }
```


---

## Voraussetzungen

- Docker  
- (Optional) Docker Compose  

Keine weiteren Abhängigkeiten erforderlich.

---

## Lokales Starten (ohne Docker)

```bash
pip install -r requirements.txt
python app.py
```

App läuft dann unter http://localhost:5000

# Starten mit Docker
## 1. Docker Image bauen
```bash
docker build -t flask-basis-app .
```
## 2. Container starten
```bash
docker run -p 5000:5000 flask-basis-app
```
## 3. App im Browser öffnen
``bash
http://localhost:5000
```

## 4. Health check
```bash
curl http://localhost:5000/health
```

# Weitere Branches
`multidocker`: Implementiert ein Multidocker setup mit Kubernetes und Minikube. 
Die Branches `multidocker-database` und `multidocker-database-connection`
zeigen die jeweweiligen Zwischenschritte.
