import os
import json
import logging
from glob import glob
from ewoksjob.client import submit
from ewoksjob.tasks import execute_graph


def modify_workflow(old_processed: str, new_processed: str, workflow: dict):
    # Modify destination for results
    for nodeattrs in workflow["nodes"]:
        for idict in nodeattrs.get("default_inputs", list()):
            if (
                isinstance(idict["value"], str)
                and old_processed in idict["value"]
                and "ring_detection" not in idict["value"]
            ):
                idict["value"] = idict["value"].replace(old_processed, new_processed)

    # Modify workflow links
    for linkattrs in workflow["links"]:
        data_mapping = linkattrs.get("data_mapping", list())
        if any("detector" in data.values() for data in data_mapping):
            data_mapping.append(
                {
                    "source_output": "detector_config",
                    "target_input": "detector_config",
                }
            )

    # Modify calibration file
    for nodeattrs in workflow["nodes"]:
        if "PyFaiConfig" in nodeattrs["task_identifier"]:
            is_pdf = False
            for param in nodeattrs["default_inputs"]:
                if param["name"] == "filename":
                    is_pdf = "PDF" in param["value"]
                    break
            if is_pdf:
                for param in nodeattrs["default_inputs"]:
                    if param["name"] == "integration_options":
                        param["value"][
                            "mask_file"
                        ] = "fabio:///data/visitor/im21/id31/20230227/calibration_WDN/mask_PDF.edf"


def reprocess(
    proposal: str, session: str, process_name: str, backup_root: str = "/tmp"
) -> None:
    remote = os.environ.get("BEACON_HOST")
    if not remote:
        logging.basicConfig(level=logging.INFO)
    processed_dir = f"/data/visitor/{proposal}/id31/{session}/processed/"
    if not backup_root:
        backup_root = processed_dir
    backup_dir = os.path.join(backup_root, "_nobackup")

    workflows = glob(os.path.join(processed_dir, "streamline", "*", "*.json"))
    for wffilename in workflows:
        with open(wffilename, "r") as f:
            workflow = json.load(f)

        kwargs = dict()
        kwargs["varinfo"] = {
            "root_uri": backup_dir,
            "scheme": "nexus",
        }

        old_processed = os.path.join("processed", "streamline")
        new_processed = os.path.join("processed", process_name)
        kwargs["convert_destination"] = wffilename.replace(old_processed, new_processed)

        modify_workflow(old_processed, new_processed, workflow)

        if remote:
            submit(args=(workflow,), kwargs=kwargs)
        else:
            execute_graph(workflow, **kwargs)


if __name__ == "__main__":
    # os.environ["BEACON_HOST"] = "id31:25000"
    reprocess("im21", "20230227", "streamline_fix_pdf_mask")
