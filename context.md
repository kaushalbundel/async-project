# Things that I do not understand from the topic

    - (Article link)[https://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html]
        -  What is socket? It is a kind of library but used for what?
        - How is the request objects being created?
            - The examples used in the article are too complicated for me to understand. I need a custom project that can fulfill my needs.

# Key Pointers about async? How to think about it?

    - There are two types of tasks:
        1. CPU bound tasks: Computations like 2+2 and so on. These computations take use CPU directly. To speed up such calculations we can do use threads. Threads enable individual computations to be run on the individual cpu threads. Each thread will have a Calculation run for 100 or so ms, after which it gets blocked and subsequently of calculating a parallel computation is given to another thread.

        2. IO bound tasks: Reading/writing to file or waiting to a network to get some data from the network. ~~In this case having thread does not make sense ~~ Having threads make sense, but using threads has an inherent associated cost. Like, every thread consumes some memory to run and little cpu time is used when the threads are switched as the calculations are going on that are not heavily dependent on the CPU. asyncio basically helps in this case, where instead of the code running in a sequential manner the control is given to the multiple operations using a thing called event loop.
