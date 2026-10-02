"""Scoped checks for the reusable workflow's embedded shell scripts.

Run with: python3 -m unittest discover -s .github/tests -v
"""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / "workflows/build_publish.yaml"


class BuildPublishTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.jobs = yaml.safe_load(WORKFLOW.read_text())["jobs"]

    def run_step(self, job, name, root, **env):
        script = next(
            step["run"] for step in self.jobs[job]["steps"]
            if step.get("name") == name
        )
        return subprocess.run(
            ["bash", "-c", script], cwd=root,
            env={**os.environ, **env}, capture_output=True, text=True,
        )

    def test_one_build_and_cleanup_with_per_rock_publish(self):
        self.assertNotIn("strategy", self.jobs["build"])
        self.assertNotIn("strategy", self.jobs["cleanup"])
        self.assertEqual(self.jobs["stage"]["needs"], "build")
        self.assertEqual(self.jobs["publish"]["needs"], "stage")
        self.assertEqual(self.jobs["build"]["env"]["LP_PREFIX"],
                         self.jobs["cleanup"]["env"]["LP_PREFIX"])

    def test_batch_arguments_and_empty_list_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rock in ("alpha", "beta"):
                directory = root / "rocks" / rock
                directory.mkdir(parents=True)
                (directory / "rockcraft.yaml").touch()
            binaries = root / "bin"
            binaries.mkdir()
            (binaries / "git").write_text("#!/bin/sh\nexit 0\n")
            (binaries / "sunbeam-watchtower").write_text(
                '#!/bin/sh\nprintf "%s\\n" "$@" > "$GITHUB_WORKSPACE/args"\n'
            )
            for binary in binaries.iterdir():
                binary.chmod(0o755)
            env = dict(
                PATH=f"{binaries}:{os.environ['PATH']}",
                GITHUB_WORKSPACE=tmp, GITHUB_RUN_ID="1", GITHUB_RUN_ATTEMPT="2",
                LP_OWNER="owner", LP_PREFIX="prefix",
            )
            result = self.run_step(
                "build", "Build on Launchpad and download ROCKs", root,
                ROCKS=json.dumps(["alpha", "beta"]), **env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            args = (root / "args").read_text().splitlines()
            self.assertEqual(args[-2:], ["alpha", "beta"])
            (root / "args").unlink()
            for selection in ([], ["../alpha"], ["alpha\nbeta"]):
                result = self.run_step(
                    "build", "Build on Launchpad and download ROCKs", root,
                    ROCKS=json.dumps(selection), **env,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / "args").exists())

    def stage_fixture(self, root):
        directory = root / "rocks/alpha"
        directory.mkdir(parents=True)
        (directory / "rockcraft.yaml").write_text(
            "platforms:\n  amd64:\n  arm64:\nparts:\n"
        )
        for rock in ("alpha", "beta", "alpha-extra"):
            artifacts = root / "artifacts" / f"gh-rocks-1-2-55ed1c31-{rock}"
            artifacts.mkdir(parents=True)
            for arch in ("amd64", "arm64"):
                (artifacts / f"{rock}_1_{arch}.rock").touch()
        return root / "artifacts/gh-rocks-1-2-55ed1c31-alpha"

    def test_stage_keeps_rock_artifacts_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.stage_fixture(root)
            result = self.run_step(
                "stage", "Stage ROCKs for existing release workflow", root,
                ROCK="alpha",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                sorted(p.name for p in (root / "rocks/alpha").glob("*.rock")),
                ["alpha_1_amd64.rock", "alpha_1_arm64.rock"],
            )

    def test_stage_rejects_missing_and_duplicate_architectures(self):
        for duplicate in (False, True):
            with self.subTest(duplicate=duplicate), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                artifacts = self.stage_fixture(root)
                (artifacts / "alpha_1_arm64.rock").unlink()
                if duplicate:
                    (artifacts / "alpha_2_amd64.rock").touch()
                result = self.run_step(
                    "stage", "Stage ROCKs for existing release workflow", root,
                    ROCK="alpha",
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(list((root / "rocks/alpha").glob("*.rock")), [])


if __name__ == "__main__":
    unittest.main()
