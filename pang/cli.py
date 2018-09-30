# -*- coding: utf-8 -*-

"""Console script for pang."""
import sys
import click
import yaml
from .helpers.nso import NSO
from .helpers.playbook import DEFAULT_PLAYBOOK
from .helpers import create_dirs
from .helpers.inventory import create_inventory


@click.command()
@click.option('--nso',
              help="FQDN/IP of NSO Server (default: localhost)",
              metavar="<host_or_ip>",
              default="localhost")
@click.option('--username',
              help="NSO Username (default: admin)",
              metavar='<username>',
              default="admin")
@click.option('--password',
              help="NSO Password (default: admin)",
              metavar="<password>",
              default="admin")
def main(nso, username, password):
    """PANG - Playbook for Ansible + NSO Generator"""

    # creates basic folder structure
    create_dirs()

    url = "http://{}:{}".format(nso, 8080)
    nso = NSO(url, username, password)

    # url is now only used for ansible
    url = url + '/jsonrpc'
    try:
        nso.sync_from()
        click.echo("Syncing Configuration from Devices")
    except Exception as e:
        click.secho("Error Connecting to NSO: {}".format(e), fg="red")
        sys.exit(1)

    devices = nso.get_device_list()
    # track devices to be added to inventory
    inv_devices = list()

    for d in devices:
        print("Generating host_vars for {}".format(d))
        config = dict()
        try:
            config['config'] = nso.get_device_config(d)['tailf-ncs:config']
            with open('host_vars/{}.yaml'.format(d), 'w') as fh:
                yaml.safe_dump(config, fh, default_flow_style=False,
                               explicit_start=False)
            inv_devices.append(d)
        except ValueError:
            print("Failed to parse JSON for {}".format(d))

    inv_dict = {k: None for k in inv_devices}
    # inventory representing source
    create_inventory("prod",
                     url,
                     username,
                     password,
                     inv_dict)

    # also creates a netsim dev environment
    create_inventory("dev",
                     "http://localhost:8080/jsonrpc",
                     username,
                     password,
                     inv_dict)

    click.echo("Generating Ansible Playbook...")

    with open('site.yaml', 'w') as pb:
        pb.write(DEFAULT_PLAYBOOK)

    click.echo("Exporting Netsim configuration")
    nso.generate_netsim_configs(devices)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
