# This test script was automatically generated by the contrib-patch-tests.py
# script. If you want to make changes to it, you should make sure that you have
# removed the ``_generated`` suffix from the file name, to prevent the content
# from being overwritten by future re-generations.

from ddtrace.contrib.vertica.patch import patch


try:
    from ddtrace.contrib.vertica.patch import unpatch
except ImportError:
    unpatch = None
from tests.contrib.patch import PatchTestCase


class TestVerticaPatch(PatchTestCase.Base):
    __integration_name__ = "vertica"
    __module_name__ = "vertica_python"
    __patch_func__ = patch
    __unpatch_func__ = unpatch

    def assert_module_patched(self, vertica_python):
        pass

    def assert_not_module_patched(self, vertica_python):
        pass

    def assert_not_module_double_patched(self, vertica_python):
        pass
