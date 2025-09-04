from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from service.data_updater import run_updates
import asyncio

async def main():
    """
    main function that set up and run the task programator
    """

    # make instance of programator
    scheduler = AsyncIOScheduler()

    # add the tasks to the programator
    # function run_updates running and tigger is who define the interval
    scheduler.add_job(
        run_updates,
        trigger=IntervalTrigger(hours=24),
        id='update_github_data',
        name='Update data of Github'
    )

    # start the programmer
    scheduler.start()

    print('started update scheduler')
    # use the infinity loop for the program don't finish
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit): # Handles the interrupt for a clean shutdown
        pass