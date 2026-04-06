import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Fabrica")

def run_fabrica(args: list[str], cwd: str) -> str:
    """Executes the fabrica CLI and returns the output."""
    try:
        result = subprocess.run(
            ["fabrica"] + args, 
            capture_output=True, 
            text=True, 
            check=True,
            cwd=cwd
        )
        return result.stdout or "Command executed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error ({e.returncode}): {e.stderr or e.stdout}"
    except FileNotFoundError:
        return "Error: 'fabrica' command not found. Ensure it is installed and in your system PATH."

@mcp.tool()
def fabrica_init(
    working_dir: str,
    project_name: str = ".",
    auth: bool = False,
    storage: bool = True,
    metrics: bool = False,
    db: str = "sqlite",
    storage_type: str = "file",
    validation_mode: str = "strict"
) -> str:
    """Initialize a new Fabrica project. 'working_dir' MUST be the absolute path to the directory where the command should run."""
    args = ["init", project_name]
    if auth: args.append("--auth")
    if storage: args.append("--storage")
    if metrics: args.append("--metrics")
    args.extend([
        "--db", db,
        "--storage-type", storage_type,
        "--validation-mode", validation_mode
    ])
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_add_resource(working_dir: str, resource_name: str, version: str = "") -> str:
    """Add a new resource to the Fabrica project. 'working_dir' MUST be the absolute path to the project root."""
    args = ["add", "resource", resource_name]
    if version:
        args.extend(["--version", version])
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_add_version(working_dir: str, version_name: str) -> str:
    """Add a new API version. 'working_dir' MUST be the absolute path to the project root."""
    args = ["add", "version", version_name]
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_generate(
    working_dir: str,
    client: bool = False,
    openapi: bool = False,
    handlers: bool = False,
    storage: bool = False,
    force: bool = False
) -> str:
    """Generate server code and specs. 'working_dir' MUST be the absolute path to the project root."""
    args = ["generate"]
    if client: args.append("--client")
    if openapi: args.append("--openapi")
    if handlers: args.append("--handlers")
    if storage: args.append("--storage")
    if force: args.append("--force")
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_ent_migrate(working_dir: str) -> str:
    """Run database migrations. 'working_dir' MUST be the absolute path to the project root."""
    return run_fabrica(["ent", "migrate"], cwd=working_dir)

def main():
    mcp.run()