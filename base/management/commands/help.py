from pathlib import Path

from mwasa2.settings import BASE_DIR


def mwasa_data_import():
    # for local
    # return BASE_DIR.joinpath("data-import").joinpath("mwasa-data-import")
    # for server
    return BASE_DIR.parent.joinpath("data-import").joinpath("mwasa-data-import")


def mwasa_content():
    # return BASE_DIR.parent.joinpath("content")
    return BASE_DIR.joinpath("content").joinpath("content")


# pass old path and new path
def check_file_and_delete(old, new):
    if old == new:
        return
    import os

    oldf_size = os.path.getsize(old)
    newf_size = os.path.getsize(new)
    print("oldf_size", oldf_size)
    print("newf_size", newf_size)
    # os.remove()
    import filecmp

    if oldf_size == newf_size and filecmp.cmp(old, new):
        print("true oldf_size == newf_size")
        # her to remove old file
        os.remove(old)
