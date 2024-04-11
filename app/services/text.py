import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")
async def analyze_text():
    data = {
        'text': 'Contact rick(at)gmail(dot)com to have sx',
        'mode': 'ml',
        'lang': 'en',
        'opt_countries': 'us,gb,fr',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post('https://api.sightengine.com/1.0/text/check.json', data=data)
            response.raise_for_status() 
            output = response.json()
            
            # check if sexual
            sexual_prob = output.get("moderation_classes", {}).get("sexual", 0)
            if sexual_prob > 0:
                moderate = True
                return {"moderate": moderate, "moderation_class": "sexual", "probability": sexual_prob}

            # check other categories
            categories = ["discriminatory", "insulting", "violent", "toxic"]
            for category in categories:
                category_prob = output.get("moderation_classes", {}).get(category, 0)
                if category_prob >= 0.02:
                    moderate = True
                    return {"moderate": moderate, "moderation_class": category, "probability": category_prob}
            
            return {"moderate": False}
            
        except httpx.HTTPError as e:
            # Handle HTTP errors
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            raise HTTPException(status_code=500, detail=str(e))
