#/bin/bash

# Look for relevant env var values, if not, use defaults
python -m src.fit_model \
--species ${SPECIES:-bullfrog} \
--model_type ${MODEL_TYPE:-birdnet} \
--batch_size ${BATCH_SIZE:-128}