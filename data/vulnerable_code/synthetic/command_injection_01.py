import os


def check_host(hostname):
    # BUG: hostname passed directly to shell command
    cmd = "ping -c 1 " + hostname
    result = os.popen(cmd).read()
    return result


def health_check(targets):
    results = {}
    for host in targets:
        results[host] = check_host(host)
    return results
