"""Build the Oldrim release archive."""
import config
import os
import logging
import release
import shutil
import tempfile


def copy_and_check_plugins(src: os.PathLike, dst: os.PathLike, version: str):
    plugins = release.find_plugins(src)
    plugins_full_path = [os.path.join(src, plugin) for plugin in plugins]
    release.check_version(plugins_full_path, version)
    for plugin in plugins:
        src_path = os.path.join(src, plugin)
        dst_path = os.path.join(dst, plugin)
        shutil.copy2(src_path, dst_path)


def build_oldrim_unp(release_name: str, version: str):
    with tempfile.TemporaryDirectory() as dir_temp:
        src = os.path.join(config.DIR_REPO, "Meshes - Oldrim")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Textures")
        dst = os.path.join(dir_temp, "Textures")
        shutil.copytree(src, dst)
        dir_plugin = os.path.join(config.DIR_REPO, "Plugin - Oldrim")
        bsa_name = release.find_bsa_name(dir_plugin)
        src = dir_temp
        dst = os.path.join(dir_temp, bsa_name)
        release.build_bsa(src, dst, config.BSARCH, "tes5", True)
        copy_and_check_plugins(dir_plugin, dir_temp, version)
        dir_release = os.path.join(config.DIR_REPO, "Releases", "Oldrim")
        release.make_archive(release_name, version, dir_temp, dir_release)


def build_oldrim_cbbe(release_name: str, version: str):
    with tempfile.TemporaryDirectory() as dir_temp:
        src = os.path.join(config.DIR_REPO, "Meshes - Oldrim")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst)
        src = os.path.join(config.DIR_REPO, "Meshes - Oldrim CBBE")
        dst = os.path.join(dir_temp, "Meshes")
        shutil.copytree(src, dst, dirs_exist_ok=True)
        src = os.path.join(config.DIR_REPO, "Textures")
        dst = os.path.join(dir_temp, "Textures")
        shutil.copytree(src, dst)
        dir_plugin = os.path.join(config.DIR_REPO, "Plugin - Oldrim")
        bsa_name = release.find_bsa_name(dir_plugin)
        src = dir_temp
        dst = os.path.join(dir_temp, bsa_name)
        release.build_bsa(src, dst, config.BSARCH, "tes5", True)
        copy_and_check_plugins(dir_plugin, dir_temp, version)
        dir_release = os.path.join(config.DIR_REPO, "Releases", "Oldrim")
        release.make_archive(release_name, version, dir_temp, dir_release)


logger = logging.getLogger(release.__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler = logging.FileHandler("{}.log".format(release.__name__), "w")
handler.setFormatter(formatter)
logger.addHandler(handler)
try:
    build_oldrim_unp("{} UNP".format(config.MOD_NAME), config.MOD_VERSION)
    build_oldrim_cbbe("{} CBBE".format(config.MOD_NAME), config.MOD_VERSION)
except Exception as error:
    logger.exception(error)
