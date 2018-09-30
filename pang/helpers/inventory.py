import yaml


def write_yaml(filename, data):
    with open(filename, 'w') as fh:
        yaml.safe_dump(data, fh,
                       default_flow_style=False,
                       explicit_start=False,
                       encoding='utf-8')


def create_inventory(env, url, username, password, hosts):
        data = {
            "all": {
                "vars": {
                    "nso": {
                        "url": url,
                        "username": username,
                        "password": password
                    }
                },
                "hosts": hosts
            }

        }
        write_yaml('inventory/{}.yaml'.format(env), data)
