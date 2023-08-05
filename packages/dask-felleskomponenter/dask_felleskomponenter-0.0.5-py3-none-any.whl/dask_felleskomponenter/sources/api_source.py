import apache_beam as beam
from apache_beam.io.iobase import Read
from apache_beam.transforms import PTransform
from apache_beam.pipeline import Pipeline, PipelineOptions

from dask_felleskomponenter.common.api_client import ApiClient


class SinglePageApiSource(beam.io.iobase.BoundedSource):
    def __init__(self, client: ApiClient, path: str):
        self.api_client: ApiClient = client
        self.path: str = path
        self.weight = 0
        self.source = self
        self.start_position = 0
        self.stop_position = beam.io.range_trackers.OffsetRangeTracker.OFFSET_INFINITY

    def estimate_size(self):
        return None  # We don't have a reliable size estimate for this source.

    def split(self, desired_bundle_size, start_position=None, stop_position=None):
        return [self]

    def get_range_tracker(self, start_position, stop_position):
        if start_position is None:
            start_position = 0
        if stop_position is None:
            stop_position = beam.io.range_trackers.OffsetRangeTracker.OFFSET_INFINITY

        range_tracker = beam.io.range_trackers.OffsetRangeTracker(
            start_position, stop_position)
        range_tracker = beam.io.range_trackers.UnsplittableRangeTracker(
            range_tracker)
        return range_tracker

    def read(self, range_tracker):
        if range_tracker.try_claim(0):
            data = self.api_client.get_data(self.path)
            if isinstance(data, list):
                for item in data:
                    yield item
            else:
                yield data


class ReadFromApi(PTransform):
    source = SinglePageApiSource

    def __init__(self, client: ApiClient, path: str, **kwargs):
        super().__init__(**kwargs)
        self.api_client = client
        self.path = path

    def expand(self, pvalue):
        return pvalue.pipeline | Read(SinglePageApiSource(self.api_client, self.path))
