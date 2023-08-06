import asyncio
import httpx

# Only for json sent, json returned
class RequestApi:
    client = httpx.AsyncClient()

    @staticmethod
    def parse_date(response) -> str:
        try:
            return response.headers['date']
        except Exception as e:
            return e

    # Always expects a json return
    @classmethod
    async def request_handler(cls, url: str, request_type: str, json_data: dict, headers: dict):
        if request_type == "post":
            response = await cls.client.post(url, data=json_data, headers=headers)
        elif request_type == "get":
            response = await cls.client.get(url, headers=headers)
        else:
            raise Exception(f"Can't handle the request type of {request_type}")

        if response.status_code == 200:
            return cls.parse_date(response), response.json()
        else:
            return False, False
        
    def __init__(self):
        # Option for bulk request
        self.bulk_queue = asyncio.Queue()

    async def internal_parser(self, url: str, request_type: str, json_data: dict = {}, add_to_queue = False, headers: dict = {}):
        date, json_response = await self.request_handler(url, request_type, json_data, headers)

        if add_to_queue:
            await self.bulk_queue.put({"url": url, "date": date, "json_response": json_response})
    
        return date, json_response

    async def get(self, url, add_to_queue: bool = False, headers: dict = {}, _return: bool = True):
        response = await self.internal_parser(url, "get", add_to_queue=add_to_queue, headers=headers) 
        
        if _return:
            return response

    async def post(self, url, json_data: dict, add_to_queue: bool = False, headers: dict = {}, _return: bool = True):
        response = await self.internal_parser(url, "post", json_data=json_data, add_to_queue=add_to_queue, headers=headers) 

        if _return:
            return response

if __name__ == "__main__":
    async def main():
        handler = RequestApi()
        print(await handler.post('http://127.0.0.1:5000/test', {"username": "jacob", "password": "python"}, headers = {"x-apikey": "hello"}))

    asyncio.run(main())
