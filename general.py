import os
import aiohttp
import asyncio

class MexcAPI:
    def __init__(self):
        self.url = 'https://api.mexc.com'

        self.headers = {
            'Content-Type': 'application/json',
            'X-MEXC-APIKEY': os.getenv('MEXC_API_KEY'),
        }

    async def _get(self, endpoint):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.url}{endpoint}', headers=self.headers) as response:
                return await response.json()
            
    async def _post(self, endpoint, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{self.url}{endpoint}', headers=self.headers, json=data) as response:
                return await response.json()
            
    async def test_connection(self):
        return await self._get('/api/v3/ping')
    
    async def get_server_time(self):
        return await self._get('/api/v3/time')
    
    async def get_default_symbols(self):
        return await self._get('/api/v3/defaultSymbols')
    
    async def get_exchange_info(self,
                                symbols: list[str] = []):
        if len(symbols) == 0:
            return await self._get('/api/v3/exchangeInfo')
        elif len(symbols) == 1:
            return await self._get(f'/api/v3/exchangeInfo?symbol={symbols[0]}')
        else:
            return await self._get(f'/api/v3/exchangeInfo?symbols={",".join(symbols)}')
        
    async def get_book_snapshot(self,
                                symbol: str,
                                limit: int = 100):
        return await self._get(f'/api/v3/depth?symbol={symbol}&limit={limit}')
    
    async def get_recent_trades(self,
                                symbol: str,
                                limit: int = 500):
        return await self._get(f'/api/v3/trades?symbol={symbol}&limit={limit}')
    
    async def get_recent_agg_trades(self,
                                    symbol: str,
                                    startTime: int = None,
                                    endTime: int = None,
                                    limit: int = 500):
        if startTime is None or endTime is None:
            return await self._get(f'/api/v3/aggTrades?symbol={symbol}&limit={limit}')
        else:
            return await self._get(f'/api/v3/aggTrades?symbol={symbol}&'
                                f'limit={limit}&startTime={startTime}&'
                                f'endTime={endTime}')
    
    async def get_klines(self,
                         symbol: str,
                         interval: str,
                         startTime: int=None,
                         endTime: int=None,
                         limit: int=500):
        if interval not in ['1m', '5m', '15m', '30m', '60m', '4h', '1d', '1W', '1M']:
            raise ValueError('Invalid interval')
        if startTime is None or endTime is None:
            return await self._get(f'/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}')
        else:
            return await self._get(f'/api/v3/klines?symbol={symbol}&interval={interval}&'
                                f'startTime={startTime}&endTime={endTime}&limit={limit}')
        
    async def get_avg_price(self,
                            symbol: str):
        return await self._get(f'/api/v3/avgPrice?symbol={symbol}')
    
    async def get_24h_ticker_price_change(self,
                                          symbols: list[str] = []):
        if len(symbols) == 0:
            return await self._get('/api/v3/ticker/24hr')
        elif len(symbols) == 1:
            return await self._get(f'/api/v3/ticker/24hr?symbol={symbols[0]}')
        else:
            return await self._get(f'/api/v3/ticker/24hr?symbols={",".join(symbols)}')
        
    async def price_ticker(self,
                           symbols: list[str] = []):
        if len(symbols) == 0:
            return await self._get('/api/v3/ticker/price')
        elif len(symbols) == 1:
            return await self._get(f'/api/v3/ticker/price?symbol={symbols[0]}')
        else:
            return await self._get(f'/api/v3/ticker/price?symbols={",".join(symbols)}')
        
    async def book_ticker(self,
                          symbol: str):
        return await self._get(f'/api/v3/ticker/bookTicker?symbol={symbol}')
    
    async def place_order(self,
                          symbol: str,
                          side: str,
                          type: str,
                          quantity: float = None,
                          quoteOrderQty: float = None,
                          price: float = None,
                          newClientOrderId: str = None,
                          test: bool = False):
        if side not in ['BUY', 'SELL']:
            raise ValueError('Invalid side. Accepted values are BUY or SELL')
        if type not in ['LIMIT', 'MARKET', 'LIMIT_MAKER', 'IMMEDIATE_OR_CANCEL', 'FILL_OR_KILL']:
            raise ValueError('Invalid type. Accepted values are LIMIT, MARKET, LIMIT_MAKER, IMMEDIATE_OR_CANCEL, FILL_OR_KILL')
        
        if type == 'MARKET' and price is not None:
            raise ValueError('Price should not be set for MARKET orders')
        if type == 'LIMIT' and price is None:
            raise ValueError('Price should be set for LIMIT orders')
        
        if quantity is None and quoteOrderQty is None:
            raise ValueError('Either quantity or quoteOrderQty should be set')
        
        
        


async def main():
    mexc = MexcAPI()
    print(await mexc.book_ticker(symbol='BTCUSDT'))

if __name__ == '__main__':
    asyncio.run(main())