# Monica File System API Project

## 🎯 Project Doel
Een API bouwen die Monica toegang geeft tot lokale bestanden en mappen, met:
- Overzicht van mapinhoud en context
- Mogelijkheid om bestandsinhoud op te vragen
- Configureerbare mapstructuur
- Draaiend in Docker, bereikbaar via Ngrok

## 📋 Huidige Status
- **Project Fase**: Initialisatie
- **Sprint**: Week 1 - Docker Setup
- **Laatste Update**: [DATUM]

## 🚀 Deze Week
- [ ] Docker omgeving opzetten
  - [ ] Basis Dockerfile schrijven
  - [ ] docker-compose.yml maken
  - [ ] Test build uitvoeren
- [ ] Framework kiezen en installeren
  - [ ] Onderzoek snelste development flow
  - [ ] Eerste endpoint testen

## 📝 Backlog

### 1. API-ontwerp en configuratie
- [ ] Framework kiezen en basis project opzetten
- [ ] Config.json structuur ontwerpen
- [ ] Basis endpoints definiëren:
  - [ ] /folders
  - [ ] /overview
  - [ ] /file-content
- [ ] Error handling toevoegen

### 2. Mapverkenner en contextbeheer
- [ ] Functie voor map scannen
- [ ] Submappen ondersteuning
- [ ] Metadata verzamelen
- [ ] JSON response format

### 3. Bestandsinhoud ophalen
- [ ] Bestandslezen implementeren
- [ ] Content type detectie
- [ ] Foutafhandeling grote bestanden
- [ ] Caching strategie

### 4. Docker & Deployment
- [ ] Docker container optimaliseren
- [ ] Volume mapping testen
- [ ] Ngrok integratie
- [ ] Logging setup

### 5. Testen & Documentatie
- [ ] Basis tests schrijven
- [ ] API documentatie
- [ ] Gebruiksvoorbeelden
- [ ] Configuratie handleiding

## ✅ Afgerond
- [x] Project planning opgezet
- [x] Initiële projectstructuur bepaald

## 📈 Voortgang Log

### Week 1
- **Doel**: Docker setup en framework keuze
- **Gedaan**:
  - 
- **Blokkades**:
  - 
- **Volgende Stap**:
  - 

## 🔧 Technische Details

### Gekozen Stack
- Framework: [NOG TE BEPALEN]
- Docker base image: [NOG TE BEPALEN]
- Port: 8000

### Configuratie Template
```json
{
  "watched_folders": [
    {
      "path": "/path/to/folder",
      "name": "Project X",
      "description": "Optional description"
    }
  ]
}
