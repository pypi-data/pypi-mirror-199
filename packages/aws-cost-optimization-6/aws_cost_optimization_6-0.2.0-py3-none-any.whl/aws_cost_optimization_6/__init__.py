import time

from boto3 import session
import logging

from aws_cost_optimization_6 import _savings_plan, _ri_recommendations, _ec2_costing, _rds_costing
from aws_cost_optimization_6.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = "Dheeraj Banodha"
__version__ = '0.2.0'


class aws_client(_ri_recommendations.ri, _savings_plan.sp, _ec2_costing.ec2, _rds_costing.rds):
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

        self.regions = get_regions(self.session)
        self.aws_region_map = {
            'ca-central-1': 'Canada (Central)',
            'ap-northeast-3': 'Asia Pacific (Osaka-Local)',
            'us-east-1': 'US East (N. Virginia)',
            'ap-northeast-2': 'Asia Pacific (Seoul)',
            'us-gov-west-1': 'AWS GovCloud (US)',
            'us-east-2': 'US East (Ohio)',
            'ap-northeast-1': 'Asia Pacific (Tokyo)',
            'ap-south-1': 'Asia Pacific (Mumbai)',
            'ap-southeast-2': 'Asia Pacific (Sydney)',
            'ap-southeast-1': 'Asia Pacific (Singapore)',
            'sa-east-1': 'South America (Sao Paulo)',
            'us-west-2': 'US West (Oregon)',
            'eu-west-1': 'EU (Ireland)',
            'eu-west-3': 'EU (Paris)',
            'eu-west-2': 'EU (London)',
            'us-west-1': 'US West (N. California)',
            'eu-central-1': 'EU (Frankfurt)',
            'eu-north-1': 'EU (Stockholm)'
        }

    # returns the cost details of recommendations
    def cost_details(self, data: dict) -> dict:
        """
        :param data:
        :return:
        """
        available_cost_details = {
            'Delete idle EBS volume': self.unused_ebs_costing,
            'Associate the EIP with a running active instance, or release the unassociated EIP': self.unallocated_eip,
            'Migrate GP2 volume to GP3': self.gp2_to_gp3,
            'Remove unused EBS volume': self.unused_ebs_costing,
            'Purge unattached volume': self.unused_ebs_costing,
            'Purge 8 week older snapshot': self.older_snapshot_costing,
            # 'Remove AMI': None,
            # 'Remove Unused ELB': None,
            # 'Remove Customer Master Key': None,
            'Delete idle rds instance': self.delete_rds_costing,
            # 'Upgrade to General Purpose SSD': self.rds_gp_ssd,
            # 'Delete idle compute instance': self.remove_ec2_costing,
        }
        if data['Recommendation'] in available_cost_details.keys():
            response = available_cost_details[data['Recommendation']](data)
        else:
            response = {
                'Current Cost': None,
                'Effective Cost': None,
                'Savings': None,
                'Savings %': None
            }

        return response
