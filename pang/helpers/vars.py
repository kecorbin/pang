import yaml


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')


yaml.add_representer(type(None), represent_none)


def create_group_vars(host="localhost",
                      port=8080,
                      username="admin",
                      password="admin"):
    """
    creates group_vars directory, and places
    NSO configuration in group 'all' returns
    resulting vars as a dictionary
    """

    url = "http://{}:{}/jsonrpc"
    url = url.format(host, port)
    data = {
        "nso": {
            "url": url,
            "username": username,
            "password": password
        }
    }
    write_yaml('group_vars/all.yaml', data)
    return data


def write_yaml(filename, data):
    with open(filename, 'w') as fh:
        yaml.safe_dump(data, fh,
                       default_flow_style=False,
                       explicit_start=False,
                       encoding='utf-8')
