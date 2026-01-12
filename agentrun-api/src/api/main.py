import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from agentrun import AgentRun


class RunInputSchema(BaseModel):
    file_content: str
    sandbox_dir: str


class WriteInputSchema(BaseModel):
    content: str
    filename: str
    sandbox_dir: str


class ReadInputSchema(BaseModel):
    filename: str
    sandbox_dir: str


class CleanInputSchema(BaseModel):
    sandbox_dir: str


class OutputSchema(BaseModel):
    output: str


class FileOutputSchema(BaseModel):
    success: bool
    content: str


app = FastAPI()

# allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/v1/health/", response_model=dict)
async def health():
    return {
        "status": "ok",
    }


@app.get("/")
async def redirect_docs():
    return RedirectResponse(url="/docs")


@app.post("/v1/run/", response_model=OutputSchema)
async def run_code(input_schema: RunInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    python_code = input_schema.file_content
    with ThreadPoolExecutor() as executor:
        future = executor.submit(runner.execute_code_in_container, python_code)
        output = await asyncio.wrap_future(future)
    return OutputSchema(output=output)


@app.post("/v1/write/", response_model=FileOutputSchema)
async def write_file(input_schema: WriteInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    container = runner.client.containers.get(runner.container_name)
    result = runner.copy_file_to_container(container, input_schema.content, input_schema.filename)
    return FileOutputSchema(success=result["success"], content=result["message"])


@app.post("/v1/read/", response_model=FileOutputSchema)
async def read_file(input_schema: ReadInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    container = runner.client.containers.get(runner.container_name)
    result = runner.read_file_from_container(container, input_schema.filename)
    return FileOutputSchema(success=result["success"], content=result["content"])


@app.post("/v1/clean/", response_model=FileOutputSchema)
async def clean_sandbox(input_schema: CleanInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    container = runner.client.containers.get(runner.container_name)
    runner.clean_up(container, [])
    return FileOutputSchema(success=True, content="Sandbox cleaned successfully")
