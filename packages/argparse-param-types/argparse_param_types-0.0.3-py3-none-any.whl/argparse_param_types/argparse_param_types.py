import argparse
import logging
from typing import Union

import ipaddress

logger = logging.getLogger(__name__)


def file_type(val: str, message: str = "Provided file does not exist ({val})..", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is an existing file
    on the filesystem.

    :param val: file path to check if it exists
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    from os import path

    if path.isfile(val):
        return val
    else:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def directory_type(
    val: str,
    message: str = "Provided directory does not exist ({val})..",
    logs: bool = True,
) -> str:
    """
    Argparse parameter type, checking that the parameter is an existing directory
    on the filesystem.

    :param val: directory path to check if it exists
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    from os import path

    if path.isdir(val):
        return val
    else:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def host_type(val: str, message: str = "Provided host is not valid ({val}).", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is a valid host. valid host is either a valid domain name or an IP address.

    :param val: host to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    import regex

    # https://stackoverflow.com/questions/11809631/fully-qualified-domain-name-validation
    domain_regex = "^(?!.*?_.*?)(?!(?:[\w]+?\.)?\-[\w\.\-]*?)(?![\w]+?\-\.(?:[\w\.\-]+?))(?=[\w])(?=[\w\.\-]*?\.+[\w\.\-]*?)(?![\w\.\-]{254})(?!(?:\.?[\w\-\.]*?[\w\-]{64,}\.)+?)[\w\.\-]+?(?<![\w\-\.]*?\.[\d]+?)(?<=[\w\-]{2,})(?<![\w\-]{25})$"

    try:
        ip_type(val, logs=False)
    except argparse.ArgumentTypeError as e:
        if not regex.match(domain_regex, val):
            message = message.format(val=val)
            if logs:
                logger.error(message)
            raise argparse.ArgumentTypeError(message)

    return val


def ip_type(val: str, message: str = "Provided IP is not valid ({val}).", logs: bool = True) -> Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
    """
    Argparse parameter type, checking that the parameter is a vali IP address. Return value as an `ipaddress` object.

    :param val: IP to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: IP from `val` represented in an `ipaddress` object
    :rtype: ipaddress.IPv4Address | ipaddress.IPv6Address
    """
    try:
        return ipaddress.ip_address(val)
    except Exception as e:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def rawip_type(val: str, message: str = "Provided IP is not valid ({val}).", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is a valid IP address. Return value in a string format.

    :param val: IP to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    ip_type(val, message, logs)

    return val


def ip4_type(val: str, message: str = "Provided IP is not a valid IPv4 ({val}).", logs: bool = True) -> ipaddress.IPv4Address:
    """
    Argparse parameter type, checking that the parameter is a valid IPv4 address. Return value as an `ipaddress` object.

    :param val: IPv4 to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: IPv4 from `val` represented in an `ipaddress` object
    :rtype: ipaddress.IPv4Address
    """
    try:
        return ipaddress.IPv4Address(val)
    except Exception as e:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def rawip4_type(val: str, message: str = "rovided IP is not a valid IPv4 ({val}).", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is a valid IPv4 address. Return value in a string format.

    :param val: IPv4 to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    ip4_type(val, message, logs)

    return val


def ip6_type(val: str, message: str = "Provided IP is not a valid IPv6 ({val}).", logs: bool = True) -> ipaddress.IPv6Address:
    """
    Argparse parameter type, checking that the parameter is a valid IPv6 address. Return value as an `ipaddress` object.

    :param val: IPv6 to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: IPv6 from `val` represented in an `ipaddress` object
    :rtype: ipaddress.IPv6Address
    """
    try:
        return ipaddress.IPv6Address(val)
    except Exception as e:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def rawip6_type(val: str, message: str = "Provided IP is not a valid IPv6 ({val}).", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is a valid IPv6 address. Return value in a string format.

    :param val: IPv6 to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    ip6_type(val, message, logs)

    return val


def net_type(val: str, message: str = "Provided network is not valid ({val}).", logs: bool = True) -> Union[ipaddress.IPv4Network, ipaddress.IPv6Network]:
    """
    Argparse parameter type, checking that the parameter is a valid IP network address. Return value as an `ipaddress` object.

    :param val: IP network to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: IP network from `val` represented in an `ipaddress` object
    :rtype: ipaddress.IPv4Network | ipaddress.IPv6Network
    """
    try:
        return ipaddress.ip_network(val)
    except Exception as e:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def rawnet_type(val: str, message: str = "Provided network is not valid ({val}).", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is a valid IP network address. Return value in a string format.

    :param val: IP network to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    # Should it allow IP? maybe do a seperate?
    net_type(val, message, logs)

    try:
        ip_type(val, logs=False)
    except argparse.ArgumentTypeError as e:
        return val

    try:
        ip4_type(val, logs=False)
        return f"{val}/32"
    except argparse.ArgumentTypeError as e:
        return f"{val}/128"


def net4_type(val: str, message: str = "Provided network is not a valid IPv4 network ({val}).", logs: bool = True) -> ipaddress.IPv4Network:
    """
    Argparse parameter type, checking that the parameter is a valid IPv4 network address. Return value as an `ipaddress` object.

    :param val: IPv5 network to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: IPv4 network from `val` represented in an `ipaddress` object
    :rtype: ipaddress.IPv4Network
    """
    try:
        return ipaddress.IPv4Network(val)
    except Exception as e:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def rawnet4_type(val: str, message: str = "Provided network is not a valid IPv4 network ({val}).", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is a valid IPv4 network address. Return value in a string format.

    :param val: IPv4 network to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    net4_type(val, message, logs)

    try:
        ip4_type(val, logs=False)
        return f"{val}/32"
    except argparse.ArgumentTypeError as e:
        return val


def net6_type(val: str, message: str = "Provided network is not a valid IPv6 network ({val}).", logs: bool = True) -> ipaddress.IPv6Network:
    """
    Argparse parameter type, checking that the parameter is a valid IPv6 network address. Return value as an `ipaddress` object.

    :param val: IPv6 network to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: IPv6 network from `val` represented in an `ipaddress` object
    :rtype: ipaddress.IPv6Network
    """
    try:
        return ipaddress.IPv6Network(val)
    except Exception as e:
        message = message.format(val=val)
        if logs:
            logger.error(message)
        raise argparse.ArgumentTypeError(message)


def rawnet6_type(val: str, message: str = "Provided network is not a valid IPv6 network ({val}).", logs: bool = True) -> str:
    """
    Argparse parameter type, checking that the parameter is a valid IPv6 network address. Return value in a string format.

    :param val: IPv6 network to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    net6_type(val, message, logs)

    try:
        ip6_type(val, logs=False)
        return f"{val}/128"
    except argparse.ArgumentTypeError as e:
        return val


def port_type(val: str, message: str = "Provided port is not valid ({val}).", logs: bool = True) -> int:
    """
    Argparse parameter type, checking that the parameter is a valid network port.

    :param val: network port to check if it is valid
    :param message: (optional) Message string used in raised error
    :param logs: (optional) Boolean to deactivate logging. Logging is activated y default
    :return: Same value as param `val`
    :rtype: str
    """
    if val.isdigit() and 0 < int(val) <= 65535:
        return int(val)

    message = message.format(val=val)
    if logs:
        logger.error(message)
    raise argparse.ArgumentTypeError(message)
