from typing import List

import requests

from . import helpers


def check_health(url: str, **kwargs) -> int:
    is_simulate = kwargs.get('is_simulate', False)
    status_code = None
    try:
        if is_simulate:
            return 200
        response = requests.get(url, timeout=30)
        return response.status_code
    except Exception:
        status_code = None
    return status_code



def load_base_urls(config) -> List[str]:
    items = {x.get('base_url') for x in config.load_projects() if x.get('base_url') is not None}
    return list(set(items))


def cli_main(args, config) -> int:
    if args.action == 'health':
        items = load_base_urls(config)
        datas = [{
            'url': x,
            'status_code': check_health(x, is_simulate=args.simulate)
        } for x in items]
        datas = [{
            **x,
            **{
                'status': 'DOWN' if x.get('status_code') is None else 'OK' if 200 <= x.get('status_code') < 300 else 'DOWN'
            }
        } for x in datas]

        if args.debug:
            print(datas)

        for d in datas:
            if d.get('status') == 'DOWN':
                print(f"- {d.get('url')} {helpers.bcolors.FAIL}DOWN{helpers.bcolors.ENDC}")
            elif d.get('status') == 'OK':
                print(f"- {d.get('url')} {helpers.bcolors.OKGREEN}{d.get('status_code')} OK{helpers.bcolors.ENDC}")

        if [x for x in datas if x.get('status') == 'DOWN']:
            return 1

    return 0
