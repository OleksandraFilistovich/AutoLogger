import redis


host_rs = 'redis'
port_rs = 6379
password_rs = ''


class Cache:
    """Redis connection. Methods to work with redis cache."""
    def __init__(self, number_db: int, host: str = host_rs,
                 port: int = port_rs, password: str = password_rs) -> None:
        
        self.red = redis.Redis(host=host, port=port, db=number_db,
                               password=password, decode_responses=True)
        self.pipeline = self.red.pipeline()

    def add_results(self, email: str, results: list) -> None:
        """Stores cookies info."""
        ind = -1
        for result in results:
            ind += 1
            for key in result.keys():
                key_name = f'{key}_{ind}'
                self.pipeline.hset(name=email, key=key_name, value=str(result[key]))
        self.pipeline.execute()
    
    def get_results(self) -> dict:
        """
        Returns all stored cookies info.
        """
        results = {}
        cookies = self.red.keys()

        for cookie in cookies:
            results[cookie] = {}
            keys =  self.red.hkeys(cookie)
            
            for key in keys:
                results[cookie][key] = self.red.hget(cookie, key)
            self.pipeline.delete(cookie)

        self.pipeline.execute()        
        return results
