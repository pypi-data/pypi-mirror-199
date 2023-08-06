from setuptools import build_meta as _orig

prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel
build_wheel = _orig.build_wheel
build_sdist = _orig.build_sdist


def print_hun():
    print("hun")


def build_sdist(sdist_directory, config_settings=None):
    print("source build test")
    # return _orig.build_sdist(sdist_directory, config_settings)
    return []


def build_wheel(sdist_directory, config_settings=None):
    print("wheel build test")
    # return _orig.build_wheel(sdist_directory, config_settings)
    return []


def get_requires_for_build_wheel(config_settings=None):
    print("get required for wheel-building test")
    return _orig.get_requires_for_build_wheel(config_settings) + [...]


def get_requires_for_build_sdist(config_settings=None):
    print("get required for backend build")
    return _orig.get_requires_for_build_sdist(config_settings) + [...]