from mcp.server.fastmcp import FastMCP
import subprocess

mcp = FastMCP("Fabrica")

@mcp.tool()
def generate_code(config_path: str, output_directory: str) -> str:
    """Generates Go API code using Fabrica given a configuration file."""
    # Placeholder for the actual Fabrica command execution
    # subprocess.run(["fabrica", "generate", "--config", config_path, "--out", output_directory], check=True)
    return f"Simulated Fabrica execution: generated code from {config_path} into {output_directory}"

if __name__ == "__main__":
    mcp.run()