# Coffee AI Assistant with Monocle AI Telemetry

This is a FastAPI application that integrates with OpenAI to answer coffee-related questions, featuring **Monocle AI** instrumentation for specialized AI/LLM observability and tracing.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **OpenAI Integration**: Powered by GPT-3.5-turbo for intelligent coffee advice
- **Monocle AI Telemetry**: 
  - Specialized telemetry for AI/ML applications with LLM-specific tracing
  - Automatic instrumentation of OpenAI API calls
  - Token usage tracking and cost analysis
  - Conversation scope tracking
  - File-based trace exports for analysis
- **Distributed Tracing**: Track OpenAI API calls with detailed request/response data
- **Coffee Expertise**: Specialized AI assistant focused on coffee knowledge

## Quick Start

### Local Development

1. **Clone and navigate to the project:**
   ```bash
   cd ./
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```
   Or create a `.env` file:
   ```bash
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc docs: http://localhost:8000/redoc

7. **View telemetry traces:**
   - Monocle traces are exported to local files in the project directory
   - Check for trace files with timestamps to analyze OpenAI API interactions

## API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with API information
- `POST /ask-coffee` - Ask the AI assistant coffee-related questions

### Coffee AI Assistant
The main API endpoint accepts coffee questions and returns expert advice powered by OpenAI's GPT-3.5-turbo model. All OpenAI interactions are automatically traced by Monocle AI, providing insights into:
- Request and response content
- Token usage and costs
- Latency and performance
- Model parameters and settings

## Sample API Usage

### Get API Information
```bash
curl "http://localhost:8000/"
```

### Ask a Coffee Question (with specific question)
```bash
curl -X POST "http://localhost:8000/ask-coffee" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is the best brewing method for coffee?"
     }'
```

### Ask a Coffee Question (with default question)
```bash
curl -X POST "http://localhost:8000/ask-coffee" \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Example Coffee Questions to Try
- "What's the difference between espresso and regular coffee?"
- "How do I make the perfect French press coffee?"
- "What are the best coffee beans for beginners?"
- "Tell me about cold brew coffee"
- "What equipment do I need to start making specialty coffee?"

## Monocle AI Telemetry Configuration

The application uses Monocle AI for specialized LLM/AI observability:

### File Exporter
Monocle traces are automatically exported to local files in the project directory. These files contain detailed information.

### Configuration
Monocle telemetry is configured in `telemetry_monocle.py`:
- `workflow_name`: Identifies your application in traces (default: "coffee-ai-assistant")
- `monocle_exporters_list`: Export destination (default: "file")

## Development

### Project Structure
```
fastapi/
├── main.py                 # FastAPI application and endpoints
├── app.py                  # Application startup with Monocle telemetry
├── telemetry_monocle.py    # Monocle AI telemetry configuration
├── scope_methods.json      # Conversation scope configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
└── README.md              # This file
```

### Key Files Explained

**app.py**: Entry point that configures Monocle telemetry before starting the server. This ensures all frameworks are instrumented from the start.

**main.py**: FastAPI application with the coffee AI assistant endpoint. Contains the OpenAI integration logic.

**telemetry_monocle.py**: Configures Monocle AI telemetry with file-based exports.


## Testing the Instrumentation

1. **Make some API calls:**
   ```bash
   # Ask various coffee questions
   curl -X POST "http://localhost:8000/ask-coffee" \
        -H "Content-Type: application/json" \
        -d '{"question": "What makes perfect espresso?"}'
   
   curl -X POST "http://localhost:8000/ask-coffee" \
        -H "Content-Type: application/json" \
        -d '{"question": "How do I make cold brew coffee?"}'
   
   curl -X POST "http://localhost:8000/ask-coffee" \
        -H "Content-Type: application/json" \
        -d '{"question": "What are the best coffee beans for beginners?"}'
   ```

2. **Check the trace files:**
   Look for JSON files in your project directory with timestamps
   
3. **Review the logs:**
   Check console output for INFO logs about OpenAI API calls