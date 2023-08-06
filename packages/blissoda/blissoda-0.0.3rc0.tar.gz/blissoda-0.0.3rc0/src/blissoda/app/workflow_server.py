from gevent import monkey

monkey.patch_all()

import logging  # noqa E402
import json  # noqa E402
from typing import Mapping  # noqa E402

from blissdata.data.node import get_session_node  # noqa E402
from ewoksjob.client import submit  # noqa E402

logger = logging.getLogger(__name__)


def session_watcher(session_name, **kw):
    session = get_session_node(session_name)
    logger.info(f"Started listening to Bliss session '{session_name}'")
    scan_types = ("scan", "scan_group")

    for ev in session.walk_on_new_events(exclude_children=scan_types, wait=True):
        if ev.type == ev.type.NEW_NODE and ev.node.type == "scan":
            info = ev.node.info
            workflows = info.get("workflows")
            if not workflows:
                continue
            filename = info.get("filename")
            scan_nb = info.get("scan_nb")
            for wfname, nxprocess in workflows.items():
                if not isinstance(nxprocess, Mapping):
                    continue
                try:
                    config = nxprocess["configuration"]
                    job_id = submit_scan_workflow(
                        config["data"], options=config.get("options")
                    )
                except Exception:
                    logger.exception(
                        f"Error when submitting workflow {wfname} for scan {scan_nb} of file {filename}"
                    )
                else:
                    logger.info(
                        f"Submitted workflow '{wfname}' (JOB ID {job_id}) for scan {scan_nb} of file {filename}"
                    )


def submit_scan_workflow(workflow, options=None):
    if options:
        kwargs = json.loads(options)
    else:
        kwargs = None
    future = submit(args=(workflow,), kwargs=kwargs)
    return future.task_id


def main(args):
    session_watcher(args.session)
