import argparse
import urllib.request

from bioblend import galaxy

WF = "https://drive.google.com/uc?export=download&id=13xE8o7tucHGNA0qYkEP98FfUGl2wdOU5"
HIST = (
    "https://zenodo.org/record/4686436/files/TFdemo_wf_april13_planemo.ga?download=1"
)
WF_FILE = "tf_workflow.ga"
HIST_FILE = "tf_history.tgz"


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g", "--galaxy", help="URL of target galaxy", default="http://localhost:8080"
    )
    parser.add_argument("-a", "--key", help="Galaxy admin key", default="8993d65865e6d6d1773c2c34a1cc207d")
    return parser


def main():
    """
    load the planemo tool_factory demonstration history and tool generating workflow
    fails in planemo served galaxies because there seems to be no user in trans?
    """
    args = _parser().parse_args()
    urllib.request.urlretrieve(WF, WF_FILE)
    urllib.request.urlretrieve(HIST, HIST_FILE)
    assert args.key, "Need an administrative key for the target Galaxy supplied please"
    gi = galaxy.GalaxyInstance(
        url=args.galaxy, key=args.key, email="planemo@galaxyproject.org"
    )
    x = gi.workflows.import_workflow_from_local_path(WF_FILE, publish=True)
    print(f"installed {WF_FILE} Returned = {x}\n")
    x = gi.histories.import_history(file_path=HIST_FILE)
    print(f"installed {HIST_FILE} Returned = {x}\n")


if __name__ == "__main__":
    main()
