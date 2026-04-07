import os
import subprocess
from typing import Optional, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Fabrica")

def run_fabrica(args: list[str], cwd: str) -> str:
    """Executes the fabrica CLI and returns the output."""
    safe_cwd = os.path.abspath(os.path.expanduser(cwd))
    try:
        result = subprocess.run(
            ["fabrica"] + args, 
            capture_output=True, 
            text=True, 
            check=True,
            cwd=safe_cwd
        )
        return result.stdout or "Command executed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error ({e.returncode}): {e.stderr or e.stdout}"
    except FileNotFoundError:
        return "Error: 'fabrica' command not found. Ensure it is installed and in your system PATH."

@mcp.tool()
def fabrica_init(
    working_dir: str,
    project_name: str = "myproject",
    module: str = "",
    description: str = "",
    auth: bool = False,
    storage: bool = True,
    storage_type: str = "file",
    db: str = "sqlite",
    metrics: bool = False,
    validation_mode: str = "strict",
    events: bool = False,
    group: str = "",
    versions: str = "v1"
) -> str:
    """
    Initialize a new Fabrica project.
    'working_dir' must be the absolute path to the parent directory.
    'versions' is a comma-separated list of API versions.
    """
    safe_cwd = os.path.abspath(os.path.expanduser(working_dir))
    project_path = os.path.join(safe_cwd, project_name)
    
    # Using the -d flag added to init.go to anchor initialization
    args = ["init", ".", "-d", project_path]
    if module: args.extend(["--module", module])
    if description: args.extend(["--description", description])
    if auth: args.append("--auth")
    if not storage: args.append("--storage=false")
    if storage_type: args.extend(["--storage-type", storage_type])
    if db: args.extend(["--db", db])
    if metrics: args.append("--metrics")
    if validation_mode: args.extend(["--validation-mode", validation_mode])
    if events: args.append("--events")
    if group: args.extend(["--group", group])
    if versions: args.extend(["--versions", versions])
    
    return run_fabrica(args, cwd=safe_cwd)

@mcp.tool()
def fabrica_add_resource(
    working_dir: str,
    resource_name: str,
    version: str = "",
    package: str = "",
    with_validation: bool = True,
    with_status: bool = True,
    with_versioning: bool = False,
    force: bool = False
) -> str:
    """
    Add a new resource definition to the project.
    'working_dir' must be the absolute path to the Fabrica project root.
    """
    args = ["add", "resource", resource_name]
    if version: args.extend(["--version", version])
    if package: args.extend(["--package", package])
    if not with_validation: args.append("--with-validation=false")
    if not with_status: args.append("--with-status=false")
    if with_versioning: args.append("--with-versioning")
    if force: args.append("--force")
    
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_add_version(working_dir: str, version_name: str) -> str:
    """Add a new API version to the Fabrica project."""
    return run_fabrica(["add", "version", version_name], cwd=working_dir)

@mcp.tool()
def fabrica_generate(
    working_dir: str,
    handlers: bool = False,
    storage: bool = False,
    client: bool = False,
    openapi: bool = False,
    force: bool = False,
    debug: bool = False
) -> str:
    """
    Generate code from resource definitions. 
    If no specific flags are provided, it generates everything.
    """
    args = ["generate"]
    if handlers: args.append("--handlers")
    if storage: args.append("--storage")
    if client: args.append("--client")
    if openapi: args.append("--openapi")
    if force: args.append("--force")
    if debug: args.append("--debug")
    
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_ent_migrate(working_dir: str, dry_run: bool = False) -> str:
    """Run database migrations for Ent storage backend."""
    args = ["ent", "migrate"]
    if dry_run: args.append("--dry-run")
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_ent_describe(working_dir: str) -> str:
    """Describe the Ent schema and entities."""
    return run_fabrica(["ent", "describe"], cwd=working_dir)

def main():
    mcp.run()

if __name__ == "__main__":
    main()