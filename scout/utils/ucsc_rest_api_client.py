# -*- coding: UTF-8 -*-
import csv
import json
import logging
import requests
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

LOG = logging.getLogger(__name__)

HEADERS = {"Content-type": "application/json"}

RESTAPI_GET_ENDPOINT = "http://api.genome.ucsc.edu/getData/track?genome={0};track={1};chrom={2};start={3};end={4}"

class UCSCRestApiClient:
    """A class handling requests and responses to and from the UCSC (http://genome.ucsc.edu/)
    Simplifies track retrieval from the UCSC Rest API.
    More info on the API: http://genome.ucsc.edu/goldenPath/help/api.html
    """

    def __init__(self, build="37"):
        self.track = None
        self.type = None
        if build == "38":
            self.genome = "hg38"
        else:
            self.genome = "hg19"


    def get_track(self, track_name, chrom=None, start=None, stop=None):
        """Retrieve a specific track from a UCSC database genome as a json object

        To display tracks for a genome: http://api.genome.ucsc.edu/list/tracks?genome=hg38

        Accepts:
            track_name(str): clinvarMain, clinvarCnv
            chrom(str): chromosome
            start(int): start position
            stop(int): stop position

        Returns:
            json_track(dict): A json object containing track data
        """
        json_track = {}
        url = self._compose_url(track_name, chrom, start, stop)
        try:
            request = Request(url)
            response = urlopen(request)
            content = response.read()
            if content:
                json_track = json.loads(content)

        except HTTPError as e:
            LOG.error("Request failed for url {0}: Error: {1}\n".format(url, e))
            json_track = e

        except ValueError as e:
            LOG.error("Request failed for url {0}: Error: {1}\n".format(url, e))
            track = e

        return json_track


    def json_track_to_bigbed(self, track_items, fieldnames, file):
        """Write json track data to a bigBed file

        Accepts:
            track_items(list): list of objects to write to file, one per line
            fieldnames(list): item-specific keys to write to file
            file(File): file to write to
        """
        with open(file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            writer.writerows(track_items)


    def _compose_url(self, track_name, chrom, start, stop):
        """Compose the URL used to retrieve data from the UCSC rest API

        Accepts:
            track_name(str): clinvarMain, clinvarCnv
            chrom(str): chromosome
            start(int): start position
            stop(int): stop position

        Returns:
            url(str): complete url to be used in the Request to the API service

        """
        url = RESTAPI_GET_ENDPOINT.format(self.genome, track_name, chrom, start, stop)
        return url
