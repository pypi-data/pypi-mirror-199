import socket

JOB_NAME = f"pyslurmutils.{socket.gethostname()}"  # keep filename friendly
PYTHON_CMD = "python3"
SHEBANG = "#!/usr/bin/env bash"
SPAWN_ARGUMENTS_NAME = "_slurm_spawn_arguments"
