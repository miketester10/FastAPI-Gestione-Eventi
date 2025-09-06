# 🎉 FastAPI Event Management System

Un sistema completo di gestione eventi costruito con **FastAPI**, **PostgreSQL** e **SQLAlchemy**. Il progetto include autenticazione JWT, crittografia dei dati sensibili, gestione prenotazioni e sistema di commenti.

## 🚀 Caratteristiche Principali

- **🔐 Autenticazione JWT** con access token e refresh token
- **🛡️ Crittografia AES** per i dati sensibili
- **📅 Gestione Eventi** completa (CRUD)
- **🎫 Sistema Prenotazioni** con controllo capacità
- **💬 Sistema Commenti** con rating
- **👥 Gestione Utenti** con ruoli admin
- **🗄️ Database PostgreSQL** con migrazioni Alembic
- **🐳 Containerizzazione Docker**
- **📚 Documentazione API** automatica

## 🏗️ Architettura del Progetto

```
fastapi/
├── src/
│   ├── main.py                 # Entry point dell'applicazione
│   ├── config.py              # Configurazione e settings
│   ├── database.py            # Configurazione database
│   ├── security.py            # JWT e autenticazione
│   ├── encryption.py          # Crittografia AES
│   ├── schemas.py             # Schema base Pydantic
│   ├── users/                 # Modulo gestione utenti
│   │   ├── models.py          # Modello User
│   │   ├── routers.py         # API endpoints utenti
│   │   └── schemas.py         # Schema utenti
│   ├── events/                # Modulo gestione eventi
│   │   ├── models.py          # Modello Event
│   │   ├── routers.py         # API endpoints eventi
│   │   └── schemas.py         # Schema eventi
│   ├── reservations/          # Modulo prenotazioni
│   │   ├── models.py          # Modello Reservation
│   │   ├── routers.py         # API endpoints prenotazioni
│   │   └── schemas.py         # Schema prenotazioni
│   └── comments/              # Modulo commenti
│       ├── models.py          # Modello Comment
│       ├── routers.py         # API endpoints commenti
│       └── schemas.py         # Schema commenti
├── migrations/                # Migrazioni database Alembic
├── docker-compose.yml         # Configurazione Docker
├── alembic.ini               # Configurazione Alembic
└── requirements.txt          # Dipendenze Python
```

## 🛠️ Tecnologie Utilizzate

- **FastAPI** 0.103.1 - Framework web moderno e veloce
- **SQLAlchemy** 2.0.22 - ORM per database
- **PostgreSQL** - Database relazionale
- **Alembic** 1.12.0 - Migrazioni database
- **Pydantic** 2.4.0 - Validazione dati
- **PyJWT** 2.8.0 - Gestione token JWT
- **Passlib** 1.7.4 - Hashing password
- **PyCryptodome** - Crittografia AES
- **Docker** - Containerizzazione

## 📋 Prerequisiti

- Python 3.11+
- PostgreSQL 12+
- Docker e Docker Compose (opzionale)

## ⚙️ Installazione e Configurazione

### 1. Clona il repository

```bash
git clone https://github.com/miketester10/FastAPI-Gestione-Eventi.git
cd FastAPI-Gestione-Eventi
```

### 2. Crea un ambiente virtuale

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura le variabili d'ambiente

Crea un file `.env` nella root del progetto:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=your_db_name

# JWT Configuration
ALGORITHM=HS256
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRES_IN=30
JWT_REFRESH_SECRET=your_jwt_refresh_secret_key
JWT_REFRESH_EXPIRES_IN=10080

# Encryption
ENCRYPTION_KEY=your_encryption_key_32_chars

# App
APP_NAME=FastAPI Event Management System
```

### 5. Configura il database

```bash
# Esegui le migrazioni
alembic upgrade head
```

### 6. Avvia l'applicazione

```bash
uvicorn src.main:app --reload
```

L'API sarà disponibile su `http://localhost:8000`

## 🐳 Utilizzo con Docker

### Avvio rapido con Docker Compose

```bash
# Assicurati che la rete 'backend' esista
docker network create backend

# Avvia l'applicazione
docker-compose up -d
```

L'applicazione sarà disponibile su `http://localhost:8000`

## 📚 API Endpoints

### 🔐 Autenticazione

| Metodo | Endpoint               | Descrizione                |
| ------ | ---------------------- | -------------------------- |
| POST   | `/users/`              | Registrazione nuovo utente |
| POST   | `/users/login`         | Login utente               |
| POST   | `/users/refresh-token` | Refresh del token          |
| DELETE | `/users/logout`        | Logout utente              |

### 👥 Gestione Utenti

