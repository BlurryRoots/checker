# checker

## Idea

Processes run a deamonized client, which checks if a specific process is alive and frequently reports to the monitor server. The status of each node is shown on the dashboard. Nodes can also be stopped and started/restarted.

## Setup

Just build the docker image using the ```build.sh``` script.
After that you can run the server instance via ```run.sh```.
The client has not yet been implemented.


## Testing

If you have python and requests installed, you can use ```send-test.py```.

