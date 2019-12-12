import logging

import requests

from borgmatic.hooks import monitor

logger = logging.getLogger(__name__)

MONITOR_STATE_TO_CRONHUB = {
    monitor.State.START: 'start',
    monitor.State.FINISH: 'finish',
    monitor.State.FAIL: 'fail',
}


def ping_monitor(ping_url, config_filename, state, dry_run):
    '''
    Ping the given Cronhub URL, modified with the monitor.State. Use the given configuration
    filename in any log entries. If this is a dry run, then don't actually ping anything.
    '''
    dry_run_label = ' (dry run; not actually pinging)' if dry_run else ''
    formatted_state = '/{}/'.format(MONITOR_STATE_TO_CRONHUB[state])
    ping_url = ping_url.replace('/start/', formatted_state).replace('/ping/', formatted_state)

    logger.info(
        '{}: Pinging Cronhub {}{}'.format(config_filename, state.name.lower(), dry_run_label)
    )
    logger.debug('{}: Using Cronhub ping URL {}'.format(config_filename, ping_url))

    if not dry_run:
        logging.getLogger('urllib3').setLevel(logging.ERROR)
        requests.get(ping_url)