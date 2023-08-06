# pychangelogfactory (c) by chacha
#
# pychangelogfactory  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""
Main module __init__ file.
"""

from importlib.metadata import version, PackageNotFoundError

try:  # pragma: no cover
    __version__ = version("pychangelogfactory")
except PackageNotFoundError:  # pragma: no cover
    import warnings

    warnings.warn("can not read __version__, assuming local test context, setting it to ?.?.?")
    __version__ = "?.?.?"

from .changelogfactory import ChangeLogFactory, ChangeLogFormaterRecordType, ChangeLogFormater
