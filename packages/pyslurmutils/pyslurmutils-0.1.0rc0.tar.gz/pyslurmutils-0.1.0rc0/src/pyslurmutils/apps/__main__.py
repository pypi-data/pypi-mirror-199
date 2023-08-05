"""Monitor SLURM jobs and status"""

import sys
import time
import argparse
import datetime
from typing import List
import numpy

from .cli import common as common_cli
from .cli import status as status_cli
from .cli import cancel as cancel_cli
from ..client import SlurmScriptRestClient


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        description="Slurm Job Monitor", prog="pyslurmutils"
    )
    subparsers = parser.add_subparsers(help="Commands", dest="command")

    check = subparsers.add_parser("check", help="Check slurm connection")
    common_cli.add_parameters(check)

    status = subparsers.add_parser("status", help="Job status")
    common_cli.add_parameters(status)
    status_cli.add_parameters(status)

    status = subparsers.add_parser("cancel", help="Cancel Slurm jobs")
    common_cli.add_parameters(status)
    cancel_cli.add_parameters(status)

    args = parser.parse_args(argv[1:])

    if args.command == "status":
        command_status(args)
    elif args.command == "check":
        command_check(args)
    elif args.command == "cancel":
        command_cancel(args)
    else:
        parser.print_help()
    return 0


def command_status(args):
    common_cli.apply_parameters(args)
    status_cli.apply_parameters(args)

    with SlurmScriptRestClient(
        args.url,
        args.user_name,
        args.token,
        log_directory=args.log_directory,
    ) as client:
        for _ in _monitor_loop(args.interval):
            _print_jobs(client, args.jobid, args.all)
            if args.jobid:
                client.print_stdout_stderr(args.jobid)


def command_check(args):
    common_cli.apply_parameters(args)

    with SlurmScriptRestClient(
        args.url,
        args.user_name,
        args.token,
        log_directory=args.log_directory,
    ) as client:
        assert client.server_has_api(), "Wrong Rest API version"


def command_cancel(args):
    cancel_cli.apply_parameters(args)
    with SlurmScriptRestClient(
        args.url,
        args.user_name,
        args.token,
        log_directory=args.log_directory,
    ) as client:
        job_ids = args.job_ids
        if not job_ids:
            job_ids = client.get_all_job_properties()
        for job_id in job_ids:
            client.cancel_job(job_id)


def _monitor_loop(interval):
    try:
        if not interval:
            yield
            return
        while True:
            yield
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


def _print_jobs(client, jobid, all_users):
    if jobid:
        jobs = [client.get_job_properties(jobid)]
    else:
        if all_users:
            filter = {"user_name": None}
        else:
            filter = None
        jobs = client.get_all_job_properties(filter=filter)
    fields = {
        "job_id": _passthrough,
        "name": _passthrough,
        "job_state": _passthrough,
        "user_name": _passthrough,
        "submit_time": _duration,
        "start_time": _duration,
        "tres_alloc_str": _passthrough,
    }
    titles = {
        "job_id": "Job ID",
        "job_state": "State",
        "user_name": "User",
        "submit_time": "Submit time",
        "start_time": "Run time",
        "tres_alloc_str": "Resources",
        "name": "Name",
    }
    rows = list()
    for info in jobs:
        rows.append([parser(info[k]) for k, parser in fields.items()])
    if not rows:
        return
    titles = [titles.get(k, k) for k in fields]
    print(_format_info(titles, rows))


def _passthrough(x):
    return str(x)


def _duration(x):
    if x == 0:
        return "-"
    duration = datetime.datetime.now() - datetime.datetime.fromtimestamp(x)
    if duration.total_seconds() < 0:
        return "-"
    return str(duration)


def _format_info(titles: List[str], rows: List[List[str]]):
    lengths = numpy.array([[len(s) for s in row] for row in rows])
    fmt = "   ".join(["{{:<{}}}".format(n) for n in lengths.max(axis=0)])
    infostr = "\n "
    infostr += fmt.format(*titles)
    infostr += "\n "
    infostr += "\n ".join([fmt.format(*row) for row in rows])
    return infostr


if __name__ == "__main__":
    sys.exit(main())
