"""
Contains the methods which provides the costing details of AWS KMS service
"""

from aws_cost_optimization_7.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class kms:
    def cmk_cost(self, data: dict) -> dict:
        """
        :param data: recommendations data
        :return: cost details for kms cmk
        """
        logger.info(" ---Inside _kms_costing.kms :: cmk_cost")





