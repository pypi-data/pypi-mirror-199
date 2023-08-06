import click
import loci
import loci.cli
from rich.progress import Progress

from loci_sarif import utils, SOURCE_FOLDER_NAME


@click.command("import")
@click.option("-f", "--file",
              prompt="SARIF JSON file",
              help="The SARIF file with the output of a scan",
              required=True,
              type=str)
@click.option("-i", "--imports",
              help="Specific vulnerabilities or severities (comma separated) to import",
              required=True,
              type=str,
              default="error,warning,note")
def add(file, imports):
    """Process a SARIF file and import results to Loci Notes"""

    loci.cli.print_info("Getting directory project information...")
    project = loci.get_local_project()
    if project is None:
        loci.cli.print_error("Unable to determine the associated project. Run this importer under a directory "
                             "associated with a Loci Notes project.")
        quit(-1)

    loci.cli.print_success(f"Using [bold]{project.name}[/bold].")

    results_list = utils.open_sarif_file_and_get_results(file)

    imports_list = imports.split(",")

    for i in range(len(imports_list)):
        # Remove whitespace, lowercase all, remove underscores
        imports_list[i] = imports_list[i].strip().lower().replace("_", " ")

    imported_severities_list = []
    if "error" in imports_list:
        imported_severities_list.append("error")
    if "warning" in imports_list:
        imported_severities_list.append("warning")
    if "note" in imports_list:
        imported_severities_list.append("note")

    # First count up total number of results to get a semi-accurate count of the results for the progress bar
    valid_results_found = 0
    for result in results_list:
        if result.ruleid.lower() in imports_list or result.severity.lower() in imported_severities_list:
            valid_results_found += 1

    if valid_results_found == 0:
        loci.cli.print_error("No results were found for the given imports. See the [bold]summary[/bold]"
                             " for valid vulnerabilities, or use 'Error', 'Warning', and 'Note' "
                             "to import by severity.")
        quit(-1)

    with Progress() as progress_bar:
        task = progress_bar.add_task(f"Importing {valid_results_found} results...", total=valid_results_found)

        for result in results_list:
            if result.ruleid.lower() in imports_list or result.severity.lower() in imported_severities_list:
                # Create note contents
                new_note_contents = "**Security Issue Detected**\n\n"
                new_note_contents += "**Rule ID** - " + result.ruleid + "\n"
                new_note_contents += "**Severity** - " + result.severity.capitalize() + "\n"
                new_note_contents += "**Message** - " + result.message

                # Send the info to the LN server for the result
                artifact_descriptor_filename = utils.calculate_artifact_from_fq_filename(
                    result.get_artifact(), SOURCE_FOLDER_NAME)
                loci.api_new_note(project, artifact_descriptor_filename, result.tool, "LOG", new_note_contents)
                progress_bar.update(task, advance=1)
