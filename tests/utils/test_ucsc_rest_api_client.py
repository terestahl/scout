# -*- coding: UTF-8 -*-
import os
import tempfile
from scout.utils import ucsc_rest_api_client as urac

def test_get_clinvar_ucsc_track_37():
    """Test get clinvar track data for genome build 37"""

    # WHEN using the UCSC Rest API to retrieve clinvar vars in a genomic interval (build37)
    client = urac.UCSCRestApiClient(build="37")
    json_track = client.get_track("clinvarMain", "chr1", 930000, 950000)

    # Then a dictionary object should be returned, containing a number of variants
    assert json_track['itemsReturned'] == 27

    # in a list specified by the key 'clinvarMain
    assert isinstance(json_track["clinvarMain"], list)


def test_get_clinvar_ucsc_track_38():
    """Test get clinvar track data for genome build 37"""

    # WHEN using the UCSC Rest API to retrieve clinvar vars in a genomic interval (build38)
    client = urac.UCSCRestApiClient(build="38")
    json_track = client.get_track("clinvarMain", "chr1", 930000, 950000)

    # Then a dictionary object should be returned, containing a number of variants
    assert json_track['itemsReturned'] == 4

    # in a list specified by the key 'clinvarMain
    assert isinstance(json_track["clinvarMain"], list)


def test_json_track_to_bigbed():
    """Test convert a dictionary data track to bigBed file"""

    # Having a  json-formatted UCSC track
    client = urac.UCSCRestApiClient(build="38")
    json_track = client.get_track("clinvarMain", "chr1", 930000, 950000)

    # and a list of items to be written to a bigBed file, for each available track
    bigbed_header = list(json_track['clinvarMain'][0].keys())

    file_content = None
    # WHEN using the UCSC REST API function to convert dictionary (from json) data to a bigBed file
    with tempfile.NamedTemporaryFile(suffix=".bb") as tmp:
        client.json_track_to_bigbed(json_track['clinvarMain'], bigbed_header, tmp.name)
        file_content = [x.decode('utf8').strip() for x in tmp.readlines()]

    # File should contain one header +  4 lines (4 clinvar variants)
    assert len(file_content) == 5

    # the first line should be the header
    assert file_content[0].split('\t') == bigbed_header

    # and  the following lines should have as many elements as the header:
    for line in file_content[1:]:
        assert len(line.split("\t")) == len(bigbed_header)
