import httpx
import os
from dotenv import load_dotenv
from ..models.image import Image

load_dotenv()
API_USER = os.getenv("API_USER")
API_SECRET = os.getenv("API_SECRET")

async def analyze_nsfw_image(image: Image):
    #https://cdn.i-scmp.com/sites/default/files/d8/images/canvas/2023/10/03/7192bc9c-cfc3-459f-aea6-a3a89cc462d6_0f519f43.jpg
    url = image.url
    if not url:
        raise HTTPException(status_code=400, detail="URL not in request body")
    params = {
        'url': url,
        'models': 'nudity-2.0',
        'api_user': API_USER,
        'api_secret': API_SECRET
        }
    moderate = False
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get('https://api.sightengine.com/1.0/check.json', params=params)
            output = r.json()
            none_value = output['nudity']['none']
            if (none_value< 0.80): 
                moderate= True
            message = {
                "moderate": moderate,
                "not-adult" : none_value,
            }
            return message
        except httpx.HTTPError as e:
            # Handle HTTP errors
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            raise HTTPException(status_code=500, detail=str(e))


async def analyze_gore_image(image: Image):
    #'https://cdn-apgml.nitrocdn.com/LebpnhtoivqQZrhySxTgIGIqkErReVqW/assets/images/optimized/rev-935bbea/www.shouselaw.com/wp-content/uploads/2022/08/bloody-knife-homicide-murder.jpeg'
    url = image.url
    if not url:
        raise HTTPException(status_code=400, detail="URL not in request body")
    params = {
        'url': url,
        'models': 'gore',
        'api_user': API_USER,
        'api_secret': API_SECRET
        }
    moderate = False
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get('https://api.sightengine.com/1.0/check.json', params=params)
            output = r.json()
            gore_value = output['gore']['prob']
            if (gore_value > 0.4): 
                moderate= True
            message = {
                "moderate": moderate,
                "gore" : gore_value,
            }
            return message
        except httpx.HTTPError as e:
            # Handle HTTP errors
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            raise BaseException()



async def analyze_offensive_image(image: Image):
    #'https://eadn-wc03-11391632.nxedge.io/wp-content/uploads/2022/01/2c7ecbe491cbc694e4948f3c23f7d1ea.swastika_1.webp'
    url = image.url
    if not url:
        raise HTTPException(status_code=400, detail="URL not in request body")
    params = {
        'url': url,
        'models': 'offensive',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    moderate = False
    highest_category = None
    highest_prob = 0
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get('https://api.sightengine.com/1.0/check.json', params=params)
            output = r.json()
            
            # overall probability
            offensive_prob = output.get("offensive", {}).get("prob", 0)
            if offensive_prob > 0.5:
                moderate = True
                
            # individual categories
            offensive_categories = ["nazi", "confederate", "supremacist", "terrorist", "middle_finger"]
            for category in offensive_categories:
                prob = output.get("offensive", {}).get(category, 0)
                if prob > highest_prob:
                    offensive_prob = prob
                    highest_category = category
                if prob > 0.5:
                    moderate = True
                    break

            message = {
                "moderate": moderate,
                "offensive_prob": offensive_prob,
                "highest_category": highest_category,
            }
            return message
        except httpx.HTTPError as e:
            # Handle HTTP errors
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            raise HTTPException(status_code=500, detail=str(e))

async def analyze_text_image(image: Image):
    #'https://i.pinimg.com/564x/d9/69/1d/d9691d6914f3e0cdb156bda01d90b464.jpg'
    url = image.url
    params = {
        'url': url,
        'models': 'text-content',
        'api_user': API_USER,
        'api_secret': API_SECRET
    }
    moderate = False
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get('https://api.sightengine.com/1.0/check.json', params=params)
            output = r.json()
            
            # check if profanities
            if output.get("text", {}).get("profanity"):
                moderate = True
                profanities = output["text"]["profanity"]


            message = {"moderate": moderate, "profanities":profanities}
            return message
        except httpx.HTTPError as e:
            # Handle HTTP errors
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            raise HTTPException(status_code=500, detail=str(e))
