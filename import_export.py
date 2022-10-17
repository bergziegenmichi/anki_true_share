import os.path

from anki.collection import DeckIdLimit, ImportCsvRequest, Delimiter, \
    DupeResolution
from aqt import mw

from .preferences import Preferences


def export_to_csv(deck_name: str, output_path: str) -> str:
    if not os.path.exists(output_path):
        raise FileNotFoundError

    if os.path.isdir(output_path):
        output_path += f"/{deck_name}.csv"

    mw.col.export_note_csv(out_path=output_path, limit=DeckIdLimit(
        mw.col.decks.id_for_name(deck_name)), with_html=True, with_tags=True,
                           with_deck=True, with_notetype=True, with_guid=False)

    return output_path


def import_from_csv(path: str):
    dr = Preferences.DUPE_RESOLUTION.get()
    if dr == "update":
        dupe_resolution = DupeResolution.UPDATE
    elif dr == "ignore":
        dupe_resolution = DupeResolution.IGNORE
    elif dr == "add":
        dupe_resolution = DupeResolution.ADD
    else:
        raise Exception
    metadata = mw.col.get_csv_metadata(path=path, delimiter=Delimiter.TAB)
    request = ImportCsvRequest(path=path, metadata=metadata,
                               dupe_resolution=dupe_resolution)
    mw.col.import_csv(request)
