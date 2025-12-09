# Notes Backend (FastAPI)

A simple FastAPI backend providing CRUD operations for notes using an in-memory store.

## Run (development)

- With uvicorn:
  uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001

- API docs:
  http://localhost:3001/docs

The preview environment of this project should already start the app automatically.

## Endpoints

- Health: GET /
- Create note: POST /notes
- List notes: GET /notes
- Retrieve note: GET /notes/{id}
- Update note: PUT /notes/{id}
- Delete note: DELETE /notes/{id}

### Models

- NoteCreate: { "title": string, "content": string }
- NoteUpdate: { "title"?: string, "content"?: string }
- Note: { "id": number, "title": string, "content": string, "created_at": string, "updated_at": string }

### Status codes

- Create: 201
- List: 200
- Retrieve: 200 or 404
- Update: 200 or 404
- Delete: 204 or 404

## Curl examples

Create:
curl -s -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First","content":"Hello world"}'

List:
curl -s http://localhost:3001/notes

Retrieve:
curl -s http://localhost:3001/notes/1

Update (full fields optional):
curl -s -X PUT http://localhost:3001/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","content":"Updated content"}'

Delete:
curl -s -X DELETE http://localhost:3001/notes/1 -i

## CORS

CORS is enabled for localhost and common dev ports (and permissive for preview).

## Notes

- Storage is in-memory and resets on service restart.
- OpenAPI docs available at /docs.
