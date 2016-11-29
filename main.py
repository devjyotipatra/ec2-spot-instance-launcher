from boto.ec2.connection import EC2Connection
from time import sleep
import subprocess
import ConfigParser, os, socket
import sys


def get_existing_instance(client):
		instances = client.get_all_instances(filters = { 'tag:Name': config.get('EC2', 'name_tag') , 'tag:Type': config.get('EC2', 'type_tag')})
		if len(instances) > 0:
				return instances[0].instances[0]
		else:
				return None


def list_all_existing_instances(client):
		reservations = client.get_all_instances(filters = { 'tag:Name': config.get('EC2', 'name_tag') , 'tag:Type': config.get('EC2', 'type_tag')})
		if len(reservations) > 0:
				r_instances = [inst for resv in reservations for inst in resv.instances]
				for inst in r_instances:
						print "Instance Id: %s (%s) %s" % (inst.id, inst.state, dir(inst))




def create_client():
		client = EC2Connection(config.get('IAM', 'access'), config.get('IAM', 'secret'))
		regions = client.get_all_regions()
		for r in regions:
				if r.name == config.get('EC2', 'region'):
						client = EC2Connection(config.get('IAM', 'access'), config.get('IAM', 'secret'), region = r)
						return client
		return None


def read_instance_data_from_local_config():
	return None

def main():
		# Entry
		action = 'start' if len(sys.argv) == 1 else sys.argv[1]
		client = create_client()
		if client is None:
				print 'Unable to create EC2 client'
				sys.exit(0)

		instance_data = read_instance_data_from_local_config()

		if instance_data == None:
			instance_data = list_all_existing_instances(client)
		'''
		if action == 'start':
				if inst is None or inst.state == 'terminated':
						spot_price = get_spot_price(client)
						print 'Spot price is ' + str(spot_price) + ' ...',
						if spot_price > float(config.get('EC2', 'max_bid')):
								print 'too high!'
								sys.exit(0)
						else:
								print 'below maximum bid, continuing'
								provision_instance(client, user_data)
								inst = get_existing_instance(client)
				wait_for_up(client, inst)
		elif action == 'stop' and inst is not None:
				destroy_instance(client, inst)
		elif action == 'list':
				print 'Active Spot Instnaces (AMI: %s)' % config.get('EC2', 'ami')
				list_all_existing_instances(client)
		else:
				print 'No action taken'
		'''


if __name__ == "__main__":
		config = ConfigParser.ConfigParser()
		config.read('ec2-spot-instance-launcher.cfg')
		main()
