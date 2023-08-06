import json
import loci
import loci.cli
from loci_sarif import SUPPORTED_SARIF_VERSIONS, SUPPORTED_SARIF_TOOLS


def calculate_artifact_from_fq_filename(fq_file_path, src_root_dir):
    # Next, we need to figure out if we can autodetect the full artifact filename (usually by looking
    # for the source root directory).
    tmp_srd = "/" + src_root_dir + "/"
    if tmp_srd in fq_file_path:
        # Easy mode, slice away the source root dir and everything before it.
        idx = fq_file_path.index(tmp_srd)
        return fq_file_path[idx+len(tmp_srd):]

    tmp_srd = src_root_dir + "/"
    if tmp_srd in fq_file_path:
        # Easy mode, slice away the source root dir and everything before it.
        idx = fq_file_path.index(tmp_srd)
        return fq_file_path[idx+len(tmp_srd):]

    else:
        # Harder mode. We can guess the name by looking at the basename of the "path" stored in the run.
        # TODO

        # For now, just return as is.
        return fq_file_path


class SarifResult():
    def __init__(self,
                 ruleid: str,
                 severity: str,
                 filename: str,
                 line: int,
                 message: str,
                 tool: str):
        self.ruleid = ruleid
        self.severity = severity
        self.filename = filename
        self.line = line
        self.message = message
        self.tool = tool

    def get_artifact(self):
        return self.filename + ":" + str(self.line)


def open_sarif_file_and_get_results(input_filename):
    loci.cli.print_info("Opening SARIF file...")
    try:
        with open(input_filename) as fd:
            sarif_dict = json.load(fd)
    except FileNotFoundError:
        loci.cli.print_error(f"Failed to open the file '{input_filename}'. Please check to make sure it exists.")
        quit(-1)
    except json.JSONDecodeError:
        loci.cli.print_error(f"Failed to parse the file '{input_filename}'. It does not appear to be valid JSON.")
        quit(-1)
    try:
        if "https://docs.oasis-open.org/sarif/sarif/" not in sarif_dict["$schema"]:
            raise KeyError
    except KeyError:
        loci.cli.print_error(f"Failed to parse the file '{input_filename}'. It does not appear to be a valid "
                             "SARIF file.")
        quit(-1)

    if sarif_dict["version"] not in SUPPORTED_SARIF_VERSIONS:
        version = sarif_dict["version"]
        loci.cli.print_warning(f"The file '{input_filename}' is SARIF v{version}, while only v2.1.0 is supported."
                               " The file may still import correctly, but if not, open a new issue in the source"
                               " code repo for loci-sarif.")

    loci.cli.print_success("SARIF file loaded.")

    results = []

    for run_dict in sarif_dict["runs"]:
        if run_dict["tool"]["driver"]["name"] not in SUPPORTED_SARIF_TOOLS:
            loci.cli.print_warning(f"The tool used to generate a run, '{input_filename}', is not officially "
                                   "supported by this Loci Notes importer. We'll try to import it anyhow, and "
                                   "it should work, but if not open an issue and include which tool was used to"
                                   " generate it. If it does work, let us know, we can add it to the list of "
                                   "known good tools.")
        for result_dict in run_dict["results"]:
            ruleid = result_dict["ruleId"]
            if len(result_dict["locations"]) > 1:
                loci.cli.print_warning(f"Multiple locations are reported in the result for {ruleid}. This is "
                                       "weird and not officially supported by this Loci Notes importer. Please "
                                       "open an issue if you see this, and we'll try to import the first one.")

            # TODO we might be able to slice out everything past _src if it's in the result.
            filename = result_dict["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
            line = result_dict["locations"][0]["physicalLocation"]["region"]["endLine"]
            message = result_dict["message"]["text"]

            rule_info_dict = None
            for rule_info in run_dict["tool"]["driver"]["rules"]:
                if rule_info["id"] == ruleid:
                    rule_info_dict = rule_info
                    break

            if rule_info_dict is None:
                loci.cli.print_error(f"Failed to find the rule {ruleid}. Please check to make sure the SARIF "
                                     "file is correct.")
                quit(-1)

            severity = rule_info_dict["defaultConfiguration"]["level"]
            tool = run_dict["tool"]["driver"]["name"]

            tmp_result = SarifResult(ruleid=ruleid,
                                     filename=filename,
                                     line=line,
                                     message=message,
                                     severity=severity,
                                     tool=tool)
            results.append(tmp_result)
    return results
