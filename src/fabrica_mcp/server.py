import os
import subprocess
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

    Args:
        working_dir: Absolute path to the parent directory where the project will be created.
        project_name: Name of the new project directory.
        module: Go module path (e.g., github.com/user/project).
        description: Short project description.
        auth: Enable authentication with TokenSmith.
        storage: Enable persistent storage backend.
        storage_type: Storage backend type: 'file' (simple) or 'ent' (database).
        db: Database driver for Ent: 'postgres', 'mysql', or 'sqlite'.
        metrics: Enable Prometheus metrics.
        validation_mode: Validation strictness: 'strict', 'warn', or 'disabled'.
        events: Enable CloudEvents support.
        group: API group name (e.g., infra.example.io).
        versions: Comma-separated list of API versions (e.g., v1,v1beta1).
    """
    safe_cwd = os.path.abspath(os.path.expanduser(working_dir))
    project_path = os.path.join(safe_cwd, project_name)
    
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

    Args:
        working_dir: Absolute path to the Fabrica project root.
        resource_name: Name of the resource to add (e.g., Device).
        version: API version (required for versioned projects, e.g., v1alpha1).
        package: Package name (defaults to lowercase resource name).
        with_validation: Include validation tags in the generated structs.
        with_status: Include a Status struct for the resource.
        with_versioning: Enable per-resource spec versioning snapshots.
        force: Force adding to non-alpha version.
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
    """
    Add a new API version to the Fabrica project.

    Args:
        working_dir: Absolute path to the Fabrica project root.
        version_name: Name of the new version (e.g., v1beta1).
    """
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

    Args:
        working_dir: Absolute path to the Fabrica project root.
        handlers: Generate HTTP handlers only.
        storage: Generate storage adapters only.
        client: Generate client code only.
        openapi: Generate OpenAPI spec only.
        force: Force regeneration even with version warnings.
        debug: Enable debug output showing detailed generation steps.
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
    """
    Run database migrations for projects using the Ent storage backend.

    Args:
        working_dir: Absolute path to the Fabrica project root.
        dry_run: Show migrations without applying them.
    """
    args = ["ent", "migrate"]
    if dry_run: args.append("--dry-run")
    return run_fabrica(args, cwd=working_dir)

@mcp.tool()
def fabrica_ent_describe(working_dir: str) -> str:
    """
    Display information about the Ent schema and entities.

    Args:
        working_dir: Absolute path to the Fabrica project root.
    """
    return run_fabrica(["ent", "describe"], cwd=working_dir)

def main():
    mcp.run()

if __name__ == "__main__":
    main()