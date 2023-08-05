import os
import re


def get_config(key: str):
    '''
    :param key:
    :return: the configuration associated with the given key. raises ValueError if key not found
    '''
    value = os.getenv(key)
    if value is None:
        raise ValueError(f'the environmental variable {key} is not found')

    return value


def get_config_with_default_value(key: str, default_value):
    '''
    :param key
    :param default_value
    :return: the configuration associated with the given key.
    '''
    return os.getenv(key, default_value)


def get_configs(rq: re.Pattern) -> dict:
    '''
    :param rq: regex pattern
    :return: list of key value pairs where the key matches the regex pattern
    '''
    results = {}
    for k, v in os.environ.items():
        if rq.search(k):
            results[k] = v
    return results


def main():
    result = get_config('PLATFORM')
    print(result)

    prefix = "TELEGRAM_QUERY_"
    rq = re.compile('^' + prefix)
    results = get_configs(rq)
    print(results)


if __name__ == '__main__':
    main()
