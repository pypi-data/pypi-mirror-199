import gzip
import json

import yaml


def read_json(file_name, mode='rt'):
    dat = read_file(file_name, mode)
    jobj = json.loads(dat)
    return jobj


def write_json(jobj, write_file, mode='wt'):
    if write_file.endswith('.gz'):
        f = gzip.open(write_file, mode)
    else:
        f = open(write_file, mode)
    with f:
        f.write(json.dumps(jobj, default=str, ensure_ascii=False))


def read_yaml(yaml_file):
    with open(yaml_file, "r") as f:
        return yaml.safe_load(f)


def read_file(read_file, mode='rt'):
    if read_file.endswith('.gz'):
        f = gzip.open(read_file, mode)
    else:
        f = open(read_file, mode)
    with f:
        return f.read()
