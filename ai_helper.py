"""
AI Helper Module
Handles AI-powered documentation generation and text-to-speech
"""

import os
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from typing import Dict, Tuple
import re


class AIDocumentationGenerator:
    """AI-powered code documentation generator with TTS"""
    
    def __init__(self, user_gemini_key: str = None):
        """
        Initialize AI services with API keys
        
        Args:
            user_gemini_key: Optional user-provided Gemini API key
        """
        # Initialize Gemini - prioritize user key, then env var
        self.gemini_key = user_gemini_key or os.environ.get("GEMINI_API_KEY")
        
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.gemini_model = None
        
        # Initialize ElevenLabs
        self.elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
        if self.elevenlabs_key:
            self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_key)
        else:
            self.elevenlabs_client = None
    
    def generate_documentation(self, code_content: str, language: str, filename: str) -> Dict[str, str]:
        """
        Generate comprehensive documentation from code using Gemini
        
        Args:
            code_content: The source code to analyze
            language: Programming language (python, javascript, etc.)
            filename: Original filename
            
        Returns:
            Dict with 'documentation' and 'summary' keys
        """
        if not self.gemini_model:
            raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY environment variable.")
        
        # Create prompt for Gemini
        prompt = f"""Analyze this {language} code from file "{filename}":

```{language}
{code_content}
```

Generate comprehensive documentation in README markdown format with these sections:
1. **Overview** - What this code does (2-3 sentences)
2. **Key Components** - Main functions/classes with brief descriptions
3. **Usage Examples** - How to use this code (with code blocks)
4. **Dependencies** - Required libraries/packages
5. **Installation** - Setup instructions

Then provide a STRICT 2-LINE SUMMARY (maximum 2 sentences, around 150-200 characters total) that captures the essence of this code.

Format your response EXACTLY like this:

## Documentation

[Full documentation here in markdown format]

## Summary

[Exactly 2 lines/sentences here - be concise and clear]
"""
        
        try:
            # Generate content with Gemini
            response = self.gemini_model.generate_content(prompt)
            full_response = response.text
            
            # Parse documentation and summary
            parts = full_response.split("## Summary")
            
            if len(parts) == 2:
                documentation = parts[0].replace("## Documentation", "").strip()
                summary = parts[1].strip()
                
                # Ensure summary is max 2 lines
                summary_lines = [line.strip() for line in summary.split('\n') if line.strip()]
                summary = ' '.join(summary_lines[:2])
            else:
                # Fallback if format is not as expected
                documentation = full_response
                summary = self._extract_summary_fallback(full_response)
            
            return {
                "documentation": documentation,
                "summary": summary
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate documentation: {str(e)}")
    
    def _extract_summary_fallback(self, text: str) -> str:
        """Extract a 2-line summary if the format is not as expected"""
        # Take first 2 sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return '. '.join(sentences[:2]) + '.'
    
    def text_to_speech(self, text: str) -> bytes:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio bytes (MP3 format)
        """
        if not self.elevenlabs_client:
            raise ValueError("ElevenLabs API key not configured. Set ELEVENLABS_API_KEY environment variable.")
        
        try:
            # Generate audio with professional voice using new API
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id="EXAVITQu4vr4xnSDxMaL",  # Rachel voice ID
                model_id="eleven_monolingual_v1"
            )
            
            # Collect audio bytes
            audio_bytes = b"".join(audio_generator)
            return audio_bytes
            
        except Exception as e:
            raise Exception(f"Failed to generate audio: {str(e)}")
    
    def process_file(self, file_content: str, language: str, filename: str) -> Tuple[str, str, bytes]:
        """
        Complete pipeline: analyze code, generate docs, create TTS
        
        Args:
            file_content: Code content
            language: Programming language
            filename: Original filename
            
        Returns:
            Tuple of (documentation, summary, audio_bytes)
        """
        # Generate documentation and summary
        result = self.generate_documentation(file_content, language, filename)
        
        # Generate audio from summary
        audio = self.text_to_speech(result["summary"])
        
        return result["documentation"], result["summary"], audio
