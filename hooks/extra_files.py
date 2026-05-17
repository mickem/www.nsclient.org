import shutil
from pathlib import Path


def on_post_build(config):
    root = Path(config['config_file_path']).parent
    dst = Path(config['site_dir']) / 'img' / 'logo.png'
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / 'img' / 'logo.png', dst)
