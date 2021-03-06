#!/usr/bin/python

import logging
import os
import subprocess
import tarfile
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class ToolHandler(PatternMatchingEventHandler):
    def __init__(self, watchme='/export/galaxy/tools', galaxy_root='/galaxy-central', conda_prefix='/galaxy-central/planemo/con', patterns=['.testme',]):
        PatternMatchingEventHandler.__init__(
            self, patterns=patterns, ignore_directories=True,
            case_sensitive=False
        )
        self.tool_dir = watchme
        self.work_dir = os.path.join(galaxy_root,'planemo')
        self.GALAXY_ROOT = galaxy_root
        self.CONDA_PREFIX = conda_prefix
        self.galaxy_root = galaxy_root
        logging.info('Starting watchdog toolhandler in %s' % self.galaxy_root)
        self.tar_dir = os.path.join(self.galaxy_root, "tested_TF_tools")
        if not os.path.exists(self.tar_dir):
            os.mkdir(self.tar_dir)
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)

    def on_any_event(self, event):
        # rsync and watchdog work strangely
        if event.is_directory:
            logging.info(
                "ignore directory event %s on %s" % (event.event_type, event.event_path)
            )
            return
        logging.info("### saw %s on %s" % (event.event_type, event.src_path))
        targ = os.path.join(os.path.split(event.src_path)[0], ".testme")
        time.sleep(0.1)
        if os.path.exists(targ):
            try:
                os.remove(targ)
            except Exception:
                logging.info("Cannot delete %s" % targ)
            tooldir = os.path.split(event.src_path)[0]
            toolname = os.path.split(tooldir)[1]
            logging.info(f"{event.src_path} {toolname} requests testing")
            dirlist = os.listdir(tooldir)
            logging.info("### test dirlist %s, path %s" % (dirlist, tooldir))
            xmls = [x for x in dirlist if os.path.splitext(x)[1] == ".xml"]
            if not "%s.xml" % toolname in xmls:
                logging.warning(
                    "Found no %s.xml file after change to %s"
                    % (toolname, event.src_path)
                )
                return
            p = self.planemo_test(tooldir, toolname)
            if p:
                if p.returncode == 0:
                    newtarpath = self.makeToolTar(tooldir, toolname)
                    logging.info("### Tested toolshed tarball %s written" % newtarpath)
                else:
                    logging.debug("### planemo stdout:")
                    logging.debug(p.stdout)
                    logging.debug("### planemo stderr:")
                    logging.debug(p.stderr)
                    logging.info("### Planemo call return code = %d" % p.returncode)
        else:
            logging.info("Event %s on %s ignored" % (event.event_type, event.src_path))

    def planemo_test(self, tooldir, toolname):
        testrepdir = os.path.join(self.tar_dir, toolname)
        tool_test_output = os.path.join(
            testrepdir, f"{toolname}_planemo_test_report.html"
        )
        if not os.path.exists(testrepdir):
            os.makedirs(testrepdir)
        cll = [
            "planemo",
            "test",
            "--conda_prefix",
            self.CONDA_PREFIX,
            "--galaxy_root",
            self.GALAXY_ROOT,
            "--test_output",
            tool_test_output,
            "--update_test_data",
            os.path.join(tooldir, "%s.xml" % toolname),
        ]
        logging.info("### calling %s" % " ".join(cll))
        p = subprocess.run(
            cll,
            cwd=self.work_dir,
            shell=False,
            capture_output=True,
            encoding="utf8",
        )
        return p

    def makeToolTar(self, tooldir, toolname):
        """move outputs into test-data and prepare the tarball"""
        excludeme = "_planemo_test_report.html"

        def exclude_function(tarinfo):
            filename = tarinfo.name
            return None if filename.endswith(excludeme) else tarinfo

        os.chdir(os.path.split(tooldir)[0])
        newtarpath = os.path.join(self.tar_dir, toolname, "%s_toolshed.gz" % toolname)
        tf = tarfile.open(newtarpath, "w:gz")
        tf.add(
            name=toolname,
            arcname=toolname,
            filter=exclude_function,
        )
        tf.close()
        os.chdir(self.work_dir)
        return newtarpath


if __name__ == "__main__":
    WATCHME = "/export/galaxy/tools/" # in the galaxy-server container
    GALAXY_ROOT = "/galaxy-central" # in our container
    WATCH_PATTERN = [".testme"] # in the galaxy_server container
    CONDA_PREFIX = "/galaxy-central/planemo/con"
    logging.basicConfig(
        level=logging.INFO,
        filename=os.path.join('/export/galaxy', "toolwatcher.log"),
        filemode="w",
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    event_handler = ToolHandler(watchme=WATCHME, galaxy_root=GALAXY_ROOT, conda_prefix=CONDA_PREFIX, patterns=WATCH_PATTERN)
    observer = Observer()
    observer.schedule(event_handler, path=WATCHME, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
