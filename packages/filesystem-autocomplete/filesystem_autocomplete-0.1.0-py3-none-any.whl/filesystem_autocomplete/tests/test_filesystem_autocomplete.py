import os

from filesystem_autocomplete import walk_directory


def test_walk_directory(tmp_path):
    d = tmp_path / "top_level"
    d.mkdir()

    p = d / "hello.txt"
    p.write_text("yup")

    d2 = d / "level_1_dir1"
    d2.mkdir()

    d3 = d / "level_1_dir2"
    d3.mkdir()

    d4 = d3 / "level_2_dir1"
    d4.mkdir()

    for fi in "123":
        d3fi = d3 / f"test_file_{fi}.txt"
        d3fi.write_text("test")

        d4fi = d4 / f"test_file_{fi}.txt"
        d4fi.write_text("a different test")

    dir_info = walk_directory(str(d))

    assert hasattr(dir_info, "level_1_dir1")
    assert hasattr(dir_info, "level_1_dir2")

    for fi in "123":
        fname_orig = f"test_file_{fi}.txt"
        fname = fname_orig.replace(".", "_")
        assert hasattr(dir_info.level_1_dir2, fname)
        assert hasattr(dir_info.level_1_dir2.level_2_dir1, fname)

        thepath = getattr(dir_info.level_1_dir2, fname).filepath
        assert thepath == str(d3 / fname_orig)

        thisfile = getattr(dir_info.level_1_dir2, fname)
        disp_name = thisfile.__repr__()
        assert os.path.basename(disp_name) == fname_orig

        disp_str = str(thisfile)
        assert os.path.basename(disp_str) == fname_orig

    thepath = dir_info.level_1_dir2.dirpath
    assert thepath == str(d3)

    dir_contents = dir_info.level_1_dir2.__repr__()
    assert "Directory" in dir_contents
    assert "test_file" in dir_contents


def test_problem_files(tmp_path):
    d = tmp_path / "top_level"
    d.mkdir()
    dfi = d / "problem-file.whatever.txt"
    dfi.write_text("test")
    dfi = d / "0problemfile.whatever.txt"
    dfi.write_text("test")
    dir_info = walk_directory(str(d))

    fname = os.path.basename(dir_info._0problemfile_whatever_txt.filepath)
    assert fname == "0problemfile.whatever.txt"

    fname = os.path.basename(dir_info.problem_file_whatever_txt.filepath)
    assert fname == "problem-file.whatever.txt"
