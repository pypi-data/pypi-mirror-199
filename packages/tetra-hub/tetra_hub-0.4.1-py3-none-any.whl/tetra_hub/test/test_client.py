import shutil
import tempfile
from pathlib import Path

from tetra_hub.client import _is_valid_zipped_mlmodelc


def create_sample_mlmodelc(modelDir: Path):
    Path(modelDir).mkdir(parents=True)
    Path(modelDir / "model.espresso.net").touch()
    Path(modelDir / "model.espresso.shape").touch()
    Path(modelDir / "model.espresso.weights").touch()


def test_valid_zipped_mlmodelc():
    #  1. <filepath>/model.espresso.net or
    #  2. <filepath>/model0/model.espresso.net in case of pipeline model
    #  3. <filepath>/foo.mlmodelc/model.espresso.net or
    #  4. <filepath>/foo.mlmodelc/model0/model.espresso.net in case of pipeline model

    # Case 1 and 3:
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / "myModel.mlmodelc"

        create_sample_mlmodelc(modelDir)
        # Case 1
        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(zipPath, "zip", root_dir=modelDir, base_dir=modelDir)
        assert _is_valid_zipped_mlmodelc(f"{zipPath}.zip")

        # Case 3
        zipPath = Path(baseDir) / "my_model_archive_flat"
        shutil.make_archive(zipPath, "zip", root_dir=modelDir, base_dir=baseDir)
        assert _is_valid_zipped_mlmodelc(f"{zipPath}.zip")

    # Case 2 and 4:
    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        modelDir = Path(baseDir) / "myModel.mlmodelc"
        pipelinePath = Path(modelDir) / "model0"
        create_sample_mlmodelc(pipelinePath)

        # Case 2
        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(zipPath, "zip", root_dir=modelDir, base_dir=modelDir)
        assert _is_valid_zipped_mlmodelc(f"{zipPath}.zip")

        # Case 4
        zipPath = Path(baseDir) / "my_model_archive_flat"
        shutil.make_archive(zipPath, "zip", root_dir=modelDir, base_dir=baseDir)
        assert _is_valid_zipped_mlmodelc(f"{zipPath}.zip")

    with tempfile.TemporaryDirectory(suffix="baseDir") as baseDir:
        # Make an invalid model
        modelDir = Path(baseDir) / "myModel.mlmodelc"
        Path(modelDir).mkdir()
        Path(modelDir / "bad_file").touch()

        # Check that this fails
        zipPath = Path(baseDir) / "my_model_archive"
        shutil.make_archive(zipPath, "zip", root_dir=modelDir, base_dir=baseDir)
        assert not _is_valid_zipped_mlmodelc(f"{zipPath}.zip")
