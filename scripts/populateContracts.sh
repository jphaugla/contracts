export END=10; export REDIS_HOSTNAME=redis; export REDIS_PORT=6379; export INDEX_NAME=contracts; export COUNT=1000; for i in $(seq 1 $END); do python /home/jovyan/scripts/contracts.py; done
