#/bin/bash

# Check if the environment variable IS_DEVCONTAINER is set to true
if [ "$IS_DEVCONTAINER" = "true" ]; then
  # If it's true, tail /dev/null to keep the container running
  echo "Running in DevContainer mode. Keeping container alive..."
  tail -f /dev/null
else
  # If it's false, run the workflow
  echo "Running production mode. Executing production run..."
  source run_prod_workflow.sh
fi