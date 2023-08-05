import unittest
from dask_felleskomponenter.common.api_client import ApiClient


class TestDivideByThree(unittest.TestCase):

	def test_divide_by_three(self):
		base_url = "base/url/for/api"
		client = ApiClient(base_url=base_url)
		self.assertEqual(base_url, client.base_url)


if __name__ == "__main__":
	unittest.main()
