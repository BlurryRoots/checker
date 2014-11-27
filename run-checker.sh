# starts the checker process monitor
python checker.py \
	# path to pid file
	-f dongle.pid \
	# adress and port of monitor report server
	-r 127.0.0.1 -R 8080 \
	# adress and port of node on which checker is running
	-n 127.0.0.1 -N 42
