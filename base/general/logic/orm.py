from filer.models.filemodels import File as FilerFile

from base.general.logic.general import sizify


def get_file_url(id):
    if not id:
        return None
    file = FilerFile.objects.filter(id=id).first()
    if not file:
        return None

    return file.file.url


def get_file_data(id):
    filer = get_filer(id)
    if not filer:
        return None
    return {
        "size": filer.size,
        "sizify": sizify(filer.size),
        "type": filer.mime_type,
    }


def get_filer(id):
    if not id:
        return None
    file = FilerFile.objects.filter(id=id).first()
    return file
