import os.path

from anki.collection import DeckIdLimit, ImportCsvRequest, Delimiter, \
    DupeResolution
from anki.decks import DeckId
from anki.importing import AnkiPackageImporter
from aqt import mw


def export_to_apkg(deck_id: DeckId, output_path: str = "auto tmp") -> str:
    if output_path == "auto tmp":
        output_path = f"/tmp/anki_true_share_{deck_id}_apkg_export.apkg"

    if os.path.isdir(output_path):
        output_path += f"/{deck_id}.apkg"

    mw.col.export_anki_package(out_path=output_path,
                               limit=DeckIdLimit(deck_id),
                               with_scheduling=False,
                               with_media=True, legacy_support=True)
    return output_path


def import_from_apkg(file: str):
    importer = AnkiPackageImporter(mw.col, file)
    importer.run()
    mw.reset()


def export_to_csv(deck_name: str, output_path: str = "auto tmp") -> str:
    if output_path == "auto tmp":
        output_path = f"/tmp/anki_true_share_{deck_name}_csv_export.csv"

    if os.path.isdir(output_path):
        output_path += f"/{deck_name}.csv"

    mw.col.export_note_csv(out_path=output_path, limit=DeckIdLimit(
        mw.col.decks.id_for_name(deck_name)), with_html=True, with_tags=True,
                           with_deck=True, with_notetype=True, with_guid=False)

    return output_path


def import_from_csv(path: str):
    metadata = mw.col.get_csv_metadata(path=path, delimiter=Delimiter.TAB)
    request = ImportCsvRequest(path=path, metadata=metadata, dupe_resolution=DupeResolution.UPDATE)
    mw.col.import_csv(request)
