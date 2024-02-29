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

    def add_info(self, tasks: list[int]) -> None:
        """Adds given tasks to queue."""
        for task in tasks:
            self.pipeline.lpush('queue_tasks', task)
        self.pipeline.execute()
    
    def get_tasks(self, amount: int) -> list[str]:
        """Returns set amount of tasks."""
        tasks = self.red.rpop(name='queue_tasks', count=amount)
        return tasks
    
    def add_results(self, results: list[dict]) -> None:
        """Stores cookies info."""
        for result in results:
            for key in result.keys():
                name = result['email']
                self.pipeline.hset(name=name, key=key, value=result[key])
        self.pipeline.execute()
    
    def get_results(self) -> dict:
        """
        Returns all stored cars data in dict {index:car_info_as_dict}.
        Deletes all tasks from which cars been collected.
        """
        results = {}
        cars = self.red.keys()

        for car in cars:
            results[car] = {}
            keys =  self.red.hkeys(car)
            
            for key in keys:
                results[car][key] = self.red.hget(car, key)
            self.pipeline.delete(car)

        self.pipeline.execute()        
        return results
