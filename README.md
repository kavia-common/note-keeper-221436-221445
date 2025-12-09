# note-keeper-221436-221445

This project is a simple Notes application. The `notes_backend` container exposes a FastAPI REST API with CRUD endpoints for managing notes (in-memory).

- Docs (when running locally): http://localhost:3001/docs
- Entrypoint module: notes_backend/src/api/main.py

Endpoints:
- GET / — health check
- POST /notes — create a note (201)
- GET /notes — list notes (200)
- GET /notes/{id} — retrieve a note (200 or 404)
- PUT /notes/{id} — update a note (200 or 404)
- DELETE /notes/{id} — delete a note (204 or 404)