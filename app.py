"""
Application startup script

This script serves as the entry point for the FastAPI Coffee AI Assistant application.
It configures Monocle telemetry before starting the server to ensure all API calls
and interactions are properly traced and monitored.

The telemetry is configured at module import time to instrument the OpenAI client
and other components before the FastAPI app is initialized.
"""
import uvicorn
from telemetry_monocle import configure_monocle_telemetry

# Configure telemetry before importing the app
# This ensures OpenAI and other libraries are instrumented from the start
configure_monocle_telemetry()

if __name__ == "__main__":
    print("Starting FastAPI application with instrumentation...")
    
    # Start the server using module:variable syntax
    # This tells uvicorn to import 'app' from 'main' module
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

