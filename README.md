# Cloud Computing Demo – Docker & Kubernetes mit Minikube

Dieses Projekt demonstriert eine einfache **Microservice-Architektur** mit  
**Docker**, **Kubernetes** und **Minikube**.

Die Anwendung besteht aus:
- einem **Frontend Service** (Flask Web App)
- einem **Database Service** (Flask REST API mit persistentem Speicher)

Die Services laufen in **separaten Kubernetes Pods** und kommunizieren über **ClusterIP Services**.

---

## Architekturübersicht
```
Browser
   │
   ▼
Frontend Service (NodePort)
   │
   ▼
Database Service (ClusterIP)
   │
   ▼
Persistent Volume (PVC)
```

### Komponenten
| Komponente | Beschreibung |
|---|---|
| Frontend | Web-UI, ruft Daten vom Database Service ab |
| Database Service | REST API zur Speicherung & Abfrage von Daten |
| Kubernetes | Orchestrierung der Container |
| Minikube | Lokales Kubernetes Cluster |
| Persistent Volume | Dauerhafte Datenspeicherung |

---

## Voraussetzungen

- Docker
- Minikube
- kubectl

Optional:
- curl
- Browser
---

## Services im Detail

### Frontend Service
- Flask Web App
- Port: **5000**
- Von außen erreichbar über **NodePort**
- Holt Daten vom Database Service über die Umgebungsvariable `DB_URL`

### Database Service
- Flask REST API
- Port: **5002**
- Nur intern im Cluster erreichbar (**ClusterIP**)
- Verwendet **PersistentVolumeClaim** für dauerhafte Speicherung
- Health Endpoint: `/health`

---

## Kubernetes Health Checks

Der Database Service stellt einen Health Endpoint bereit:


Dieser wird verwendet für:
- **Liveness Probe** → Neustart bei Fehler
- **Readiness Probe** → Pod bereit für Traffic?

---

## Projekt starten (Minikube)

### 1. Minikube starten
```bash
minikube start
```
### 2. Docker Images in Minikube bauen
```bash
eval $(minikube docker-env)

docker build -t frontend:latest ./frontend
docker build -t database-service:latest ./database-service
```

### 3. Kubernetes Ressourcen deployen
```bash
kubectl apply -f kubernetes/
```

### 4. Status überprüfen
```bash
kubectl get pods
kubectl get services
```
### Beispiel: Daten in den Database Service einfügen

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"value": {"id": 0, "name": "john", "email": "john@doe.com"}}' \
  http://localhost:5002/db/set/0
```