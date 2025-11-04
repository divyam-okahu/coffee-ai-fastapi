"""
Telemetry configuration - Using Monocle AI

This module configures Monocle AI telemetry for tracing and monitoring OpenAI API calls,
conversation scopes, and application behavior. It exports trace data to file-based storage
for analysis and debugging.
"""
import os
import logging

from monocle_apptrace.instrumentation import setup_monocle_telemetry


logger = logging.getLogger(__name__)

def configure_monocle_telemetry():
    """
    Configure Monocle AI telemetry for the application.
    
    Returns:
        bool: True if telemetry was configured successfully, None if configuration failed
        
    Note:
        This should be called before the FastAPI app is created to ensure proper
        instrumentation of all components.
    """
    try:
        setup_monocle_telemetry(
            workflow_name="coffee-ai-assistant",
            monocle_exporters_list="file",
        )
        logger.info("Monocle AI telemetry configured successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to configure Monocle AI telemetry: {e}")
        return None
