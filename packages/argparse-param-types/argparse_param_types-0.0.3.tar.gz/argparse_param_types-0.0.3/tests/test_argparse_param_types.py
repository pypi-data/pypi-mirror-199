import argparse
import ipaddress

import pytest

from argparse_param_types import *

arg_fail = pytest.mark.xfail(raises=argparse.ArgumentTypeError, strict=True)


class TestFilesystem:
    """
    Unit tests for filesystem based operation types.
    """

    @pytest.mark.parametrize("filename", [
        "existing_file.txt",
        pytest.param("unknown.txt", marks=arg_fail),
        pytest.param("existing_directory.txt", marks=arg_fail),
    ])
    def test_file_type(self, filename, fs):
        fs.create_file("existing_file.txt")
        fs.create_dir("existing_directory.txt")

        assert file_type(filename) == filename

    @pytest.mark.parametrize("dirname", [
        "existing_directory.txt",
        pytest.param("unknown.txt", marks=arg_fail),
        pytest.param("existing_file.txt", marks=arg_fail),
    ])
    def test_directory_type(self, dirname, fs):
        fs.create_file("existing_file.txt")
        fs.create_dir("existing_directory.txt")

        assert directory_type(dirname) == dirname


class TestNetwork:
    """
    Unit tests for network based operation types.
    """

    @pytest.mark.parametrize("host", [
        "www.google.com",
        "google.com",
        "mkyong123.com",
        "mkyong-info.com",
        "sub.mkyong.com",
        "sub.mkyong-info.com",
        "mkyong.com.au",
        "g.co",
        "a.12E",
        "mkyong.t.t.co",
        "xn--stackoverflow.com",
        "stackoverflow.xn--com",
        "xn--d1ai6ai.xn--p1ai",
        "stackoverflow.co.uk",
        "a.xn--wgbh1c",
        "1.2.3.4.com",
        "x.XN--VERMGENSBERATUNG-PWB",
        "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com",
        "www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com",
        "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcde.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.com",
        pytest.param("http://google.com", marks=arg_fail),
        pytest.param("http://www.google.com", marks=arg_fail),
        pytest.param("dot.", marks=arg_fail),
        pytest.param("space com", marks=arg_fail),
        pytest.param("under_score.com", marks=arg_fail),
        pytest.param("underscore.c_om", marks=arg_fail),
        pytest.param("-dash.com", marks=arg_fail),
        pytest.param("dash-.com", marks=arg_fail),
        pytest.param("sub.-dash.com", marks=arg_fail),
        pytest.param("sub-.dash.com", marks=arg_fail),
        pytest.param("-.com", marks=arg_fail),
        pytest.param("-com", marks=arg_fail),
        pytest.param(".com", marks=arg_fail),
        pytest.param("com", marks=arg_fail),
        pytest.param("mx.gmail.com.", marks=arg_fail),
        pytest.param("mkyong.t.t.c", marks=arg_fail),
        pytest.param("mkyong,com", marks=arg_fail),
        pytest.param("mkyong.com/users", marks=arg_fail),
        pytest.param("a.123", marks=arg_fail),
        pytest.param("x.XN--VERMGENSBERATUNG-PWBB", marks=arg_fail),
        pytest.param("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkk.com", marks=arg_fail),
        pytest.param("www.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkk.co.uk", marks=arg_fail),
        pytest.param("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcde.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijk.comm", marks=arg_fail),
        pytest.param("0123456789 +-.,!@#$%^&*();\\/|<>\"\'", marks=arg_fail),
        pytest.param("12345 -98.7 3.141 .6180 9,000 +42", marks=arg_fail),
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_host_type(self, host):
        assert host_type(host) == host

    @pytest.mark.parametrize("ip", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_ip_type(self, ip):
        res = ip_type(ip)

        assert isinstance(res, ipaddress.IPv4Address) or isinstance(res, ipaddress.IPv6Address)
        assert str(res) == ip or str(res) == "2001:db8::ff00:42:8329"

    @pytest.mark.parametrize("ip", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_rawip_type(self, ip):
        res = rawip_type(ip)

        assert res == ip

    @pytest.mark.parametrize("ip4", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0042:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8::ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_ip4_type(self, ip4):
        res = ip4_type(ip4)

        assert isinstance(res, ipaddress.IPv4Address)
        assert str(res) == ip4

    @pytest.mark.parametrize("ip4", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0042:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8::ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_rawip4_type(self, ip4):
        res = rawip4_type(ip4)

        assert res == ip4

    @pytest.mark.parametrize("ip6", [
        pytest.param("192.168.0.1", marks=arg_fail),
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_ip6_type(self, ip6):
        res = ip6_type(ip6)

        assert isinstance(res, ipaddress.IPv6Address)
        assert str(res) == "2001:db8::ff00:42:8329"

    @pytest.mark.parametrize("ip6", [
        pytest.param("192.168.0.1", marks=arg_fail),
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_rawip6_type(self, ip6):
        res = rawip6_type(ip6)

        assert res == ip6

    @pytest.mark.parametrize("net", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        "192.168.0.0/24",
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0000:0000/96",
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        "2001:db8:0:0:0:ff00:0:0/96",
        "2001:db8::ff00:0:0/96",
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_net_type(self, net):
        res = net_type(net)

        assert isinstance(res, ipaddress.IPv4Network) or isinstance(res, ipaddress.IPv6Network)
        if str(res)[-2:] != "32" and str(res)[-3:] != "128":
            assert str(res) == net or str(res) == "2001:db8::ff00:0:0/96"
        else:
            assert str(res).split("/")[0] == net or str(res).split("/")[0] == "2001:db8::ff00:42:8329"

    @pytest.mark.parametrize("net", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        "192.168.0.0/24",
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0000:0000/96",
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        "2001:db8:0:0:0:ff00:0:0/96",
        "2001:db8::ff00:0:0/96",
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_rawnet_type(self, net):
        res = rawnet_type(net)

        if "/" in net:
            assert res == net
        else:
            assert res == f"{net}/32" or res == f"{net}/128"

    @pytest.mark.parametrize("net4", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        "192.168.0.0/24",
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0042:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8::ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_net4_type(self, net4):
        res = net4_type(net4)

        assert isinstance(res, ipaddress.IPv4Network)
        if str(res)[-2:] != "32":
            assert str(res) == net4
        else:
            assert str(res).split("/")[0] == net4

    @pytest.mark.parametrize("net4", [
        "192.168.0.1",
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        "192.168.0.0/24",
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0042:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8::ff00:42:8329", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0000/96", marks=arg_fail),
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00:0:0/96", marks=arg_fail),
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_rawnet4_type(self, net4):
        res = rawnet4_type(net4)

        if "/" in net4:
            assert res == net4
        else:
            assert res == f"{net4}/32"

    @pytest.mark.parametrize("net6", [
        pytest.param("192.168.0.1", marks=arg_fail),
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0000:0000/96",
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        "2001:db8:0:0:0:ff00:0:0/96",
        "2001:db8::ff00:0:0/96",
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_net6_type(self, net6):
        res = net6_type(net6)

        assert isinstance(res, ipaddress.IPv6Network)
        if str(res)[-3:] != "128":
            assert str(res) == "2001:db8::ff00:0:0/96"
        else:
            assert str(res).split("/")[0] == "2001:db8::ff00:42:8329"

    @pytest.mark.parametrize("net6", [
        pytest.param("192.168.0.1", marks=arg_fail),
        pytest.param("192.168.0.1.1", marks=arg_fail),
        pytest.param("192.168.0.300", marks=arg_fail),
        pytest.param("192.168.0.0/24", marks=arg_fail),
        pytest.param("192.168.0.1/24", marks=arg_fail),
        pytest.param("192.168.300.0/24", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0042:8329",
        "2001:db8:0:0:0:ff00:42:8329",
        "2001:db8::ff00:42:8329",
        pytest.param("2001:db8:0:0:0:ff00:42:8329:ff", marks=arg_fail),
        pytest.param("2001:db8:0:0:0:ff00:42:8329f", marks=arg_fail),
        "2001:0db8:0000:0000:0000:ff00:0000:0000/96",
        pytest.param("2001:0db8:0000:0000:0000:ff00:0000:0001/96", marks=arg_fail),
        "2001:db8:0:0:0:ff00:0:0/96",
        "2001:db8::ff00:0:0/96",
        pytest.param("2001:db8::ff00::/96", marks=arg_fail),
        pytest.param("2001:db8::ff00f:0:0/96", marks=arg_fail),
    ])
    def test_rawnet6_type(self, net6):
        res = rawnet6_type(net6)

        if "/" in net6:
            assert res == net6
        else:
            assert res == f"{net6}/128"

    @pytest.mark.parametrize("port", [
        "1",
        "5000",
        "65535",
        pytest.param("0", marks=arg_fail),
        pytest.param("-100", marks=arg_fail),
        pytest.param("100000", marks=arg_fail),
        pytest.param("invalid", marks=arg_fail),
    ])
    def test_port_type(self, port):
        res = port_type(port)

        assert isinstance(res, int)
        assert str(res) == port
