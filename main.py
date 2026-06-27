'''
Project: The objective is to run 50 sequential api calls and get the result of these api calls in an async fashion.

Other projects can also be:

- https://aiohttp-demos.readthedocs.io/en/latest/index.html#aiohttp-demos-polls-beginning
- projects shared by gemini
    - Getting 50 simultaneous requests at a time 
    - Psuedocode:
        - Uses aiohttp which is like an async version of request in python
        - every pokemon has an id, and iterating on the ids we intend to get the individual pokemon names
        - Use asyncio.gather to run all such tasks concurrently 


'''
import asyncio
import aiohttp
import time

async def fetch_pokemon(session, pokemon_id):
    '''
    This function is declared async since we are fetching the data from an api call. 
    '''
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    async with session.get(url) as response: # why an async is used here?
        data = await response.json()
        return data['name']

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, id) for id in range(1, 51)]
        results = await asyncio.gather(*tasks) #why is there a *against tasks? Are we unpacking items in a list?: Yes
        return results

# if __name__ =="__main__":
#     start_time=time.time()

#     name = asyncio.run(main())
#     print(f"First 5 pokemons: {name[:5]}")
#     print(f"Time to result= {time.time()-start_time}")


# async def single_pokemon_func():
#     start_time = time.time()
#     result = []
#     for id in range(1, 50):
#         async with aiohttp.ClientSession() as session:
#             url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
#             async with session.get(url) as response:
#                 data = await response.json()
#                 result.append(data["name"])
#     print(f"The first 5 elements are: {result[:5]}")
#     print(f"Time to result: {time.time() - start_time} ms")

# A couple of issues with the above code:
# 1. using regular loops make the process sequential and not async, so we should avoid using them when we are using async
# 2. Opening new sessions for every new request defeats the purpose of async, so that should be avoided as well


# async def single_pokemon_func():
#     start_time = time.time()

#     async def fetch_single_item(session, id):
#         url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
#         async with session.get(url) as response:
#             data = await response.json()
#             return data["name"]

#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch_single_item(session, id) for id in range(1, 51)]
#         result = await asyncio.gather(*tasks)
#     print(f"The first 5 elements are: {result[:5]}")
#     print(f"Time to result: {time.time() - start_time} ms")


# if __name__ == "__main__":
#     asyncio.run(single_pokemon_func())

# On meta level following steps are needed to create an async function
# 1. One should know which operation should be async based
# 2. We need to think in terms of tasks. Tasks are indvidual operations that use async to optimize their working.
# 2.1 One should define an individual task using async
# 2.2 Since the operation is async it has bound to be many such tasks running. These tasks should be aggregate together and run asynchroniously


# refactoring the code using types and adding error validation
# We can use the class object from where the class is taken to annotate the type
async def single_pokemon_func():
    start_time = time.time()

    async def fetch_single_item(session: aiohttp.ClientSession, id: int) -> None:
        url: str = f"https://pokeapi.co/api/v2/pokemon/{id}/"
        try: 
            async with session.get(url) as response:
                data = await response.json()
                return data["name"]
        except ConnectionError as e:
            print(f"You have encountered a connection Error: {e}")
        except Exception as e:
            print(f"You have encountered a connection Error: {e}")


    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single_item(session, id) for id in range(1, 51)]
        result = await asyncio.gather(*tasks)
    print(f"The first 5 elements are: {result[:5]}")
    print(f"Time to result: {time.time() - start_time} ms")


# if __name__ == "__main__":
#     asyncio.run(single_pokemon_func())

# Scripts with Rate Limiting
# Why Rate limiting?
# A server can hypothetically handle many requests but it should not handle too many such requests. If too many requests are centered around the server:
# 1. The server might block your IP address over a concern over DDoS (Distributed Denials of Service) attack. 
# 2. Since multiple requests required multiple sockets to run, it could crash even the machine as well. 

# To avoid this asyncio uses Semaphore  (Semaphore is a visual signalling across a distance. Refer the flags that were used earlier to signal an approaching enemy or fire.)
# A semaphore essentially tell the client about maximum concurrent calls that would be coming from client to the server. 


async def single_pokemon_func_w_rate_limiting():
    start_time = time.time()
    max_concurrant_requests: int = 100
    # creating semphore object
    semaphore = asyncio.Semaphore(max_concurrant_requests)

    async def fetch_single_item(session: aiohttp.ClientSession, id: int, semaphore: asyncio.Semaphore) -> None:
        url: str = f"https://pokeapi.co/api/v2/pokemon/{id}/"
        try: 
            async with session.get(url) as response:
                data = await response.json()
                return data["name"]
        except ConnectionError as e:
            print(f"You have encountered a connection Error: {e}")
        except Exception as e:
            print(f"You have encountered a connection Error: {e}")


    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single_item(session, id, semaphore=semaphore) for id in range(1, 120)]
        result = await asyncio.gather(*tasks)
    print(f"The first 5 elements are: {result[:5]}")
    print(f"Time to result: {time.time() - start_time} ms")
    print(result)

if __name__ == "__main__":
    asyncio.run(single_pokemon_func_w_rate_limiting())
