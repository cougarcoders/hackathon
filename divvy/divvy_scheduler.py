# Larry Wells
# 02/21/2016

# Schedule events to fire off get content and send content to user
import build_queues
import schedule
from time import sleep

def sequence(schedule):
	print("sequence called *** for: " + str(schedule))
	# Look at content and update if needed
	print("building queues")
	build_queues.get_content(schedule)

	# Send out data to use per schedule
	print("sending data to users")
	build_queues.divvy_queue(schedule)

schedule.every(1).minutes.do(lambda: sequence(1))
schedule.every(2).minutes.do(lambda: sequence(2))
schedule.every(3).minutes.do(lambda: sequence(3))
schedule.every(4).minutes.do(lambda: sequence(4))

while True:
	schedule.run_pending()
	sleep(1)

