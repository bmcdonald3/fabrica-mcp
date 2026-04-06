import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Fabrica")

def run_fabrica(args: list[str]) -> str:
    """Executes the fabrica CLI and returns the output."""
    try:
        result = subprocess.run(
            ["fabrica"] + args, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout or "Command executed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error ({e.returncode}): {e.stderr or e.stdout}"
    except FileNotFoundError:
        return "Error: 'fabrica' command not found. Ensure it is installed and in your system PATH."

@mcp.tool()
def fabrica_init(
    project_name: str = ".",
    auth: bool = False,
    storage: bool = True,
    metrics: bool = False,
    db: str = "sqlite",
    storage_type: str = "file",
    validation_mode: str = "strict"
) -> str:
    """Initialize a new Fabrica project."""
    args = ["init", project_name]
    if auth: args.append("--auth")
    if storage: args.append("--storage")
    if metrics: args.append("--metrics")
    args.extend([
        "--db", db,
        "--storage-type", storage_type,
        "--validation-mode", validation_mode
    ])
    return run_fabrica(args)

@mcp.tool()
def fabrica_add_resource(resource_name: str, version: str = "") -> str:
    """Add a new resource to the Fabrica project."""
    args = ["add", "resource", resource_name]
    if version:
        args.extend(["--version", version])
    return run_fabrica(args)

@mcp.tool()
def fabrica_add_version(version_name: str) -> str:
    """Add a new API version to the Fabrica project."""
    args = ["add", "version", version_name]
    return run_fabrica(args)

@mcp.tool()
def fabrica_generate(
    client: bool = False,
    openapi: bool = False,
    handlers: bool = False,
    storage: bool = False,
    force: bool = False
) -> str:
    """Generate server handlers, storage adapters, client code, and OpenAPI specs."""
    args = ["generate"]
    if client: args.append("--client")
    if openapi: args.append("--openapi")
    if handlers: args.append("--handlers")
    if storage: args.append("--storage")
    if force: args.append("--force")
    return run_fabrica(args)

@mcp.tool()
def fabrica_ent_migrate() -> str:
    """Run database migrations for Ent storage backend."""
    return run_fabrica(["ent", "migrate"])

def main():
    mcp.run()