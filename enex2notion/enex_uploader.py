from notion.block import CollectionViewPageBlock, PageBlock
from progress.bar import Bar

from enex2notion.enex_parser import EvernoteNote
from enex2notion.note_parser_dom import logger
from enex2notion.note_uploader import upload_block


def get_import_root(client, title):
    for page in client.get_top_level_pages():
        if isinstance(page, PageBlock) and page.title == title:
            logger.info(f"'{title}' page found")
            return page

    logger.info(f"Creating '{title}' page...")
    return client.current_space.add_page(title)


def upload_note(root, note: EvernoteNote, note_blocks):
    logger.info(f"Creating new page for note '{note.title}'")
    new_page = _make_page(note, root)

    for block in Bar(f"Uploading '{note.title}'").iter(note_blocks):
        upload_block(new_page, block)

    # Set proper name after everything is uploaded
    new_page.title = note.title


def _make_page(note, root):
    tmp_name = f"{note.title} [UNFINISHED UPLOAD]"

    return (
        root.collection.add_row(
            title=tmp_name,
            url=note.url,
            tags=note.tags,
            created=note.created,
        )
        if isinstance(root, CollectionViewPageBlock)
        else root.children.add_new(PageBlock, title=tmp_name)
    )