import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from agentrun import AgentRun


class RunInputSchema(BaseModel):
    command: str
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
def run_command(input_schema: RunInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    container = runner.client.containers.get(runner.container_name)
    exit_code, output = runner.execute_command_in_container(
        container,
        input_schema.command,
        runner.default_timeout,
    )
    return OutputSchema(success=exit_code == 0, content=output)


@app.post("/v1/write/", response_model=OutputSchema)
async def write_file(input_schema: WriteInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    container = runner.client.containers.get(runner.container_name)
    result = runner.copy_file_to_container(container, input_schema.content, input_schema.filename)
    return OutputSchema(success=result["success"], content=result["message"])


@app.post("/v1/read/", response_model=OutputSchema)
async def read_file(input_schema: ReadInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    container = runner.client.containers.get(runner.container_name)
    result = runner.read_file_from_container(container, input_schema.filename)
    return OutputSchema(success=result["success"], content=result["content"])


@app.post("/v1/clean/", response_model=OutputSchema)
async def clean_sandbox(input_schema: CleanInputSchema):
    runner = AgentRun(
        sandbox_dir=input_schema.sandbox_dir,
        container_name=os.environ.get("CONTAINER_NAME", "agentrun-api-python_runner-1"),
        default_timeout=60 * 5,
    )
    container = runner.client.containers.get(runner.container_name)
    runner.clean_up(container, [])
    return OutputSchema(success=True, content="Sandbox cleaned successfully")
