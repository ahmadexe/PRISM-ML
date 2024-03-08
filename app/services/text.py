import httpx
async def analyze_text():
    data = {
        'text': 'Contact rick(at)gmail(dot)com to have sx',
        'mode': 'ml',
        'lang': 'en',
        'opt_countries': 'us,gb,fr',
        'api_user': '1999593760',
        'api_secret': 'Hxb9QKqyTha3xfoSRiZhXm6nfKtvauk4'
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post('https://api.sightengine.com/1.0/text/check.json', data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            output = response.json()
            return output
        except httpx.HTTPError as e:
            # Handle HTTP errors
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            # Handle other exceptions
            raise HTTPException(status_code=500, detail=str(e))