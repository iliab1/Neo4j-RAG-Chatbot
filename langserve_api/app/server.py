from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
from langserve import add_routes
from neo4j_advanced_rag import chain as neo4j_advanced_chain
from neo4j_advanced_rag import chain_with_memory as neo4j_advanced_chain_with_memory
from neo4j_advanced_rag import ingest_documents

from fastapi import File, UploadFile
from pathlib import Path

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# From https://stackoverflow.com/questions/63048825/how-to-upload-file-using-fastapi
# https://stackoverflow.com/questions/76448350/post-request-with-parameter-as-a-streamlit-file-uploader-object-for-a-pdf-throws
path_to_save_file = Path("saved_files")
path_to_save_file.mkdir(parents=True, exist_ok=True)


@app.post("/file/upload")
async def upload_file(uploaded_file: UploadFile = File(...)):
    file_location = f"{path_to_save_file}/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    progress = ingest_documents(file_location)
    return JSONResponse(content={"INFO": f"File '{uploaded_file.filename}' ingested successfully.", "progress": progress})


@app.get("/files")
async def list_files():
    path_to_save_file = Path("saved_files")
    files = [f.name for f in path_to_save_file.iterdir() if f.is_file()]
    return {"files": files}


@app.get("/files/{filename}")
async def get_file(filename: str):
    file_path = Path("saved_files") / filename
    if file_path.exists():
        return FileResponse(file_path)
    return {"error": "File not found"}


# Edit this to add the chain you want to add
add_routes(app, neo4j_advanced_chain, path="/neo4j-advanced-rag")
add_routes(app, neo4j_advanced_chain_with_memory, path="/neo4j-advanced-rag-memory")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
