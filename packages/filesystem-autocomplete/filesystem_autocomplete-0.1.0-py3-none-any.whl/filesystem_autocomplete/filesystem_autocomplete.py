import os


def _make_filename_safe(fname):
    safename = fname.replace(".", "_").replace("-", "_")
    if safename[0].isnumeric():
        safename = "_" + safename
    return safename


class _FileLikeHelper:
    def __init__(self, pathlike):
        self._fullpath = os.path.abspath(pathlike)
        self._name = os.path.basename(str(self._fullpath))
        self._safe_name = _make_filename_safe(self._name)

    def __str__(self):
        return str(self._fullpath)

    def __repr__(self):
        return self._fullpath


class _FileInfo(_FileLikeHelper):
    @property
    def filepath(self):
        return self._fullpath


class DirectoryInfo(_FileLikeHelper):
    def __init__(self, pathlike, top_path, max_recursion_level=10):
        super().__init__(pathlike)
        self.___files = []
        self.___directories = []
        for file_or_dir in os.listdir(self._fullpath):

            fullfidir = os.path.join(self._fullpath, file_or_dir)
            if os.path.isfile(fullfidir):
                newfile = _FileInfo(fullfidir)
                setattr(self, newfile._safe_name, newfile)
                self.___files.append(file_or_dir)
            elif os.path.isdir(fullfidir):
                new_dir_path = os.path.join(self._fullpath, fullfidir)
                rel_to_top = os.path.relpath(os.path.abspath(top_path), new_dir_path)
                self.___directories.append(file_or_dir)
                dist_to_top = len(rel_to_top.split(os.path.pathsep))
                if dist_to_top <= max_recursion_level:
                    newdir = DirectoryInfo(
                        new_dir_path, top_path, max_recursion_level=max_recursion_level
                    )
                    setattr(self, newdir._safe_name, newdir)
        self.___files.sort()
        self.___directories.sort()

    def __repr__(self):
        finfi = f"Directory: {self._fullpath}\n\n"
        finfi = finfi + "Files:\n"
        for fi in self.___files:
            finfi += f"{fi}\n"
        finfi += "\nSubdirectories:\n"

        for thisdir in self.___directories:
            finfi += f"{thisdir}\n"

        return finfi

    @property
    def dirpath(self):
        return self._fullpath


def walk_directory(starting_directory, max_levels=10):
    return DirectoryInfo(
        starting_directory, starting_directory, max_recursion_level=max_levels
    )
