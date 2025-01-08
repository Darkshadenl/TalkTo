# Monica File System API Project

## 🎯 Project Doel

Een API bouwen die Monica toegang geeft tot lokale bestanden en mappen, met:

- Overzicht van mapinhoud en context
- Mogelijkheid om bestandsinhoud op te vragen
- Configureerbare mapstructuur
- Draaiend in Docker, bereikbaar via Ngrok

| Category | Requirement | Description | Priority | Min Hours | Max Hours | Dependencies | Status |
|----------|-------------|-------------|-----------|-----------|-----------|--------------|--------|
| Setup | Project Structure | Opzetten basis project structuur met Poetry en FastAPI | High | 1 | 2 | None | Not Started |
| Setup | Docker Setup | Development Docker setup met hot-reload | High | 1 | 2 | Project Structure | Not Started |
| Setup | Configuration | Environment configuratie met Pydantic BaseSettings | High | 0.5 | 1 | Project Structure | Not Started |
| Core | File Scanner | Basis file system scanning functionaliteit (directories & files) | High | 2 | 4 | Project Structure | Not Started |
| Core | Basic Search | Simpele zoekfunctie op bestandsnamen | Medium | 1 | 2 | File Scanner | Not Started |
| API | List Endpoint | GET endpoint voor directory listing | High | 1 | 2 | File Scanner | Not Started |
| API | File Info Endpoint | GET endpoint voor file metadata | High | 1 | 2 | File Scanner | Not Started |
| API | File Operations | POST/DELETE voor basis file operaties (verplaatsen/verwijderen) | Medium | 2 | 4 | List Endpoint | Not Started |
| Security | Basic Path Validation | Simpele checks tegen path traversal | High | 1 | 1.5 | File Scanner | Not Started |
| Documentation | Basic API Docs | Minimale FastAPI auto-docs voor gebruik | Low | 0.5 | 1 | All Endpoints | Not Started |



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
