"""
FastAPI application for Coffee AI Assistant with Monocle Telemetry

This module defines a FastAPI application that provides a coffee expert AI assistant
powered by OpenAI's GPT models. The application is instrumented with Monocle AI
telemetry for comprehensive tracing and monitoring of API calls and conversations.

Key features:
- Coffee-related Q&A using OpenAI GPT-3.5-turbo
- Automatic telemetry instrumentation with Monocle AI
- RESTful API endpoints for easy integration
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class CoffeeQuestion(BaseModel):
    """
    Request model for coffee-related questions.
    
    Attributes:
        question (Optional[str]): The coffee-related question to ask the AI.
                                 If None, a default question will be used.
    """
    question: Optional[str] = None

# Create FastAPI app FIRST
app = FastAPI(
    title="Coffee AI Assistant with OpenTelemetry",
    description="A FastAPI application that asks OpenAI about coffee with OpenTelemetry tracing",
    version="1.0.0"
)

# Configure OpenAI client
openai_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
)

@app.get("/")
async def root():
    """
    Root endpoint providing API information and usage instructions.
    
    Returns:
        dict: API usage instructions including:
            - Description of available endpoints
            - Example usage for asking coffee questions
    """
    logger.info("Root endpoint called")
    return {
        "message": "Welcome to Coffee AI Assistant!", 
        "description": "Use POST /ask-coffee to ask questions about coffee",
        "example": "POST /ask-coffee with body: {'question': 'What is the best brewing method for coffee?'}"
    }

async def ask_coffee_question(question: str) -> str:
    """
    Ask OpenAI a coffee-related question and get an expert response.
    
    This function constructs a specialized prompt for coffee expertise and queries
    OpenAI's GPT-3.5-turbo model to get detailed, informative answers about coffee
    topics including brewing methods, equipment, beans, and coffee culture.
    
    Args:
        question (str): The coffee-related question to ask. If empty or None,
                       a default question about brewing methods is used.
    
    Returns:
        dict: A response dictionary containing:
            - status: Success indicator
            - question: The question that was asked
            - ai_response: The AI-generated answer
            - model_used: The OpenAI model identifier
            - coffee_expert: Indicator that this is from the AI barista
    
    Raises:
        HTTPException: For various error conditions:
            - 401: Authentication error (invalid API key)
            - 429: Rate limit exceeded
            - 500: API errors or unexpected failures
    """
    try:
        # Use provided question or default
        if not question:
            question = "What are the top 5 coffee brewing methods and their characteristics?"
        
        logger.info(f"Asking OpenAI about coffee: {question}")
        
        # Create a coffee-focused prompt
        coffee_prompt = f"""You are a coffee expert and barista with deep knowledge about coffee beans, brewing methods, equipment, and coffee culture. 
        Please answer the following coffee question in a helpful, informative, and engaging way:
        
        Question: {question}
        
        Please provide a detailed answer that would be helpful to someone interested in coffee."""
        
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable coffee expert and barista."},
                {"role": "user", "content": coffee_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract the response
        ai_response = response.choices[0].message.content
        
        logger.info("Successfully received response from OpenAI")
        
        return {
            "status": "success",
            "question": question,
            "ai_response": ai_response,
            "model_used": "gpt-3.5-turbo",
            "coffee_expert": "☕ AI Barista"
        }
        
    except openai.AuthenticationError:
        logger.error("OpenAI API key authentication failed")
        raise HTTPException(
            status_code=401, 
            detail="OpenAI API key not configured or invalid. Please set OPENAI_API_KEY environment variable."
        )
    except openai.RateLimitError:
        logger.error("OpenAI API rate limit exceeded")
        raise HTTPException(
            status_code=429, 
            detail="OpenAI API rate limit exceeded. Please try again later."
        )
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"OpenAI API error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling OpenAI: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to get coffee advice: {str(e)}"
        )

@app.post("/ask-coffee")
async def ask_coffee_endpoint(
    coffee_question: CoffeeQuestion,
) -> dict:
    """
    POST endpoint for asking the AI coffee expert a question.
    
    This endpoint accepts a coffee-related question and returns a detailed,
    expert-level answer generated by OpenAI's GPT model. All interactions
    are automatically traced and monitored by Monocle AI telemetry.
    
    Args:
        coffee_question (CoffeeQuestion): Request body containing the question.
                                         The question field is optional.
    
    Returns:
        dict: Response containing the AI-generated answer and metadata including:
            - status: Success indicator
            - question: The question that was asked
            - ai_response: Detailed answer from the AI barista
            - model_used: OpenAI model identifier
            - coffee_expert: AI barista identifier
    
    Raises:
        HTTPException: If there are issues with the OpenAI API (authentication,
                      rate limits, or other API errors)
    
    Example:
        POST /ask-coffee
        {
            "question": "What makes perfect espresso?"
        }
        
        Response:
        {
            "status": "success",
            "question": "What makes perfect espresso?",
            "ai_response": "Perfect espresso requires...",
            "model_used": "gpt-3.5-turbo",
            "coffee_expert": "☕ AI Barista"
        }
    """
    logger.info("Ask coffee endpoint called")
    
    question = coffee_question.question if coffee_question.question else None
    
    response = await ask_coffee_question(question)
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
