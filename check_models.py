import requests
import json

def list_available_models(api_key):
    """List all available Gemini models for the given API key"""
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        print("=" * 60)
        print("AVAILABLE GEMINI MODELS")
        print("=" * 60)
        
        if 'models' in data:
            for model in data['models']:
                model_name = model.get('name', 'Unknown')
                display_name = model.get('displayName', 'Unknown')
                description = model.get('description', 'No description')
                
                # Check supported generation methods
                supported_methods = model.get('supportedGenerationMethods', [])
                
                print(f"\n[Model]: {model_name}")
                print(f"   Display Name: {display_name}")
                print(f"   Description: {description[:100]}...")
                print(f"   Supported Methods: {', '.join(supported_methods)}")
                
                # Temperature ranges
                if 'temperature' in model:
                    print(f"   Temperature Range: {model['temperature']}")
                
                # Token limits
                if 'inputTokenLimit' in model:
                    print(f"   Input Token Limit: {model['inputTokenLimit']:,}")
                if 'outputTokenLimit' in model:
                    print(f"   Output Token Limit: {model['outputTokenLimit']:,}")
        
        print("\n" + "=" * 60)
        print("Models that support 'generateContent' can be used for text generation")
        print("=" * 60)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching models: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    # Use the provided API key
    API_KEY = "AIzaSyDOiNo_lWkMaDbodN8WCj2PBe31hNn375o"
    list_available_models(API_KEY)