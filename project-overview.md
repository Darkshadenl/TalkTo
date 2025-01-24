# Monica File System API Project

## 🎯 Project Doel

Een API bouwen die Monica toegang geeft tot lokale bestanden en mappen, met:

- Overzicht van mapinhoud en context
- Mogelijkheid om bestandsinhoud op te vragen
- Configureerbare mapstructuur
- Draaiend in Docker, bereikbaar via Ngrok

| Category | Requirement | Description | Priority | Min Hours | Max Hours | Dependencies | Status |
|----------|-------------|-------------|-----------|-----------|-----------|--------------|--------|
| Setup | Project Structure | Opzetten basis project structuur met Poetry en FastAPI | High | 1 | 2 | None | Completed |
| Setup | Docker Setup | Development Docker setup met hot-reload | High | 1 | 2 | Project Structure | Not Started |
| Setup | Configuration | Environment configuratie met Pydantic BaseSettings | High | 0.5 | 1 | Project Structure | Completed |
| Core | File Scanner | Basis file system scanning functionaliteit (directories & files) | High | 2 | 4 | Project Structure | Completed |
| Core | Basic Search | Simpele zoekfunctie op bestandsnamen | Medium | 1 | 2 | File Scanner | Not Started |
| API | List Endpoint | GET endpoint voor directory listing | High | 1 | 2 | File Scanner | Completed |
| API | File Info Endpoint | GET endpoint voor file metadata | High | 1 | 2 | File Scanner | Completed |
| API | File Operations | POST/PUT/DELETE voor basis file operaties | Medium | 2 | 4 | List Endpoint | Completed |
| Security | Basic Path Validation | Simpele checks tegen path traversal | High | 1 | 1.5 | File Scanner | Completed |
| Documentation | Basic API Docs | Minimale FastAPI auto-docs voor gebruik | Low | 0.5 | 1 | All Endpoints | Not Started |

### Implementatie Details

#### Configuratie
- Gebruikt Pydantic BaseSettings voor omgevingsconfiguratie
- Ondersteunt dynamische configuratie via .env
- Type-veilige configuratie met automatische conversie

#### Bestandsbeheer
- Async file operations voor betere performance
- Volledige CRUD-ondersteuning
- Beveiliging met path validation
- Respecteert ALLOWED_EXTENSIONS en MAX_FILE_SIZE

### Configuratie Template

```YAML
watched_folders:
  - path: /path/to/folder
    name: Project X
    description: Optional description
```

### Toekomstige Ontwikkeling
- Docker containerisatie
- Ngrok integratie
- Uitbreiding zoekfunctionaliteit
- Verbeterde API documentatie
