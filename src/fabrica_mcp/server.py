import os
import subprocess
from typing import Annotated
from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Fabrica")

def run_fabrica(args: list[str], cwd: str) -> str:
    """Executes the fabrica CLI and returns the output."""
    safe_cwd = os.path.abspath(os.path.expanduser(cwd))
    # Replace with the output of 'which fabrica'
    FABRICA_BIN = "/Users/ben.mcdonald/go/bin/fabrica"
    try:
        result = subprocess.run(
            [FABRICA_BIN] + args, 
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
    working_dir: Annotated[str, Field(description="Absolute path to the parent directory where the project will be created")],
    project_name: Annotated[str, Field(description="Name of the new project directory")] = "myproject",
    module: Annotated[str, Field(description="Go module path (e.g., github.com/user/project)")] = "",
    description: Annotated[str, Field(description="Short project description")] = "",
    auth: Annotated[bool, Field(description="Enable authentication with TokenSmith")] = False,
    storage: Annotated[bool, Field(description="Enable persistent storage backend")] = True,
    storage_type: Annotated[str, Field(description="Storage backend type: 'file' (simple) or 'ent' (database)")] = "file",
    db: Annotated[str, Field(description="Database driver for Ent: 'postgres', 'mysql', or 'sqlite'")] = "sqlite",
    metrics: Annotated[bool, Field(description="Enable Prometheus metrics")] = False,
    validation_mode: Annotated[str, Field(description="Validation strictness: 'strict', 'warn', or 'disabled'")] = "strict",
    events: Annotated[bool, Field(description="Enable CloudEvents support")] = False,
    group: Annotated[str, Field(description="API group name (e.g., infra.example.io)")] = "",
    versions: Annotated[str, Field(description="Comma-separated list of API versions (e.g., v1,v1beta1)")] = "v1",
    reconcile: Annotated[bool, Field(description="Enable the Kubernetes-style reconciliation framework")] = False,
    reconcile_workers: Annotated[int, Field(description="Number of concurrent reconciler workers")] = 5,
    reconcile_requeue: Annotated[int, Field(description="Default requeue delay in minutes")] = 5
) -> str:
    """
    Initialize a new Fabrica project with a full set of configuration options.
    """
    safe_cwd = os.path.abspath(os.path.expanduser(working_dir))
    project_path = os.path.join(safe_cwd, project_name)
    
    # Base command with the anchoring directory flag
    args = ["init", ".", "-d", project_path]
    
    # Feature Flags
    if auth: args.append("--auth")
    if not storage: args.append("--storage=false")
    if metrics: args.append("--metrics")
    if events: args.append("--events")
    if reconcile: args.append("--reconcile")
    
    # String/Value Flags
    if module: args.extend(["--module", module])
    if description: args.extend(["--description", description])
    if storage_type: args.extend(["--storage-type", storage_type])
    if db: args.extend(["--db", db])
    if validation_mode: args.extend(["--validation-mode", validation_mode])
    if group: args.extend(["--group", group])
    if versions: args.extend(["--versions", versions])
    
    # Reconciliation Specifics
    if reconcile:
        args.extend(["--reconcile-workers", str(reconcile_workers)])
        args.extend(["--reconcile-requeue", str(reconcile_requeue)])
    
    return run_fabrica(args, cwd=safe_cwd)

@mcp.tool()
def fabrica_add_resource(
    working_dir: Annotated[str, Field(description="Absolute path to the Fabrica project root.")],
    resource_name: Annotated[str, Field(description="Name of the resource to add (e.g., Device).")],
    version: Annotated[str, Field(description="API version (required for versioned projects, e.g., v1alpha1).")] = "",
    package: Annotated[str, Field(description="Package name (defaults to lowercase resource name).")] = "",
    with_validation: Annotated[bool, Field(description="Include validation tags in the generated structs.")] = True,
    with_status: Annotated[bool, Field(description="Include a Status struct for the resource.")] = True,
    with_versioning: Annotated[bool, Field(description="Enable per-resource spec versioning snapshots.")] = False,
    force: Annotated[bool, Field(description="Force adding to non-alpha version.")] = False
) -> str:
    """
    Add a new resource definition to the project.
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
def fabrica_add_version(
    working_dir: Annotated[str, Field(description="Absolute path to the Fabrica project root.")],
    version_name: Annotated[str, Field(description="Name of the new version (e.g., v1beta1).")]
) -> str:
    """
    Add a new API version to the Fabrica project.
    """
    return run_fabrica(["add", "version", version_name], cwd=working_dir)

@mcp.tool()
def fabrica_generate(
    working_dir: Annotated[str, Field(description="Absolute path to the Fabrica project root.")],
    handlers: Annotated[bool, Field(description="Generate HTTP handlers only.")] = False,
    storage: Annotated[bool, Field(description="Generate storage adapters only.")] = False,
    client: Annotated[bool, Field(description="Generate client code only.")] = False,
    openapi: Annotated[bool, Field(description="Generate OpenAPI spec only.")] = False,
    force: Annotated[bool, Field(description="Force regeneration even with version warnings.")] = False,
    debug: Annotated[bool, Field(description="Enable debug output showing detailed generation steps.")] = False
) -> str:
    """
    Generate code from resource definitions.
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
def fabrica_ent_migrate(
    working_dir: Annotated[str, Field(description="Absolute path to the Fabrica project root.")],
    dry_run: Annotated[bool, Field(description="Show migrations without applying them.")] = False
) -> str:
    """
    Run database migrations for projects using the Ent storage backend.
    """
    args = ["ent", "migrate"]
    if dry_run: args.append("--dry-run")
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_ent_describe(
    working_dir: Annotated[str, Field(description="Absolute path to the Fabrica project root.")]
) -> str:
    """
    Display information about the Ent schema and entities.
    """
    return run_fabrica(["ent", "describe"], cwd=working_dir)

def main():
    mcp.run()

if __name__ == "__main__":
    main()