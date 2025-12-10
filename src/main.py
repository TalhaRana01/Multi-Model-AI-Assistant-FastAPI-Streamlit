"""
CLI entry point for AI Assistant
"""
import click
import uvicorn
import subprocess
from .config import settings
from src.utils.logger import logger
from src.api.database.db import create_tables


@click.group()
def cli():
    """AI Assistant CLI"""
    pass


@cli.command()
@click.option('--host', default=settings.api_host, help='API host')
@click.option('--port', default=settings.api_port, help='API port')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(host, port, reload):
    """Start FastAPI server"""
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=reload
    )


@cli.command()
@click.option('--port', default=settings.streamlit_port, help='Streamlit port')
def ui(port):
    """Start Streamlit UI"""
    logger.info(f"Starting Streamlit UI on port {port}")
    subprocess.run([
        "streamlit", "run",
        "src/streamlit_app/app.py",
        "--server.port", str(port)
    ])


@cli.command()
def init_db():
    """Initialize database"""
    from src.api.database.db import create_tables
    logger.info("Initializing database...")
    create_tables()
    logger.info("Database initialized successfully!")


if __name__ == "__main__":
    cli()