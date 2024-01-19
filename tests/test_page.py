"""Test specification for transkribus PAGE 2013 conversion

    requires pytest presence to run
"""


from pathlib import (
    Path,
)

import lxml.etree as ET

from transkribus_to_prima.convert import (
    TranskribusToPrima,
)


TEST_RES = Path(__file__).parent / 'resources'


def test_common_odem_ger_transcription():
    """Processing ReadingOrder of a common
    Transkribus transcription page"""

    # arrange
    _res = TEST_RES / 'urn+nbn+de+gbv+3+1-654854-p0102-7_ger.gt.xml'
    _tree = ET.parse(_res)
    _converter = TranskribusToPrima(_tree)

    # act
    _result = _converter.tostring()

    # assert
    assert len(_result) >= 72000


def test_empty_page_convert_reading_order():
    """Workaraound to handle ReadingOrder
    of otherwise empty page

    previously failed completely with 
        transkribus_to_prima/convert.py:29: IndexError
    """

    # arrange
    _res = TEST_RES / 'urn+nbn+de+gbv+3+1-218767-p0062-3_ger.gt.xml'
    _tree = ET.parse(_res)
    _ttp = TranskribusToPrima(_tree)

    # act
    _result = _ttp.convert_reading_order()

    # assert
    assert not _result


def test_empty_page_succeeds():
    """Ensure that otherwise empty page can
    be converted by now complete
    """

    # arrange
    _res = TEST_RES / 'urn+nbn+de+gbv+3+1-218767-p0062-3_ger.gt.xml'
    _tree = ET.parse(_res)
    _ttp = TranskribusToPrima(_tree)

    # act
    _result = _ttp.tostring()

    # assert
    assert len(_result) >= 1300
