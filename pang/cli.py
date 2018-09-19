# -*- coding: utf-8 -*-

"""Console script for pang."""
import sys
import click
import os
import yaml
from helpers.nso import NSO
from helpers.vars import create_group_vars
from helpers.playbook import DEFAULT_PLAYBOOK


@click.command()
@click.option('--nso',
              help="FQDN/IP of NSO Server",
              metavar="<host_or_ip>",
              default="localhost")
@click.option('--username',
              help="NSO Username",
              metavar='<username>',
              default="admin")
@click.option('--password',
              help="NSO Password",
              metavar="<password>",
              default="admin")
def main(nso, username, password):
    """PANG - Playbook for Ansible + NSO Generator"""
    
    if not os.path.exists('host_vars'):
        os.makedirs('host_vars')

    if not os.path.exists('group_vars'):
        os.makedirs('group_vars')

    config = create_group_vars(host=nso,
                               username=username,
                               password=password)

    url = config['nso']['url']
    username = config['nso']['username']
    password = config['nso']['password']

    if url.endswith('/jsonrpc'):
        # it very likely does...
        url = url.strip('/jsonrpc')

    nso = NSO(url, username, password)

    click.echo("Syncing Configuration from Devices")
    nso.sync_from()

    devices = nso.get_device_list()
    # track devices to be added to inventory
    inv_devices = list()

    for d in devices:
        print("Generating host_vars for {}".format(d))
        config = dict()
        try:
            config['config'] = nso.get_device_config(d)['tailf-ncs:config']
            with open('host_vars/{}.yaml'.format(d), 'w') as fh:
                yaml.dump(config, fh, default_flow_style=False,
                          explicit_start=False)
            inv_devices.append(d)
        except ValueError:
            print("Failed to parse JSON for {}".format(d))

    # create inventory yaml
    inv_dict = {"all": {"hosts": {}}}
    inv_dict["all"]["hosts"] = {k: None for k in inv_devices}

    with open('inventory.yaml', 'w') as inv:
        yaml.safe_dump(inv_dict, inv, default_flow_style=False,
                       explicit_start=False,
                       encoding='utf-8')

    click.echo("Generating Ansible Playbook...")

    with open('site.yaml', 'w') as pb:
        pb.write(DEFAULT_PLAYBOOK)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
