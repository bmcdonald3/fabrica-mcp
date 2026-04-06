# Fabrica MCP Server

A Model Context Protocol (MCP) server that exposes the Fabrica framework CLI to LLM agents. 

## Overview

This server wraps the `fabrica` command-line tool, allowing AI assistants to autonomously initialize projects, add resources, manage versions, and generate Go code.

## Requirements

* Python 3.11+
* `uv` for dependency management
* The `fabrica` CLI installed and available in the system PATH.

## Installation

Install the server as a command-line tool using `uv`:

```bash
uv tool install .
```

## Usage

Start the MCP server over standard input/output:

```bash
fabrica-mcp
```

## Testing with MCP Inspector

You can verify the exposed tools using the official MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv run fabrica-mcp
```

## Exposed Tools

- `fabrica_init`: Initializes a new project with configurable database, auth, and metrics.
- `fabrica_add_resource`: Scaffolds a new resource type.
- `fabrica_add_version`: Duplicates or bumps an API version.
- `fabrica_generate`: Generates handlers, storage adapters, and OpenAPI specs.
- `fabrica_ent_migrate`: Runs database migrations for Ent backends.