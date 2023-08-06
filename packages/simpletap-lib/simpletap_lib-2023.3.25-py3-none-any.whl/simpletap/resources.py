"""
resources.py is part of The SimpleTap Project.
https://git.benmickler.com/SimpleTap/simpletap
Copyright (C) 2023  Benjamin Mickler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import socket
import asyncio
from contextlib import closing
import subprocess
import psutil
import miniupnpc
import requests
import importlib.util

pid = os.getpid()

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def process_memory_usage():
    return psutil.Process(pid).memory_info().rss / 1024 ** 2

def internet_sync(host="8.8.8.8", port=53, timeout=3):
    """
    Source: https://stackoverflow.com/questions/3764291/how-can-i-see-if-theres-an-available-and-active-network-connection-in-python
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

async def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        return True
    except Exception as e:
        print(e)
        return False

async def execute(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        yield line.decode().strip()
    await process.wait()
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, process.args)

def get_network_interfaces():
    return psutil.net_if_addrs().keys()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def _get_public_ip_upnp():
    u = miniupnpc.UPnP()
    u.discoverdelay = 200
    u.discover()
    u.selectigd()
    return u.externalipaddress()

def _get_public_ip_amazon():
    return requests.get('https://checkip.amazonaws.com').text.strip()

def get_public_ip():
    try:
        return _get_public_ip_upnp()
    except:
        return _get_public_ip_amazon()

def get_cpus():
    cpus = []
    for cpu in os.listdir('/sys/devices/system/cpu/'):
        if cpu.startswith('cpu') and cpu[3:].isdigit():
            cpus.append(cpu)
    cpus.sort(key=lambda x: int(x[3:]))
    return cpus

def get_gov(cpus):
    gov = {}
    for cpu in cpus:
        with open(f'/sys/devices/system/cpu/{cpu}/cpufreq/scaling_governor', 'r') as f:
            gov[cpu] = f.read().strip()
    return gov

# root required
def set_gov(ipc, client_uuid, cpus, gov):
    for cpu in cpus:
        with open(f'/sys/devices/system/cpu/{cpu}/cpufreq/scaling_governor', 'w') as f:
            f.write(gov)

def get_freq(cpus):
    freq = {}
    for cpu in cpus:
        with open(f'/sys/devices/system/cpu/{cpu}/cpufreq/scaling_cur_freq', 'r') as f:
            freq[cpu] = f.read().strip()
    return freq

# root required
def set_freq(ipc, client_uuid, cpus, freq):
    for cpu in cpus:
        with open(f'/sys/devices/system/cpu/{cpu}/cpufreq/scaling_setspeed', 'w') as f:
            f.write(freq)

def get_enabled(cpus):
    enabled = {}
    for cpu in cpus:
        if os.path.exists(f'/sys/devices/system/cpu/{cpu}/online'):
            with open(f'/sys/devices/system/cpu/{cpu}/online', 'r') as f:
                enabled[cpu] = f.read().strip()
        else:
            enabled[cpu] = '1'
    return enabled

# root required
def set_enabled(ipc, client_uuid, cpus, enabled):
    for cpu in cpus:
        if os.path.exists(f'/sys/devices/system/cpu/{cpu}/online'):
            with open(f'/sys/devices/system/cpu/{cpu}/online', 'w') as f:
                f.write(enabled)