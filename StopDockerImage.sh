
#!/bin/bash

# This command will stop all instances of the CLAI playground docker container running on the local compute node...
# The command bases this on the docker image type that containers are derived from.

# Determine if there are any instances to stop...
dockerInstances=$(docker ps -a -q --filter ancestor=CLAIPlaygroundContainer --format="{{.ID}}")

# If there was anything to stop...
if [[ -n "${dockerInstances/[ ]*\n/}" ]]
then
    echo "Stopping CLAI Playground Docker Instances: $dockerInstances"
    # We stop those instances...
    docker rm $(docker stop $dockerInstances)
else
   echo "No CLAI Playgrounds were found running. Nothing stopped."
fi