| Metodo | Endpoint            | Descrizione               |
| ------ | ------------------- | ------------------------- |
| GET    | `/users/me`         | Profilo utente corrente   |
| GET    | `/users/`           | Lista tutti gli utenti    |
| GET    | `/users/{user_id}`  | Dettagli utente specifico |
| PATCH  | `/users/`           | Aggiorna profilo utente   |
| DELETE | `/users/`           | Elimina account utente    |
| GET    | `/users/get/events` | Eventi creati dall'utente |

### 📅 Gestione Eventi

| Metodo | Endpoint             | Descrizione               |
| ------ | -------------------- | ------------------------- |
| GET    | `/events/`           | Lista tutti gli eventi    |
| POST   | `/events/`           | Crea nuovo evento         |
| GET    | `/events/{event_id}` | Dettagli evento specifico |
| PATCH  | `/events/{event_id}` | Aggiorna evento           |
| DELETE | `/events/{event_id}` | Elimina evento            |

### 🎫 Gestione Prenotazioni

| Metodo | Endpoint                         | Descrizione               |
| ------ | -------------------------------- | ------------------------- |
| GET    | `/reservations/`                 | Lista prenotazioni utente |
| POST   | `/reservations/`                 | Crea nuova prenotazione   |
| GET    | `/reservations/{reservation_id}` | Dettagli prenotazione     |
| PATCH  | `/reservations/{reservation_id}` | Aggiorna prenotazione     |
| DELETE | `/reservations/{reservation_id}` | Cancella prenotazione     |

### 💬 Gestione Commenti

| Metodo | Endpoint                 | Descrizione           |
| ------ | ------------------------ | --------------------- |
| GET    | `/comments/`             | Lista commenti utente |
| POST   | `/comments/`             | Crea nuovo commento   |
| GET    | `/comments/{comment_id}` | Dettagli commento     |
| PATCH  | `/comments/{comment_id}` | Aggiorna commento     |
| DELETE | `/comments/{comment_id}` | Elimina commento      |

## 🔒 Sicurezza

### Autenticazione JWT

- **Access Token**: Durata 30 minuti (configurabile)
- **Refresh Token**: Durata 7 giorni (configurabile)
- **Crittografia**: Refresh token crittografati con AES-256

### Validazione Dati

- Validazione input con Pydantic
- Hashing password con bcrypt
- Sanitizzazione dati utente

### Autorizzazione

- Controllo proprietà risorse
- Ruoli utente (admin/user)
- Token Bearer per API protette

## 🗄️ Database Schema

### Tabelle Principali

- **users**: Gestione utenti e autenticazione
- **events**: Eventi con contenuto JSONB
- **reservations**: Prenotazioni con controllo capacità
- **comments**: Commenti con rating e contenuto JSONB

### Relazioni

- User → Events (1:N)
- User → Reservations (1:N)
- User → Comments (1:N)
- Event → Reservations (1:N)
- Event → Comments (1:N)

## 🚀 Funzionalità Avanzate

### Sistema Prenotazioni Intelligente

- Controllo automatico capacità eventi
- Prevenzione overbooking
- Gestione posti disponibili in tempo reale

### Crittografia Dati Sensibili

- Refresh token crittografati
- Chiavi di crittografia configurabili
- Algoritmo AES-256-CBC

### Gestione Contenuto Flessibile

- Campi JSONB per contenuto dinamico
- Struttura dati estendibile
- Supporto per metadati complessi

## 📖 Documentazione API

Una volta avviata l'applicazione, la documentazione interattiva è disponibile su:

- **Swagger UI**: `http://localhost:8000/docs`

## 🔧 Sviluppo

### Struttura Modulare

Il progetto segue un'architettura modulare con separazione delle responsabilità:

- **Models**: Definizione entità database
- **Schemas**: Validazione e serializzazione dati
- **Routers**: Endpoints API

### Migrazioni Database

```bash
# Crea nuova migrazione
alembic revision --autogenerate -m "Descrizione migrazione"

# Applica migrazioni
alembic upgrade head

# Rollback migrazione
alembic downgrade -1
```

## 📝 Esempi di Utilizzo

### Registrazione Utente

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario_rossi",
    "email": "mario@example.com",
    "password": "password123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario_rossi",
    "password": "password123"
  }'
```

### Creazione Evento

```bash
curl -X POST "http://localhost:8000/events/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Conferenza Tech 2024",
    "date": "2024-06-15T10:00:00Z",
    "location": "Centro Congressi Roma",
    "capacity": 200,
    "content": {
      "description": "Conferenza sulle ultime tecnologie",
      "speakers": ["Mario Rossi", "Giulia Bianchi"],
      "topics": ["AI", "Machine Learning", "Cloud"]
    }
  }'
```
