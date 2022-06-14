import logging
from pathlib import Path

log = logging.getLogger("rich-codex")


def clean_images(clean_img_paths_raw, img_obj, codex_obj):
    """Delete any images matching CLEAN_IMG_PATHS that were not generated.

    Useful to remove existing files when a target filename is changed.
    """
    clean_img_patterns = clean_img_paths_raw.splitlines() if clean_img_paths_raw else []

    if len(clean_img_patterns) == 0:
        log.debug("[dim]Nothing found to clean in 'clean_img_paths'")
        return 0

    # Search glob patterns for images
    all_img_paths = set()
    for pattern in clean_img_patterns:
        for matched_path in Path.cwd().glob(pattern):
            all_img_paths.add(matched_path.resolve())
    if len(all_img_paths) == 0:
        log.debug("[dim]No files found matching 'clean_img_paths' glob patterns")
        return 0

    # Collect list of generated images
    known_img_paths = set()
    if img_obj:
        for img_path in img_obj.img_paths:
            known_img_paths.add(Path(img_path).resolve())
    if codex_obj:
        for img in codex_obj.rich_imgs:
            for img_path in img.img_paths:
                known_img_paths.add(Path(img_path).resolve())

    # Paths found by glob that weren't generated
    clean_img_paths = all_img_paths - known_img_paths
    if len(clean_img_paths) == 0:
        log.debug("[dim]All files found matching 'clean_img_paths' were generated in this run. Nothing to clean.")
        return 0

    for path in clean_img_paths:
        path_to_delete = Path(path).resolve()
        path_relative = path_to_delete.relative_to(Path.cwd())
        log.info(f"Deleting '{path_relative}'")
        path_to_delete.unlink()

    return len(clean_img_paths)
