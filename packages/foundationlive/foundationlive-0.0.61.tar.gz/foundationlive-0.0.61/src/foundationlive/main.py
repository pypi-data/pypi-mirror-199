"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = foundationlive.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import copy
import logging
import pathlib
import platform
import sys

import yaml

from foundationlive import __version__, lib

from . import config as configmod
from . import googlesheets, model
from . import writer as writermod

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


try:
    from . import menu
except NotImplementedError:
    _logger.debug("simple_term_menu isn't supported on windows")


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from foundationlive.skeleton import fib`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return ivalue


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="report time spent on projects")
    parser.add_argument(
        "--version",
        action="version",
        version="foundationlive {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "--data-path",
        default=configmod.config["FOUNDATIONLIVE_DATA_PATH"],
        required=False,
        help="path to data.yaml",
    )
    parser.add_argument(
        "-i",
        "--invoice",
        type=check_positive,
        required=False,
        action="append",
        help="Remove all task entries that don't match invoice "
        "these invoice numbers (eg, 1, 2 10)",
    )
    parser.add_argument(
        "--google-sheets",
        required=False,
        action="store_true",
        help="update google sheets",
    )
    parser.add_argument(
        "--show-config",
        required=False,
        action="store_true",
        help="display details of how this app is configured",
    )
    parser.add_argument(
        "-r",
        "--show-reports",
        required=False,
        action="store_true",
        help="display reports",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")
    configmod.init()

    if args.show_config:
        configmod.show_config()

    records_path = pathlib.Path(args.data_path)
    if not records_path.exists():
        msg = f"{records_path} is missing"
        _logger.critical(msg)
        sys.exit(-1)

    with open(records_path, "r") as stream:
        try:
            external_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    timesheet = model.Timesheet(**external_data)
    timesheet_filtered = copy.deepcopy(timesheet)

    if args.invoice:
        for day in timesheet.days:
            if day.invoice not in args.invoice:
                timesheet_filtered.days.remove(day)

    outputs = [
        lib.Thingy(
            "view_hours_per_task.txt", lib.view_hours_per_task, timesheet_filtered
        ),
        lib.Thingy(
            "view_hours_worked_per_day.txt",
            lib.view_hours_worked_per_day,
            timesheet_filtered,
        ),
        lib.Thingy(
            "view_hours_worked_per_day_summary.txt",
            lib.view_hours_worked_per_day_summary,
            timesheet_filtered,
        ),
        lib.Thingy("view_csv.txt", lib.view_csv_jinja2, timesheet_filtered),
        # want timesheet for view_invoices instead of timesheet_filtered
        lib.Thingy("view_invoices.txt", lib.view_invoices, timesheet),
    ]

    reports_output_dir = pathlib.Path(
        configmod.config["FOUNDATIONLIVE_TEMPLATES_OUTPUT_DIRECTORY"]
    ).expanduser()

    for thing in outputs:
        out = thing.fn(thing.data)
        out_path = reports_output_dir / thing.fname
        _logger.debug(f"writing {out_path}")
        writermod.FileWriter(out_path).write(out)
    #        writermod.ConsoleWriter().write(out)

    if args.google_sheets:
        out = lib.view_google_sheets(timesheet_filtered)
        googlesheets.main(out)

    windows = platform.system() == "Windows" or platform.system().startswith("CYGWIN")
    if args.show_reports and not windows:
        menu.main()


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m foundationlive.skeleton 42
    #
    run()
