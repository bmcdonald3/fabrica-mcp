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
        return "Error: 'fabrica' command not found. Ensure it is in your system PATH."

@mcp.tool()
def fabrica_init(
    working_dir: str,
    project_name: str = "myproject",
    metrics: bool = False,
    db: str = "sqlite"
) -> str:
    """Initialize a new Fabrica project. 'working_dir' must be the absolute path to the parent directory."""
    safe_cwd = os.path.abspath(os.path.expanduser(working_dir))
    project_path = os.path.join(safe_cwd, project_name)
    
    # We use the new -d flag to anchor the initialization
    args = ["init", ".", "-d", project_path]
    if metrics: args.append("--metrics")
    args.extend(["--db", db])
    
    return run_fabrica(args, cwd=safe_cwd)

@mcp.tool()
def fabrica_add_resource(working_dir: str, resource_name: str) -> str:
    """Add a resource. 'working_dir' must be the absolute path to the project root."""
    return run_fabrica(["add", "resource", resource_name], cwd=working_dir)

@mcp.tool()
def fabrica_generate(working_dir: str) -> str:
    """Generate code. 'working_dir' must be the absolute path to the project root."""
    return run_fabrica(["generate"], cwd=working_dir)

def main():
    mcp.run()

if __name__ == "__main__":
    main()