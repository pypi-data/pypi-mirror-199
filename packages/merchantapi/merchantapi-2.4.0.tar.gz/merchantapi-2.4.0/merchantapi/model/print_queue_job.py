"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

PrintQueueJob data model.
"""

from merchantapi.abstract import Model

class PrintQueueJob(Model):
	def __init__(self, data: dict = None):
		"""
		PrintQueueJob Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_queue_id(self) -> int:
		"""
		Get queue_id.

		:returns: int
		"""

		return self.get_field('queue_id', 0)

	def get_store_id(self) -> int:
		"""
		Get store_id.

		:returns: int
		"""

		return self.get_field('store_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_job_format(self) -> str:
		"""
		Get job_fmt.

		:returns: string
		"""

		return self.get_field('job_fmt')

	def get_job_data(self) -> str:
		"""
		Get job_data.

		:returns: string
		"""

		return self.get_field('job_data')

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_timestamp_field('dt_created')

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_store_code(self) -> str:
		"""
		Get store_code.

		:returns: string
		"""

		return self.get_field('store_code')

	def get_store_name(self) -> str:
		"""
		Get store_name.

		:returns: string
		"""

		return self.get_field('store_name')
