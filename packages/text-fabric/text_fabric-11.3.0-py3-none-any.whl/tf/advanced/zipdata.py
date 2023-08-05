import sys
from zipfile import ZipFile

from .helpers import splitModRef
from ..parameters import ZIP_OPTIONS, RELATIVE
from ..core.helpers import console
from ..core.files import (
    normpath,
    expanduser as ex,
    backendRep,
    DOWNLOADS,
    TEMP_DIR,
    prefixSlash,
    dirExists,
    scanDir,
    initTree,
)

DW = ex(DOWNLOADS)

__pdoc__ = {}

HELP = """
### USAGE

``` sh
text-fabric-zip --help

text-fabric-zip {org}/{repo}{relative}

text-fabric-zip {org}/{repo}{relative} --backend=gitlab.huc.knaw.nl
```

### EFFECT

Zips text-fabric data from your local github/gitlab repository into
a release file, ready to be attached to a github release.

Your repo must sit in `~/github/*org*/*repo*` or in `~/gitlab/*org*/*repo*`
or in whatever Gitlab backend you have chosen.

Your TF data is assumed to sit in the toplevel tf directory of your repo.
But if it is somewhere else, you can pass relative, e.g phrases/heads/tf

It is assumed that your tf directory contains subdirectories according to
the versions of the main datasource.
The actual .tf files are in those version directories.

Each of these version directories will be zipped into a separate file.

The resulting zip files end up in ~/Downloads/*backend*/*org*-release/*repo*
and the are named *relative*-*version*.zip
(where the / in relative have been replaced by -)

"""

EXCLUDE = {".DS_Store"}


def zipData(
    backend,
    org,
    repo,
    relative=RELATIVE,
    version=None,
    tf=True,
    keep=True,
    source=None,
    dest=None,
):
    """Zips TF data into a single file, ready to be attached to a release.

    Parameters
    ----------
    backend: string
        The backend for which the zip file is meant (`github`, `gitlab`, etc).
    org, repo: string
        Where the corpus is located on the backend,
    relative: string, optional "tf"
        The subdirectory of the repo that will be zipped.
    version: string, optional None
        If passed, only data of this version is zipped, otherwise all versions
        will be zipped.
    tf: boolean, optional True
        Whether the data to be zipped are tf feature files or other kinds of data.
    keep: boolean, optional True
        Whether previously generated zipfiles in the destination directory should
        be kept or deleted.
    source: string, optional None
        Top directory under which the repository is found, if None; this directory
        is given by the backend: `~/github`, `~/gitlab`, etc.
    dest: string, optional None
        Top directory under which the generated zipfiles are saved; if None,
        this directory under the user's Downloads directory and further determined by
        the backend: `~/Downloads/github`, `~/Downloads/gitlab`, etc.
    """

    if source is None:
        source = backendRep(backend, "clone")
    if dest is None:
        dest = f"{DW}/{backendRep(backend, 'norm')}"
    relative = prefixSlash(normpath(relative))
    console(f"Create release data for {org}/{repo}{relative}")
    sourceBase = normpath(f"{source}/{org}")
    destBase = normpath(f"{dest}/{org}-release")
    sourceDir = f"{sourceBase}/{repo}{relative}"
    destDir = f"{destBase}/{repo}"
    dataFiles = {}

    initTree(destDir, fresh=not keep)
    relativeDest = relative.removeprefix("/").replace("/", "-")

    if tf:
        if not dirExists(sourceDir):
            return
        with scanDir(sourceDir) as sd:
            versionEntries = [(sourceDir, e.name) for e in sd if e.is_dir()]
        if versionEntries:
            console(f"Found {len(versionEntries)} versions")
        else:
            versionEntries.append((sourceDir, ""))
            console("Found unversioned features")
        for (versionDir, ver) in versionEntries:
            if ver == TEMP_DIR:
                continue
            if version is not None and version != ver:
                continue
            versionRep = f"/{ver}" if ver else ""
            versionRep2 = f"{ver}/" if ver else ""
            versionRep3 = f"-{ver}" if ver else ""
            tfDir = f"{versionDir}{versionRep}"
            with scanDir(tfDir) as sd:
                for e in sd:
                    if not e.is_file():
                        continue
                    featureFile = e.name
                    if featureFile in EXCLUDE:
                        continue
                    if not featureFile.endswith(".tf"):
                        console(
                            f'WARNING: non feature file "{versionRep2}{featureFile}"',
                            error=True,
                        )
                        continue
                    dataFiles.setdefault(ver, set()).add(featureFile)

        console(f"zip files end up in {destDir}")
        for (ver, features) in sorted(dataFiles.items()):
            item = f"{org}/{repo}"
            versionRep = f"/{ver}" if ver else ""
            versionRep3 = f"-{ver}" if ver else ""
            target = f"{relativeDest}{versionRep3}.zip"
            console(
                f"zipping {item:<25} {ver:>4} with {len(features):>3} features ==> {target}"
            )
            with ZipFile(f"{destDir}/{target}", "w", **ZIP_OPTIONS) as zipFile:
                for featureFile in sorted(features):
                    zipFile.write(
                        f"{sourceDir}{versionRep}/{featureFile}",
                        arcname=featureFile,
                    )
    else:

        def collectFiles(base, path, results):
            thisPath = f"{base}/{path}" if path else base
            # internalBase = f"{relative}/{path}" if path else relative
            internalBase = path
            with scanDir(thisPath) as sd:
                for e in sd:
                    name = e.name
                    if name in EXCLUDE:
                        continue
                    if e.is_file():
                        results.append(
                            (f"{internalBase}/{name}", f"{base}/{path}/{name}")
                        )
                    elif e.is_dir():
                        collectFiles(base, f"{path}/{name}", results)

        results = []
        versionRep = f"/{version}" if version else ""
        sourceDir = f"{sourceDir}{versionRep}"
        collectFiles(sourceDir, "", results)
        if not relativeDest:
            relativeDest = "-"
        console(f"zipping {org}/{repo}{relative}{versionRep} with {len(results)} files")
        console(f"zip file is {destDir}/{relativeDest}.zip")
        with ZipFile(f"{destDir}/{relativeDest}.zip", "w", **ZIP_OPTIONS) as zipFile:
            for (internalPath, path) in sorted(results):
                zipFile.write(
                    path,
                    arcname=internalPath,
                )


def main(cargs=sys.argv):
    if len(cargs) < 2 or any(
        arg in {"--help", "-help", "-h", "?", "-?"} for arg in cargs
    ):
        console(HELP)
        return

    backend = None

    newArgs = []
    for arg in cargs:
        if arg.startswith("--backend="):
            backend = arg[10:]
        else:
            newArgs.append(arg)
    cargs = newArgs

    moduleRef = cargs[1]

    parts = splitModRef(moduleRef)
    if not parts:
        console(HELP)
        return

    (org, repo, relative, checkout, theBackend) = parts
    relative = prefixSlash(normpath(relative))

    tf = (
        relative.removeprefix("/") == RELATIVE
        or relative.endswith(RELATIVE)
        or relative.startswith(f"{RELATIVE}/")
        or f"/{RELATIVE}/" in relative
    )
    tfMsg = "This is a TF dataset" if tf else "These are additional files"
    sys.stdout.write(f"{tfMsg}\n")

    zipData(theBackend or backend, org, repo, relative=relative, tf=tf)


__pdoc__["main"] = HELP


if __name__ == "__main__":
    main()
