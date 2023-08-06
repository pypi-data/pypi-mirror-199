class Client:
    async def __aenter__(self):
        await self.connect()
        self
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.close()
    async def connect(self):
        pass
    async def close(self):
        pass