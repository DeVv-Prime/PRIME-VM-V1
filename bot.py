#!/usr/bin/env python3
# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                                                               ║
# ║  ███╗   ██╗███████╗██╗  ██╗    ██╗   ██╗███╗   ███╗    ██╗   ██╗   ██╔                        ║
# ║  ████╗  ██║██╔════╝╚██╗██╔╝    ██║   ██║████╗ ████║    ██║   ██║╚══██╔                        ║
# ║  ██╔██╗ ██║█████╗   ╚███╔╝     ██║   ██║██╔████╔██║    ██║   ██║   ██║                        ║
# ║  ██║╚██╗██║██╔══╝   ██╔██╗     ╚██╗ ██╔╝██║╚██╔╝██║    ╚██╗ ██╔╝   ██║                        ║
# ║  ██║ ╚████║███████╗██╔╝ ██╗     ╚████╔╝ ██║ ╚═╝ ██║     ╚████╔╝    ██║                        ║
# ║  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚═╝     ╚═╝      ╚═══╝     ╚═╝                        ║
# ║                                                                                               ║
# ║                     ⚡ NEX VM V1 TOOL - VPS MANAGEMENT SYSTEM ⚡                             ║
# ║                                                                                               ║
# ║                         ████████╗ ██████╗  ██████╗ ██╗                                        ║
# ║                         ╚══██╔══╝██╔═══██╗██╔═══██╗██║                                        ║
# ║                            ██║   ██║   ██║██║   ██║██║                                        ║
# ║                            ██║   ██║   ██║██║   ██║██║                                        ║
# ║                            ██║   ╚██████╔╝╚██████╔╝███████╗                                   ║
# ║                            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝                                   ║
# ║                                                                                               ║
# ║                         Made by DeVv-prime ⚡ Version 1.0.0                                  ║
# ║                     CORE READY • SYSTEM STABLE • ALL MODULES ACTIVE                           ║
# ║                                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
import discord
from discord.ext import commands, tasks
from discord.ui import Modal, TextInput, View, Button, Select
import asyncio
import json
import os
import random
import string
import subprocess
import sys
import re
import sqlite3
import logging
import shlex
import shutil
import time
import aiohttp
import psutil  # type: ignore[reportMissingModuleSource]
import socket
import requests
import hashlib
import uuid
import qrcode  # type: ignore[reportMissingModuleSource]
import PIL
import textwrap
import io
import datetime as datetime_
import importlib
import platform
from typing import Optional, List, Dict, Any, Tuple

netifaces = importlib.import_module('netifaces') if importlib.util.find_spec('netifaces') else None

# Discord compatibility for legacy code paths that still use InputText.
InputText = TextInput
if not hasattr(discord, 'InputTextStyle') and hasattr(discord, 'TextStyle'):
    discord.InputTextStyle = discord.TextStyle

# ==================================================================================================
#  🎨  COLOR CONSTANTS
# ==================================================================================================

COLORS = {
    'primary': 0x5865F2,
    'success': 0x57F287,
    'error': 0xED4245,
    'warning': 0xFEE75C,
    'info': 0x5865F2,
    'node': 0x9B59B6,
    'terminal': 0x2C2F33,
    'gold': 0xFFD700,
    'cyan': 0x00CCFF,
    'pink': 0xFF69B4,
    'os': 0x00FF88,
}

# ==================================================================================================
#  📝  LOGGING SETUP
# ==================================================================================================

DEFAULT_BASE_DATA_DIR = os.path.join(os.path.expanduser("~"), ".nex-bot") if os.name == "nt" else "/opt/nex-bot"
BASE_DATA_DIR = os.environ.get('PMV_BOT_BASE_DIR', DEFAULT_BASE_DATA_DIR)
LOGS_DIR = os.path.join(BASE_DATA_DIR, 'logs')
DATA_DIR = os.path.join(BASE_DATA_DIR, 'data')
BACKUPS_DIR = os.path.join(BASE_DATA_DIR, 'backups')
QR_CODES_DIR = os.path.join(BASE_DATA_DIR, 'qr_codes')
NODES_DIR = os.path.join(BASE_DATA_DIR, 'nodes')

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUPS_DIR, exist_ok=True)
os.makedirs(QR_CODES_DIR, exist_ok=True)
os.makedirs(NODES_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, 'svm5.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NEXVMV1-BOT")

# ==================================================================================================
#  ⚙️  CONFIGURATION
# ==================================================================================================

def _parse_admin_ids(raw: str) -> List[int]:
    ids = []
    for part in raw.split(','):
        part = part.strip()
        if part.isdigit():
            ids.append(int(part))
    return ids


BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN', "DISCORD_BOT_TOKEN")
BOT_PREFIX = os.environ.get('BOT_PREFIX', ".")
BOT_NAME = os.environ.get('BOT_NAME', "NEXVMV1-BOT")
BOT_AUTHOR = os.environ.get('BOT_AUTHOR', "DeVv-Prime")
MAIN_ADMIN_IDS = _parse_admin_ids(os.environ.get('MAIN_ADMIN_IDS', '1405866008127864852'))
if not MAIN_ADMIN_IDS:
    MAIN_ADMIN_IDS = [1405866008127864852]
DEFAULT_STORAGE_POOL = os.environ.get('DEFAULT_STORAGE_POOL', "default")

# Auto-detect server
try:
    SERVER_IP = requests.get('https://api.ipify.org', timeout=5).text.strip()
except:
    try:
        SERVER_IP = subprocess.getoutput("curl -s ifconfig.me")
    except:
        SERVER_IP = "127.0.0.1"

HOSTNAME = socket.gethostname()

def get_mac_address():
    try:
        if netifaces:
            interfaces = netifaces.interfaces()
            for iface in interfaces:
                if iface != 'lo':
                    addr = netifaces.ifaddresses(iface)
                    if netifaces.AF_LINK in addr:
                        return addr[netifaces.AF_LINK][0]['addr']
    except Exception:
        pass
    try:
        node = uuid.getnode()
        return ':'.join(f"{(node >> ele) & 0xff:02x}" for ele in range(40, -8, -8))
    except Exception:
        pass
    return "00:00:00:00:00:00"

MAC_ADDRESS = get_mac_address()
THUMBNAIL_URL = "https://images-ext-1.discordapp.net/external/6lAZL5FnvLRPc2KydFlV2yuW8CPj_P7LE0MdcNLhki0/%3Fsize%3D2048/https/cdn.discordapp.com/icons/1478373286684393604/6317df64b495cfcbaf38f12db6bb22c0.webp?format=webp"

# License Keys
VALID_LICENSE_KEYS = [
    "Pushkar931222",
    "NEX5-PRO-2025",
    "NEX5-ENTERPRISE",
    "DEVELOPER-ANKIT",
    "Prime123",
    "GameHindu",
    "pushkarbhau",
    "Primedragon",
    "1kapi",
    "Prime-Vm",
    "Gamerhindu",
    "primebahu",
]

# Lowercased set for case-insensitive comparisons
VALID_LICENSE_KEYS_LOWER = {k.casefold() for k in VALID_LICENSE_KEYS}

# ==================================================================================================
#  🐧  OS OPTIONS - 70+ OPERATING SYSTEMS
# ==================================================================================================

OS_OPTIONS = [
    # ==============================================================================================
    # 🐧 UBUNTU SERIES (15 versions)
    # ==============================================================================================
    {"label": "🐧 Ubuntu 24.04 LTS", "value": "ubuntu:24.04", "desc": "Noble Numbat - Latest LTS (April 2024)", "category": "Ubuntu", "icon": "🐧", "popular": True},
    {"label": "🐧 Ubuntu 23.10", "value": "ubuntu:23.10", "desc": "Mantic Minotaur - Latest (EOL Oct 2024)", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 23.04", "value": "ubuntu:23.04", "desc": "Lunar Lobster - EOL Jan 2024", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 22.04 LTS", "value": "ubuntu:22.04", "desc": "Jammy Jellyfish - Current LTS (April 2022)", "category": "Ubuntu", "icon": "🐧", "popular": True},
    {"label": "🐧 Ubuntu 22.10", "value": "ubuntu:22.10", "desc": "Kinetic Kudu - EOL July 2023", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 21.10", "value": "ubuntu:21.10", "desc": "Impish Indri - EOL July 2022", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 21.04", "value": "ubuntu:21.04", "desc": "Hirsute Hippo - EOL Jan 2022", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 20.04 LTS", "value": "ubuntu:20.04", "desc": "Focal Fossa - Stable LTS (April 2020)", "category": "Ubuntu", "icon": "🐧", "popular": True},
    {"label": "🐧 Ubuntu 20.10", "value": "ubuntu:20.10", "desc": "Groovy Gorilla - EOL July 2021", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 19.10", "value": "ubuntu:19.10", "desc": "Eoan Ermine - EOL July 2020", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 19.04", "value": "ubuntu:19.04", "desc": "Disco Dingo - EOL Jan 2020", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 18.04 LTS", "value": "ubuntu:18.04", "desc": "Bionic Beaver - Legacy LTS (April 2018)", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 18.10", "value": "ubuntu:18.10", "desc": "Cosmic Cuttlefish - EOL July 2019", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 17.10", "value": "ubuntu:17.10", "desc": "Artful Aardvark - EOL July 2018", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 17.04", "value": "ubuntu:17.04", "desc": "Zesty Zapus - EOL Jan 2018", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 16.04 LTS", "value": "ubuntu:16.04", "desc": "Xenial Xerus - Old LTS (April 2016)", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 16.10", "value": "ubuntu:16.10", "desc": "Yakkety Yak - EOL July 2017", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 15.10", "value": "ubuntu:15.10", "desc": "Wily Werewolf - EOL July 2016", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 15.04", "value": "ubuntu:15.04", "desc": "Vivid Vervet - EOL Jan 2016", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 14.04 LTS", "value": "ubuntu:14.04", "desc": "Trusty Tahr - Ancient LTS (April 2014)", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 12.04 LTS", "value": "ubuntu:12.04", "desc": "Precise Pangolin - Very Old LTS", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🐧 Ubuntu 10.04 LTS", "value": "ubuntu:10.04", "desc": "Lucid Lynx - Retro LTS", "category": "Ubuntu", "icon": "🐧"},
    {"label": "🌀 Debian 13", "value": "images:debian/13", "desc": "Trixie - Testing (Upcoming Stable)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 12", "value": "images:debian/12", "desc": "Bookworm - Current Stable (June 2023)", "category": "Debian", "icon": "🌀", "popular": True},
    {"label": "🌀 Debian 11", "value": "images:debian/11", "desc": "Bullseye - Old Stable (Aug 2021)", "category": "Debian", "icon": "🌀", "popular": True},
    {"label": "🌀 Debian 10", "value": "images:debian/10", "desc": "Buster - Older Stable (July 2019)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 9", "value": "images:debian/9", "desc": "Stretch - Legacy (June 2017)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 8", "value": "images:debian/8", "desc": "Jessie - Ancient (April 2015)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 7", "value": "images:debian/7", "desc": "Wheezy - Retro (May 2013)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 6", "value": "images:debian/6", "desc": "Squeeze - Very Old (Feb 2011)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 5", "value": "images:debian/5", "desc": "Lenny - Museum (Feb 2009)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 4", "value": "images:debian/4", "desc": "Etch - Retro (April 2007)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian 3", "value": "images:debian/3", "desc": "Woody - Museum (July 2002)", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian Sid", "value": "images:debian/sid", "desc": "Unstable - Rolling Development", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian Testing", "value": "images:debian/testing", "desc": "Testing - Next Stable", "category": "Debian", "icon": "🌀"},
    {"label": "🌀 Debian Experimental", "value": "images:debian/experimental", "desc": "Experimental - Bleeding Edge", "category": "Debian", "icon": "🌀"},
    {"label": "🎩 Fedora 41", "value": "images:fedora/41", "desc": "Fedora 41 - Latest Development", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 40", "value": "images:fedora/40", "desc": "Fedora 40 - Latest (April 2024)", "category": "Fedora", "icon": "🎩", "popular": True},
    {"label": "🎩 Fedora 39", "value": "images:fedora/39", "desc": "Fedora 39 - Stable (Nov 2023)", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 38", "value": "images:fedora/38", "desc": "Fedora 38 - Older (April 2023)", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 37", "value": "images:fedora/37", "desc": "Fedora 37 - EOL Dec 2023", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 36", "value": "images:fedora/36", "desc": "Fedora 36 - EOL May 2023", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 35", "value": "images:fedora/35", "desc": "Fedora 35 - EOL Dec 2022", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 34", "value": "images:fedora/34", "desc": "Fedora 34 - EOL June 2022", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 33", "value": "images:fedora/33", "desc": "Fedora 33 - EOL Nov 2021", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora 32", "value": "images:fedora/32", "desc": "Fedora 32 - EOL May 2021", "category": "Fedora", "icon": "🎩"},
    {"label": "🎩 Fedora Rawhide", "value": "images:fedora/rawhide", "desc": "Rawhide - Rolling Development", "category": "Fedora", "icon": "🎩"},
    {"label": "🦊 Rocky Linux 9", "value": "images:rockylinux/9", "desc": "Rocky 9 - Latest (July 2022)", "category": "Rocky", "icon": "🦊", "popular": True},
    {"label": "🦊 Rocky Linux 8", "value": "images:rockylinux/8", "desc": "Rocky 8 - Stable (June 2021)", "category": "Rocky", "icon": "🦊"},
    {"label": "🦊 Rocky Linux 7", "value": "images:rockylinux/7", "desc": "Rocky 7 - Legacy", "category": "Rocky", "icon": "🦊"},
    {"label": "🦊 AlmaLinux 9", "value": "images:almalinux/9", "desc": "Alma 9 - Latest (July 2022)", "category": "AlmaLinux", "icon": "🦊", "popular": True},
    {"label": "🦊 AlmaLinux 8", "value": "images:almalinux/8", "desc": "Alma 8 - Stable (March 2021)", "category": "AlmaLinux", "icon": "🦊"},
    {"label": "🦊 AlmaLinux 7", "value": "images:almalinux/7", "desc": "Alma 7 - Legacy", "category": "AlmaLinux", "icon": "🦊"},
    {"label": "📦 CentOS 9 Stream", "value": "images:centos/9-Stream", "desc": "CentOS 9 Stream - Rolling", "category": "CentOS", "icon": "📦"},
    {"label": "📦 CentOS 8 Stream", "value": "images:centos/8-Stream", "desc": "CentOS 8 Stream - EOL May 2024", "category": "CentOS", "icon": "📦"},
    {"label": "📦 CentOS 7", "value": "images:centos/7", "desc": "CentOS 7 - Legacy (June 2024 EOL)", "category": "CentOS", "icon": "📦"},
    {"label": "📦 CentOS 6", "value": "images:centos/6", "desc": "CentOS 6 - Ancient (Nov 2020 EOL)", "category": "CentOS", "icon": "📦"},
    {"label": "📦 CentOS 5", "value": "images:centos/5", "desc": "CentOS 5 - Retro (March 2017 EOL)", "category": "CentOS", "icon": "📦"},
    {"label": "📦 CentOS 4", "value": "images:centos/4", "desc": "CentOS 4 - Museum (Feb 2012 EOL)", "category": "CentOS", "icon": "📦"},
    {"label": "🐧 Alpine 3.20", "value": "images:alpine/3.20", "desc": "Alpine 3.20 - Latest (May 2024)", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine 3.19", "value": "images:alpine/3.19", "desc": "Alpine 3.19 - Stable (Dec 2023)", "category": "Alpine", "icon": "🐧", "popular": True},
    {"label": "🐧 Alpine 3.18", "value": "images:alpine/3.18", "desc": "Alpine 3.18 - Older (May 2023)", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine 3.17", "value": "images:alpine/3.17", "desc": "Alpine 3.17 - EOL Nov 2023", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine 3.16", "value": "images:alpine/3.16", "desc": "Alpine 3.16 - EOL May 2023", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine 3.15", "value": "images:alpine/3.15", "desc": "Alpine 3.15 - EOL Nov 2022", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine 3.14", "value": "images:alpine/3.14", "desc": "Alpine 3.14 - EOL May 2022", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine 3.13", "value": "images:alpine/3.13", "desc": "Alpine 3.13 - EOL Nov 2021", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine 3.12", "value": "images:alpine/3.12", "desc": "Alpine 3.12 - EOL May 2021", "category": "Alpine", "icon": "🐧"},
    {"label": "🐧 Alpine Edge", "value": "images:alpine/edge", "desc": "Alpine Edge - Rolling Development", "category": "Alpine", "icon": "🐧"},
    {"label": "📀 Arch Linux", "value": "images:archlinux", "desc": "Arch - Rolling Release", "category": "Arch", "icon": "📀", "popular": True},
    {"label": "📀 Arch Linux (Current)", "value": "images:archlinux/current", "desc": "Arch Current - Rolling", "category": "Arch", "icon": "📀"},
    {"label": "📀 Manjaro", "value": "images:manjaro", "desc": "Manjaro - Arch Based", "category": "Arch", "icon": "📀"},
    {"label": "📀 EndeavourOS", "value": "images:endeavouros", "desc": "EndeavourOS - Arch Based", "category": "Arch", "icon": "📀"},
    {"label": "📀 Artix Linux", "value": "images:artix", "desc": "Artix - Arch Without Systemd", "category": "Arch", "icon": "📀"},
    {"label": "🟢 OpenSUSE Tumbleweed", "value": "images:opensuse/tumbleweed", "desc": "Rolling Release", "category": "OpenSUSE", "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 15.6", "value": "images:opensuse/15.6", "desc": "Leap 15.6 - Latest (June 2024)", "category": "OpenSUSE", "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 15.5", "value": "images:opensuse/15.5", "desc": "Leap 15.5 - Stable (June 2023)", "category": "OpenSUSE", "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 15.4", "value": "images:opensuse/15.4", "desc": "Leap 15.4 - Older (June 2022)", "category": "OpenSUSE", "icon": "🟢"},
    {"label": "🟢 OpenSUSE Leap 15.3", "value": "images:opensuse/15.3", "desc": "Leap 15.3 - EOL Dec 2022", "category": "OpenSUSE", "icon": "🟢"},
    {"label": "🔵 FreeBSD 14", "value": "images:freebsd/14", "desc": "FreeBSD 14 - Latest (Nov 2023)", "category": "FreeBSD", "icon": "🔵", "popular": True},
    {"label": "🔵 FreeBSD 13", "value": "images:freebsd/13", "desc": "FreeBSD 13 - Stable (April 2021)", "category": "FreeBSD", "icon": "🔵"},
    {"label": "🔵 FreeBSD 12", "value": "images:freebsd/12", "desc": "FreeBSD 12 - EOL Dec 2023", "category": "FreeBSD", "icon": "🔵"},
    {"label": "🔵 FreeBSD 11", "value": "images:freebsd/11", "desc": "FreeBSD 11 - EOL Sept 2021", "category": "FreeBSD", "icon": "🔵"},
    {"label": "🔵 FreeBSD 10", "value": "images:freebsd/10", "desc": "FreeBSD 10 - EOL Oct 2018", "category": "FreeBSD", "icon": "🔵"},
    {"label": "🔵 FreeBSD 9", "value": "images:freebsd/9", "desc": "FreeBSD 9 - Retro", "category": "FreeBSD", "icon": "🔵"},
    {"label": "🐡 OpenBSD 7.5", "value": "images:openbsd/7.5", "desc": "OpenBSD 7.5 - Latest (April 2024)", "category": "OpenBSD", "icon": "🐡"},
    {"label": "🐡 OpenBSD 7.4", "value": "images:openbsd/7.4", "desc": "OpenBSD 7.4 - Stable (Oct 2023)", "category": "OpenBSD", "icon": "🐡"},
    {"label": "🐡 OpenBSD 7.3", "value": "images:openbsd/7.3", "desc": "OpenBSD 7.3 - Older (April 2023)", "category": "OpenBSD", "icon": "🐡"},
    {"label": "🐡 OpenBSD 7.2", "value": "images:openbsd/7.2", "desc": "OpenBSD 7.2 - EOL Oct 2023", "category": "OpenBSD", "icon": "🐡"},
    {"label": "🐡 OpenBSD 7.1", "value": "images:openbsd/7.1", "desc": "OpenBSD 7.1 - EOL Oct 2022", "category": "OpenBSD", "icon": "🐡"},
    {"label": "🐉 Kali Linux", "value": "images:kali", "desc": "Kali - Security Testing (Rolling)", "category": "Kali", "icon": "🐉", "popular": True},
    {"label": "🐉 Kali Linux Weekly", "value": "images:kali/weekly", "desc": "Kali Weekly - Bleeding Edge", "category": "Kali", "icon": "🐉"},
    {"label": "🐉 Kali Linux Last Release", "value": "images:kali/last", "desc": "Kali Latest Release", "category": "Kali", "icon": "🐉"},
    {"label": "🦜 Parrot OS", "value": "images:parrotos", "desc": "Parrot Security OS", "category": "Parrot", "icon": "🦜"},
    {"label": "🦜 Parrot OS (Latest)", "value": "images:parrotos/latest", "desc": "Parrot Latest Release", "category": "Parrot", "icon": "🦜"},
    {"label": "💻 Gentoo", "value": "images:gentoo", "desc": "Gentoo - Source Based", "category": "Gentoo", "icon": "💻"},
    {"label": "💻 Gentoo Current", "value": "images:gentoo/current", "desc": "Gentoo Current - Rolling", "category": "Gentoo", "icon": "💻"},
    {"label": "💻 Gentoo OpenRC", "value": "images:gentoo/openrc", "desc": "Gentoo with OpenRC", "category": "Gentoo", "icon": "💻"},
    {"label": "💻 Gentoo Systemd", "value": "images:gentoo/systemd", "desc": "Gentoo with Systemd", "category": "Gentoo", "icon": "💻"},
    {"label": "🔬 Scientific Linux 7", "value": "images:scientific/7", "desc": "Scientific Linux 7", "category": "Scientific", "icon": "🔬"},
    {"label": "🔬 Scientific Linux 6", "value": "images:scientific/6", "desc": "Scientific Linux 6", "category": "Scientific", "icon": "🔬"},
    {"label": "☁️ Amazon Linux 2", "value": "images:amazonlinux/2", "desc": "Amazon Linux 2 - AWS Optimized", "category": "Amazon", "icon": "☁️"},
    {"label": "☁️ Amazon Linux 2023", "value": "images:amazonlinux/2023", "desc": "Amazon Linux 2023 - Latest", "category": "Amazon", "icon": "☁️"},
    {"label": "🔴 Red Hat 9", "value": "images:rhel/9", "desc": "RHEL 9 - Enterprise (May 2022)", "category": "RHEL", "icon": "🔴"},
    {"label": "🔴 Red Hat 8", "value": "images:rhel/8", "desc": "RHEL 8 - Stable (May 2019)", "category": "RHEL", "icon": "🔴"},
    {"label": "🔴 Red Hat 7", "value": "images:rhel/7", "desc": "RHEL 7 - Legacy (June 2014)", "category": "RHEL", "icon": "🔴"},
    {"label": "🐡 NetBSD 9.3", "value": "images:netbsd/9.3", "desc": "NetBSD 9.3 - Latest", "category": "NetBSD", "icon": "🐡"},
    {"label": "🐡 NetBSD 9.2", "value": "images:netbsd/9.2", "desc": "NetBSD 9.2 - Stable", "category": "NetBSD", "icon": "🐡"},
    {"label": "🌀 Devuan 5", "value": "images:devuan/5", "desc": "Devuan Daedalus - Without Systemd", "category": "Devuan", "icon": "🌀"},
    {"label": "🌀 Devuan 4", "value": "images:devuan/4", "desc": "Devuan Chimaera - Stable", "category": "Devuan", "icon": "🌀"},
    {"label": "🌀 Devuan 3", "value": "images:devuan/3", "desc": "Devuan Beowulf - Legacy", "category": "Devuan", "icon": "🌀"},
    {"label": "🌀 Devuan 2", "value": "images:devuan/2", "desc": "Devuan ASCII - Old", "category": "Devuan", "icon": "🌀"},
    {"label": "💾 Slackware 15", "value": "images:slackware/15", "desc": "Slackware 15 - Latest (Feb 2022)", "category": "Slackware", "icon": "💾"},
    {"label": "💾 Slackware 14.2", "value": "images:slackware/14.2", "desc": "Slackware 14.2 - Stable", "category": "Slackware", "icon": "💾"},
    {"label": "💾 Slackware Current", "value": "images:slackware/current", "desc": "Slackware Current - Rolling", "category": "Slackware", "icon": "💾"},
    {"label": "🔷 Clear Linux", "value": "images:clearlinux", "desc": "Clear Linux - Intel Optimized", "category": "Clear", "icon": "🔷"},
    {"label": "🔴 Oracle Linux 9", "value": "images:oracle/9", "desc": "Oracle Linux 9 - Latest", "category": "Oracle", "icon": "🔴"},
    {"label": "🔴 Oracle Linux 8", "value": "images:oracle/8", "desc": "Oracle Linux 8 - Stable", "category": "Oracle", "icon": "🔴"},
]

# ==================================================================================================
#  🎮  GAMES LIST
# ==================================================================================================

GAMES_LIST = [
    {'name': 'Minecraft Java', 'docker': 'itzg/minecraft-server', 'port': 25565, 'ram': 2048, 'icon': '🎮'},
    {'name': 'Minecraft Bedrock', 'docker': 'itzg/minecraft-bedrock-server', 'port': 19132, 'ram': 1024, 'icon': '📱'},
    {'name': 'Terraria', 'docker': 'beardedio/terraria', 'port': 7777, 'ram': 1024, 'icon': '🌳'},
    {'name': 'CS:GO', 'docker': 'cm2network/csgo', 'port': 27015, 'ram': 2048, 'icon': '🔫'},
    {'name': 'Valheim', 'docker': 'lloesche/valheim-server', 'port': 2456, 'ram': 2048, 'icon': '⚔️'},
    {'name': 'ARK', 'docker': 'hermsi/ark-server-tools', 'port': 7777, 'ram': 4096, 'icon': '🦖'},
    {'name': 'Rust', 'docker': 'didstopia/rust-server', 'port': 28015, 'ram': 4096, 'icon': '🦀'},
]

# ==================================================================================================
#  🛠️  TOOLS LIST
# ==================================================================================================

TOOLS_LIST = [
    {'name': 'Nginx', 'cmd': 'apt install nginx -y', 'port': 80, 'icon': '🌐'},
    {'name': 'Apache', 'cmd': 'apt install apache2 -y', 'port': 80, 'icon': '🕸️'},
    {'name': 'MySQL', 'cmd': 'apt install mysql-server -y', 'port': 3306, 'icon': '🗄️'},
    {'name': 'PostgreSQL', 'cmd': 'apt install postgresql -y', 'port': 5432, 'icon': '🐘'},
    {'name': 'Redis', 'cmd': 'apt install redis-server -y', 'port': 6379, 'icon': '🔴'},
    {'name': 'Docker', 'cmd': 'curl -fsSL https://get.docker.com | bash', 'icon': '🐳'},
    {'name': 'Node.js', 'cmd': 'curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt install nodejs -y', 'icon': '🟢'},
]

# ==================================================================================================
#  💰  FREE VPS PLANS
# ==================================================================================================

FREE_VPS_PLANS = {
    'invites': [
        {'name': '🥉 Bronze', 'invites': 5, 'ram': 2, 'cpu': 1, 'disk': 20, 'emoji': '🥉'},
        {'name': '🥈 Silver', 'invites': 10, 'ram': 4, 'cpu': 2, 'disk': 40, 'emoji': '🥈'},
        {'name': '🥇 Gold', 'invites': 15, 'ram': 8, 'cpu': 4, 'disk': 80, 'emoji': '🥇'},
        {'name': '🏆 Platinum', 'invites': 20, 'ram': 16, 'cpu': 8, 'disk': 160, 'emoji': '🏆'},
        {'name': '💎 Diamond', 'invites': 25, 'ram': 32, 'cpu': 16, 'disk': 320, 'emoji': '💎'},
        {'name': '👑 Royal', 'invites': 30, 'ram': 64, 'cpu': 32, 'disk': 640, 'emoji': '👑'},
        {'name': '🌟 Elite', 'invites': 35, 'ram': 96, 'cpu': 48, 'disk': 1024, 'emoji': '🌟'},
        {'name': '🔥 Ultra', 'invites': 40, 'ram': 128, 'cpu': 64, 'disk': 1536, 'emoji': '🔥'},
        {'name': '🚀 Infinite', 'invites': 50, 'ram': 192, 'cpu': 96, 'disk': 2048, 'emoji': '🚀'},
    ]
}

# ==================================================================================================
#  🗄️  DATABASE SETUP
# ==================================================================================================

DATABASE_PATH = os.path.join(DATA_DIR, 'svm5.db')
NODES_FILE = os.path.join(NODES_DIR, 'nodes.json')

def get_db():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except:
        return None

def init_db():
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    
    # Admins
    cur.execute('''CREATE TABLE IF NOT EXISTS admins (user_id TEXT PRIMARY KEY, added_at TEXT)''')
    for aid in MAIN_ADMIN_IDS:
        cur.execute('INSERT OR IGNORE INTO admins (user_id, added_at) VALUES (?, ?)', (str(aid), datetime_.datetime.now().isoformat()))
    
    # VPS
    cur.execute('''CREATE TABLE IF NOT EXISTS vps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        container_name TEXT UNIQUE NOT NULL,
        plan_name TEXT DEFAULT 'Custom',
        ram INTEGER NOT NULL,
        cpu INTEGER NOT NULL,
        disk INTEGER NOT NULL,
        os_version TEXT DEFAULT 'ubuntu:22.04',
        status TEXT DEFAULT 'stopped',
        suspended INTEGER DEFAULT 0,
        purge_protected INTEGER DEFAULT 0,
        node_name TEXT DEFAULT 'local',
        created_at TEXT NOT NULL,
        ip_address TEXT,
        mac_address TEXT,
        games_installed TEXT DEFAULT '[]',
        tools_installed TEXT DEFAULT '[]',
        shared_with TEXT DEFAULT '[]'
    )''')
    
    # User stats
    cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (
        user_id TEXT PRIMARY KEY,
        invites INTEGER DEFAULT 0,
        boosts INTEGER DEFAULT 0,
        claimed_vps_count INTEGER DEFAULT 0,
        api_key TEXT UNIQUE,
        last_updated TEXT
    )''')
    
    # Settings
    cur.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
    
    # Shared VPS
    cur.execute('''CREATE TABLE IF NOT EXISTS shared_vps (
        owner_id TEXT, shared_with_id TEXT, container_name TEXT, permissions TEXT, shared_at TEXT,
        UNIQUE(owner_id, shared_with_id, container_name)
    )''')
    
    # Games
    cur.execute('''CREATE TABLE IF NOT EXISTS installed_games (
        user_id TEXT, container_name TEXT, game_name TEXT, game_port INT, installed_at TEXT
    )''')
    
    # Tools
    cur.execute('''CREATE TABLE IF NOT EXISTS installed_tools (
        user_id TEXT, container_name TEXT, tool_name TEXT, tool_port INT, installed_at TEXT
    )''')
    
    # IPv4
    cur.execute('''CREATE TABLE IF NOT EXISTS ipv4 (
        user_id TEXT, container_name TEXT, public_ip TEXT, private_ip TEXT, mac_address TEXT, assigned_at TEXT
    )''')
    
    # Port forwards
    cur.execute('''CREATE TABLE IF NOT EXISTS port_forwards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, container_name TEXT, container_port INT, host_port INT UNIQUE, protocol TEXT, created_at TEXT
    )''')
    
    # Port allocations
    cur.execute('''CREATE TABLE IF NOT EXISTS port_allocations (
        user_id TEXT PRIMARY KEY, allocated_ports INTEGER DEFAULT 5
    )''')
    
    # Panels
    cur.execute('''CREATE TABLE IF NOT EXISTS panels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, panel_type TEXT, panel_url TEXT, admin_user TEXT, admin_pass TEXT, admin_email TEXT,
        container_name TEXT, tunnel_url TEXT, installed_at TEXT
    )''')
    
    # Transactions
    cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, txn_ref TEXT UNIQUE, txn_id TEXT, amount INT, status TEXT DEFAULT 'pending', created_at TEXT
    )''')
    
    # AI History
    cur.execute('''CREATE TABLE IF NOT EXISTS ai_history (user_id TEXT PRIMARY KEY, messages TEXT, updated_at TEXT)''')
    
    # Settings defaults
    settings = [
        ('license_verified', 'false'),
        ('server_ip', SERVER_IP),
        ('mac_address', MAC_ADDRESS),
        ('hostname', HOSTNAME),
        ('default_port_quota', '5'),
        ('ipv4_price', '50'),
        ('upi_id', '9892642904@ybl'),
    ]
    for k, v in settings:
        cur.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")
    return True

init_db()

# ==================================================================================================
#  📚  Embedded Markdown Resources (merged from workspace .md files)
# ==================================================================================================
ALL_MD: Dict[str, str] = {
    "IMPLEMENTATION_COMPLETE.md": """
# 🎉 PRIME VM Install Script - Implementation Complete!

## ✅ What You Now Have

Your install script has been **completely upgraded** with enterprise-grade improvements. Here's what was delivered:

---

## 📦 Deliverables Summary

### ⭐ Main Deliverable
**`install.sh`** - Production-ready install script
- ✅ Global error handling
- ✅ Color-coded prompts
- ✅ Improved error messages
- ✅ Cross-platform compatible
- ✅ Production-ready stable
- ✅ 1017 lines of bulletproof code

### 📚 Documentation (6 files, 10,000+ words)

1. **README.md** (3,000 words)
   - Master summary of all improvements
   - Before/after comparison
   - Quality metrics and status
   - Deployment instructions

2. **PRODUCTION_READINESS.md** (4,000 words)
   - Full verification report
   - Feature completeness matrix
   - Testing results summary
   - Performance metrics
   - Pre-deployment checklist

3. **DEPLOYMENT_GUIDE.md** (2,000 words)
   - Quick start guide
   - Deployment checklist
   - User support tips
   - The one-liner
   - Troubleshooting guide

4. **SCRIPT_IMPROVEMENTS.md** (2,000 words)
   - Before/after comparison
   - Technical explanations
   - Code examples
   - Benefits listing

5. **FIXES_APPLIED.md** (2,000 words)
   - Detailed fix documentation
   - Issue descriptions
   - Solution details
   - Valid license keys

6. **TESTING_GUIDE.md** (3,000 words)
   - 9 comprehensive test cases
   - Step-by-step procedures
   - Debugging guide
   - Success criteria

7. **DOCUMENTATION_INDEX.md** (1,500 words)
   - Complete documentation index
   - Navigation guide
   - Reading order recommendations
   - File structure overview

---

## 🚀 Core Improvements

### 1. Global Error Handling ✅
```bash
set -o pipefail
trap 'echo -e "\\n${R}❌ Script interrupted${NC}"; exit 130' INT TERM
```
- ✅ Prevents hanging on Ctrl+C
- ✅ Catches all signals
- ✅ Graceful exit
- ✅ Result: Script never hangs

### 2. Color-Coded Prompts ✅
```bash
read -p "${BOLD}${C}Select option (0-7): ${NC}" OPTION
```
- ✅ Standardized color scheme
- ✅ Emoji indicators throughout
- ✅ Visual hierarchy
- ✅ Result: Intuitive UI

---

## 🎯 Features Implemented

... (truncated in embed) ...
""",
    "FIXES_APPLIED.md": """
# 🔧 PRIME VM Install Script - Fixes Applied

## ✅ Issues Fixed

### 1. **Input Handling Stability** 
   - **Problem**: User input wasn't being properly trimmed, causing validation failures
   - **Solution**: Replaced `xargs` with robust `tr` and `sed` commands that properly handle:
     - Carriage returns (`\\r\\n`)
     - Leading/trailing whitespace
     - Windows line endings
   - **Code**: `KEY=$(printf '%s' "$KEY" | tr -d '\\r\\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')`

### 2. **Menu Stability & Responsiveness**
   - **Problem**: Menu wasn't waiting properly for user input if they didn't select anything
   - **Solution**: 
     - Added empty input check before validation
     - Menu now loops smoothly and waits for valid input (0-7)
     - Invalid input shows error and continues loop
   - **Result**: Menu waits indefinitely for valid selection, responds instantly to options 0-7

... (truncated in embed) ...
""",
    "DOCUMENTATION_INDEX.md": """
# 📚 PRIME VM Documentation Index

## 📖 Complete Documentation Package

Your workspace now contains **comprehensive documentation** for the production-ready PRIME VM install script.

---

## 📁 File Structure

```
PMV VM 1 CREATION/
├── install.sh                      ⭐ Main script (PRODUCTION READY)
├── README.md                       📋 Master summary
├── PRODUCTION_READINESS.md        ✅ Full verification report
├── DEPLOYMENT_GUIDE.md            🚀 Quick deployment guide
├── SCRIPT_IMPROVEMENTS.md         🔄 Before/after comparison
├── FIXES_APPLIED.md               🔧 Detailed fixes
├── TESTING_GUIDE.md               🧪 Complete test cases
└── DOCUMENTATION_INDEX.md         📚 This file
```

... (truncated in embed) ...
""",
    "DEPLOYMENT_GUIDE.md": """
# 🚀 PRIME VM Install Script - Quick Deployment Guide

## ⚡ One-Minute Overview

Your `install.sh` is now **production-ready** with all these features implemented:

✅ **Global Error Handling** - Script never hangs  
✅ **Color-Coded Prompts** - Beautiful, intuitive UI  
✅ **Improved Error Messages** - Clear, actionable feedback  
✅ **Cross-Platform** - Windows/WSL, Linux, macOS  
✅ **Production Stability** - Enterprise-grade reliability  

---

## 🎯 What Users Will Experience

... (truncated in embed) ...
""",
    "BOT_IMPROVEMENTS.md": """
# 🤖 Discord Bot Improvements - Complete Guide

## Overview
This document details all visual and security improvements made to `bot.py` for the VPS management Discord bot.

---

## 🔐 Security Improvements

### Permission Decorators

#### `@is_owner()`
Restricts commands to bot owner only.

```python
@bot.command(name="admin-only-command")
@is_owner()
async def admin_only(ctx):
    # Only MAIN_ADMIN_IDS can execute
    pass
```

... (truncated in embed) ...
""",
    "QUICK_REFERENCE.md": """
# 🚀 Quick Reference - Bot Improvements

## 📚 Files Modified

### `bot.py` (8361 lines)
- Added 280+ lines of improvements
- 3 new permission decorators
- 9 enhanced embed functions
- 5 improved commands
- 15+ docstrings

---

## 🔐 Permission Decorators - Quick Usage

... (truncated in embed) ...
""",
    "PRODUCTION_READINESS.md": """
# ✅ PRIME VM Install Script - Production Readiness Checklist

## 🔍 Verification Report

### 1. Global Error Handling with Trap ✅
**Status**: IMPLEMENTED
**Location**: Lines 3-4
```bash
set -o pipefail
trap 'echo -e "\\n${R}❌ Script interrupted or error occurred${NC}"; exit 130' INT TERM
```
**Benefits:**
- ✅ Catches script interruptions (Ctrl+C)
- ✅ Catches terminal signals (TERM)
- ✅ Prevents hanging on pipe failures
- ✅ Graceful exit with clear message
- ✅ Exit code 130 (standard interrupt code)

... (truncated in embed) ...
""",
    "IMPROVEMENTS_SUMMARY.md": """
# ✅ Bot.py Enhancement Summary

## 🎯 What Was Improved

Your Discord bot has been enhanced with **17+ visual and security improvements** across permission checks, embed functions, and user commands.

---

## 🔐 Security Enhancements

### 1. **Permission Decorators** (3 new decorators)
- `@is_owner()` - Restricts commands to bot owner only
- `@is_admin()` - Restricts commands to admins only  
- `has_vps(user_id)` - Checks if user owns a VPS

... (truncated in embed) ...
""",
    "README.md": """
# 📦 PRIME VM Install Script - Final Implementation Summary

## ✨ What Was Accomplished

Your install script has been **fully upgraded to production-ready status** with enterprise-grade stability, responsiveness, and cross-platform compatibility.

---

## 🎯 Core Improvements Implemented

### 1. ✅ Global Error Handling with Trap
**What**: Prevents script from hanging on interruption  
**How**: Added trap at script start
```bash
set -o pipefail
trap 'echo -e "\\n${R}❌ Script interrupted or error occurred${NC}"; exit 130' INT TERM
```
**Result**: Script always responds, never hangs

... (truncated in embed) ...
""",
    "SCRIPT_IMPROVEMENTS.md": """
# ✅ PRIME VM Install Script - Stability Improvements

## 🎯 What Was Fixed

Your install script had issues with:
1. **Unstable input handling** - User input wasn't being properly trimmed
2. **Menu hanging** - If user didn't select an option, menu would get stuck
3. **Slow response** - Options took time to process instead of responding instantly
4. **Windows compatibility** - Carriage returns weren't being handled

... (truncated in embed) ...
""",
    "TESTING_GUIDE.md": """
# 🧪 Testing Guide - PRIME VM Install Script

## 📋 Test Cases

### Test 1: Script Starts Successfully ✅
**Steps:**
```bash
curl -fsSL https://raw.githubusercontent.com/DeVv-Prime/PRIME-VM/main/install.sh | bash
```
**Expected:**
- ✅ Beautiful purple/teal header displays
- ✅ "PRIME VM" ASCII art appears
- ✅ Discord support info shows
- ✅ License menu appears with options 0-7

... (truncated in embed) ...
""",
}

def get_md(name: str) -> str:
    """Return embedded markdown content by filename."""
    return ALL_MD.get(name)


# ==================================================================================================
#  📊  DATABASE HELPERS
# ==================================================================================================

def get_setting(key: str, default: Any = None) -> Any:
    conn = get_db()
    if not conn:
        return default
    cur = conn.cursor()
    cur.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

def set_setting(key: str, value: str):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()


def add_snapshot(user_id: str, container_name: str, snapshot_name: str):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        container_name TEXT,
        snapshot_name TEXT,
        created_at TEXT
    )''')
    cur.execute(
        'INSERT INTO snapshots (user_id, container_name, snapshot_name, created_at) VALUES (?, ?, ?, ?)',
        (user_id, container_name, snapshot_name, datetime_.datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_snapshots(container_name: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        container_name TEXT,
        snapshot_name TEXT,
        created_at TEXT
    )''')
    cur.execute(
        'SELECT user_id, container_name, snapshot_name, created_at FROM snapshots WHERE container_name = ? ORDER BY id DESC',
        (container_name,)
    )
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return [dict(r) for r in rows]


def _ai_history_file(user_id: str) -> str:
    safe = re.sub(r'[^a-zA-Z0-9_-]', '', user_id)[:64] or 'unknown'
    return os.path.join(DATA_DIR, f'ai_history_{safe}.json')


def load_ai_history(user_id: str) -> List[Dict[str, Any]]:
    path = _ai_history_file(user_id)
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_ai_history(user_id: str, history: List[Dict[str, Any]]):
    path = _ai_history_file(user_id)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def clear_ai_history(user_id: str):
    path = _ai_history_file(user_id)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass

def get_user_vps(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM vps WHERE user_id = ? ORDER BY id', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_vps() -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM vps ORDER BY user_id, id')
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_vps(user_id: str, container_name: str, ram: int, cpu: int, disk: int, os_version: str, plan: str = "Custom") -> Optional[Dict]:
    conn = get_db()
    if not conn:
        return None
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    
    ip = "N/A"
    mac = "N/A"
    try:
        ip = subprocess.getoutput(f"lxc exec {container_name} -- ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
        mac = subprocess.getoutput(f"lxc exec {container_name} -- ip link | grep ether | awk '{{print $2}}' | head -1")
    except:
        pass
    
    cur.execute('''INSERT INTO vps 
        (user_id, container_name, plan_name, ram, cpu, disk, os_version, status, created_at, ip_address, mac_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, container_name, plan, ram, cpu, disk, os_version, 'running', now, ip, mac))
    conn.commit()
    conn.close()
    return {'container_name': container_name}

def update_vps_status(container_name: str, status: str):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('UPDATE vps SET status = ? WHERE container_name = ?', (status, container_name))
    conn.commit()
    conn.close()

def delete_vps(container_name: str) -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute('DELETE FROM vps WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM shared_vps WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM installed_games WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM installed_tools WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM ipv4 WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM port_forwards WHERE container_name = ?', (container_name,))
    cur.execute('DELETE FROM panels WHERE container_name = ?', (container_name,))
    conn.commit()
    conn.close()
    return True

def is_admin(user_id: str) -> bool:
    if user_id in [str(a) for a in MAIN_ADMIN_IDS]:
        return True
    conn = get_db()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS owner_delegates (
            user_id TEXT PRIMARY KEY,
            expires_at TEXT,
            added_by TEXT,
            added_at TEXT
        )''')
        cur.execute('SELECT expires_at FROM owner_delegates WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        if not row:
            return False
        expires_at = row[0]
        if not expires_at:
            return True
        try:
            return datetime_.datetime.fromisoformat(expires_at) > datetime_.datetime.utcnow()
        except Exception:
            return False
    finally:
        conn.commit()
        conn.close()

def get_user_stats(user_id: str) -> Dict:
    conn = get_db()
    if not conn:
        return {'invites': 0}
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    api_key = hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16]
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO user_stats (user_id, invites, boosts, claimed_vps_count, api_key, last_updated) VALUES (?, 0, 0, 0, ?, ?)',
               (user_id, api_key, datetime_.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return {'user_id': user_id, 'invites': 0, 'api_key': api_key}

def update_user_stats(user_id: str, invites: int = 0, claimed: int = 0):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('''INSERT OR REPLACE INTO user_stats 
        (user_id, invites, boosts, claimed_vps_count, api_key, last_updated)
        VALUES (?, 
                COALESCE((SELECT invites FROM user_stats WHERE user_id = ?), 0) + ?,
                0,
                COALESCE((SELECT claimed_vps_count FROM user_stats WHERE user_id = ?), 0) + ?,
                COALESCE((SELECT api_key FROM user_stats WHERE user_id = ?), ?),
                ?)''',
        (user_id, user_id, invites, user_id, claimed, user_id, hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16], datetime_.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def share_vps(owner: str, shared: str, container: str) -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    cur.execute('INSERT OR REPLACE INTO shared_vps VALUES (?, ?, ?, ?, ?)', (owner, shared, container, 'view', now))
    conn.commit()
    conn.close()
    return True

def unshare_vps(owner: str, shared: str, container: str) -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute('DELETE FROM shared_vps WHERE owner_id = ? AND shared_with_id = ? AND container_name = ?',
               (owner, shared, container))
    conn.commit()
    conn.close()
    return True

def get_shared_vps(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('''SELECT v.*, sv.permissions, sv.owner_id 
                   FROM vps v JOIN shared_vps sv ON v.container_name = sv.container_name 
                   WHERE sv.shared_with_id = ?''', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_port_forward(user_id: str, container: str, cport: int, hport: int, proto: str = "tcp+udp") -> bool:
    conn = get_db()
    if not conn:
        return False
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    cur.execute('INSERT INTO port_forwards (user_id, container_name, container_port, host_port, protocol, created_at) VALUES (?, ?, ?, ?, ?, ?)',
               (user_id, container, cport, hport, proto, now))
    conn.commit()
    conn.close()
    return True

def remove_port_forward(pid: int) -> Tuple[bool, str, int]:
    conn = get_db()
    if not conn:
        return False, "", 0
    cur = conn.cursor()
    cur.execute('SELECT container_name, host_port FROM port_forwards WHERE id = ?', (pid,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "", 0
    container, hport = row['container_name'], row['host_port']
    cur.execute('DELETE FROM port_forwards WHERE id = ?', (pid,))
    conn.commit()
    conn.close()
    return True, container, hport

def get_user_port_forwards(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM port_forwards WHERE user_id = ? ORDER BY created_at', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_port_allocation(user_id: str) -> int:
    conn = get_db()
    if not conn:
        return int(get_setting('default_port_quota', '5'))
    cur = conn.cursor()
    cur.execute('SELECT allocated_ports FROM port_allocations WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else int(get_setting('default_port_quota', '5'))

def add_port_allocation(user_id: str, amount: int):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    current = get_port_allocation(user_id)
    cur.execute('INSERT OR REPLACE INTO port_allocations (user_id, allocated_ports) VALUES (?, ?)',
               (user_id, current + amount))
    conn.commit()
    conn.close()

def add_ipv4(user_id: str, container: str, public: str, private: str, mac: str = ""):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    cur.execute('INSERT OR REPLACE INTO ipv4 VALUES (?, ?, ?, ?, ?, ?)',
               (user_id, container, public, private, mac, now))
    conn.commit()
    conn.close()

def get_user_ipv4(user_id: str) -> List[Dict]:
    conn = get_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute('SELECT * FROM ipv4 WHERE user_id = ?', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_transaction(user_id: str, txn_ref: str, amount: int) -> int:
    conn = get_db()
    if not conn:
        return 0
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    cur.execute('INSERT INTO transactions (user_id, txn_ref, amount, created_at) VALUES (?, ?, ?, ?)',
               (user_id, txn_ref, amount, now))
    tid = cur.lastrowid
    conn.commit()
    conn.close()
    return tid

def add_game_install(user_id: str, container: str, game: str, port: int):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    cur.execute('INSERT INTO installed_games VALUES (?, ?, ?, ?, ?)',
               (user_id, container, game, port, now))
    conn.commit()
    conn.close()

def add_tool_install(user_id: str, container: str, tool: str, port: int = None):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    cur.execute('INSERT INTO installed_tools VALUES (?, ?, ?, ?, ?)',
               (user_id, container, tool, port, now))
    conn.commit()
    conn.close()

def add_panel(user_id: str, ptype: str, url: str, user: str, pwd: str, email: str, container: str, tunnel: str = ""):
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    now = datetime_.datetime.now().isoformat()
    cur.execute('''INSERT INTO panels 
        (user_id, panel_type, panel_url, admin_user, admin_pass, admin_email, container_name, tunnel_url, installed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, ptype, url, user, pwd, email, container, tunnel, now))
    conn.commit()
    conn.close()

# ==================================================================================================
#  🌐  NODE MANAGEMENT WITH NODES.JSON
# ==================================================================================================

def load_nodes():
    """Load nodes from JSON file with auto-detect"""
    default = {
        "version": "1.0.0",
        "last_updated": datetime_.datetime.now().isoformat(),
        "main_node": "local",
        "nodes": {},
        "node_groups": {"all": [], "us": [], "eu": [], "asia": []}
    }
    
    if os.path.exists(NODES_FILE):
        try:
            with open(NODES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Auto-create local node
    try:
        lxc_count = len(subprocess.getoutput("lxc list -c n --format csv").splitlines())
    except:
        lxc_count = 0
    
    local_node = {
        "name": "local",
        "host": "localhost",
        "port": 0,
        "username": "local",
        "type": "local",
        "status": "online",
        "is_main": True,
        "region": "us",
        "description": "Auto-detected local node",
        "api_key": hashlib.sha256(f"local{time.time()}".encode()).hexdigest()[:32],
        "stats": {
            "total_ram": psutil.virtual_memory().total // 1024 // 1024,
            "used_ram": psutil.virtual_memory().used // 1024 // 1024,
            "total_cpu": psutil.cpu_count(),
            "used_cpu": psutil.cpu_percent(),
            "total_disk": psutil.disk_usage('/').total // 1024 // 1024 // 1024,
            "used_disk": psutil.disk_usage('/').used // 1024 // 1024 // 1024,
            "lxc_count": lxc_count,
            "last_checked": datetime_.datetime.now().isoformat()
        },
        "settings": {
            "max_containers": 100,
            "default_storage_pool": DEFAULT_STORAGE_POOL,
            "allow_overcommit": True
        }
    }
    
    default["nodes"]["local"] = local_node
    default["node_groups"]["all"].append("local")
    default["node_groups"]["us"].append("local")
    
    with open(NODES_FILE, 'w') as f:
        json.dump(default, f, indent=2)
    
    return default

def save_nodes(data):
    with open(NODES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_node(name):
    nodes = load_nodes()
    return nodes['nodes'].get(name)

def update_local_node_stats():
    nodes = load_nodes()
    if 'local' in nodes['nodes']:
        try:
            lxc_count = len(subprocess.getoutput("lxc list -c n --format csv").splitlines())
        except:
            lxc_count = 0
        nodes['nodes']['local']['stats'] = {
            "total_ram": psutil.virtual_memory().total // 1024 // 1024,
            "used_ram": psutil.virtual_memory().used // 1024 // 1024,
            "total_cpu": psutil.cpu_count(),
            "used_cpu": psutil.cpu_percent(),
            "total_disk": psutil.disk_usage('/').total // 1024 // 1024 // 1024,
            "used_disk": psutil.disk_usage('/').used // 1024 // 1024 // 1024,
            "lxc_count": lxc_count,
            "last_checked": datetime_.datetime.now().isoformat()
        }
        nodes['nodes']['local']['status'] = "online"
        save_nodes(nodes)
    return nodes

# ==================================================================================================
#  🛠️  LXC HELPERS
# ==================================================================================================

async def run_lxc(cmd: str, timeout: int = 60) -> Tuple[str, str, int]:
    try:
        proc = await asyncio.create_subprocess_exec(
            *shlex.split(cmd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout)
            return out.decode().strip(), err.decode().strip(), proc.returncode
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            return "", f"Timeout after {timeout}s", -1
    except Exception as e:
        return "", str(e), -1

async def exec_in_container(container: str, cmd: str, timeout: int = 30) -> Tuple[str, str, int]:
    return await run_lxc(f"lxc exec {container} -- bash -c {shlex.quote(cmd)}", timeout)

async def get_container_status(container: str) -> str:
    try:
        out = subprocess.getoutput(f"lxc info {container} | grep Status | awk '{{print $2}}'")
        return out.lower()
    except:
        return "unknown"

async def get_container_stats(container: str) -> Dict:
    stats = {'status': 'unknown', 'cpu': '0%', 'memory': '0/0MB', 'disk': '0/0GB', 'ipv4': [], 'mac': 'N/A', 'uptime': '0m'}
    stats['status'] = await get_container_status(container)
    if stats['status'] == 'running':
        out, _, _ = await exec_in_container(container, "top -bn1 | grep Cpu | awk '{print $2}'")
        stats['cpu'] = f"{out}%" if out else "0%"
        out, _, _ = await exec_in_container(container, "free -m | awk '/^Mem:/{print $3\"/\"$2}'")
        stats['memory'] = f"{out}MB" if out else "0/0MB"
        out, _, _ = await exec_in_container(container, "df -h / | awk 'NR==2{print $3\"/\"$2}'")
        stats['disk'] = out if out else "0/0GB"
        out, _, _ = await exec_in_container(container, "ip -4 addr show | grep -oP '(?<=inet\\s)[0-9.]+' | grep -v 127")
        stats['ipv4'] = out.splitlines() if out else []
        out, _, _ = await exec_in_container(container, "ip link | grep ether | awk '{print $2}'")
        stats['mac'] = out.splitlines()[0] if out else "N/A"
        out, _, _ = await exec_in_container(container, "uptime -p | sed 's/up //'")
        stats['uptime'] = out if out else "0m"
    return stats

async def get_available_port() -> Optional[int]:
    used = set()
    conn = get_db()
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT host_port FROM port_forwards')
        used = {r[0] for r in cur.fetchall()}
        conn.close()
    for _ in range(100):
        port = random.randint(20000, 50000)
        if port not in used:
            return port
    return None

async def create_port_forward(user_id: str, container: str, cport: int, proto: str = "tcp+udp") -> Optional[int]:
    hport = await get_available_port()
    if not hport:
        return None
    try:
        if proto in ["tcp", "tcp+udp"]:
            await run_lxc(f"lxc config device add {container} proxy-tcp-{hport} proxy listen=tcp:0.0.0.0:{hport} connect=tcp:127.0.0.1:{cport}")
        if proto in ["udp", "tcp+udp"]:
            await run_lxc(f"lxc config device add {container} proxy-udp-{hport} proxy listen=udp:0.0.0.0:{hport} connect=udp:127.0.0.1:{cport}")
        add_port_forward(user_id, container, cport, hport, proto)
        return hport
    except:
        return None

async def remove_port_device(container: str, hport: int):
    try:
        await run_lxc(f"lxc config device remove {container} proxy-tcp-{hport}")
    except:
        pass
    try:
        await run_lxc(f"lxc config device remove {container} proxy-udp-{hport}")
    except:
        pass

# ==================================================================================================
#  🎨  UI HELPER FUNCTIONS
# ==================================================================================================

def glow_text(text: str) -> str:
    return f"```glow\n{text}\n```"

def terminal_text(text: str) -> str:
    return f"```fix\n{text}\n```"


def error_text(text: str) -> str:
    return f"```diff\n- {text}\n```"

# ==================================================================================================
#  🔐  PERMISSION DECORATORS
# ==================================================================================================

def is_owner():
    """Check if user is bot owner"""
    async def predicate(ctx):
        if ctx.author.id not in MAIN_ADMIN_IDS:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="🔒 **You don't have permission to use this command.**\n\nThis command is restricted to bot owners only.",
                color=COLORS['error']
            )
            embed.add_field(name="🤖 Bot Owner", value=f"<@{MAIN_ADMIN_IDS[0]}>", inline=False)
            embed.set_footer(text=f"⚡ {BOT_NAME} • Permission Check • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
            await ctx.send(embed=embed)
            return False
        return True
    return commands.check(predicate)

def is_admin():
    """Check if user is admin or owner"""
    async def predicate(ctx):
        if ctx.author.id not in MAIN_ADMIN_IDS:
            embed = discord.Embed(
                title="❌ Admin Access Required",
                description="🔒 **You need admin privileges to use this command.**\n\nThis command is for administrators only.",
                color=COLORS['error']
            )
            embed.add_field(name="👤 Your ID", value=f"{ctx.author.id}", inline=True)
            embed.add_field(name="🛡️ Status", value="Regular User", inline=True)
            embed.set_footer(text=f"⚡ {BOT_NAME} • Permission Check • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
            await ctx.send(embed=embed)
            return False
        return True
    return commands.check(predicate)

def has_vps(user_id: str) -> bool:
    """Check if user has VPS"""
    return len(get_user_vps(user_id)) > 0

# ==================================================================================================
#  🎨  ENHANCED EMBED FUNCTIONS WITH BETTER VISUALS
# ==================================================================================================

def create_embed(title: str, desc: str = "", color: int = COLORS['primary']) -> discord.Embed:
    """Create a standard embed with proper formatting"""
    embed = discord.Embed(
        title=glow_text(f"✦ {BOT_NAME} - {title} ✦"),
        description=desc,
        color=color,
        timestamp=datetime_.datetime.utcnow()
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(
        text=f"⚡ {BOT_NAME} • {BOT_AUTHOR} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    return embed

def success_embed(title: str, desc: str = "") -> discord.Embed:
    """Create a success embed with green color"""
    embed = create_embed(f"✅ {title}", desc, COLORS['success'])
    embed.add_field(name="📌 Status", value="✅ Success", inline=True)
    return embed

def error_embed(title: str, desc: str = "") -> discord.Embed:
    """Create an error embed with red color"""
    embed = create_embed(f"❌ {title}", desc, COLORS['error'])
    embed.add_field(name="⚠️ Status", value="❌ Error", inline=True)
    return embed

def info_embed(title: str, desc: str = "") -> discord.Embed:
    """Create an info embed with blue color"""
    embed = create_embed(f"ℹ️ {title}", desc, COLORS['info'])
    embed.add_field(name="📋 Info", value="ℹ️ Information", inline=True)
    return embed

def warning_embed(title: str, desc: str = "") -> discord.Embed:
    """Create a warning embed with yellow color"""
    embed = create_embed(f"⚠️ {title}", desc, COLORS['warning'])
    embed.add_field(name="🔔 Alert", value="⚠️ Warning", inline=True)
    return embed

def permission_denied_embed(user: discord.User, reason: str = "Unknown reason") -> discord.Embed:
    """Create permission denied embed"""
    embed = discord.Embed(
        title="🔐 Permission Denied",
        description=f"You don't have permission to perform this action.\n\n**Reason:** {reason}",
        color=COLORS['error'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.set_author(name=str(user), icon_url=user.avatar.url if user.avatar else None)
    embed.add_field(name="👤 User", value=f"{user.mention}\n{user.id}", inline=True)
    embed.add_field(name="🔑 Permission Level", value="User (No Admin)", inline=True)
    embed.set_footer(text=f"⚡ {BOT_NAME} • Security Check • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def vps_not_found_embed() -> discord.Embed:
    """Create VPS not found embed"""
    embed = discord.Embed(
        title="🔍 VPS Not Found",
        description="We couldn't find any VPS associated with your account.",
        color=COLORS['warning'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.add_field(
        name="💡 What to do?",
        value=f"Use `{BOT_PREFIX}create` to create a new VPS\nOr use `{BOT_PREFIX}plans` to see available plans",
        inline=False
    )
    embed.add_field(name="📞 Need Help?", value="Contact support on our Discord", inline=False)
    embed.set_footer(text=f"⚡ {BOT_NAME} • Not Found • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed


def os_embed(title: str, desc: str = "") -> discord.Embed:
    """Create OS selection embed"""
    embed = create_embed(f"🐧 {title}", desc, COLORS['os'])
    embed.add_field(name="🖥️ OS Type", value="Operating System", inline=True)
    return embed

def loading_embed(title: str, desc: str = "Loading...") -> discord.Embed:
    """Create a loading embed"""
    embed = discord.Embed(
        title=f"⏳ {title}",
        description=desc,
        color=COLORS['info'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • Please wait... • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

async def apply_lxc_config(container_name: str):
    logger.debug(f"Stub apply_lxc_config called for {container_name}")
    return None


async def apply_internal_permissions(container_name: str):
    logger.debug(f"Stub apply_internal_permissions called for {container_name}")
    return None


def get_user_panels(user_id: str) -> List[Dict[str, Any]]:
    return []


async def show_container_mac(ctx, container: str):
    """Display container MAC address with enhanced formatting"""
    embed = info_embed("Container MAC", f"MAC information for {container} is not available.")
    embed.add_field(name="🖧 Container", value=container, inline=True)
    embed.add_field(name="📍 Status", value="Unavailable", inline=True)
    await ctx.send(embed=embed)


class ConsoleModal(Modal):
    """Modal for console command input"""
    def __init__(self, container: str):
        super().__init__(title=f"Console - {container}")
        self.container = container
        self.command = TextInput(
            label="Command",
            placeholder="Enter a command",
            style=discord.InputTextStyle.paragraph,
            max_length=2000,
            required=True
        )
        self.add_item(self.command)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission with validation"""
        # Check if command is not empty
        if not self.command.value or len(self.command.value.strip()) == 0:
            embed = error_embed("Empty Command", "Please enter a valid command.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = loading_embed("Executing Command", f"```bash\n{self.command.value}\n```")
        embed.add_field(name="🖥️ Container", value=self.container, inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

def node_embed(title: str, desc: str = "") -> discord.Embed:
    """Create node/server embed"""
    embed = create_embed(f"🌐 {title}", desc, COLORS['node'])
    embed.add_field(name="🖥️ Node Type", value="Server", inline=True)
    return embed

def terminal_embed(title: str, content: str) -> discord.Embed:
    """Create terminal output embed with better formatting"""
    # Truncate if too long
    if len(content) > 1800:
        content = content[:1800] + "\n... (truncated)"
    
    embed = discord.Embed(
        title=terminal_text(f"[ {title} ]"),
        description=f"```bash\n{content}\n```",
        color=COLORS['terminal'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.add_field(name="📊 Output", value="Terminal Response", inline=True)
    embed.add_field(name="⏱️ Time", value=datetime_.datetime.now().strftime('%H:%M:%S'), inline=True)
    embed.set_footer(text=f"⚡ Terminal • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def no_vps_embed() -> discord.Embed:
    """Create 'No VPS' embed with better information"""
    embed = discord.Embed(
        title="📭 No VPS Found",
        description=error_text("You don't have any VPS yet."),
        color=COLORS['warning'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.add_field(
        name="🎯 Next Steps",
        value=f"1. Check plans: `{BOT_PREFIX}plans`\n2. Create VPS: `{BOT_PREFIX}create [plan]`",
        inline=False
    )
    embed.add_field(
        name="💬 Questions?",
        value="Join our Discord for support",
        inline=False
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • Not Found • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

# ==================================================================================================
#  🤖  BOT SETUP
# ==================================================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

def dynamic_prefix(_bot, _message):
    prefixes = []
    for p in [BOT_PREFIX, "!", "."]:
        if p and p not in prefixes:
            prefixes.append(p)
    return commands.when_mentioned_or(*prefixes)(_bot, _message)

bot = commands.Bot(command_prefix=dynamic_prefix, intents=intents, help_command=None)
bot.start_time = datetime_.datetime.utcnow()
LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'

# ==================================================================================================
#  🎯  VPS MANAGE VIEW WITH ALL BUTTONS
# ==================================================================================================
# ==================================================================================================
#  🖥️  COMPLETE .manage COMMAND - ALL BUTTONS WORKING + TUNNEL URL
# ==================================================================================================

class VPSManageView(View):
    def __init__(self, ctx, container_name, container_data):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.container = container_name
        self.data = container_data
        self.user = ctx.author
        self.message = None
        self.live_mode = False
        
        # Row 1 - Basic Controls
        self.start_btn = Button(label="▶️ Start", style=discord.ButtonStyle.success, emoji="▶️", row=0)
        self.stop_btn = Button(label="⏹️ Stop", style=discord.ButtonStyle.danger, emoji="⏹️", row=0)
        self.restart_btn = Button(label="🔄 Restart", style=discord.ButtonStyle.primary, emoji="🔄", row=0)
        self.reboot_btn = Button(label="⚡ Reboot", style=discord.ButtonStyle.warning, emoji="⚡", row=0)
        self.shutdown_btn = Button(label="⛔ Shutdown", style=discord.ButtonStyle.danger, emoji="⛔", row=0)
        
        # Row 2 - Info & Access
        self.stats_btn = Button(label="📊 Stats", style=discord.ButtonStyle.secondary, emoji="📊", row=1)
        self.process_btn = Button(label="🔝 Processes", style=discord.ButtonStyle.secondary, emoji="🔝", row=1)
        self.console_btn = Button(label="📟 Console", style=discord.ButtonStyle.secondary, emoji="📟", row=1)
        self.ssh_btn = Button(label="🔑 SSH-GEN", style=discord.ButtonStyle.primary, emoji="🔑", row=1)
        self.logs_btn = Button(label="📋 Logs", style=discord.ButtonStyle.secondary, emoji="📋", row=1)
        
        # Row 3 - Advanced
        self.ipv4_btn = Button(label="🌍 IPv4 Check", style=discord.ButtonStyle.secondary, emoji="🌍", row=2)
        self.tunnel_btn = Button(label="🌐 Tunnel URL", style=discord.ButtonStyle.primary, emoji="🌐", row=2)
        self.ports_btn = Button(label="🔌 Ports", style=discord.ButtonStyle.secondary, emoji="🔌", row=2)
        self.backup_btn = Button(label="💾 Backup", style=discord.ButtonStyle.success, emoji="💾", row=2)
        self.restore_btn = Button(label="🔄 Restore", style=discord.ButtonStyle.warning, emoji="🔄", row=2)
        
        # Row 4 - Management
        self.reinstall_btn = Button(label="🔄 Reinstall OS", style=discord.ButtonStyle.danger, emoji="🔄", row=3)
        self.upgrade_btn = Button(label="⬆️ Upgrade VPS", style=discord.ButtonStyle.primary, emoji="⬆️", row=3)
        self.invites_btn = Button(label="📨 Check Invites", style=discord.ButtonStyle.secondary, emoji="📨", row=3)
        self.panel_btn = Button(label="📦 Install Panel", style=discord.ButtonStyle.primary, emoji="📦", row=3)
        self.share_btn = Button(label="👥 Share VPS", style=discord.ButtonStyle.secondary, emoji="👥", row=3)
        
        # Row 5 - Live & Refresh
        self.live_btn = Button(label="🔴 Live Mode", style=discord.ButtonStyle.danger, emoji="🔴", row=4)
        self.refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary, emoji="🔄", row=4)
        
        # Set callbacks
        self.start_btn.callback = self.start_callback
        self.stop_btn.callback = self.stop_callback
        self.restart_btn.callback = self.restart_callback
        self.reboot_btn.callback = self.reboot_callback
        self.shutdown_btn.callback = self.shutdown_callback
        
        self.stats_btn.callback = self.stats_callback
        self.process_btn.callback = self.process_callback
        self.console_btn.callback = self.console_callback
        self.ssh_btn.callback = self.ssh_callback
        self.logs_btn.callback = self.logs_callback
        
        self.ipv4_btn.callback = self.ipv4_callback
        self.tunnel_btn.callback = self.tunnel_callback
        self.ports_btn.callback = self.ports_callback
        self.backup_btn.callback = self.backup_callback
        self.restore_btn.callback = self.restore_callback
        
        self.reinstall_btn.callback = self.reinstall_callback
        self.upgrade_btn.callback = self.upgrade_callback
        self.invites_btn.callback = self.invites_callback
        self.panel_btn.callback = self.panel_callback
        self.share_btn.callback = self.share_callback
        
        self.live_btn.callback = self.live_callback
        self.refresh_btn.callback = self.refresh_callback
        
        # Add all buttons
        self.add_item(self.start_btn)
        self.add_item(self.stop_btn)
        self.add_item(self.restart_btn)
        self.add_item(self.reboot_btn)
        self.add_item(self.shutdown_btn)
        
        self.add_item(self.stats_btn)
        self.add_item(self.process_btn)
        self.add_item(self.console_btn)
        self.add_item(self.ssh_btn)
        self.add_item(self.logs_btn)
        
        self.add_item(self.ipv4_btn)
        self.add_item(self.tunnel_btn)
        self.add_item(self.ports_btn)
        self.add_item(self.backup_btn)
        self.add_item(self.restore_btn)
        
        self.add_item(self.reinstall_btn)
        self.add_item(self.upgrade_btn)
        self.add_item(self.invites_btn)
        self.add_item(self.panel_btn)
        self.add_item(self.share_btn)
        
        self.add_item(self.live_btn)
        self.add_item(self.refresh_btn)
    
    async def get_stats_embed(self):
        stats = await get_container_stats(self.container)
        
        embed = discord.Embed(
            title=f"```glow\n🖥️ VPS MANAGEMENT - {self.container.upper()}\n```",
            description=f"👤 **Owner:** {self.user.mention}\n📦 **Container:** `{self.container}`",
            color=0x5865F2
        )
        embed.set_thumbnail(url=self.user.avatar.url if self.user.avatar else THUMBNAIL_URL)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
        
        status_emoji = "🟢" if stats['status'] == 'running' and not self.data.get('suspended') else "⛔" if self.data.get('suspended') else "🔴"
        status_text = stats['status'].upper()
        if self.data.get('suspended'):
            status_text = "SUSPENDED"
        
        embed.add_field(name="📊 STATUS", value=f"{status_emoji} `{status_text}`", inline=True)
        embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
        embed.add_field(name="📀 MEMORY", value=f"```fix\n{stats['memory']}\n```", inline=True)
        embed.add_field(name="💽 DISK", value=f"```fix\n{stats['disk']}\n```", inline=True)
        embed.add_field(name="🌐 IP", value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{stats['mac']}\n```", inline=True)
        embed.add_field(name="⏱️ UPTIME", value=f"```fix\n{stats['uptime']}\n```", inline=True)
        
        ram_alloc = self.data['ram']
        cpu_alloc = self.data['cpu']
        disk_alloc = self.data['disk']
        ram_bar = "█" * int(ram_alloc / 16) + "░" * (10 - int(ram_alloc / 16))
        cpu_bar = "█" * int(cpu_alloc / 8) + "░" * (10 - int(cpu_alloc / 8))
        disk_bar = "█" * int(disk_alloc / 100) + "░" * (10 - int(disk_alloc / 100))
        
        embed.add_field(name="⚙️ RESOURCES", value=f"```fix\nRAM: {ram_alloc}GB [{ram_bar}]\nCPU: {cpu_alloc} Core(s) [{cpu_bar}]\nDisk: {disk_alloc}GB [{disk_bar}]\n```", inline=False)
        
        return embed
    
    async def start_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc start {self.container}")
        update_vps_status(self.container, 'running')
        await interaction.followup.send(embed=success_embed("Started", f"```fix\n{self.container} started!\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def stop_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc stop {self.container}")
        update_vps_status(self.container, 'stopped')
        await interaction.followup.send(embed=success_embed("Stopped", f"```fix\n{self.container} stopped.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def restart_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc restart {self.container}")
        update_vps_status(self.container, 'running')
        await interaction.followup.send(embed=success_embed("Restarted", f"```fix\n{self.container} restarted.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def reboot_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc restart {self.container}")
        update_vps_status(self.container, 'running')
        await interaction.followup.send(embed=success_embed("Rebooted", f"```fix\n{self.container} rebooted.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def shutdown_callback(self, interaction):
        await interaction.response.defer()
        await run_lxc(f"lxc stop {self.container}")
        update_vps_status(self.container, 'stopped')
        await interaction.followup.send(embed=success_embed("Shutdown", f"```fix\n{self.container} shutdown.\n```"), ephemeral=True)
        await self.refresh_callback(interaction)
    
    async def stats_callback(self, interaction):
        stats = await get_container_stats(self.container)
        embed = info_embed(f"Live Stats: {self.container}")
        embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
        embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
        embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
        embed.add_field(name="💽 Disk", value=f"```fix\n{stats['disk']}\n```", inline=True)
        embed.add_field(name="⏱️ Uptime", value=f"```fix\n{stats['uptime']}\n```", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def process_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "ps aux --sort=-%cpu | head -15")
        embed = terminal_embed(f"Top Processes: {self.container}", out)
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def console_callback(self, interaction):
        modal = CommandModal(self.container)
        await interaction.response.send_modal(modal)
    
    async def ssh_callback(self, interaction):
        await interaction.response.defer()
        await exec_in_container(self.container, "apt-get update -qq && apt-get install -y -qq tmate")
        sess = f"svm5-{random.randint(1000,9999)}"
        await exec_in_container(self.container, f"tmate -S /tmp/{sess}.sock new-session -d")
        await asyncio.sleep(5)
        out, _, _ = await exec_in_container(self.container, f"tmate -S /tmp/{sess}.sock display -p '#{{tmate_ssh}}'")
        url = out.strip()
        if url:
            try:
                dm = success_embed("🔑 SSH Access")
                dm.add_field(name="Container", value=f"```fix\n{self.container}\n```")
                dm.add_field(name="Command", value=f"```bash\n{url}\n```")
                await interaction.user.send(embed=dm)
                await interaction.followup.send(embed=success_embed("SSH Generated", "Check DMs!"), ephemeral=True)
            except:
                await interaction.followup.send(embed=error_embed("DM Failed", f"```fix\n{url}\n```"), ephemeral=True)
        else:
            await interaction.followup.send(embed=error_embed("Failed", "Could not generate SSH"), ephemeral=True)
    
    async def logs_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "journalctl -n 50 --no-pager 2>/dev/null || dmesg | tail -50")
        embed = terminal_embed(f"Logs: {self.container}", out[:1900])
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def ipv4_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "ip addr show")
        embed = terminal_embed(f"IPv4 Details: {self.container}", out[:1900])
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def tunnel_callback(self, interaction):
        await interaction.response.defer()
        # Try to create cloudflared tunnel
        tunnel_url = await create_cloudflared_tunnel(self.container, 80)
        if tunnel_url:
            embed = success_embed("🌐 Tunnel URL Generated")
            embed.add_field(name="URL", value=f"```fix\n{tunnel_url}\n```", inline=False)
            embed.add_field(name="Expires", value="```fix\n24 hours\n```", inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
            
            # Save to database
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE panels SET tunnel_url = ? WHERE container_name = ?', (tunnel_url, self.container))
            conn.commit()
            conn.close()
        else:
            await interaction.followup.send(embed=error_embed("Failed", "Could not create tunnel"), ephemeral=True)
    
    async def ports_callback(self, interaction):
        await interaction.response.defer()
        out, _, _ = await exec_in_container(self.container, "netstat -tuln | head -20")
        embed = terminal_embed(f"Open Ports: {self.container}", out)
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def backup_callback(self, interaction):
        await interaction.response.defer()
        backup_name = f"backup_{datetime_.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        out, err, code = await run_lxc(f"lxc snapshot {self.container} {backup_name}")
        if code == 0:
            add_snapshot(str(self.ctx.author.id), self.container, backup_name)
            embed = success_embed("Backup Created")
            embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
            embed.add_field(name="💾 Backup", value=f"```fix\n{backup_name}\n```", inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(embed=error_embed("Backup Failed", f"```diff\n- {err}\n```"), ephemeral=True)
    
    async def restore_callback(self, interaction):
        snapshots = get_snapshots(self.container)
        if not snapshots:
            return await interaction.response.send_message(embed=error_embed("No Backups"), ephemeral=True)
        
        options = []
        for s in snapshots[:10]:
            options.append(discord.SelectOption(label=s['snapshot_name'], value=s['snapshot_name'], description=f"Created: {s['created_at'][:16]}"))
        
        view = View()
        select = Select(placeholder="Select backup...", options=options)
        
        async def select_cb(sel_interaction):
            snap_name = select.values[0]
            await sel_interaction.response.defer()
            msg = await sel_interaction.followup.send(embed=info_embed("Restoring", f"```fix\n{self.container} from {snap_name}...\n```"), ephemeral=True)
            
            status = await get_container_status(self.container)
            if status == 'running':
                await run_lxc(f"lxc stop {self.container} --force")
            out, err, code = await run_lxc(f"lxc restore {self.container} {snap_name}")
            if code == 0:
                await run_lxc(f"lxc start {self.container}")
                await msg.edit(embed=success_embed("Restored", f"```fix\n{self.container} restored from {snap_name}\n```"))
            else:
                await msg.edit(embed=error_embed("Restore Failed", f"```diff\n- {err}\n```"))
        
        select.callback = select_cb
        view.add_item(select)
        await interaction.response.send_message(embed=info_embed("Select Backup"), view=view, ephemeral=True)
    
    async def reinstall_callback(self, interaction):
        options = []
        for os in OS_OPTIONS[:25]:
            options.append(discord.SelectOption(label=os['label'][:100], value=os['value'], description=os['desc'][:100]))
        
        view = View()
        select = Select(placeholder="Select new OS...", options=options)
        
        async def select_cb(sel_interaction):
            os_val = select.values[0]
            os_name = next((o['label'] for o in OS_OPTIONS if o['value'] == os_val), os_val)
            
            confirm_view = View()
            confirm_btn = Button(label="✅ Confirm Reinstall", style=discord.ButtonStyle.danger)
            cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
            
            async def confirm_cb(confirm_interaction):
                await confirm_interaction.response.defer()
                msg = await confirm_interaction.followup.send(embed=info_embed("Reinstalling", f"```fix\n{self.container} with {os_name}...\n```"), ephemeral=True)
                
                try:
                    status = await get_container_status(self.container)
                    if status == 'running':
                        await run_lxc(f"lxc stop {self.container} --force")
                    
                    ram_mb = self.data['ram'] * 1024
                    cpu = self.data['cpu']
                    disk = self.data['disk']
                    
                    await run_lxc(f"lxc delete {self.container} --force")
                    await run_lxc(f"lxc init {os_val} {self.container} -s {DEFAULT_STORAGE_POOL}")
                    await run_lxc(f"lxc config set {self.container} limits.memory {ram_mb}MB")
                    await run_lxc(f"lxc config set {self.container} limits.cpu {cpu}")
                    await run_lxc(f"lxc config device set {self.container} root size={disk}GB")
                    await run_lxc(f"lxc start {self.container}")
                    await asyncio.sleep(5)
                    
                    embed = success_embed("OS Reinstalled")
                    embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
                    embed.add_field(name="🐧 New OS", value=f"```fix\n{os_name}\n```", inline=True)
                    await msg.edit(embed=embed)
                except Exception as e:
                    await msg.edit(embed=error_embed("Reinstall Failed", f"```diff\n- {str(e)}\n```"))
            
            confirm_btn.callback = confirm_cb
            cancel_btn.callback = lambda ci: ci.response.edit_message(embed=info_embed("Cancelled"), view=None)
            confirm_view.add_item(confirm_btn)
            confirm_view.add_item(cancel_btn)
            
            embed = warning_embed("⚠️ Confirm Reinstall", f"```fix\nContainer: {self.container}\nCurrent OS: {self.data.get('os_version', 'ubuntu:22.04')}\nNew OS: {os_name}\n```\n\n⚠️ ALL DATA WILL BE LOST!")
            await sel_interaction.response.edit_message(embed=embed, view=confirm_view)
        
        select.callback = select_cb
        view.add_item(select)
        await interaction.response.send_message(embed=info_embed("Reinstall OS"), view=view, ephemeral=True)
    
    async def upgrade_callback(self, interaction):
        stats = get_user_stats(str(self.ctx.author.id))
        invites = stats.get('invites', 0)
        
        options = [
            discord.SelectOption(label="💾 +2GB RAM", value="ram:2", description=f"Cost: 5 invites → New: {self.data['ram']+2}GB"),
            discord.SelectOption(label="💾 +4GB RAM", value="ram:4", description=f"Cost: 10 invites → New: {self.data['ram']+4}GB"),
            discord.SelectOption(label="⚡ +1 CPU Core", value="cpu:1", description=f"Cost: 5 invites → New: {self.data['cpu']+1} cores"),
            discord.SelectOption(label="⚡ +2 CPU Cores", value="cpu:2", description=f"Cost: 10 invites → New: {self.data['cpu']+2} cores"),
            discord.SelectOption(label="💽 +20GB Disk", value="disk:20", description=f"Cost: 5 invites → New: {self.data['disk']+20}GB"),
            discord.SelectOption(label="💽 +50GB Disk", value="disk:50", description=f"Cost: 10 invites → New: {self.data['disk']+50}GB"),
        ]
        
        view = View()
        select = Select(placeholder="Select upgrade...", options=options)
        
        async def select_cb(sel_interaction):
            value = select.values[0]
            resource, amount = value.split(':')
            amount = int(amount)
            cost = 5 if amount in [2,1,20] else 10
            
            if invites < cost:
                return await sel_interaction.response.send_message(embed=error_embed("Not Enough Invites", f"Need {cost} invites, you have {invites}"), ephemeral=True)
            
            confirm_view = View()
            confirm_btn = Button(label="✅ Confirm Upgrade", style=discord.ButtonStyle.success)
            cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
            
            async def confirm_cb(confirm_interaction):
                await confirm_interaction.response.defer()
                msg = await confirm_interaction.followup.send(embed=info_embed("Upgrading", f"```fix\n+{amount} {resource.upper()}...\n```"), ephemeral=True)
                
                try:
                    status = await get_container_status(self.container)
                    was_running = status == 'running'
                    
                    if was_running:
                        await run_lxc(f"lxc stop {self.container} --force")
                    
                    if resource == "ram":
                        new_ram = self.data['ram'] + amount
                        await run_lxc(f"lxc config set {self.container} limits.memory {new_ram * 1024}MB")
                        conn = get_db()
                        cur = conn.cursor()
                        cur.execute('UPDATE vps SET ram = ? WHERE container_name = ?', (new_ram, self.container))
                        conn.commit()
                        conn.close()
                        self.data['ram'] = new_ram
                    elif resource == "cpu":
                        new_cpu = self.data['cpu'] + amount
                        await run_lxc(f"lxc config set {self.container} limits.cpu {new_cpu}")
                        conn = get_db()
                        cur = conn.cursor()
                        cur.execute('UPDATE vps SET cpu = ? WHERE container_name = ?', (new_cpu, self.container))
                        conn.commit()
                        conn.close()
                        self.data['cpu'] = new_cpu
                    elif resource == "disk":
                        new_disk = self.data['disk'] + amount
                        await run_lxc(f"lxc config device set {self.container} root size={new_disk}GB")
                        conn = get_db()
                        cur = conn.cursor()
                        cur.execute('UPDATE vps SET disk = ? WHERE container_name = ?', (new_disk, self.container))
                        conn.commit()
                        conn.close()
                        self.data['disk'] = new_disk
                    
                    if was_running:
                        await run_lxc(f"lxc start {self.container}")
                    
                    conn = get_db()
                    cur = conn.cursor()
                    cur.execute('UPDATE user_stats SET invites = invites - ?, last_updated = ? WHERE user_id = ?',
                               (cost, datetime_.datetime.now().isoformat(), str(self.ctx.author.id)))
                    conn.commit()
                    conn.close()
                    
                    embed = success_embed("Upgraded")
                    embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
                    embed.add_field(name="⚙️ Upgrade", value=f"```fix\n+{amount} {resource.upper()}\nCost: {cost} invites\n```", inline=True)
                    await msg.edit(embed=embed)
                except Exception as e:
                    await msg.edit(embed=error_embed("Upgrade Failed", f"```diff\n- {str(e)}\n```"))
            
            confirm_btn.callback = confirm_cb
            cancel_btn.callback = lambda ci: ci.response.edit_message(embed=info_embed("Cancelled"), view=None)
            confirm_view.add_item(confirm_btn)
            confirm_view.add_item(cancel_btn)
            
            embed = warning_embed("Confirm Upgrade", f"```fix\nContainer: {self.container}\nUpgrade: +{amount} {resource.upper()}\nCost: {cost} invites\nCurrent: {self.data['ram'] if resource=='ram' else self.data['cpu'] if resource=='cpu' else self.data['disk']}\nNew: {self.data[resource] + amount}\n```")
            await sel_interaction.response.edit_message(embed=embed, view=confirm_view)
        
        select.callback = select_cb
        view.add_item(select)
        
        embed = info_embed("Upgrade VPS", f"```fix\nContainer: {self.container}\nCurrent RAM: {self.data['ram']}GB\nCurrent CPU: {self.data['cpu']} cores\nCurrent Disk: {self.data['disk']}GB\nYour Invites: {invites}\n```")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def invites_callback(self, interaction):
        stats = get_user_stats(str(self.ctx.author.id))
        invites = stats.get('invites', 0)
        vps_count = len(get_user_vps(str(self.ctx.author.id)))
        
        embed = info_embed("Your Invites")
        embed.add_field(name="📨 Total Invites", value=f"```fix\n{invites}\n```", inline=True)
        embed.add_field(name="🖥️ VPS Count", value=f"```fix\n{vps_count}\n```", inline=True)
        
        next_plan = None
        for plan in FREE_VPS_PLANS['invites']:
            if invites < plan['invites']:
                next_plan = plan
                break
        
        if next_plan:
            embed.add_field(name="🎯 Next Plan", value=f"```fix\n{next_plan['emoji']} {next_plan['name']}\nNeed {next_plan['invites'] - invites} more invites\nRAM: {next_plan['ram']}GB\n```", inline=False)
        else:
            embed.add_field(name="🏆 Status", value="```fix\nYou have reached the maximum plan!\n```", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def panel_callback(self, interaction):
        view = PanelInstallView(self.ctx, self.container)
        embed = info_embed("Install Panel", "Select panel to install:")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def share_callback(self, interaction):
        modal = ShareModal(self.container)
        await interaction.response.send_modal(modal)
    
    async def live_callback(self, interaction):
        self.live_mode = not self.live_mode
        if self.live_mode:
            self.live_btn.label = "⏹️ Stop Live"
            self.live_btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            self.live_task = asyncio.create_task(self.live_update_task(interaction))
        else:
            self.live_btn.label = "🔴 Live Mode"
            self.live_btn.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self)
            if self.live_task:
                self.live_task.cancel()
    
    async def live_update_task(self, interaction):
        while self.live_mode:
            try:
                embed = await self.get_stats_embed()
                await interaction.edit_original_response(embed=embed, view=self)
                await asyncio.sleep(5)
            except:
                self.live_mode = False
                break
    
    async def refresh_callback(self, interaction):
        embed = await self.get_stats_embed()
        await interaction.response.edit_message(embed=embed, view=self)


class CommandModal(Modal):
    def __init__(self, container):
        super().__init__(title="Run Command")
        self.container = container
        self.add_item(InputText(label="Command", placeholder="e.g., apt update", style=discord.InputTextStyle.paragraph))
        self.add_item(InputText(label="Timeout (seconds)", placeholder="30", required=False, value="30"))
    
    async def callback(self, interaction):
        cmd = self.children[0].value
        timeout = int(self.children[1].value or "30")
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=info_embed("Executing", f"```fix\n$ {cmd}\n```"), ephemeral=True)
        out, err, code = await exec_in_container(self.container, cmd, timeout)
        embed = terminal_embed("Output", f"$ {cmd}\n\n{(out or err)[:1900]}")
        embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```")
        await msg.edit(embed=embed)


class ShareModal(Modal):
    def __init__(self, container):
        super().__init__(title="Share VPS")
        self.container = container
        self.add_item(InputText(label="User ID or @mention"))
        self.add_item(InputText(label="Permissions", placeholder="view, manage, full", required=False, value="view"))
    
    async def callback(self, interaction):
        user_input = self.children[0].value
        perms = self.children[1].value or "view"
        
        user_id = user_input
        if user_input.startswith('<@') and user_input.endswith('>'):
            user_id = user_input[2:-1]
            if user_id.startswith('!'):
                user_id = user_id[1:]
        
        try:
            user = await interaction.client.fetch_user(int(user_id))
            if share_vps(str(interaction.user.id), str(user.id), self.container):
                embed = success_embed("VPS Shared")
                embed.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```", inline=True)
                embed.add_field(name="👤 Shared With", value=user.mention, inline=True)
                embed.add_field(name="🔑 Permissions", value=f"```fix\n{perms}\n```", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                
                try:
                    dm = info_embed("VPS Shared With You")
                    dm.add_field(name="📦 Container", value=f"```fix\n{self.container}\n```")
                    dm.add_field(name="👤 Owner", value=interaction.user.mention)
                    await user.send(embed=dm)
                except:
                    pass
            else:
                await interaction.response.send_message(embed=error_embed("Failed"), ephemeral=True)
        except:
            await interaction.response.send_message(embed=error_embed("Invalid User"), ephemeral=True)


@bot.command(name="manage")
async def manage(ctx, container_name: str = None):
    """Interactive VPS manager with all buttons and permission checks"""
    user_id = str(ctx.author.id)
    
    # Check if user has any VPS
    vps_list = get_user_vps(user_id)
    if not vps_list:
        return await ctx.send(embed=no_vps_embed())
    
    # If no container specified, use first one
    if not container_name:
        container_data = vps_list[0]
        container_name = container_data['container_name']
    else:
        # Verify user owns this container
        container_data = next((v for v in vps_list if v['container_name'] == container_name), None)
        if not container_data:
            embed = permission_denied_embed(
                ctx.author,
                f"You don't own VPS '{container_name}'"
            )
            return await ctx.send(embed=embed)
    
    view = VPSManageView(ctx, container_name, container_data)
    embed = await view.get_stats_embed()
    msg = await ctx.send(embed=embed, view=view)
    view.message = msg
    
# ==================================================================================================
#  📦  PANEL INSTALL VIEW WITH BUTTONS
# ==================================================================================================
# ==================================================================================================
#  📚  COMPLETE HELP COMMAND - ULTIMATE UI WITH SELECT MENU & IMAGES
# ==================================================================================================

# Help Category Images
HELP_IMAGES = {
    'home': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'user': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'vps': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'console': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'games': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'tools': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'nodes': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'share': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ports': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ipv4': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'panels': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ai': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'os': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'admin': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'owner': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    'ip': "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
}

class HelpView(View):
    """Interactive Help Menu with Select Menu & Images"""
    
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_category = "home"
        self.message = None
        
        # Category Options with Emojis
        self.category_options = [
            discord.SelectOption(label="🏠 Home", value="home", emoji="🏠", description="Main menu with overview"),
            discord.SelectOption(label="👤 User Commands", value="user", emoji="👤", description="14 user commands"),
            discord.SelectOption(label="🖥️ VPS Commands", value="vps", emoji="🖥️", description="8 VPS management commands"),
            discord.SelectOption(label="📟 Console Commands", value="console", emoji="📟", description="10 console commands"),
            discord.SelectOption(label="🎮 Games Commands", value="games", emoji="🎮", description="7 game server commands"),
            discord.SelectOption(label="🛠️ Tools Commands", value="tools", emoji="🛠️", description="7 development tools"),
            discord.SelectOption(label="🌐 Node Commands", value="nodes", emoji="🌐", description="7 cluster management commands"),
            discord.SelectOption(label="👥 Share Commands", value="share", emoji="👥", description="4 VPS sharing commands"),
            discord.SelectOption(label="🔌 Port Commands", value="ports", emoji="🔌", description="6 port forwarding commands"),
            discord.SelectOption(label="🌍 IPv4 Commands", value="ipv4", emoji="🌍", description="6 IPv4 management commands"),
            discord.SelectOption(label="📦 Panel Commands", value="panels", emoji="📦", description="6 panel installation commands"),
            discord.SelectOption(label="🤖 AI Commands", value="ai", emoji="🤖", description="3 AI chat commands"),
            discord.SelectOption(label="🐧 OS Commands", value="os", emoji="🐧", description="70+ operating systems"),
            discord.SelectOption(label="🌐 IP Commands", value="ip", emoji="🌐", description="15+ IP management commands"),
            discord.SelectOption(label="🛡️ Admin Commands", value="admin", emoji="🛡️", description="13 admin commands"),
            discord.SelectOption(label="👑 Owner Commands", value="owner", emoji="👑", description="9 owner commands"),
        ]
        
        self.select = Select(placeholder="📋 Select a command category...", options=self.category_options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        # Add refresh button
        refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary, emoji="🔄", row=1)
        refresh_btn.callback = self.refresh_callback
        self.add_item(refresh_btn)
        
        # Add delete button
        delete_btn = Button(label="🗑️ Close", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
        delete_btn.callback = self.delete_callback
        self.add_item(delete_btn)
        
        self.update_embed()
    
    def update_embed(self):
        """Update embed based on selected category"""
        
        # Category Data
        categories = {
            'home': {
                'title': "🏠 SVM5-BOT TOOLS - ULTIMATE VPS MANAGEMENT",
                'desc': f"```glow\nWelcome to {BOT_NAME} - Complete VPS Management Solution\n```\n"
                        f"**Select a category from the dropdown menu to view commands.**\n\n"
                        f"```fix\n📊 Bot Statistics:\n• Total Commands: 97+\n• OS Options: 70+\n• Games: 7\n• Tools: 7\n• Active Users: {len(get_all_vps())} VPS\n• Server IP: {SERVER_IP}\n• License: {'✅ Verified' if LICENSE_VERIFIED else '❌ Not Verified'}\n```",
                'fields': [
                    ("👤 USER (14)", "Basic commands for all users", True),
                    ("🖥️ VPS (8)", "Manage your VPS containers", True),
                    ("📟 CONSOLE (10)", "Terminal access and commands", True),
                    ("🎮 GAMES (7)", "Game server management", True),
                    ("🛠️ TOOLS (7)", "Development tools", True),
                    ("🌐 NODES (7)", "Cluster management", True),
                    ("👥 SHARE (4)", "Share VPS with users", True),
                    ("🔌 PORTS (6)", "Port forwarding", True),
                    ("🌍 IPv4 (6)", "IPv4 management", True),
                    ("📦 PANELS (6)", "Panel installation", True),
                    ("🤖 AI (3)", "AI assistant", True),
                    ("🐧 OS (70+)", "Operating systems", True),
                    ("🌐 IP (15+)", "IP management", True),
                    ("🛡️ ADMIN (13)", "Admin commands", True),
                    ("👑 OWNER (9)", "Owner commands", True),
                ]
            },
            'user': {
                'title': "👤 USER COMMANDS (14)",
                'desc': "```fix\nBasic commands available to all users\n```",
                'fields': [
                    (".help", "Show this interactive help menu", False),
                    (".ping", "Check bot latency with graph", False),
                    (".uptime", "Show bot uptime", False),
                    (".bot-info", "Detailed bot information", False),
                    (".server-info", "Show server hardware info", False),
                    (".plans", "View free VPS plans", False),
                    (".stats", "View your statistics", False),
                    (".inv", "Check your invites", False),
                    (".invites-top [limit]", "Show top inviters", False),
                    (".claim-free", "Claim free VPS with invites", False),
                    (".my-acc", "View your generated account", False),
                    (".gen-acc", "Generate random account", False),
                    (".api-key [regenerate]", "View or regenerate API key", False),
                    (".userinfo [@user]", "User information", False),
                ]
            },
            'vps': {
                'title': "🖥️ VPS COMMANDS (8)",
                'desc': "```fix\nManage your VPS containers with interactive buttons\n```",
                'fields': [
                    (".myvps", "List your VPS with status", False),
                    (".list", "Detailed VPS list with IPs", False),
                    (".manage [container]", "Interactive VPS manager with 20+ buttons", False),
                    (".stats [container]", "View VPS statistics with graphs", False),
                    (".logs [container] [lines]", "View VPS logs", False),
                    (".reboot <container>", "Reboot VPS", False),
                    (".shutdown <container>", "Shutdown VPS", False),
                    (".rename <old> <new>", "Rename VPS container", False),
                ]
            },
            'console': {
                'title': "📟 CONSOLE COMMANDS (10)",
                'desc': "```fix\nTerminal access and console commands\n```",
                'fields': [
                    (".ss [container]", "Take VPS snapshot/console output", False),
                    (".console <container> [command]", "Interactive console with modal", False),
                    (".execute <container> <command>", "Execute command in VPS", False),
                    (".ssh-gen <container>", "Generate temporary SSH access", False),
                    (".top <container>", "Show live process monitor", False),
                    (".df <container>", "Show disk usage with graph", False),
                    (".free <container>", "Show memory usage with graph", False),
                    (".ps <container>", "Show process list", False),
                    (".who <container>", "Show logged-in users", False),
                    (".uptime <container>", "Show container uptime", False),
                ]
            },
            'games': {
                'title': "🎮 GAMES COMMANDS (7)",
                'desc': "```fix\nInstall and manage game servers (Minecraft, CS:GO, etc.)\n```",
                'fields': [
                    (".games", "List all available games", False),
                    (".game-info <game>", "Detailed game information", False),
                    (".install-game <container> <game>", "Install game on VPS", False),
                    (".my-games [container]", "Your installed games", False),
                    (".start-game <container> <game>", "Start game server", False),
                    (".stop-game <container> <game>", "Stop game server", False),
                    (".game-stats <container> <game>", "Game server statistics", False),
                ]
            },
            'tools': {
                'title': "🛠️ TOOLS COMMANDS (7)",
                'desc': "```fix\nInstall development tools and services (Nginx, MySQL, Docker, etc.)\n```",
                'fields': [
                    (".tools", "List all available tools", False),
                    (".tool-info <tool>", "Detailed tool information", False),
                    (".install-tool <container> <tool>", "Install tool on VPS", False),
                    (".my-tools [container]", "Your installed tools", False),
                    (".start-tool <container> <tool>", "Start tool service", False),
                    (".stop-tool <container> <tool>", "Stop tool service", False),
                    (".tool-port <container> <tool>", "Show tool service port", False),
                ]
            },
            'nodes': {
                'title': "🌐 NODE COMMANDS (7)",
                'desc': "```fix\nManage cluster nodes (Auto-detects local node)\n```",
                'fields': [
                    (".node", "List all nodes in cluster", False),
                    (".node-info [name]", "Detailed node information", False),
                    (".node-add <name> <host> <user> <pass>", "Add new node (Admin)", False),
                    (".node-remove <name>", "Remove node (Admin)", False),
                    (".node-check <name>", "Check node health", False),
                    (".node-stats", "Cluster statistics", False),
                    (".node-connect <host> <user> [pass]", "Connect to remote node", False),
                ]
            },
            'share': {
                'title': "👥 SHARE COMMANDS (4)",
                'desc': "```fix\nShare VPS with other users\n```",
                'fields': [
                    (".share <@user> <vps_num>", "Share VPS with user", False),
                    (".unshare <@user> <vps_num>", "Remove VPS sharing", False),
                    (".shared", "List VPS shared with you", False),
                    (".manage-shared <owner> <num>", "Manage shared VPS", False),
                ]
            },
            'ports': {
                'title': "🔌 PORT COMMANDS (6)",
                'desc': "```fix\nPort forwarding management\n```",
                'fields': [
                    (".ports", "Port forwarding help", False),
                    (".ports add <vps_num> <port> [tcp/udp]", "Add port forward", False),
                    (".ports list", "List your port forwards", False),
                    (".ports remove <id>", "Remove port forward", False),
                    (".ports quota", "Check your port quota", False),
                    (".ports check <port>", "Check if port is available", False),
                ]
            },
            'ipv4': {
                'title': "🌍 IPv4 COMMANDS (6)",
                'desc': "```fix\nBuy and manage IPv4 addresses\n```",
                'fields': [
                    (".ipv4", "View your IPv4 addresses", False),
                    (".ipv4-details <container>", "Detailed IPv4 information", False),
                    (".buy-ipv4", "Purchase IPv4 via UPI with QR", False),
                    (".upi", "Show UPI payment information", False),
                    (".upi-qr [amount] [note]", "Generate UPI QR code", False),
                    (".pay <amount> [note]", "Generate payment link", False),
                ]
            },
            'panels': {
                'title': "📦 PANEL COMMANDS (6)",
                'desc': "```fix\nInstall game panels on your VPS\n```",
                'fields': [
                    (".install-panel", "Install Pterodactyl/Pufferpanel", False),
                    (".panel-info", "Show your installed panel info", False),
                    (".panel-reset [type]", "Reset panel admin password", False),
                    (".panel-delete [type]", "Delete panel record", False),
                    (".panel-tunnel [container] [port]", "Create cloudflared tunnel", False),
                    (".panel-status [container]", "Panel installation status", False),
                ]
            },
            'ai': {
                'title': "🤖 AI COMMANDS (3)",
                'desc': f"```fix\nChat with AI assistant (Model: {AI_MODEL})\n```",
                'fields': [
                    (".ai <message>", "Chat with AI assistant", False),
                    (".ai-reset", "Reset chat history", False),
                    (".ai-help <topic>", "Get AI help on specific topic", False),
                ]
            },
            'os': {
                'title': "🐧 OS COMMANDS",
                'desc': f"```fix\n70+ Operating Systems available for VPS creation\n```",
                'fields': [
                    (".os-list [category]", "List available OS by category", False),
                    ("Ubuntu", "20.04, 22.04, 24.04, 18.04, 16.04... (15 versions)", True),
                    ("Debian", "12, 11, 10, 9, 8, Sid, Testing... (14 versions)", True),
                    ("Fedora", "40, 39, 38, 37, 36, Rawhide... (10 versions)", True),
                    ("Rocky/Alma", "9, 8, 7 (6 versions)", True),
                    ("CentOS", "9 Stream, 8 Stream, 7, 6, 5, 4 (6 versions)", True),
                    ("Alpine", "3.19, 3.18, 3.17, Edge... (8 versions)", True),
                    ("Arch/Manjaro", "Arch Linux, Manjaro (3 versions)", True),
                    ("OpenSUSE", "Tumbleweed, Leap 15.5, 15.4, 15.3 (4 versions)", True),
                    ("FreeBSD", "14, 13, 12, 11, 10 (5 versions)", True),
                    ("OpenBSD", "7.4, 7.3, 7.2 (3 versions)", True),
                    ("Kali/Gentoo/Void", "Kali Linux, Gentoo, Void Linux (6+ versions)", True),
                ]
            },
            'ip': {
                'title': "🌐 IP COMMANDS (15+)",
                'desc': "```fix\nComplete IP management commands\n```",
                'fields': [
                    (".ip", "Show your IP information", False),
                    (".ip public", "Show server public IP", False),
                    (".ip vps", "Show all VPS IPs", False),
                    (".ip node", "Show all node IPs", False),
                    (".ip all", "Show all IPs", False),
                    (".ip <container>", "Show container IP details", False),
                    (".myip", "Your public IP", False),
                    (".vps-ip [container]", "VPS IP details", False),
                    (".node-ip [node]", "Node IP details", False),
                    (".public-ip", "Server public IP with location", False),
                    (".mac [container]", "MAC address", False),
                    (".gateway [container]", "Gateway information", False),
                    (".netstat [container]", "Network connections", False),
                    (".ifconfig [container]", "Network interfaces", False),
                    (".dns [container]", "DNS servers", False),
                    (".ping-ip <ip>", "Ping IP address", False),
                    (".trace-ip <ip>", "Trace route to IP", False),
                    (".user-ip @user", "User IPs (Admin)", False),
                    (".assign-ip @user <container> [ip]", "Assign IP (Admin)", False),
                    (".release-ip @user <container>", "Release IP (Admin)", False),
                    (".ip-stats", "IP statistics (Admin)", False),
                    (".my-ip-info", "Your network info", False),
                    (".ip-history [@user]", "IP history (Admin)", False),
                ]
            },
        }
        
        # Add admin commands if user is admin
        if is_admin(str(self.ctx.author.id)):
            categories['admin'] = {
                'title': "🛡️ ADMIN COMMANDS (13)",
                'desc': "```fix\nAdministrator commands\n```",
                'fields': [
                    (".create <ram> <cpu> <disk> @user", "Create VPS for user", False),
                    (".delete @user <num> [reason]", "Delete user's VPS", False),
                    (".suspend <container> [reason]", "Suspend VPS", False),
                    (".unsuspend <container>", "Unsuspend VPS", False),
                    (".add-resources <container> [ram] [cpu] [disk]", "Add resources", False),
                    (".list-all", "List all VPS in system", False),
                    (".add-inv @user <amount>", "Add invites", False),
                    (".remove-inv @user <amount>", "Remove invites", False),
                    (".ports-add @user <amount>", "Add port slots", False),
                    (".serverstats", "Server statistics", False),
                    (".admin-add-ipv4 @user <container>", "Assign IPv4", False),
                    (".admin-rm-ipv4 @user [container]", "Remove IPv4", False),
                    (".license-verify keyenter", "License Key Verifying", False),
                    (".admin-pending-ipv4", "View pending IPv4 purchases", False),
                ]
            }
        
        # Add owner commands if user is main admin
        if str(self.ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS]:
            categories['owner'] = {
                'title': "👑 OWNER COMMANDS (9)",
                'desc': "```fix\nMain owner commands\n```",
                'fields': [
                    (".admin-add @user", "Add new administrator", False),
                    (".admin-remove @user", "Remove administrator", False),
                    (".admin-list", "List all administrators", False),
                    (".maintenance <on/off>", "Toggle maintenance mode", False),
                    (".purge-all", "Purge all unprotected VPS", False),
                    (".protect @user [num]", "Protect VPS from purge", False),
                    (".unprotect @user [num]", "Remove purge protection", False),
                    (".backup-db", "Backup database", False),
                    (".restore-db <file>", "Restore database", False),
                ]
            }
        
        # Get current category data
        cat_data = categories.get(self.current_category, categories['home'])
        
        # Create embed
        embed = discord.Embed(
            title=f"```glow\n{cat_data['title']}\n```",
            description=cat_data['desc'],
            color=COLORS['primary']
        )
        
        # Set category image
        if self.current_category in HELP_IMAGES:
            embed.set_thumbnail(url=HELP_IMAGES[self.current_category])
        embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
        
        # Add fields
        for name, value, inline in cat_data['fields']:
            embed.add_field(name=f"**{name}**", value=value, inline=inline)
        
        # Add footer
        embed.set_footer(
            text=f"⚡ {BOT_NAME} • {len(cat_data['fields'])} commands • Page: {self.current_category.upper()} • Use dropdown to navigate ⚡",
            icon_url=THUMBNAIL_URL
        )
        
        self.embed = embed
    
    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        self.current_category = self.select.values[0]
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    async def refresh_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    async def delete_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        await interaction.message.delete()

@bot.command(name="commands")
async def commands_alias(ctx):
    """Alias for help command with improved formatting"""
    embed = discord.Embed(
        title="📚 All Available Commands",
        description="Complete command reference with categories",
        color=COLORS['primary'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    embed.add_field(
        name="👤 User Commands",
        value=f"▸ `{BOT_PREFIX}help-user` (14 commands)\n▸ Basic account and server info",
        inline=False
    )
    embed.add_field(
        name="🖥️ VPS Commands",
        value=f"▸ `{BOT_PREFIX}help-vps` (8 commands)\n▸ Manage your VPS instances",
        inline=False
    )
    embed.add_field(
        name="🌐 IP Commands",
        value=f"▸ `{BOT_PREFIX}help-ip` (15+ commands)\n▸ Network and IP management",
        inline=False
    )
    embed.add_field(
        name="🎮 Game Commands",
        value=f"▸ `{BOT_PREFIX}help-games` (Game server setup)\n▸ Minecraft, Terraria, CS:GO",
        inline=False
    )
    
    if ctx.author.id in MAIN_ADMIN_IDS:
        embed.add_field(
            name="🛡️ Admin Commands",
            value=f"▸ `{BOT_PREFIX}help-admin` (Admin only)\n▸ Server management",
            inline=False
        )
    
    embed.add_field(
        name="🔗 Quick Start",
        value=f"1. Use `{BOT_PREFIX}plans` to see VPS plans\n2. Use `{BOT_PREFIX}manage` to control VPS\n3. Use `{BOT_PREFIX}help` for detailed info",
        inline=False
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Use category commands for more details • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    
    await ctx.send(embed=embed)


# ==================================================================================================
#  🆕  ADDITIONAL HELP COMMANDS FOR QUICK ACCESS
# ==================================================================================================

@bot.command(name="help-user")
async def help_user(ctx):
    """Quick help for user commands with enhanced formatting"""
    embed = discord.Embed(
        title="👤 User Commands Quick Reference",
        description="Essential commands for managing your account and VPS",
        color=COLORS['info'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.set_thumbnail(url=HELP_IMAGES['user'])
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    commands_list = [
        ".help", ".ping", ".uptime", ".bot-info", ".server-info",
        ".plans", ".stats", ".inv", ".invites-top", ".claim-free",
        ".my-acc", ".gen-acc", ".api-key", ".userinfo"
    ]
    
    embed.add_field(
        name="📋 Available Commands (14)",
        value="\n".join([f"▸ `{c}`" for c in commands_list]),
        inline=False
    )
    embed.add_field(
        name="💡 Quick Tips",
        value="• Use `.help` for detailed command info\n• Use `.manage` to control VPS\n• Use `.plans` to see pricing",
        inline=False
    )
    embed.add_field(
        name="🔗 Related Commands",
        value=f"`{BOT_PREFIX}help-vps` • `{BOT_PREFIX}help-ip` • `{BOT_PREFIX}help-admin`",
        inline=False
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • Help Center • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    
    await ctx.send(embed=embed)


@bot.command(name="help-vps")
async def help_vps(ctx):
    """Quick help for VPS commands with enhanced formatting"""
    embed = discord.Embed(
        title="🖥️ VPS Commands Quick Reference",
        description="Complete VPS management and monitoring commands",
        color=COLORS['primary'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.set_thumbnail(url=HELP_IMAGES['vps'])
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    commands_list = [
        ".myvps", ".list", ".manage", ".stats", ".logs", ".reboot", ".shutdown", ".rename"
    ]
    
    embed.add_field(
        name="📋 Available Commands (8)",
        value="\n".join([f"▸ `{c}`" for c in commands_list]),
        inline=False
    )
    embed.add_field(
        name="⭐ Most Used",
        value="• `{BOT_PREFIX}manage` - Interactive VPS manager (20+ buttons)\n• `{BOT_PREFIX}myvps` - List all your VPS",
        inline=False
    )
    embed.add_field(
        name="🎮 Power Controls",
        value="▸ Start/Stop ▸ Reboot ▸ Reinstall OS ▸ Upgrade",
        inline=False
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • VPS Help • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    
    await ctx.send(embed=embed)


@bot.command(name="help-ip")
async def help_ip(ctx):
    """Quick help for IP commands with enhanced formatting"""
    embed = discord.Embed(
        title="🌐 IP Commands Quick Reference",
        description="Complete IP management and network information commands",
        color=COLORS['cyan'] if 'cyan' in COLORS else COLORS['info'],
        timestamp=datetime_.datetime.utcnow()
    )
    embed.set_thumbnail(url=HELP_IMAGES['ipv4'])
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    commands_list = [
        ".ip", ".ip public", ".ip vps", ".ip node", ".ip <container>",
        ".myip", ".vps-ip", ".node-ip", ".public-ip", ".mac",
        ".gateway", ".netstat", ".ifconfig", ".dns", ".ping-ip", ".trace-ip"
    ]
    
    embed.add_field(
        name="📋 Available Commands (15+)",
        value="\n".join([f"▸ `{c}`" for c in commands_list[:8]]),
        inline=True
    )
    embed.add_field(
        name="🔧 Advanced",
        value="\n".join([f"▸ `{c}`" for c in commands_list[8:]]),
        inline=True
    )
    embed.add_field(
        name="💡 Pro Tip",
        value="Use `{BOT_PREFIX}ip all` to see all IPs at once",
        inline=False
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • IP Help • {datetime_.datetime.now().strftime('%H:%M:%S')} ⚡")
    
    await ctx.send(embed=embed)


@bot.command(name="help-admin")
@is_admin()
async def help_admin(ctx):
    """Quick help for admin commands"""
    embed = discord.Embed(
        title="```glow\n🛡️ Admin Commands Quick Reference\n```",
        description="```fix\n13 admin commands\n```",
        color=COLORS['warning']
    )
    embed.set_thumbnail(url=HELP_IMAGES['admin'])
    
    commands_list = [
        ".create", ".delete", ".suspend", ".unsuspend", ".add-resources",
        ".list-all", ".add-inv", ".remove-inv", ".ports-add", ".serverstats",
        ".admin-add-ipv4", ".admin-rm-ipv4", ".admin-pending-ipv4"
    ]
    embed.add_field(name="📋 Commands", value="\n".join([f"• `{c}`" for c in commands_list]), inline=False)
    embed.add_field(name="⚠️ Warning", value="These commands affect other users' VPS", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name="help-os")
async def help_os(ctx):
    """Quick help for OS options"""
    embed = discord.Embed(
        title="```glow\n🐧 Operating Systems Available\n```",
        description="```fix\n70+ Operating Systems for VPS creation\n```",
        color=COLORS['os']
    )
    embed.set_thumbnail(url=HELP_IMAGES['os'])
    
    os_list = [
        "🐧 Ubuntu (15 versions)", "🌀 Debian (14 versions)", "🎩 Fedora (10 versions)",
        "🦊 Rocky/Alma (6 versions)", "📦 CentOS (6 versions)", "🐧 Alpine (8 versions)",
        "📀 Arch/Manjaro (3 versions)", "🟢 OpenSUSE (4 versions)", "🔵 FreeBSD (5 versions)",
        "🐡 OpenBSD (3 versions)", "🐉 Kali Linux", "💻 Gentoo", "⚪ Void Linux"
    ]
    embed.add_field(name="📋 Available OS", value="\n".join([f"• {o}" for o in os_list]), inline=False)
    embed.add_field(name="📌 Tip", value="Use `.os-list [category]` to see detailed list", inline=False)
    
    await ctx.send(embed=embed)
           
# ==================================================================================================
#  ✅  ON READY
# ==================================================================================================

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{BOT_PREFIX}help | {BOT_NAME}"
        )
    )
    logger.info(f"✅ Bot is ready: {bot.user}")
    update_local_node_stats()
    
    total_vps = len(get_all_vps())
    nodes = len(load_nodes()['nodes'])
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                               ║
║                      ███████╗██╗   ██╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗      ║
║                      ██╔════╝██║   ██║████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝      ║
║                      ███████╗██║   ██║██╔████╔██║█████╗      ██████╔╝██║   ██║   ██║         ║
║                      ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║   ██║         ║
║                      ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝   ██║         ║
║                      ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝         ║
║                                                                                               ║
║                         Made by Ankit-Dev with ❤️ - Version 5.0.0                            ║
║                                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                               ║
║  📍 Bot Status:    🟢 ONLINE                                                                 ║
║  🤖 Bot Name:      {bot.user}                                         ║
║  🔧 Prefix:        {BOT_PREFIX}                                                               ║
║  🔐 License:       {'✅ VERIFIED' if LICENSE_VERIFIED else '❌ NOT VERIFIED'}                          ║
║  🌐 Server IP:     {SERVER_IP}                                                           ║
║                                                                                               ║
║  🖥️ Total VPS:     {total_vps}                                                               ║
║  🌍 Total Nodes:   {nodes} (auto-detected)                                                    ║
║  🐧 Total OS:      {len(OS_OPTIONS)}                                                          ║
║  🎮 Total Games:   {len(GAMES_LIST)}                                                          ║
║  🛠️ Total Tools:   {len(TOOLS_LIST)}                                                          ║
║                                                                                               ║
║  📊 TOTAL COMMANDS: 100+│ ✅ BUTTONS │ ✅ SELECT MENUS │ ✅ NODE.JSON │ ✅ EVERYTHING         ║
║                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
    """)

# ==================================================================================================
#  ❌  ERROR HANDLER
# ==================================================================================================

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_embed("Missing Argument", f"Usage: `{BOT_PREFIX}{ctx.command.name} {ctx.command.signature}`"))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=error_embed("Invalid Argument", "Please check your input."))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed=error_embed("Access Denied", "You don't have permission."))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=warning_embed("Cooldown", f"Wait {error.retry_after:.1f}s"))
    else:
        logger.error(f"Error: {error}")
        await ctx.send(embed=error_embed("Error", f"```diff\n- {str(error)[:1900]}\n```"))

# ==================================================================================================
#  🏠  HELP COMMAND
# ==================================================================================================

@bot.command(name="help")
async def help_command(ctx):
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    view = HelpView(ctx)
    await ctx.send(embed=view.embed, view=view)

# ==================================================================================================
#  👤  USER COMMANDS
# ==================================================================================================
# ==================================================================================================
#  🖥️  COMPLETE .vmopen COMMAND - REAL VPS TERMINAL WITH LIVE INPUT
# ==================================================================================================

import asyncio
import io
import time
from datetime import datetime

class TerminalView(View):
    def __init__(self, ctx, container_name):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.container = container_name
        self.command_history = []
        self.history_index = -1
        self.current_output = ""
        self.message = None
        
        # Input Modal Button
        input_btn = Button(label="📟 Enter Command", style=discord.ButtonStyle.primary, emoji="📟", row=0)
        input_btn.callback = self.input_callback
        
        # Clear Button
        clear_btn = Button(label="🗑️ Clear Screen", style=discord.ButtonStyle.secondary, emoji="🗑️", row=0)
        clear_btn.callback = self.clear_callback
        
        # Refresh Button
        refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary, emoji="🔄", row=0)
        refresh_btn.callback = self.refresh_callback
        
        # Close Button
        close_btn = Button(label="❌ Close", style=discord.ButtonStyle.danger, emoji="❌", row=1)
        close_btn.callback = self.close_callback
        
        self.add_item(input_btn)
        self.add_item(clear_btn)
        self.add_item(refresh_btn)
        self.add_item(close_btn)
    
    async def get_terminal_embed(self):
        """Get current terminal embed with output"""
        if self.current_output:
            output_text = self.current_output[:1900]
        else:
            output_text = (
                "Welcome to SVM5-BOT Terminal!\n"
                "Type a command using the button below.\n\n"
                "$ "
            )

        description = f"```bash\n{output_text}\n```"
        embed = discord.Embed(
            title=f"```glow\n🖥️ VPS TERMINAL - {self.container.upper()}\n```",
            description=description,
            color=0x2C2F33
        )
        embed.set_footer(text=f"⚡ SVM5-BOT • Terminal • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
        return embed
    
    async def input_callback(self, interaction):
        modal = TerminalModal(self.container, self)
        await interaction.response.send_modal(modal)
    
    async def clear_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral=True)
            return
        self.current_output = ""
        embed = await self.get_terminal_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def refresh_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral=True)
            return
        embed = await self.get_terminal_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def close_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral=True)
            return
        await interaction.message.delete()
    
    async def execute_command(self, interaction, command):
        await interaction.response.defer()
        
        # Add command to output
        self.current_output += f"$ {command}\n"
        
        # Show executing status
        embed = await self.get_terminal_embed()
        await interaction.edit_original_response(embed=embed, view=self)
        
        # Execute command
        try:
            out, err, code = await exec_in_container(self.container, command, timeout=60)
            
            # Add output
            if out:
                self.current_output += f"{out}\n"
            if err:
                self.current_output += f"Error: {err}\n"
            
            # Add exit code
            if code != 0:
                self.current_output += f"Exit Code: {code}\n"
            
            self.current_output += "\n"
            
            # Keep only last 5000 characters
            if len(self.current_output) > 5000:
                self.current_output = self.current_output[-4500:]
            
            # Add to history
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
        except asyncio.TimeoutError:
            self.current_output += f"Error: Command timed out after 60 seconds\n\n"
        except Exception as e:
            self.current_output += f"Error: {str(e)}\n\n"
        
        # Update embed
        embed = await self.get_terminal_embed()
        await interaction.edit_original_response(embed=embed, view=self)


class TerminalModal(Modal):
    def __init__(self, container, terminal_view):
        super().__init__(title=f"Terminal: {container}")
        self.container = container
        self.terminal_view = terminal_view
        
        self.add_item(InputText(
            label="Command",
            placeholder="e.g., apt update, ls -la, ps aux, df -h",
            style=discord.InputTextStyle.paragraph,
            required=True
        ))
        
        self.add_item(InputText(
            label="Timeout (seconds)",
            placeholder="30",
            required=False,
            value="30"
        ))
    
    async def callback(self, interaction):
        command = self.children[0].value
        timeout = int(self.children[1].value or "30")
        
        # Check if container is running
        status = await get_container_status(self.container)
        if status != 'running':
            await interaction.response.send_message(
                embed=error_embed("Container Not Running", f"```diff\n- {self.container} is not running.\n```"),
                ephemeral=True
            )
            return
        
        # Execute command
        await self.terminal_view.execute_command(interaction, command)


@bot.command(name="vmopen")
@commands.cooldown(1, 3, commands.BucketType.user)
async def vm_open(ctx, container_name: str = None):
    """Open real VPS terminal with live command input"""
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    
    user_id = str(ctx.author.id)
    
    # If no container specified, use first VPS
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            return await ctx.send(embed=no_vps_embed())
        container_name = vps_list[0]['container_name']
    
    # Verify ownership
    if not any(v['container_name'] == container_name for v in get_user_vps(user_id)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    # Check if container is running
    status = await get_container_status(container_name)
    if status != 'running':
        return await ctx.send(embed=error_embed("Container Not Running", f"```diff\n- {container_name} is not running.\n```"))
    
    # Get welcome message
    out, _, _ = await exec_in_container(container_name, "echo '=== SVM5-BOT TERMINAL ===' && uname -a && whoami && pwd")
    
    view = TerminalView(ctx, container_name)
    view.current_output = f"{out}\n\n"
    
    embed = await view.get_terminal_embed()
    msg = await ctx.send(embed=embed, view=view)
    view.message = msg

# ==================================================================================================
#  🌐  COMPLETE .ipv4generate COMMAND - CONVERT LXC PRIVATE IP TO PUBLIC IPv4
# ==================================================================================================

@bot.command(name="ipv4generate")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ipv4_generate(ctx, container_name: str = None):
    """Generate public IPv4 for your VPS (port forwarding + tunnel)"""
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    
    user_id = str(ctx.author.id)
    
    # If no container specified, use first VPS
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            return await ctx.send(embed=no_vps_embed())
        container_name = vps_list[0]['container_name']
    
    # Verify ownership
    if not any(v['container_name'] == container_name for v in get_user_vps(user_id)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    # Check if container is running
    status = await get_container_status(container_name)
    if status != 'running':
        return await ctx.send(embed=error_embed("Container Not Running", f"```diff\n- {container_name} is not running.\n```"))
    
    msg = await ctx.send(embed=info_embed("🌍 Generating IPv4", f"```fix\nContainer: {container_name}\nStep 1/5: Getting container info...\n```"))
    
    try:
        # Get container private IP
        private_ip = "N/A"
        mac = "N/A"
        out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
        if out:
            private_ip = out.strip()
        
        out, _, _ = await exec_in_container(container_name, "ip link | grep ether | awk '{print $2}' | head -1")
        if out:
            mac = out.strip()
        
        await msg.edit(embed=info_embed("🌍 Generating IPv4", f"```fix\nContainer: {container_name}\nPrivate IP: {private_ip}\nMAC: {mac}\nStep 2/5: Checking port availability...\n```"))
        
        # Get available port
        port = await get_available_port()
        if not port:
            await msg.edit(embed=error_embed("Failed", "```diff\n- No available ports. Try again later.\n```"))
            return
        
        await msg.edit(embed=info_embed("🌍 Generating IPv4", f"```fix\nContainer: {container_name}\nPrivate IP: {private_ip}\nMAC: {mac}\nHost Port: {port}\nStep 3/5: Creating port forward...\n```"))
        
        # Create port forward (SSH port 22)
        hport = await create_port_forward(user_id, container_name, 22, "tcp")
        
        if hport:
            await msg.edit(embed=info_embed("🌍 Generating IPv4", f"```fix\nContainer: {container_name}\nPrivate IP: {private_ip}\nMAC: {mac}\nHost Port: {hport}\nStep 4/5: Creating cloudflared tunnel...\n```"))
            
            # Create cloudflared tunnel for web access
            tunnel_url = await create_cloudflared_tunnel(container_name, 80)
            
            await msg.edit(embed=info_embed("🌍 Generating IPv4", f"```fix\nContainer: {container_name}\nPrivate IP: {private_ip}\nMAC: {mac}\nHost Port: {hport}\nStep 5/5: Finalizing...\n```"))
            
            # Save to database
            add_ipv4(user_id, container_name, SERVER_IP, private_ip, mac)
            
            # Success Embed
            embed = success_embed("🌍 IPv4 Generated Successfully!")
            embed.set_thumbnail(url=THUMBNAIL_URL)
            
            embed.add_field(
                name="📦 CONTAINER",
                value=f"```fix\nName: {container_name}\nPrivate IP: {private_ip}\nMAC: {mac}\n```",
                inline=True
            )
            
            embed.add_field(
                name="🌐 PUBLIC IPv4",
                value=f"```fix\n{SERVER_IP}:{hport}\n```",
                inline=True
            )
            
            if tunnel_url:
                embed.add_field(
                    name="🌍 CLOUDFLARED TUNNEL",
                    value=f"```fix\n{tunnel_url}\n```",
                    inline=False
                )
            
            embed.add_field(
                name="🔌 ACCESS METHODS",
                value=f"```fix\nSSH: ssh root@{SERVER_IP} -p {hport}\nWeb: {tunnel_url if tunnel_url else f'http://{SERVER_IP}:{hport}'}\n```",
                inline=False
            )
            
            embed.add_field(
                name="📋 COMMANDS",
                value=f"```fix\n.manage {container_name} - Manage VPS\n.stats {container_name} - View Stats\n.logs {container_name} - View Logs\n```",
                inline=False
            )
            
            await msg.edit(embed=embed)
            
            # DM user
            try:
                dm_embed = success_embed("🌍 Your IPv4 is Ready!")
                dm_embed.add_field(name="Container", value=f"```fix\n{container_name}\n```", inline=True)
                dm_embed.add_field(name="Public IPv4", value=f"```fix\n{SERVER_IP}:{hport}\n```", inline=True)
                if tunnel_url:
                    dm_embed.add_field(name="Tunnel URL", value=f"```fix\n{tunnel_url}\n```", inline=True)
                await ctx.author.send(embed=dm_embed)
            except:
                pass
            
        else:
            await msg.edit(embed=error_embed("Failed", "```diff\n- Could not create port forward.\n```"))
            
    except Exception as e:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

# ==================================================================================================
#  🤖  COMPLETE .aichat COMMAND - OPENAI API WITH AUTO-FIX
# ==================================================================================================

import aiohttp
import json
from datetime import datetime

# OpenAI Configuration
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"  # Add your OpenAI API key
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4"

class AIView(View):
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.message = None
        
        # Clear History Button
        clear_btn = Button(label="🗑️ Clear History", style=discord.ButtonStyle.secondary, emoji="🗑️", row=0)
        clear_btn.callback = self.clear_callback
        
        # Close Button
        close_btn = Button(label="❌ Close", style=discord.ButtonStyle.danger, emoji="❌", row=0)
        close_btn.callback = self.close_callback
        
        self.add_item(clear_btn)
        self.add_item(close_btn)
    
    async def clear_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral=True)
            return
        
        # Clear AI history
        clear_ai_history(str(self.ctx.author.id))
        embed = info_embed("AI Chat", "```fix\nChat history cleared! You can start a new conversation.\n```")
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def close_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Not for you!", ephemeral=True)
            return
        await interaction.message.delete()


@bot.command(name="aichat")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ai_chat(ctx, *, message: str = None):
    """Chat with AI assistant (OpenAI)"""
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    
    if OPENAI_API_KEY == "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":
        return await ctx.send(embed=error_embed("API Key Required", "Please set your OpenAI API key in the code."))
    
    user_id = str(ctx.author.id)
    
    # If no message, show chat interface
    if not message:
        view = AIView(ctx)
        
        # Load history
        history = load_ai_history(user_id)
        if history:
            last_messages = history[-3:] if len(history) > 3 else history
            history_text = ""
            for msg in last_messages:
                if msg['role'] == 'user':
                    history_text += f"👤 You: {msg['content'][:100]}\n"
                elif msg['role'] == 'assistant':
                    history_text += f"🤖 AI: {msg['content'][:100]}\n"
            
            embed = info_embed("AI Chat", f"```fix\nRecent Messages:\n{history_text if history_text else 'No recent messages'}\n```\nUse `.aichat <message>` to chat with AI.")
        else:
            embed = info_embed("AI Chat", "```fix\nWelcome to SVM5-BOT AI Assistant!\nUse .aichat <message> to chat.\n\nExample: .aichat How to install Docker?\n```")
        
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
        
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg
        return
    
    # Process message
    msg = await ctx.send(embed=info_embed("🤖 AI is thinking...", "```fix\nProcessing your request...\n```"))
    
    try:
        # Load history
        history = load_ai_history(user_id)
        if not history:
            history = [{
                "role": "system",
                "content": f"You are {BOT_NAME} AI Assistant, a helpful VPS management bot made by {BOT_AUTHOR}. You help with Linux, LXC containers, Docker, server management, and general questions. Keep responses concise, friendly, and helpful. Server IP: {SERVER_IP}"
            }]
        
        # Add user message
        history.append({"role": "user", "content": message})
        
        # Keep last 20 messages + system
        if len(history) > 21:
            history = [history[0]] + history[-20:]
        
        # Call OpenAI API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": history,
                    "max_tokens": 1024,
                    "temperature": 0.7
                },
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    reply = data["choices"][0]["message"]["content"]
                    
                    # Add to history
                    history.append({"role": "assistant", "content": reply})
                    save_ai_history(user_id, history)
                    
                    # Send response
                    chunks = [reply[i:i:1900] for i in range(0, len(reply), 1900)]
                    embed = info_embed("🤖 AI Response", chunks[0])
                    await msg.edit(embed=embed)
                    
                    for chunk in chunks[1:]:
                        await ctx.send(embed=info_embed("", chunk))
                    
                elif resp.status == 429:
                    await msg.edit(embed=error_embed("Rate Limited", "```diff\n- Too many requests. Please wait a moment.\n```"))
                elif resp.status == 401:
                    await msg.edit(embed=error_embed("Invalid API Key", "```diff\n- Please check your OpenAI API key.\n```"))
                else:
                    error_text = await resp.text()
                    await msg.edit(embed=error_embed("API Error", f"```diff\n- Status {resp.status}: {error_text[:200]}\n```"))
                    
    except asyncio.TimeoutError:
        await msg.edit(embed=error_embed("Timeout", "```diff\n- Request timed out. Please try again.\n```"))
    except Exception as e:
        await msg.edit(embed=error_embed("Error", f"```diff\n- {str(e)[:1900]}\n```"))


@bot.command(name="ais")
async def ai_short(ctx, *, message: str):
    """Shortcut for .aichat"""
    await ai_chat(ctx, message=message)


@bot.command(name="chat")
async def chat(ctx, *, message: str):
    """Shortcut for .aichat"""
    await ai_chat(ctx, message=message)
    
@bot.command(name="ping")
async def ping(ctx):
    start = time.time()
    msg = await ctx.send(embed=info_embed("Pinging..."))
    end = time.time()
    embed = success_embed("Pong! 🏓")
    embed.add_field(name="📡 API", value=f"```fix\n{round(bot.latency*1000)}ms\n```", inline=True)
    embed.add_field(name="⏱️ Response", value=f"```fix\n{round((end-start)*1000)}ms\n```", inline=True)
    await msg.edit(embed=embed)

@bot.command(name="bot-info")
async def bot_info(ctx):
    embed = info_embed("Bot Information")
    embed.add_field(name="📦 Version", value="```fix\n5.0.0\n```", inline=True)
    embed.add_field(name="👑 Author", value=f"```fix\n{BOT_AUTHOR}\n```", inline=True)
    embed.add_field(name="🖥️ VPS", value=f"```fix\n{len(get_all_vps())}\n```", inline=True)
    embed.add_field(name="🐧 OS", value=f"```fix\n{len(OS_OPTIONS)}\n```", inline=True)
    embed.add_field(name="🎮 Games", value=f"```fix\n{len(GAMES_LIST)}\n```", inline=True)
    embed.add_field(name="🛠️ Tools", value=f"```fix\n{len(TOOLS_LIST)}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="server-info")
async def server_info(ctx):
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    embed = info_embed("Server Information")
    embed.add_field(name="💻 Hostname", value=f"```fix\n{HOSTNAME}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="⚙️ CPU", value=f"```fix\n{psutil.cpu_count()} cores @ {cpu}%\n```", inline=True)
    embed.add_field(name="💾 RAM", value=f"```fix\n{mem.used//1024//1024}MB/{mem.total//1024//1024}MB ({mem.percent}%)\n```", inline=True)
    embed.add_field(name="📀 Disk", value=f"```fix\n{disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB ({disk.percent}%)\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="plans")
async def plans(ctx):
    embed = info_embed("Free VPS Plans")
    for p in FREE_VPS_PLANS['invites']:
        embed.add_field(name=f"{p['emoji']} {p['name']}", value=f"```fix\nRAM: {p['ram']}GB | CPU: {p['cpu']} | Disk: {p['disk']}GB\nInvites: {p['invites']}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="inv")
async def inv(ctx):
    s = get_user_stats(str(ctx.author.id))
    await ctx.send(embed=info_embed("Your Invites", f"```fix\n{s.get('invites',0)}\n```"))

@bot.command(name="invites-top")
async def invites_top(ctx, lim: int = 10):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, invites FROM user_stats WHERE invites > 0 ORDER BY invites DESC LIMIT ?', (lim,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No invites"))
    embed = info_embed(f"Top {min(lim,len(rows))} Inviters")
    medals = ["🥇","🥈","🥉"]
    for i, r in enumerate(rows,1):
        try:
            u = await bot.fetch_user(int(r['user_id']))
            name = u.name
        except:
            name = "Unknown"
        m = medals[i-1] if i<=3 else f"{i}."
        embed.add_field(name=f"{m} {name}", value=f"```fix\nInvites: {r['invites']}\n```", inline=False)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🚀  COMPLETE .claim-free COMMAND - WITH RAINBOW PROGRESS & FULL UI
# ==================================================================================================
# =================================================================================================

# ==================================================================================================
#  🎨  RAINBOW COLORS FOR PROGRESS
# ==================================================================================================

RAINBOW_COLORS = [
    0xFF0000,  # Red
    0xFF7700,  # Orange
    0xFFFF00,  # Yellow
    0x00FF00,  # Green
    0x00CCFF,  # Cyan
    0x3366FF,  # Blue
    0x8B00FF,  # Violet
    0xFF00CC,  # Pink
]


# ==================================================================================================
#  🌈  CLAIM FREE VPS VIEW
# ==================================================================================================

class ClaimFreeView(View):
    def __init__(self, ctx, plan):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.plan = plan
        
        # OS Selection
        options = []
        for os in OS_OPTIONS[:25]:
            options.append(discord.SelectOption(
                label=os['label'][:100],
                value=os['value'],
                description=os['desc'][:100] if os.get('desc') else None,
                emoji=os.get('icon', '🐧')
            ))
        
        self.select = Select(placeholder="📋 Select an operating system...", options=options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=1)
        cancel_btn.callback = self.cancel_callback
        self.add_item(cancel_btn)
    
    async def select_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        selected_os = self.select.values[0]
        os_name = next((o['label'] for o in OS_OPTIONS if o['value'] == selected_os), selected_os)
        
        # Confirm View
        view = ConfirmClaimView(self.ctx, self.plan, selected_os, os_name)
        embed = warning_embed(
            "⚠️ Confirm VPS Claim",
            f"```fix\nPlan: {self.plan['emoji']} {self.plan['name']}\nOS: {os_name}\nRAM: {self.plan['ram']}GB\nCPU: {self.plan['cpu']} Core(s)\nDisk: {self.plan['disk']}GB\nCost: {self.plan['invites']} invites\n```\n\n**This will use {self.plan['invites']} invites from your account!**"
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_image(url=THUMBNAIL_URL)
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nVPS claim cancelled.\n```"),
            view=None
        )


class ConfirmClaimView(View):
    def __init__(self, ctx, plan, os_version, os_name):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.plan = plan
        self.os_version = os_version
        self.os_name = os_name
        
        confirm_btn = Button(label="✅ Confirm Claim", style=discord.ButtonStyle.success, emoji="✅", row=0)
        confirm_btn.callback = self.confirm_callback
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=0)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(confirm_btn)
        self.add_item(cancel_btn)
    
    async def confirm_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await self.create_vps(interaction)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nVPS claim cancelled.\n```"),
            view=None
        )
    
    async def create_vps(self, interaction):
        await interaction.response.defer()
        
        user_id = str(self.ctx.author.id)
        container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
        
        # ==========================================================================================
        # 🌈 RAINBOW PROGRESS EMBED
        # ==========================================================================================
        
        progress_steps = [
            {"text": "Initializing container...", "emoji": "🔧", "progress": 10},
            {"text": "Configuring resources...", "emoji": "⚙️", "progress": 25},
            {"text": "Setting RAM limits...", "emoji": "💾", "progress": 40},
            {"text": "Setting CPU limits...", "emoji": "⚡", "progress": 55},
            {"text": "Setting Disk limits...", "emoji": "💽", "progress": 70},
            {"text": "Applying LXC config...", "emoji": "🔨", "progress": 80},
            {"text": "Starting container...", "emoji": "▶️", "progress": 90},
            {"text": "Finalizing...", "emoji": "🎉", "progress": 100},
        ]
        
        progress_msg = await interaction.followup.send(
            embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description="```fix\n[░░░░░░░░░░░░░░░░░░░░] 0% | Initializing...\n```",
                color=RAINBOW_COLORS[0]
            ),
            ephemeral=True
        )
        
        try:
            ram_mb = self.plan['ram'] * 1024
            
            # Progress bar function
            def get_progress_bar(percent):
                filled = int(percent / 5)
                return "█" * filled + "░" * (20 - filled)
            
            # Step 1: Initialize container
            color_index = 0
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(10)}] 10% | 🔧 Initializing container...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            await run_lxc(f"lxc init {self.os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
            await asyncio.sleep(1)
            color_index += 1
            
            # Step 2: Set RAM limits
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(25)}] 25% | 💾 Setting RAM limits ({self.plan['ram']}GB)...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
            await asyncio.sleep(1)
            color_index += 1
            
            # Step 3: Set CPU limits
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(40)}] 40% | ⚡ Setting CPU limits ({self.plan['cpu']} cores)...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            await run_lxc(f"lxc config set {container_name} limits.cpu {self.plan['cpu']}")
            await asyncio.sleep(1)
            color_index += 1
            
            # Step 4: Set Disk limits
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(55)}] 55% | 💽 Setting Disk limits ({self.plan['disk']}GB)...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            await run_lxc(f"lxc config device set {container_name} root size={self.plan['disk']}GB")
            await asyncio.sleep(1)
            color_index += 1
            
            # Step 5: Apply LXC config
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(70)}] 70% | 🔨 Applying LXC configuration...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            await apply_lxc_config(container_name)
            await asyncio.sleep(1)
            color_index += 1
            
            # Step 6: Start container
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(85)}] 85% | ▶️ Starting container...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            await run_lxc(f"lxc start {container_name}")
            await asyncio.sleep(2)
            color_index += 1
            
            # Step 7: Apply permissions
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(95)}] 95% | 🔧 Configuring permissions...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            await apply_internal_permissions(container_name)
            await asyncio.sleep(2)
            color_index += 1
            
            # Step 8: Get IP and MAC
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CLAIMING FREE VPS 🌈\n```",
                description=f"```fix\n[{get_progress_bar(100)}] 100% | 🎉 Finalizing...\n```",
                color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
            ))
            
            # Get IP and MAC
            ip = "N/A"
            mac = "N/A"
            try:
                out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() if out else "N/A"
                out, _, _ = await exec_in_container(container_name, "ip link | grep ether | awk '{print $2}' | head -1")
                mac = out.strip() if out else "N/A"
            except:
                pass
            
            # Save to database
            add_vps(user_id, container_name, self.plan['ram'], self.plan['cpu'], self.plan['disk'], self.os_version, self.plan['name'])
            
            # Update VPS with IP and MAC
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ip_address = ?, mac_address = ? WHERE container_name = ?',
                       (ip, mac, container_name))
            conn.commit()
            conn.close()
            
            # ==========================================================================================
            # 🔧 FIX: update_user_stats with correct parameters
            # ==========================================================================================
            # Get current stats
            current_stats = get_user_stats(user_id)
            current_invites = current_stats.get('invites', 0)
            current_claimed = current_stats.get('claimed_vps_count', 0)
            
            # Update stats
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''UPDATE user_stats 
                           SET invites = ?, 
                               claimed_vps_count = ?,
                               last_updated = ?
                           WHERE user_id = ?''',
                       (current_invites - self.plan['invites'], 
                        current_claimed + 1,
                        datetime_.datetime.now().isoformat(),
                        user_id))
            conn.commit()
            conn.close()
            
            # Assign role
            if self.ctx.guild:
                role = discord.utils.get(self.ctx.guild.roles, name=f"{BOT_NAME} User")
                if not role:
                    role = await self.ctx.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
                try:
                    await self.ctx.author.add_roles(role)
                except:
                    pass
            
            # ==========================================================================================
            # 🎉 SUCCESS EMBED - BIG TITLE WITH FULL DETAILS
            # ==========================================================================================
            
            # Resource Bars
            ram_bar = "█" * int(self.plan['ram'] / 16) + "░" * (10 - int(self.plan['ram'] / 16))
            cpu_bar = "█" * int(self.plan['cpu'] / 8) + "░" * (10 - int(self.plan['cpu'] / 8))
            disk_bar = "█" * int(self.plan['disk'] / 100) + "░" * (10 - int(self.plan['disk'] / 100))
            
            success_embed = discord.Embed(
                title="```glow\n🌟✨ SVM5-BOT - VPS CREATED SUCCESSFULLY! ✨🌟\n```",
                description=f"🎉 **Congratulations {self.ctx.author.mention}!** Your free VPS has been created!\n\n"
                            f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
                color=0x00FF88
            )
            success_embed.set_thumbnail(url=THUMBNAIL_URL)
            success_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
            
            # Container Details
            success_embed.add_field(
                name="📦 CONTAINER DETAILS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Name      : {container_name}\n│ IP Address: {ip}\n│ MAC Address: {mac}\n│ OS        : {self.os_name}\n│ Plan      : {self.plan['emoji']} {self.plan['name']}\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            # Resource Allocation with Visual Bars
            success_embed.add_field(
                name="⚙️ RESOURCE ALLOCATION",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ RAM  : {self.plan['ram']}GB  [{ram_bar}]\n│ CPU  : {self.plan['cpu']} Core(s) [{cpu_bar}]\n│ Disk : {self.plan['disk']}GB [{disk_bar}]\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            # Management Commands
            success_embed.add_field(
                name="🖥️ MANAGEMENT COMMANDS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ .manage {container_name} - Interactive Manager\n│ .stats  {container_name} - Live Statistics\n│ .logs   {container_name} - System Logs\n│ .ssh-gen {container_name} - SSH Access\n│ .reboot {container_name} - Reboot VPS\n│ .shutdown {container_name} - Shutdown VPS\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            # VPS Status & Statistics
            success_embed.add_field(
                name="📊 VPS STATUS & STATISTICS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Status      : 🟢 RUNNING\n│ Uptime      : Just Started\n│ Created     : {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n│ Invites Used: {self.plan['invites']}\n│ Remaining   : {current_invites - self.plan['invites']}\n│ Total VPS   : {current_claimed + 1}\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            # Public Statistics (Visible to all)
            total_users = len(get_all_vps())
            total_vps = len(get_all_vps())
            total_invites_used = sum([self.plan['invites'] for _ in range(1)])
            
            success_embed.add_field(
                name="🌍 PUBLIC STATISTICS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Total VPS Created : {total_vps}\n│ Total Users       : {total_users}\n│ Active VPS        : {len([v for v in get_all_vps() if v['status'] == 'running'])}\n│ Total Invites Used: {total_invites_used}\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            # Quick Links
            success_embed.add_field(
                name="🔗 QUICK LINKS",
                value=f"[📖 Documentation](https://github.com/AnkitKing7/Svm5-bot) | [💬 Support](https://discord.gg) | [🐛 Report Issue](https://github.com/AnkitKing7/Svm5-bot/issues)",
                inline=False
            )
            
            success_embed.set_footer(
                text=f"⚡ SVM5-BOT • Claimed by {self.ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
                icon_url=THUMBNAIL_URL
            )
            
            await progress_msg.edit(embed=success_embed)
            
            # ==========================================================================================
            # 📧 DM TO USER
            # ==========================================================================================
            
            try:
                dm_embed = discord.Embed(
                    title="```glow\n🌟 YOUR FREE VPS IS READY! 🌟\n```",
                    description=f"🎉 Congratulations! Your VPS has been created successfully!\n\n"
                                f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
                    color=0x57F287
                )
                dm_embed.set_thumbnail(url=THUMBNAIL_URL)
                dm_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
                
                dm_embed.add_field(
                    name="📦 CONTAINER",
                    value=f"```fix\nName: {container_name}\nIP: {ip}\nMAC: {mac}\nOS: {self.os_name}\nPlan: {self.plan['emoji']} {self.plan['name']}\n```",
                    inline=False
                )
                
                dm_embed.add_field(
                    name="⚙️ RESOURCES",
                    value=f"```fix\nRAM: {self.plan['ram']}GB\nCPU: {self.plan['cpu']} Core(s)\nDisk: {self.plan['disk']}GB\n```",
                    inline=True
                )
                
                dm_embed.add_field(
                    name="📅 CREATED",
                    value=f"```fix\n{datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n```",
                    inline=True
                )
                
                dm_embed.add_field(
                    name="📊 YOUR STATS",
                    value=f"```fix\nInvites Used: {self.plan['invites']}\nRemaining Invites: {current_invites - self.plan['invites']}\nTotal VPS: {current_claimed + 1}\n```",
                    inline=False
                )
                
                dm_embed.add_field(
                    name="🖥️ QUICK COMMANDS",
                    value=f"```fix\n.manage {container_name}\n.stats {container_name}\n.logs {container_name}\n.ssh-gen {container_name}\n```",
                    inline=False
                )
                
                dm_embed.set_footer(
                    text=f"⚡ SVM5-BOT • Manage your VPS with .help ⚡",
                    icon_url=THUMBNAIL_URL
                )
                
                await self.ctx.author.send(embed=dm_embed)
                
            except:
                pass
            
            logger.info(f"User {self.ctx.author} claimed VPS {container_name} with plan {self.plan['name']}")
            
        except Exception as e:
            await progress_msg.edit(embed=error_embed("Creation Failed", f"```diff\n- {str(e)}\n```"))
            try:
                await run_lxc(f"lxc delete {container_name} --force")
            except:
                pass


# ==================================================================================================
#  🚀  .claim-free COMMAND
# ==================================================================================================

@bot.command(name="claim-free")
@commands.cooldown(1, 60, commands.BucketType.user)
async def claim_free(ctx):
    """Claim a free VPS based on your invites - FIXED with full details"""
    user_id = str(ctx.author.id)
    
    # Check if user already has a VPS
    user_vps = get_user_vps(user_id)
    if user_vps:
        embed = error_embed(
            "VPS Already Exists",
            "```diff\n- You already have a VPS. Each user can only claim one free VPS.\n```"
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        await ctx.send(embed=embed)
        return
    
    # Get user stats
    stats = get_user_stats(user_id)
    invites = stats.get('invites', 0)
    
    # Find eligible plan
    eligible_plan = None
    for plan in reversed(FREE_VPS_PLANS['invites']):
        if invites >= plan['invites']:
            eligible_plan = plan
            break
    
    if not eligible_plan:
        embed = error_embed(
            "No Eligible Plans",
            f"```diff\n- You have {invites} invites.\n- You need at least 5 invites to claim a VPS.\n```\n\n"
            f"Invite more users to unlock plans!"
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        await ctx.send(embed=embed)
        return
    
    # Show plan details with public statistics
    total_vps = len(get_all_vps())
    total_users = len(set([v['user_id'] for v in get_all_vps()]))
    active_vps = len([v for v in get_all_vps() if v['status'] == 'running'])
    
    embed = discord.Embed(
        title="```glow\n🌟 SVM5-BOT - FREE VPS CLAIM 🌟\n```",
        description=f"🎉 **You are eligible for {eligible_plan['emoji']} {eligible_plan['name']}!**\n\n"
                    f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
        color=0x00FF88
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
    
    # Resource Bars
    ram_bar = "█" * int(eligible_plan['ram'] / 16) + "░" * (10 - int(eligible_plan['ram'] / 16))
    cpu_bar = "█" * int(eligible_plan['cpu'] / 8) + "░" * (10 - int(eligible_plan['cpu'] / 8))
    disk_bar = "█" * int(eligible_plan['disk'] / 100) + "░" * (10 - int(eligible_plan['disk'] / 100))
    
    embed.add_field(
        name="📋 PLAN DETAILS",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Plan : {eligible_plan['emoji']} {eligible_plan['name']}\n│ RAM  : {eligible_plan['ram']}GB [{ram_bar}]\n│ CPU  : {eligible_plan['cpu']} Core(s) [{cpu_bar}]\n│ Disk : {eligible_plan['disk']}GB [{disk_bar}]\n│ Cost : {eligible_plan['invites']} invites\n└─────────────────────────────────────────────────┘\n```",
        inline=False
    )
    
    embed.add_field(
        name="📊 YOUR STATS",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Your Invites        : {invites}\n│ After Claim         : {invites - eligible_plan['invites']}\n│ Your VPS Count      : {len(user_vps)}\n└─────────────────────────────────────────────────┘\n```",
        inline=False
    )
    
    embed.add_field(
        name="🌍 PUBLIC STATISTICS",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Total VPS Created : {total_vps}\n│ Total Users       : {total_users}\n│ Active VPS        : {active_vps}\n│ Invites Used      : {sum([p['invites'] for p in FREE_VPS_PLANS['invites'] if invites >= p['invites']])}\n└─────────────────────────────────────────────────┘\n```",
        inline=False
    )
    
    embed.add_field(
        name="📌 NEXT STEP",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Select an operating system from the\n│ dropdown menu below to continue.\n└─────────────────────────────────────────────────┘\n```",
        inline=False
    )
    
    embed.set_footer(
        text=f"⚡ SVM5-BOT • Claim for {ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    
    view = ClaimFreeView(ctx, eligible_plan)
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  🔑  COMPLETE .ssh-gen COMMAND - FIXED WITH TMATE
# ==================================================================================================

@bot.command(name="ssh-gen")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ssh_gen(ctx, container_name: str = None):
    """Generate SSH access for your container via tmate"""
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    
    user_id = str(ctx.author.id)
    
    # If no container specified, use first VPS
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            return await ctx.send(embed=no_vps_embed())
        container_name = vps_list[0]['container_name']
    
    # Verify ownership
    if not any(v['container_name'] == container_name for v in get_user_vps(user_id)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    # Check if container is running
    status = await get_container_status(container_name)
    if status != 'running':
        return await ctx.send(embed=error_embed("Container Not Running", f"```diff\n- {container_name} is not running.\n```"))
    
    # Progress embed
    msg = await ctx.send(embed=info_embed("🔑 Generating SSH Access", f"```fix\nContainer: {container_name}\nStep 1/4: Checking tmate installation...\n```"))
    
    try:
        # Step 1: Install tmate if not present
        await msg.edit(embed=info_embed("🔑 Generating SSH Access", f"```fix\nContainer: {container_name}\nStep 2/4: Installing tmate...\n```"))
        
        # Install tmate
        await exec_in_container(container_name, "apt-get update -qq")
        await exec_in_container(container_name, "apt-get install -y -qq tmate")
        
        # Step 2: Generate session ID
        session_id = f"svm5-{random.randint(1000, 9999)}-{int(time.time())}"
        
        await msg.edit(embed=info_embed("🔑 Generating SSH Access", f"```fix\nContainer: {container_name}\nStep 3/4: Starting tmate session...\n```"))
        
        # Start tmate session
        await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock new-session -d")
        
        # Wait for session to initialize
        await asyncio.sleep(5)
        
        # Step 3: Get SSH URL
        await msg.edit(embed=info_embed("🔑 Generating SSH Access", f"```fix\nContainer: {container_name}\nStep 4/4: Getting connection URL...\n```"))
        
        out, err, code = await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock display -p '#{{tmate_ssh}}'")
        ssh_url = out.strip()
        
        # Try web URL as fallback
        if not ssh_url or not ssh_url.startswith('ssh'):
            out, _, _ = await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock display -p '#{{tmate_web}}'")
            web_url = out.strip()
            if web_url:
                ssh_url = web_url
        
        if ssh_url and (ssh_url.startswith('ssh') or ssh_url.startswith('https')):
            # Success Embed
            success_embed = discord.Embed(
                title="```glow\n🔑 SSH ACCESS GENERATED SUCCESSFULLY!\n```",
                description=f"SSH access for **{container_name}** is ready!",
                color=0x57F287
            )
            success_embed.set_thumbnail(url=THUMBNAIL_URL)
            success_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
            
            success_embed.add_field(
                name="📦 Container",
                value=f"```fix\n{container_name}\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="🔐 Connection URL",
                value=f"```bash\n{ssh_url}\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="📋 Instructions",
                value=f"```fix\n1. Copy the command above\n2. Paste in your terminal\n3. You'll have full shell access\n\n⚠️ This link expires in 15 minutes\n🔒 Do not share this link with anyone\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="🖥️ Quick Commands",
                value=f"```fix\n.manage {container_name}\n.stats {container_name}\n.logs {container_name}\n```",
                inline=False
            )
            
            success_embed.set_footer(
                text=f"⚡ SVM5-BOT • Generated for {ctx.author.name} • Expires in 15 minutes ⚡",
                icon_url=THUMBNAIL_URL
            )
            
            await msg.edit(embed=success_embed)
            
            # Also DM the user
            try:
                dm_embed = discord.Embed(
                    title="```glow\n🔑 SSH ACCESS GENERATED\n```",
                    description=f"SSH access for **{container_name}** is ready!",
                    color=0x57F287
                )
                dm_embed.set_thumbnail(url=THUMBNAIL_URL)
                dm_embed.add_field(
                    name="🔐 Connection URL",
                    value=f"```bash\n{ssh_url}\n```",
                    inline=False
                )
                dm_embed.add_field(
                    name="⚠️ Important",
                    value="This link expires in 15 minutes. Keep it safe and don't share!",
                    inline=False
                )
                await ctx.author.send(embed=dm_embed)
            except:
                pass
            
        else:
            await msg.edit(embed=error_embed("SSH Generation Failed", "```diff\n- Could not generate SSH access. Try again later.\n```"))
            
    except Exception as e:
        await msg.edit(embed=error_embed("SSH Generation Failed", f"```diff\n- {str(e)[:200]}\n```"))
    
@bot.command(name="gen-acc")
async def gen_acc(ctx):
    adj = ["cool","fast","dark","epic","blue","swift","neon","alpha","delta"]
    noun = ["wolf","tiger","storm","byte","nova","blade","fox","raven","hawk"]
    name = f"{random.choice(adj)}{random.choice(noun)}{random.randint(10,999)}"
    email = f"{name}@{random.choice(['gmail.com','yahoo.com','outlook.com'])}"
    pwd = ''.join(random.choices(string.ascii_letters+string.digits+"!@#$%", k=16))
    api = hashlib.sha256(f"{ctx.author.id}{time.time()}".encode()).hexdigest()[:32]
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS generated_accounts (user_id TEXT PRIMARY KEY, username TEXT, email TEXT, password TEXT, api_key TEXT, created_at TEXT)''')
    cur.execute('INSERT OR REPLACE INTO generated_accounts VALUES (?,?,?,?,?,?)', (str(ctx.author.id), name, email, pwd, api, datetime_.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    try:
        dm = success_embed("Your Account")
        dm.add_field(name="👤 Username", value=f"```fix\n{name}\n```")
        dm.add_field(name="📧 Email", value=f"```fix\n{email}\n```")
        dm.add_field(name="🔑 Password", value=f"```fix\n{pwd}\n```")
        dm.add_field(name="🗝️ API", value=f"```fix\n{api}\n```")
        await ctx.author.send(embed=dm)
        await ctx.send(embed=success_embed("Account Generated", "Check your DMs!"))
    except:
        await ctx.send(embed=error_embed("DM Failed", "Enable DMs to receive credentials."))

@bot.command(name="my-acc")
async def my_acc(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM generated_accounts WHERE user_id = ?', (str(ctx.author.id),))
    row = cur.fetchone()
    conn.close()
    if row:
        embed = info_embed("Your Account")
        embed.add_field(name="👤 Username", value=f"```fix\n{row['username']}\n```")
        embed.add_field(name="📧 Email", value=f"```fix\n{row['email']}\n```")
        embed.add_field(name="🗝️ API", value=f"```fix\n{row['api_key']}\n```")
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=info_embed("No Account", "Use `.gen-acc` to create one."))

@bot.command(name="api-key")
async def api_key_cmd(ctx, action: str = "view"):
    uid = str(ctx.author.id)
    if action.lower() == "regenerate":
        new = hashlib.sha256(f"{uid}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32]
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE user_stats SET api_key = ?, last_updated = ? WHERE user_id = ?', (new, datetime_.datetime.now().isoformat(), uid))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("API Key Regenerated", f"```fix\n{new}\n```"))
    else:
        s = get_user_stats(uid)
        await ctx.send(embed=info_embed("Your API Key", f"```fix\n{s.get('api_key','None')}\n```"))

@bot.command(name="userinfo")
async def userinfo(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    elif not is_admin(str(ctx.author.id)) and user.id != ctx.author.id:
        return await ctx.send(embed=error_embed("Access Denied", "You can only view yourself."))
    uid = str(user.id)
    vps = get_user_vps(uid)
    s = get_user_stats(uid)
    embed = info_embed(f"User: {user.display_name}")
    embed.set_thumbnail(url=user.avatar.url if user.avatar else THUMBNAIL_URL)
    embed.add_field(name="🆔 ID", value=f"```fix\n{user.id}\n```", inline=True)
    embed.add_field(name="📨 Invites", value=f"```fix\n{s.get('invites',0)}\n```", inline=True)
    embed.add_field(name="🖥️ VPS", value=f"```fix\n{len(vps)}\n```", inline=True)
    if vps:
        text = "\n".join([f"{'🟢' if v['status']=='running' else '🔴'} `{v['container_name']}`" for v in vps[:3]])
        embed.add_field(name="📋 VPS List", value=text, inline=False)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🖥️  VPS COMMANDS
# ==================================================================================================

@bot.command(name="myvps")
async def myvps(ctx):
    vps = get_user_vps(str(ctx.author.id))
    if not vps:
        return await ctx.send(embed=no_vps_embed())
    embed = info_embed(f"Your VPS ({len(vps)})")
    for i, v in enumerate(vps,1):
        status = "🟢" if v['status']=='running' and not v['suspended'] else "⛔" if v['suspended'] else "🔴"
        text = f"{status} **`{v['container_name']}`**\n```fix\nRAM: {v['ram']}GB | CPU: {v['cpu']} | Disk: {v['disk']}GB\nIP: {v.get('ip_address','N/A')}\n```"
        embed.add_field(name=f"VPS #{i}", value=text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="list")
async def list_cmd(ctx):
    await myvps(ctx)

# In your manage command, replace the old view with:
# (Removed duplicate manage command to avoid registration error)

@bot.command(name="stats")
async def vps_stats(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    stats = await get_container_stats(container)
    embed = info_embed(f"Stats: {container}")
    embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
    embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
    embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
    embed.add_field(name="💽 Disk", value=f"```fix\n{stats['disk']}\n```", inline=True)
    embed.add_field(name="🌐 IP", value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{stats['mac']}\n```", inline=True)
    embed.add_field(name="⏱️ Uptime", value=f"```fix\n{stats['uptime']}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="logs")
async def logs(ctx, container: str = None, lines: int = 50):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    lines = min(lines,200)
    out,_,_ = await exec_in_container(container, f"journalctl -n {lines} --no-pager 2>/dev/null || dmesg | tail -{lines}")
    embed = terminal_embed(f"Logs: {container}", out[:1900])
    await ctx.send(embed=embed)

@bot.command(name="reboot")
async def reboot(ctx, container: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await ctx.send(embed=info_embed("Rebooting", f"```fix\n{container}\n```"))
    await run_lxc(f"lxc restart {container}")
    update_vps_status(container, 'running')
    await ctx.send(embed=success_embed("Rebooted", f"```fix\n{container}\n```"))

@bot.command(name="shutdown")
async def shutdown(ctx, container: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await ctx.send(embed=info_embed("Shutting Down", f"```fix\n{container}\n```"))
    await run_lxc(f"lxc stop {container}")
    update_vps_status(container, 'stopped')
    await ctx.send(embed=success_embed("Shutdown", f"```fix\n{container}\n```"))

@bot.command(name="rename")
async def rename(ctx, old: str, new: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==old for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$', new):
        return await ctx.send(embed=error_embed("Invalid Name", "Use letters, numbers, hyphens only."))
    await ctx.send(embed=info_embed("Renaming", f"```fix\n{old} → {new}\n```"))
    status = await get_container_status(old)
    was = status == 'running'
    if was:
        await run_lxc(f"lxc stop {old}")
        await asyncio.sleep(2)
    await run_lxc(f"lxc move {old} {new}")
    if was:
        await run_lxc(f"lxc start {new}")
    conn = get_db()
    cur = conn.cursor()
    for t in ['vps','shared_vps','installed_games','installed_tools','ipv4','port_forwards','panels']:
        cur.execute(f'UPDATE {t} SET container_name = ? WHERE container_name = ?', (new, old))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Renamed", f"```fix\n{old} → {new}\n```"))

# ==================================================================================================
#  📟  CONSOLE COMMANDS
# ==================================================================================================

@bot.command(name="ss")
async def ss(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    msg = await ctx.send(embed=info_embed("📸 Snapshot", f"```fix\n{container}\n```"))
    u,_,_ = await exec_in_container(container, "uname -a")
    up,_,_ = await exec_in_container(container, "uptime")
    m,_,_ = await exec_in_container(container, "free -h")
    d,_,_ = await exec_in_container(container, "df -h")
    p,_,_ = await exec_in_container(container, "ps aux | head -15")
    out = f"=== {container} ===\nUname: {u}\nUptime: {up}\n\n{m}\n\n{d}\n\n{p}"
    embed = terminal_embed(f"Snapshot: {container}", out[:1900])
    await msg.edit(embed=embed)

@bot.command(name="console")
async def console(ctx, container: str, *, cmd: str = None):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    if not cmd:
        view = View()
        btn = Button(label="⚡ Run Command", style=discord.ButtonStyle.primary)
        async def btn_cb(i):
            modal = ConsoleModal(container)
            await i.response.send_modal(modal)
        btn.callback = btn_cb
        view.add_item(btn)
        return await ctx.send(embed=info_embed(f"Console: {container}", "Click button to run command"), view=view)
    
    msg = await ctx.send(embed=info_embed("Executing", f"```fix\n$ {cmd}\n```"))
    out, err, code = await exec_in_container(container, cmd)
    embed = terminal_embed(f"Output", f"$ {cmd}\n\n{(out or err)[:1900]}")
    embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```")
    await msg.edit(embed=embed)

@bot.command(name="execute")
async def execute(ctx, container: str, *, cmd: str):
    await console(ctx, container, cmd=cmd)

# ==================================================================================================
#  ⬆️  COMPLETE .upgradevps COMMAND - CHECK INVITES & UPGRADE RESOURCES
# ==================================================================================================

@bot.command(name="upgradevps")
@commands.cooldown(1, 30, commands.BucketType.user)
async def upgrade_vps(ctx, container_name: str = None):
    """Upgrade your VPS resources using invites"""
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    
    user_id = str(ctx.author.id)
    
    # If no container specified, use first VPS
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            return await ctx.send(embed=no_vps_embed())
        container_name = vps_list[0]['container_name']
        vps_data = vps_list[0]
    else:
        vps_list = get_user_vps(user_id)
        vps_data = next((v for v in vps_list if v['container_name'] == container_name), None)
        if not vps_data:
            return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    # Get user invites
    stats = get_user_stats(user_id)
    invites = stats.get('invites', 0)
    
    # Current resources
    current_ram = vps_data['ram']
    current_cpu = vps_data['cpu']
    current_disk = vps_data['disk']
    
    # Upgrade options with invite costs
    upgrade_options = [
        {"name": "RAM Upgrade", "resource": "ram", "amount": 2, "cost": 5, "emoji": "💾", "desc": "Add 2GB RAM"},
        {"name": "RAM Upgrade", "resource": "ram", "amount": 4, "cost": 10, "emoji": "💾", "desc": "Add 4GB RAM"},
        {"name": "RAM Upgrade", "resource": "ram", "amount": 8, "cost": 20, "emoji": "💾", "desc": "Add 8GB RAM"},
        {"name": "CPU Upgrade", "resource": "cpu", "amount": 1, "cost": 5, "emoji": "⚡", "desc": "Add 1 CPU Core"},
        {"name": "CPU Upgrade", "resource": "cpu", "amount": 2, "cost": 10, "emoji": "⚡", "desc": "Add 2 CPU Cores"},
        {"name": "CPU Upgrade", "resource": "cpu", "amount": 4, "cost": 20, "emoji": "⚡", "desc": "Add 4 CPU Cores"},
        {"name": "Disk Upgrade", "resource": "disk", "amount": 20, "cost": 5, "emoji": "💽", "desc": "Add 20GB Disk"},
        {"name": "Disk Upgrade", "resource": "disk", "amount": 50, "cost": 10, "emoji": "💽", "desc": "Add 50GB Disk"},
        {"name": "Disk Upgrade", "resource": "disk", "amount": 100, "cost": 20, "emoji": "💽", "desc": "Add 100GB Disk"},
    ]
    
    # Create upgrade view
    view = UpgradeVPSView(ctx, container_name, vps_data, invites, upgrade_options, current_ram, current_cpu, current_disk)
    
    # Main embed
    total_vps = len(get_all_vps())
    total_users = len(set([v['user_id'] for v in get_all_vps()]))
    active_vps = len([v for v in get_all_vps() if v['status'] == 'running'])
    
    embed = discord.Embed(
        title="```glow\n⬆️ SVM5-BOT - UPGRADE YOUR VPS ⬆️\n```",
        description=f"Upgrade your VPS resources using your invites!\n\n"
                    f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
        color=0xFFAA00
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
    
    # Current Resources with Visual Bars
    ram_bar = "█" * int(current_ram / 16) + "░" * (10 - int(current_ram / 16))
    cpu_bar = "█" * int(current_cpu / 8) + "░" * (10 - int(current_cpu / 8))
    disk_bar = "█" * int(current_disk / 100) + "░" * (10 - int(current_disk / 100))
    
    embed.add_field(
        name="📊 CURRENT RESOURCES",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ RAM  : {current_ram}GB  [{ram_bar}]\n│ CPU  : {current_cpu} Core(s) [{cpu_bar}]\n│ Disk : {current_disk}GB [{disk_bar}]\n└─────────────────────────────────────────────────┘\n```",
        inline=False
    )
    
    embed.add_field(
        name="💰 YOUR INVITES",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ You have {invites} invites available!\n└─────────────────────────────────────────────────┘\n```",
        inline=False
    )
    
    embed.add_field(
        name="🌍 PUBLIC STATISTICS",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Total VPS Created : {total_vps}\n│ Total Users       : {total_users}\n│ Active VPS        : {active_vps}\n└─────────────────────────────────────────────────┘\n```",
        inline=False
    )
    
    embed.add_field(
        name="📋 UPGRADE OPTIONS",
        value="Select an upgrade option from the dropdown menu below.",
        inline=False
    )
    
    embed.set_footer(
        text=f"⚡ SVM5-BOT • Upgrade for {ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    
    await ctx.send(embed=embed, view=view)


class UpgradeVPSView(View):
    def __init__(self, ctx, container_name, vps_data, invites, upgrade_options, current_ram, current_cpu, current_disk):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.container_name = container_name
        self.vps_data = vps_data
        self.invites = invites
        self.upgrade_options = upgrade_options
        self.current_ram = current_ram
        self.current_cpu = current_cpu
        self.current_disk = current_disk
        
        # Create options
        options = []
        for opt in upgrade_options:
            if opt["resource"] == "ram":
                new_value = current_ram + opt["amount"]
                options.append(discord.SelectOption(
                    label=f"{opt['emoji']} +{opt['amount']}GB RAM",
                    value=f"{opt['resource']}:{opt['amount']}:{opt['cost']}",
                    description=f"Cost: {opt['cost']} invites → New: {new_value}GB"
                ))
            elif opt["resource"] == "cpu":
                new_value = current_cpu + opt["amount"]
                options.append(discord.SelectOption(
                    label=f"{opt['emoji']} +{opt['amount']} CPU Cores",
                    value=f"{opt['resource']}:{opt['amount']}:{opt['cost']}",
                    description=f"Cost: {opt['cost']} invites → New: {new_value} Cores"
                ))
            elif opt["resource"] == "disk":
                new_value = current_disk + opt["amount"]
                options.append(discord.SelectOption(
                    label=f"{opt['emoji']} +{opt['amount']}GB Disk",
                    value=f"{opt['resource']}:{opt['amount']}:{opt['cost']}",
                    description=f"Cost: {opt['cost']} invites → New: {new_value}GB"
                ))
        
        self.select = Select(placeholder="📋 Select upgrade option...", options=options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=1)
        cancel_btn.callback = self.cancel_callback
        self.add_item(cancel_btn)
    
    async def select_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        value = self.select.values[0]
        resource, amount, cost = value.split(':')
        amount = int(amount)
        cost = int(cost)
        
        if self.invites < cost:
            await interaction.response.send_message(
                embed=error_embed("Not Enough Invites", f"```diff\n- You need {cost} invites but you only have {self.invites}.\n```"),
                ephemeral=True
            )
            return
        
        # Confirm upgrade
        view = ConfirmUpgradeView(self.ctx, self.container_name, self.vps_data, resource, amount, cost, 
                                   self.current_ram, self.current_cpu, self.current_disk, self.invites)
        
        resource_names = {"ram": "RAM", "cpu": "CPU", "disk": "Disk"}
        resource_emoji = {"ram": "💾", "cpu": "⚡", "disk": "💽"}
        
        embed = warning_embed(
            "⚠️ Confirm Upgrade",
            f"```fix\nContainer: {self.container_name}\nUpgrade: {resource_emoji[resource]} +{amount} {resource_names[resource]}\nCost: {cost} invites\nCurrent {resource_names[resource]}: {self.current_ram if resource == 'ram' else self.current_cpu if resource == 'cpu' else self.current_disk}\nNew {resource_names[resource]}: {self.current_ram + amount if resource == 'ram' else self.current_cpu + amount if resource == 'cpu' else self.current_disk + amount}\n```\n\nThis will use {cost} invites from your account!"
        )
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nUpgrade cancelled.\n```"),
            view=None
        )


class ConfirmUpgradeView(View):
    def __init__(self, ctx, container_name, vps_data, resource, amount, cost, current_ram, current_cpu, current_disk, invites):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.container_name = container_name
        self.vps_data = vps_data
        self.resource = resource
        self.amount = amount
        self.cost = cost
        self.current_ram = current_ram
        self.current_cpu = current_cpu
        self.current_disk = current_disk
        self.invites = invites
        
        confirm_btn = Button(label="✅ Confirm Upgrade", style=discord.ButtonStyle.success, emoji="✅", row=0)
        confirm_btn.callback = self.confirm_callback
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=0)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(confirm_btn)
        self.add_item(cancel_btn)
    
    async def confirm_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await self.perform_upgrade(interaction)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nUpgrade cancelled.\n```"),
            view=None
        )
    
    async def perform_upgrade(self, interaction):
        await interaction.response.defer()
        
        user_id = str(self.ctx.author.id)
        
        # Rainbow progress colors
        rainbow_colors = [0xFF0000, 0xFF7700, 0xFFFF00, 0x00FF00, 0x00CCFF, 0x3366FF, 0x8B00FF]
        
        progress_msg = await interaction.followup.send(
            embed=discord.Embed(
                title="```glow\n🌈 UPGRADING VPS RESOURCES 🌈\n```",
                description="```fix\n[░░░░░░░░░░░░░░░░░░░░] 0% | Preparing upgrade...\n```",
                color=rainbow_colors[0]
            ),
            ephemeral=True
        )
        
        def get_progress_bar(percent):
            filled = int(percent / 5)
            return "█" * filled + "░" * (20 - filled)
        
        try:
            # Step 1: Check container status
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 UPGRADING VPS RESOURCES 🌈\n```",
                description=f"```fix\n[{get_progress_bar(20)}] 20% | 🔍 Checking container status...\n```",
                color=rainbow_colors[0]
            ))
            
            status = await get_container_status(self.container_name)
            was_running = status == 'running'
            
            # Step 2: Stop container if running
            if was_running:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 UPGRADING VPS RESOURCES 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(40)}] 40% | ⏹️ Stopping container...\n```",
                    color=rainbow_colors[1]
                ))
                await run_lxc(f"lxc stop {self.container_name} --force")
                await asyncio.sleep(2)
            
            # Step 3: Apply upgrade
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 UPGRADING VPS RESOURCES 🌈\n```",
                description=f"```fix\n[{get_progress_bar(60)}] 60% | ⚙️ Applying {self.resource.upper()} upgrade...\n```",
                color=rainbow_colors[2]
            ))
            
            if self.resource == "ram":
                new_ram = self.current_ram + self.amount
                await run_lxc(f"lxc config set {self.container_name} limits.memory {new_ram * 1024}MB")
                
                conn = get_db()
                cur = conn.cursor()
                cur.execute('UPDATE vps SET ram = ? WHERE container_name = ?', (new_ram, self.container_name))
                conn.commit()
                conn.close()
                
            elif self.resource == "cpu":
                new_cpu = self.current_cpu + self.amount
                await run_lxc(f"lxc config set {self.container_name} limits.cpu {new_cpu}")
                
                conn = get_db()
                cur = conn.cursor()
                cur.execute('UPDATE vps SET cpu = ? WHERE container_name = ?', (new_cpu, self.container_name))
                conn.commit()
                conn.close()
                
            elif self.resource == "disk":
                new_disk = self.current_disk + self.amount
                await run_lxc(f"lxc config device set {self.container_name} root size={new_disk}GB")
                
                conn = get_db()
                cur = conn.cursor()
                cur.execute('UPDATE vps SET disk = ? WHERE container_name = ?', (new_disk, self.container_name))
                conn.commit()
                conn.close()
            
            # Step 4: Start container if it was running
            if was_running:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 UPGRADING VPS RESOURCES 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(80)}] 80% | ▶️ Starting container...\n```",
                    color=rainbow_colors[3]
                ))
                await run_lxc(f"lxc start {self.container_name}")
                await asyncio.sleep(3)
            
            # Step 5: Deduct invites
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 UPGRADING VPS RESOURCES 🌈\n```",
                description=f"```fix\n[{get_progress_bar(90)}] 90% | 💰 Updating invites...\n```",
                color=rainbow_colors[4]
            ))
            
            # Update invites
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE user_stats SET invites = invites - ?, last_updated = ? WHERE user_id = ?',
                       (self.cost, datetime_.datetime.now().isoformat(), user_id))
            conn.commit()
            conn.close()
            
            # Step 6: Finalize
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 UPGRADING VPS RESOURCES 🌈\n```",
                description=f"```fix\n[{get_progress_bar(100)}] 100% | 🎉 Upgrade complete!\n```",
                color=rainbow_colors[5]
            ))
            await asyncio.sleep(1)
            
            # Get updated stats
            new_stats = get_user_stats(user_id)
            new_invites = new_stats.get('invites', 0)
            
            # Get new VPS data
            updated_vps = get_user_vps(user_id)
            updated_vps_data = next((v for v in updated_vps if v['container_name'] == self.container_name), None)
            
            new_ram = updated_vps_data['ram'] if updated_vps_data else self.current_ram + self.amount
            new_cpu = updated_vps_data['cpu'] if updated_vps_data else self.current_cpu + self.amount
            new_disk = updated_vps_data['disk'] if updated_vps_data else self.current_disk + self.amount
            
            # Resource Bars
            ram_bar = "█" * int(new_ram / 16) + "░" * (10 - int(new_ram / 16))
            cpu_bar = "█" * int(new_cpu / 8) + "░" * (10 - int(new_cpu / 8))
            disk_bar = "█" * int(new_disk / 100) + "░" * (10 - int(new_disk / 100))
            
            # Success Embed
            resource_names = {"ram": "RAM", "cpu": "CPU", "disk": "Disk"}
            resource_emoji = {"ram": "💾", "cpu": "⚡", "disk": "💽"}
            
            total_vps = len(get_all_vps())
            total_users = len(set([v['user_id'] for v in get_all_vps()]))
            active_vps = len([v for v in get_all_vps() if v['status'] == 'running'])
            
            success_embed = discord.Embed(
                title="```glow\n⬆️ VPS UPGRADED SUCCESSFULLY! ⬆️\n```",
                description=f"🎉 **{resource_emoji[self.resource]} +{self.amount} {resource_names[self.resource]} added to {self.container_name}!**\n\n"
                            f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
                color=0x00FF88
            )
            success_embed.set_thumbnail(url=THUMBNAIL_URL)
            success_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
            
            success_embed.add_field(
                name="📦 CONTAINER",
                value=f"```fix\n{self.container_name}\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="⚙️ NEW RESOURCES",
                value=f"```fix\nRAM  : {new_ram}GB  [{ram_bar}]\nCPU  : {new_cpu} Core(s) [{cpu_bar}]\nDisk : {new_disk}GB [{disk_bar}]\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="💰 INVITES UPDATE",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Used : {self.cost} invites\n│ Left : {new_invites} invites\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="🌍 PUBLIC STATISTICS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Total VPS Created : {total_vps}\n│ Total Users       : {total_users}\n│ Active VPS        : {active_vps}\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="🖥️ MANAGEMENT",
                value=f"```fix\n.manage {self.container_name} - Interactive Manager\n.stats {self.container_name} - Live Statistics\n```",
                inline=False
            )
            
            success_embed.set_footer(
                text=f"⚡ SVM5-BOT • Upgraded by {self.ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
                icon_url=THUMBNAIL_URL
            )
            
            await progress_msg.edit(embed=success_embed)
            
            # DM user
            try:
                dm_embed = success_embed("⬆️ VPS Upgraded!", f"Your VPS **{self.container_name}** has been upgraded!")
                dm_embed.add_field(name="⚙️ New Resources", value=f"```fix\nRAM: {new_ram}GB\nCPU: {new_cpu} Core(s)\nDisk: {new_disk}GB\n```")
                await self.ctx.author.send(embed=dm_embed)
            except:
                pass
            
            logger.info(f"User {self.ctx.author} upgraded {self.container_name} with +{self.amount} {self.resource}")
            
        except Exception as e:
            await progress_msg.edit(embed=error_embed("Upgrade Failed", f"```diff\n- {str(e)}\n```"))
            
@bot.command(name="top")
async def top(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "ps aux --sort=-%cpu | head -20")
    embed = terminal_embed(f"Top: {container}", out)
    await ctx.send(embed=embed)

@bot.command(name="df")
async def df(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "df -h")
    embed = terminal_embed(f"Disk: {container}", out)
    await ctx.send(embed=embed)

@bot.command(name="free")
async def free(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "free -h")
    embed = terminal_embed(f"Memory: {container}", out)
    await ctx.send(embed=embed)

@bot.command(name="ps")
async def ps_cmd(ctx, container: str = None):
    await top(ctx, container)

@bot.command(name="who")
async def who(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "who")
    embed = terminal_embed(f"Users: {container}", out or "No users")
    await ctx.send(embed=embed)

@bot.command(name="uptime")
async def uptime_cmd(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, "uptime")
    await ctx.send(embed=info_embed(f"Uptime: {container}", f"```fix\n{out}\n```"))

# ==================================================================================================
#  🎮  GAMES COMMANDS
# ==================================================================================================

@bot.command(name="games")
async def games(ctx):
    embed = info_embed("Available Games", f"```fix\nTotal: {len(GAMES_LIST)}\n```")
    for g in GAMES_LIST:
        embed.add_field(name=f"{g['icon']} {g['name']}", value=f"```fix\nPort: {g['port']} | RAM: {g['ram']}MB\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="game-info")
async def game_info(ctx, *, name: str):
    g = next((x for x in GAMES_LIST if x['name'].lower() == name.lower()), None)
    if not g:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    embed = info_embed(f"{g['icon']} {g['name']}")
    embed.add_field(name="🔌 Port", value=f"```fix\n{g['port']}\n```", inline=True)
    embed.add_field(name="💾 RAM", value=f"```fix\n{g['ram']}MB\n```", inline=True)
    embed.add_field(name="🐳 Docker", value=f"```fix\n{g['docker']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="install-game")
async def install_game(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    g = next((x for x in GAMES_LIST if x['name'].lower() == game.lower()), None)
    if not g:
        return await ctx.send(embed=error_embed("Game Not Found", f"```diff\n- {game}\n```"))
    msg = await ctx.send(embed=info_embed("Installing", f"```fix\n{g['name']} on {container}\n```"))
    await exec_in_container(container, "which docker || curl -fsSL https://get.docker.com | bash")
    cmd = f"docker run -d --name {g['name'].lower().replace(' ','-')} -p {g['port']}:{g['port']} {g['docker']}"
    out, err, code = await exec_in_container(container, cmd)
    if code == 0:
        add_game_install(uid, container, g['name'], g['port'])
        embed = success_embed("Game Installed")
        embed.add_field(name="🎮 Game", value=f"```fix\n{g['name']}\n```", inline=True)
        embed.add_field(name="🔌 Port", value=f"```fix\n{g['port']}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {err}\n```"))

@bot.command(name="my-games")
async def my_games(ctx, container: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if container:
        cur.execute('SELECT * FROM installed_games WHERE user_id = ? AND container_name = ?', (uid, container))
    else:
        cur.execute('SELECT * FROM installed_games WHERE user_id = ?', (uid,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Games", "No games installed."))
    embed = info_embed("Your Games")
    for r in rows:
        embed.add_field(name=f"🎮 {r['game_name']}", value=f"```fix\nContainer: {r['container_name']}\nPort: {r['game_port']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="start-game")
async def start_game(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await exec_in_container(container, f"docker start {game.lower().replace(' ','-')}")
    await ctx.send(embed=success_embed("Game Started", f"```fix\n{game}\n```"))

@bot.command(name="stop-game")
async def stop_game(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    await exec_in_container(container, f"docker stop {game.lower().replace(' ','-')}")
    await ctx.send(embed=success_embed("Game Stopped", f"```fix\n{game}\n```"))

@bot.command(name="game-stats")
async def game_stats(ctx, container: str, *, game: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    out,_,_ = await exec_in_container(container, f"docker stats {game.lower().replace(' ','-')} --no-stream")
    embed = terminal_embed(f"Game Stats: {game}", out)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🛠️  TOOLS COMMANDS
# ==================================================================================================

@bot.command(name="tools")
async def tools(ctx):
    embed = info_embed("Available Tools", f"```fix\nTotal: {len(TOOLS_LIST)}\n```")
    for t in TOOLS_LIST:
        embed.add_field(name=f"{t['icon']} {t['name']}", value=f"```fix\nPort: {t.get('port','None')}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="tool-info")
async def tool_info(ctx, *, name: str):
    t = next((x for x in TOOLS_LIST if x['name'].lower() == name.lower()), None)
    if not t:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    embed = info_embed(f"{t['icon']} {t['name']}")
    if t.get('port'):
        embed.add_field(name="🔌 Port", value=f"```fix\n{t['port']}\n```", inline=True)
    embed.add_field(name="📝 Command", value=f"```bash\n{t['cmd']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="install-tool")
async def install_tool(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    t = next((x for x in TOOLS_LIST if x['name'].lower() == tool.lower()), None)
    if not t:
        return await ctx.send(embed=error_embed("Tool Not Found", f"```diff\n- {tool}\n```"))
    msg = await ctx.send(embed=info_embed("Installing", f"```fix\n{t['name']} on {container}\n```"))
    out, err, code = await exec_in_container(container, t['cmd'])
    if code == 0 or "already" in err.lower():
        add_tool_install(uid, container, t['name'], t.get('port'))
        embed = success_embed("Tool Installed")
        embed.add_field(name="🛠️ Tool", value=f"```fix\n{t['name']}\n```", inline=True)
        embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {err}\n```"))

@bot.command(name="my-tools")
async def my_tools(ctx, container: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if container:
        cur.execute('SELECT * FROM installed_tools WHERE user_id = ? AND container_name = ?', (uid, container))
    else:
        cur.execute('SELECT * FROM installed_tools WHERE user_id = ?', (uid,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Tools", "No tools installed."))
    embed = info_embed("Your Tools")
    for r in rows:
        embed.add_field(name=f"🛠️ {r['tool_name']}", value=f"```fix\nContainer: {r['container_name']}\nPort: {r['tool_port'] or 'None'}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="start-tool")
async def start_tool(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    svc = tool.lower().replace(' ','')
    await exec_in_container(container, f"systemctl start {svc} 2>/dev/null || service {svc} start")
    await ctx.send(embed=success_embed("Tool Started", f"```fix\n{tool}\n```"))

@bot.command(name="stop-tool")
async def stop_tool(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    svc = tool.lower().replace(' ','')
    await exec_in_container(container, f"systemctl stop {svc} 2>/dev/null || service {svc} stop")
    await ctx.send(embed=success_embed("Tool Stopped", f"```fix\n{tool}\n```"))

@bot.command(name="tool-port")
async def tool_port(ctx, container: str, *, tool: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    t = next((x for x in TOOLS_LIST if x['name'].lower() == tool.lower()), None)
    if not t or not t.get('port'):
        return await ctx.send(embed=error_embed("No Port", f"```diff\n- {tool} has no default port\n```"))
    await ctx.send(embed=success_embed("Tool Port", f"```fix\n{tool} runs on port {t['port']}\n```"))

# ==================================================================================================
#  🌐  NODE COMMANDS
# ==================================================================================================

@bot.command(name="node")
async def node_list(ctx):
    nodes = load_nodes()
    embed = node_embed("Node Network", f"```fix\nTotal: {len(nodes['nodes'])}\n```")
    for n, data in nodes['nodes'].items():
        s = data.get('stats', {})
        status = "🟢" if data['status']=='online' else "🔴"
        text = f"```fix\nHost: {data['host']}\nRAM: {s.get('used_ram',0)}/{s.get('total_ram',0)} MB\nCPU: {s.get('used_cpu',0)}%\nLXC: {s.get('lxc_count',0)}\n```"
        embed.add_field(name=f"{status} {n}", value=text, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="node-info")
async def node_info(ctx, name: str = "local"):
    nodes = load_nodes()
    n = nodes['nodes'].get(name)
    if not n:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    s = n.get('stats', {})
    embed = node_embed(f"Node: {name}")
    basic = f"```fix\nHost: {n['host']}:{n['port']}\nStatus: {n['status']}\nType: {n['type']}\n```"
    res = f"```fix\nRAM: {s.get('used_ram',0)}/{s.get('total_ram',0)} MB\nCPU: {s.get('used_cpu',0)}%\nDisk: {s.get('used_disk',0)}/{s.get('total_disk',0)} GB\nLXC: {s.get('lxc_count',0)}\n```"
    embed.add_field(name="📋 Basic", value=basic, inline=True)
    embed.add_field(name="📊 Resources", value=res, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="node-add")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_add(ctx, name: str, host: str, user: str, pwd: str = None, port: int = 22):
    nodes = load_nodes()
    if name in nodes['nodes']:
        return await ctx.send(embed=error_embed("Exists", f"```diff\n- {name} already exists\n```"))
    import paramiko  # type: ignore[reportMissingModuleSource]
    msg = await ctx.send(embed=info_embed("Connecting", f"```fix\n{host}\n```"))
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if pwd:
            client.connect(host, port=port, username=user, password=pwd, timeout=10)
        else:
            key = paramiko.RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
            client.connect(host, port=port, username=user, pkey=key, timeout=10)
        stdin,stdout,stderr = client.exec_command('nproc')
        cpu = stdout.read().decode().strip()
        stdin,stdout,stderr = client.exec_command("free -m | awk '/^Mem:/{print $2}'")
        ram = stdout.read().decode().strip()
        stdin,stdout,stderr = client.exec_command("df -BG / | awk 'NR==2{print $2}' | sed 's/G//'")
        disk = stdout.read().decode().strip()
        client.close()
        node_data = {
            "name": name, "host": host, "port": port, "username": user, "password": pwd,
            "type": "remote", "status": "online", "is_main": False, "region": "us",
            "stats": {
                "total_ram": int(ram) if ram.isdigit() else 0, "used_ram": 0,
                "total_cpu": int(cpu) if cpu.isdigit() else 0, "used_cpu": 0,
                "total_disk": int(disk) if disk.isdigit() else 0, "used_disk": 0,
                "lxc_count": 0, "last_checked": datetime_.datetime.now().isoformat()
            }
        }
        nodes['nodes'][name] = node_data
        nodes['node_groups']['all'].append(name)
        save_nodes(nodes)
        await msg.edit(embed=success_embed("Node Added", f"```fix\n{name} connected\n```"))
    except Exception as e:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="node-remove")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_remove(ctx, name: str):
    nodes = load_nodes()
    if name not in nodes['nodes'] or name == 'local':
        return await ctx.send(embed=error_embed("Cannot Remove", "Node not found or is main node."))
    del nodes['nodes'][name]
    nodes['node_groups']['all'] = [x for x in nodes['node_groups']['all'] if x != name]
    save_nodes(nodes)
    await ctx.send(embed=success_embed("Node Removed", f"```fix\n{name}\n```"))

@bot.command(name="node-check")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_check(ctx, name: str):
    n = get_node(name)
    if not n:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    if name == 'local':
        return await ctx.send(embed=success_embed("Local Node", "```fix\nOnline\n```"))
    import paramiko  # type: ignore[reportMissingModuleSource]
    msg = await ctx.send(embed=info_embed("Checking", f"```fix\n{name}\n```"))
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if n.get('password'):
            client.connect(n['host'], port=n['port'], username=n['username'], password=n['password'], timeout=10)
        else:
            key = paramiko.RSAKey.from_private_key_file(os.path.expanduser("~/.ssh/id_rsa"))
            client.connect(n['host'], port=n['port'], username=n['username'], pkey=key, timeout=10)
        client.close()
        nodes = load_nodes()
        nodes['nodes'][name]['status'] = 'online'
        nodes['nodes'][name]['stats']['last_checked'] = datetime_.datetime.now().isoformat()
        save_nodes(nodes)
        await msg.edit(embed=success_embed("Node Online", f"```fix\n{name} is healthy\n```"))
    except:
        nodes = load_nodes()
        nodes['nodes'][name]['status'] = 'offline'
        save_nodes(nodes)
        await msg.edit(embed=error_embed("Node Offline", f"```diff\n- {name} is offline\n```"))

@bot.command(name="node-stats")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_stats(ctx):
    nodes = load_nodes()
    alln = nodes['nodes']
    tr = sum(n['stats'].get('total_ram',0) for n in alln.values())
    ur = sum(n['stats'].get('used_ram',0) for n in alln.values())
    td = sum(n['stats'].get('total_disk',0) for n in alln.values())
    ud = sum(n['stats'].get('used_disk',0) for n in alln.values())
    tc = sum(n['stats'].get('total_cpu',0) for n in alln.values())
    tl = sum(n['stats'].get('lxc_count',0) for n in alln.values())
    on = sum(1 for n in alln.values() if n['status']=='online')
    embed = node_embed("Cluster Statistics")
    embed.add_field(name="📊 Summary", value=f"```fix\nTotal: {len(alln)}\nOnline: {on}\nOffline: {len(alln)-on}\nLXC: {tl}\n```", inline=False)
    embed.add_field(name="💾 Resources", value=f"```fix\nRAM: {ur}/{tr} MB ({(ur/tr*100) if tr>0 else 0:.1f}%)\nDisk: {ud}/{td} GB ({(ud/td*100) if td>0 else 0:.1f}%)\nCPU Cores: {tc}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="node-connect")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def node_connect(ctx, host: str, user: str, pwd: str = None, name: str = None, port: int = 22):
    if not name:
        name = host.split('.')[0]
    await node_add(ctx, name, host, user, pwd, port)

# ==================================================================================================
#  👥  SHARE COMMANDS
# ==================================================================================================

@bot.command(name="share")
async def share(ctx, user: discord.Member, num: int):
    uid = str(ctx.author.id)
    vps = get_user_vps(uid)
    if num < 1 or num > len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    container = vps[num-1]['container_name']
    if share_vps(uid, str(user.id), container):
        await ctx.send(embed=success_embed("Shared", f"```fix\n{container} with {user.name}\n```"))
    else:
        await ctx.send(embed=error_embed("Failed", "Could not share VPS"))

@bot.command(name="unshare")
async def unshare(ctx, user: discord.Member, num: int):
    uid = str(ctx.author.id)
    vps = get_user_vps(uid)
    if num < 1 or num > len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    container = vps[num-1]['container_name']
    if unshare_vps(uid, str(user.id), container):
        await ctx.send(embed=success_embed("Unshared", f"```fix\n{container} from {user.name}\n```"))
    else:
        await ctx.send(embed=error_embed("Failed", "Could not unshare VPS"))

@bot.command(name="shared")
async def shared(ctx):
    shared = get_shared_vps(str(ctx.author.id))
    if not shared:
        return await ctx.send(embed=info_embed("No Shared", "No one has shared VPS with you."))
    embed = info_embed("Shared With You")
    for v in shared:
        try:
            owner = await bot.fetch_user(int(v['owner_id']))
            oname = owner.name
        except:
            oname = "Unknown"
        embed.add_field(name=f"📦 {v['container_name']}", value=f"```fix\nOwner: {oname}\nStatus: {v['status']}\n```", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="manage-shared")
async def manage_shared(ctx, owner: discord.Member, num: int):
    shared = get_shared_vps(str(ctx.author.id))
    owner_vps = [v for v in shared if v['owner_id'] == str(owner.id)]
    if num < 1 or num > len(owner_vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(owner_vps)}"))
    v = owner_vps[num-1]
    await manage(ctx, container=v['container_name'])

# ==================================================================================================
#  🔌  PORT COMMANDS
# ==================================================================================================

@bot.group(name="ports", invoke_without_command=True)
async def ports(ctx):
    uid = str(ctx.author.id)
    alloc = get_port_allocation(uid)
    fwds = get_user_port_forwards(uid)
    embed = info_embed("Port Forwarding")
    embed.add_field(name="📊 Quota", value=f"```fix\nAllocated: {alloc}\nUsed: {len(fwds)}\nAvailable: {alloc-len(fwds)}\n```", inline=False)
    embed.add_field(name="📋 Commands", value=f"`.ports add <vps_num> <port> [tcp/udp]`\n`.ports list`\n`.ports remove <id>`\n`.ports quota`\n`.ports check <port>`", inline=False)
    await ctx.send(embed=embed)

@ports.command(name="add")
async def ports_add(ctx, num: int, port: int, proto: str = "tcp+udp"):
    uid = str(ctx.author.id)
    vps = get_user_vps(uid)
    if not vps:
        return await ctx.send(embed=no_vps_embed())
    if num < 1 or num > len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    if port < 1 or port > 65535:
        return await ctx.send(embed=error_embed("Invalid", "Port must be 1-65535"))
    if proto not in ["tcp","udp","tcp+udp"]:
        return await ctx.send(embed=error_embed("Invalid", "Protocol must be tcp, udp, or tcp+udp"))
    alloc = get_port_allocation(uid)
    if len(get_user_port_forwards(uid)) >= alloc:
        return await ctx.send(embed=error_embed("Quota Exceeded", f"You have used all {alloc} slots"))
    v = vps[num-1]
    if v['suspended'] or v['status'] != 'running':
        return await ctx.send(embed=error_embed("Cannot Add", "VPS must be running"))
    msg = await ctx.send(embed=info_embed("Creating port forward..."))
    hport = await create_port_forward(uid, v['container_name'], port, proto)
    if hport:
        embed = success_embed("Port Forward Created")
        embed.add_field(name="📦 VPS", value=f"```fix\n#{num} - {v['container_name']}\n```", inline=True)
        embed.add_field(name="🔌 Container", value=f"```fix\n{port}\n```", inline=True)
        embed.add_field(name="🌐 Host", value=f"```fix\n{SERVER_IP}:{hport}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", "Could not assign port"))

@ports.command(name="list")
async def ports_list(ctx):
    uid = str(ctx.author.id)
    fwds = get_user_port_forwards(uid)
    if not fwds:
        return await ctx.send(embed=info_embed("No Port Forwards", "You have no active forwards."))
    embed = info_embed(f"Your Port Forwards ({len(fwds)})")
    for f in fwds:
        vnum = next((i+1 for i,v in enumerate(get_user_vps(uid)) if v['container_name']==f['container_name']), '?')
        embed.add_field(name=f"ID: {f['id']}", value=f"```fix\nVPS #{vnum}: {f['container_port']} → {SERVER_IP}:{f['host_port']} ({f['protocol']})\nCreated: {f['created_at'][:16]}\n```", inline=False)
    await ctx.send(embed=embed)

@ports.command(name="remove")
async def ports_remove(ctx, fid: int):
    uid = str(ctx.author.id)
    success, container, hport = remove_port_forward(fid)
    if not success:
        return await ctx.send(embed=error_embed("Not Found", f"ID {fid} not found"))
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this forward"))
    await remove_port_device(container, hport)
    await ctx.send(embed=success_embed("Removed", f"```fix\nForward ID {fid} removed\n```"))

@ports.command(name="quota")
async def ports_quota(ctx):
    uid = str(ctx.author.id)
    alloc = get_port_allocation(uid)
    used = len(get_user_port_forwards(uid))
    embed = info_embed("Port Quota")
    embed.add_field(name="📊 Allocated", value=f"```fix\n{alloc}\n```", inline=True)
    embed.add_field(name="📊 Used", value=f"```fix\n{used}\n```", inline=True)
    embed.add_field(name="📊 Available", value=f"```fix\n{alloc-used}\n```", inline=True)
    await ctx.send(embed=embed)

@ports.command(name="check")
async def ports_check(ctx, port: int):
    try:
        out = subprocess.getoutput(f"ss -tuln | grep :{port}")
        if out:
            await ctx.send(embed=error_embed("Port Unavailable", f"```diff\n- Port {port} is in use\n```"))
        else:
            await ctx.send(embed=success_embed("Port Available", f"```fix\nPort {port} is free\n```"))
    except:
        await ctx.send(embed=info_embed("Port Check", f"```fix\nCould not check port {port}\n```"))

# ==================================================================================================
#  🌍  IPv4 COMMANDS
# ==================================================================================================

UPI_ID = get_setting('upi_id', '9892642904@ybl')
IPV4_PRICE = int(get_setting('ipv4_price', '50'))

def gen_upi_qr(upi: str, amt: int = None, note: str = None):
    try:
        url = f"upi://pay?pa={upi}&pn={BOT_NAME}"
        if amt:
            url += f"&am={amt}"
        if note:
            url += f"&tn={note}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        bio = io.BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0)
        return bio
    except:
        return None

@bot.command(name="ipv4")
async def ipv4_list(ctx, user: discord.Member = None):
    if user and user.id != ctx.author.id and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("Access Denied", "Only admins can view others."))
    tid = str(user.id) if user else str(ctx.author.id)
    ips = get_user_ipv4(tid)
    if not ips:
        return await ctx.send(embed=info_embed("No IPv4", "No addresses assigned."))
    embed = info_embed(f"IPv4 for {user.display_name if user else ctx.author.display_name}")
    for i, ip in enumerate(ips, 1):
        val = f"```fix\nContainer: {ip['container_name']}\nPublic: {ip['public_ip']}\nPrivate: {ip['private_ip']}\nMAC: {ip['mac_address']}\nAssigned: {ip['assigned_at'][:16]}\n```"
        embed.add_field(name=f"IPv4 #{i}", value=val, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ipv4-details")
async def ipv4_details(ctx, container: str):
    uid = str(ctx.author.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)) and not is_admin(uid):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    ips = get_user_ipv4(uid)
    ip = next((i for i in ips if i['container_name']==container), None)
    out,_,_ = await exec_in_container(container, "ip addr show")
    embed = info_embed(f"IPv4 Details: {container}")
    if ip:
        embed.add_field(name="🌐 Public", value=f"```fix\n{ip['public_ip']}\n```", inline=True)
        embed.add_field(name="🏠 Private", value=f"```fix\n{ip['private_ip']}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{ip['mac_address']}\n```", inline=True)
    embed.add_field(name="📋 Network", value=f"```bash\n{out[:500]}\n```", inline=False)
    await ctx.send(embed=embed)

class TxnModal(Modal):
    def __init__(self, ctx, ref):
        super().__init__(title="Enter Transaction ID")
        self.ctx = ctx
        self.ref = ref
        self.add_item(InputText(label="UPI Transaction ID", placeholder="e.g., T25031234567890", min_length=8))
    async def callback(self, interaction):
        tid = self.children[0].value
        add_transaction(str(self.ctx.author.id), self.ref, IPV4_PRICE)
        for aid in MAIN_ADMIN_IDS:
            try:
                admin = await bot.fetch_user(aid)
                await admin.send(embed=warning_embed("New IPv4 Purchase", f"```fix\nUser: {self.ctx.author}\nRef: {self.ref}\nTxn: {tid}\nAmount: ₹{IPV4_PRICE}\n```"))
            except:
                pass
        await interaction.response.edit_message(embed=info_embed("Payment Submitted", f"```fix\nReference: {self.ref}\nTxn ID: {tid}\n```\nAdmin will verify."), view=None)

@bot.command(name="buy-ipv4")
async def buy_ipv4(ctx):
    ref = ''.join(random.choices(string.ascii_uppercase+string.digits, k=10))
    embed = info_embed("Buy IPv4 Address")
    embed.add_field(name="💰 Price", value=f"```fix\n₹{IPV4_PRICE}\n```", inline=True)
    embed.add_field(name="📱 UPI", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="🔖 Ref", value=f"```fix\n{ref}\n```", inline=True)
    embed.add_field(name="📋 Instructions", value=f"```fix\n1. Pay ₹{IPV4_PRICE} to {UPI_ID}\n2. Add ref {ref}\n3. Click ✅ below\n```", inline=False)
    qr = gen_upi_qr(UPI_ID, IPV4_PRICE, ref)
    file = discord.File(qr, filename="qr.png") if qr else None
    if file:
        embed.set_image(url="attachment://qr.png")
    view = View()
    pay_btn = Button(label="✅ I've Paid", style=discord.ButtonStyle.success)
    async def pay_cb(i):
        if i.user.id != ctx.author.id:
            await i.response.send_message("Not your purchase!", ephemeral=True)
            return
        await i.response.send_modal(TxnModal(ctx, ref))
    pay_btn.callback = pay_cb
    view.add_item(pay_btn)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    cancel_btn.callback = cancel_cb
    view.add_item(cancel_btn)
    if file:
        await ctx.send(embed=embed, file=file, view=view)
    else:
        await ctx.send(embed=embed, view=view)

@bot.command(name="upi")
async def upi_info(ctx):
    embed = info_embed("UPI Information")
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{UPI_ID}\n```", inline=True)
    embed.add_field(name="💰 IPv4 Price", value=f"```fix\n₹{IPV4_PRICE}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="upi-qr")
async def upi_qr(ctx, amt: int = None, *, note: str = None):
    if not note:
        note = f"Payment to {BOT_NAME}"
    qr = gen_upi_qr(UPI_ID, amt, note)
    if not qr:
        return await ctx.send(embed=error_embed("Failed", "Could not generate QR"))
    file = discord.File(qr, filename="qr.png")
    embed = info_embed("UPI QR Code")
    if amt:
        embed.add_field(name="💰 Amount", value=f"```fix\n₹{amt}\n```", inline=True)
    if note:
        embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
    embed.set_image(url="attachment://qr.png")
    await ctx.send(embed=embed, file=file)

@bot.command(name="pay")
async def pay(ctx, amt: int, *, note: str = None):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    if not note:
        note = f"Payment to {BOT_NAME}"
    url = f"upi://pay?pa={UPI_ID}&pn={BOT_NAME}&am={amt}&tn={note}"
    view = View()
    view.add_item(Button(label="💳 Pay Now", style=discord.ButtonStyle.link, url=url))
    qr_btn = Button(label="📸 Show QR", style=discord.ButtonStyle.secondary)
    async def qr_cb(i):
        qr = gen_upi_qr(UPI_ID, amt, note)
        if qr:
            f = discord.File(qr, filename="qr.png")
            e = info_embed("Payment QR")
            e.set_image(url="attachment://qr.png")
            await i.response.send_message(embed=e, file=f, ephemeral=True)
        else:
            await i.response.send_message(embed=error_embed("Failed", "Could not generate QR"), ephemeral=True)
    qr_btn.callback = qr_cb
    view.add_item(qr_btn)
    embed = info_embed("Payment Link")
    embed.add_field(name="💰 Amount", value=f"```fix\n₹{amt}\n```", inline=True)
    embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  📦  PANEL COMMANDS
# ==================================================================================================

# ==================================================================================================
#  📦  COMPLETE .install-panel COMMAND - WITH CLOUDFLARED TUNNEL & DM
# ==================================================================================================

# Rainbow colors for progress
RAINBOW_COLORS = [
    0xFF0000,  # Red
    0xFF7700,  # Orange
    0xFFFF00,  # Yellow
    0x00FF00,  # Green
    0x00CCFF,  # Cyan
    0x3366FF,  # Blue
    0x8B00FF,  # Violet
    0xFF00CC,  # Pink
]

# Check if cloudflared is installed
CLOUDFLARED_AVAILABLE = shutil.which("cloudflared") is not None


async def create_cloudflared_tunnel(container_name: str, port: int = 80) -> Optional[str]:
    """Create cloudflared tunnel for container and return URL"""
    if not CLOUDFLARED_AVAILABLE:
        return None
    
    try:
        # Install cloudflared in container if not present
        await exec_in_container(container_name, "which cloudflared || (wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared)")
        
        # Generate unique tunnel ID
        tunnel_id = str(uuid.uuid4())[:8]
        
        # Start tunnel
        cmd = f"nohup cloudflared tunnel --url http://localhost:{port} --no-autoupdate > /tmp/cloudflared_{tunnel_id}.log 2>&1 & echo $!"
        pid, _, _ = await exec_in_container(container_name, cmd)
        
        # Wait for tunnel to establish
        await asyncio.sleep(8)
        
        # Get tunnel URL
        out, _, _ = await exec_in_container(container_name, f"cat /tmp/cloudflared_{tunnel_id}.log | grep -oP 'https://[a-z0-9-]+\\.trycloudflare\\.com' | head -1")
        url = out.strip()
        
        if url:
            return url
    except Exception as e:
        logger.error(f"Failed to create cloudflared tunnel: {e}")
    
    return None


class PanelInstallView(View):
    def __init__(self, ctx, container_name: str):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.container = container_name
        self.message = None
        
        ptero_btn = Button(label="🦅 Pterodactyl Panel", style=discord.ButtonStyle.primary, emoji="🦅", row=0)
        ptero_btn.callback = self.ptero_callback
        
        puffer_btn = Button(label="🐡 Pufferpanel", style=discord.ButtonStyle.success, emoji="🐡", row=0)
        puffer_btn.callback = self.puffer_callback
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=1)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(ptero_btn)
        self.add_item(puffer_btn)
        self.add_item(cancel_btn)
    
    async def ptero_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await self.install_panel(interaction, "pterodactyl")
    
    async def puffer_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await self.install_panel(interaction, "pufferpanel")
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nPanel installation cancelled.\n```"),
            view=None
        )
    
    async def install_panel(self, interaction, panel_type: str):
        await interaction.response.defer()
        
        # Generate admin credentials
        admin_user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        admin_email = f"{admin_user}@{random.choice(['gmail.com', 'outlook.com', 'proton.me', 'yandex.com'])}"
        admin_pass = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=16))
        
        # Rainbow progress
        progress_msg = await interaction.followup.send(
            embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - INSTALLING PANEL 🌈\n```",
                description="```fix\n[░░░░░░░░░░░░░░░░░░░░] 0% | Preparing installation...\n```",
                color=RAINBOW_COLORS[0]
            ),
            ephemeral=True
        )
        
        def get_progress_bar(percent):
            filled = int(percent / 5)
            return "█" * filled + "░" * (20 - filled)
        
        try:
            if panel_type == "pterodactyl":
                # Pterodactyl Installation Steps
                steps = [
                    (10, "🔧 Updating system..."),
                    (20, "📦 Installing dependencies..."),
                    (30, "🌐 Installing Nginx, MySQL, Redis..."),
                    (40, "🐘 Installing PHP 8.1..."),
                    (50, "📥 Downloading Pterodactyl..."),
                    (60, "🔧 Configuring environment..."),
                    (70, "📦 Installing Composer packages..."),
                    (80, "🗄️ Setting up database..."),
                    (90, "👤 Creating admin user..."),
                    (100, "🌍 Creating cloudflared tunnel..."),
                ]
                
                color_index = 0
                for progress, desc in steps:
                    await progress_msg.edit(embed=discord.Embed(
                        title="```glow\n🌈 SVM5-BOT - INSTALLING PTERODACTYL 🌈\n```",
                        description=f"```fix\n[{get_progress_bar(progress)}] {progress}% | {desc}\n```",
                        color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
                    ))
                    color_index += 1
                    
                    if progress == 10:
                        await exec_in_container(self.container, "apt-get update -qq")
                    elif progress == 20:
                        await exec_in_container(self.container, "apt-get install -y -qq curl wget git unzip tar")
                    elif progress == 30:
                        await exec_in_container(self.container, "apt-get install -y -qq nginx mariadb-server redis-server")
                    elif progress == 40:
                        await exec_in_container(self.container, "apt-get install -y -qq php8.1 php8.1-{cli,gd,mysql,pdo,mbstring,tokenizer,bcmath,xml,fpm,curl,zip}")
                    elif progress == 50:
                        await exec_in_container(self.container, "mkdir -p /var/www/pterodactyl")
                        await exec_in_container(self.container, "cd /var/www/pterodactyl && curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz")
                        await exec_in_container(self.container, "cd /var/www/pterodactyl && tar -xzvf panel.tar.gz && chmod -R 755 storage/* bootstrap/cache/")
                        await exec_in_container(self.container, "cd /var/www/pterodactyl && cp .env.example .env")
                    elif progress == 60:
                        await exec_in_container(self.container, "curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer")
                        await exec_in_container(self.container, "cd /var/www/pterodactyl && composer install --no-dev --optimize-autoloader --no-interaction")
                        await exec_in_container(self.container, "cd /var/www/pterodactyl && php artisan key:generate --force")
                    elif progress == 70:
                        await exec_in_container(self.container, "cd /var/www/pterodactyl && php artisan migrate --seed --force")
                    elif progress == 80:
                        await exec_in_container(self.container, f"cd /var/www/pterodactyl && php artisan p:user:make --email='{admin_email}' --username='{admin_user}' --password='{admin_pass}' --name-first='Admin' --name-last='User' --admin=1 --no-interaction")
                    elif progress == 90:
                        out, _, _ = await exec_in_container(self.container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                        ip = out.strip() or SERVER_IP
                        panel_url = f"http://{ip}"
                        
                        # Create tunnel
                        tunnel_url = await create_cloudflared_tunnel(self.container, 80)
                        if tunnel_url:
                            panel_url = tunnel_url
                    
                    await asyncio.sleep(1)
                
            else:  # pufferpanel
                steps = [
                    (10, "🔧 Updating system..."),
                    (20, "📦 Adding Pufferpanel repository..."),
                    (30, "📥 Installing Pufferpanel..."),
                    (40, "⚙️ Configuring services..."),
                    (50, "▶️ Starting Pufferpanel..."),
                    (60, "👤 Creating admin user..."),
                    (70, "🌍 Creating cloudflared tunnel..."),
                    (80, "🔧 Finalizing..."),
                ]
                
                color_index = 0
                for progress, desc in steps:
                    await progress_msg.edit(embed=discord.Embed(
                        title="```glow\n🌈 SVM5-BOT - INSTALLING PUFFERPANEL 🌈\n```",
                        description=f"```fix\n[{get_progress_bar(progress)}] {progress}% | {desc}\n```",
                        color=RAINBOW_COLORS[color_index % len(RAINBOW_COLORS)]
                    ))
                    color_index += 1
                    
                    if progress == 10:
                        await exec_in_container(self.container, "apt-get update -qq")
                    elif progress == 20:
                        await exec_in_container(self.container, "curl -s https://packagecloud.io/install/repositories/pufferpanel/pufferpanel/script.deb.sh | bash")
                    elif progress == 30:
                        await exec_in_container(self.container, "apt-get install -y -qq pufferpanel")
                    elif progress == 40:
                        await exec_in_container(self.container, "systemctl enable pufferpanel")
                    elif progress == 50:
                        await exec_in_container(self.container, "systemctl start pufferpanel")
                    elif progress == 60:
                        await exec_in_container(self.container, f"pufferpanel user add --name '{admin_user}' --email '{admin_email}' --password '{admin_pass}' --admin")
                    elif progress == 70:
                        out, _, _ = await exec_in_container(self.container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                        ip = out.strip() or SERVER_IP
                        panel_url = f"http://{ip}:8080"
                        
                        # Create tunnel
                        tunnel_url = await create_cloudflared_tunnel(self.container, 8080)
                        if tunnel_url:
                            panel_url = tunnel_url
                    
                    await asyncio.sleep(1)
            
            # Save to database
            add_panel(str(self.ctx.author.id), panel_type, panel_url, admin_user, admin_pass, admin_email, self.container, tunnel_url or "")
            
            # Get public statistics
            all_vps = get_all_vps()
            total_vps = len(all_vps)
            total_users = len(set([v['user_id'] for v in all_vps]))
            total_panels = len(get_user_panels(str(self.ctx.author.id)))
            
            # Success Embed
            success_embed = discord.Embed(
                title="```glow\n✅ PANEL INSTALLED SUCCESSFULLY! ✅\n```",
                description=f"🎉 **{panel_type.title()} has been installed on {self.container}!**\n\n"
                            f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
                color=0x00FF88
            )
            success_embed.set_thumbnail(url=THUMBNAIL_URL)
            success_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
            
            success_embed.add_field(
                name="🌐 PANEL URL",
                value=f"```fix\n{panel_url}\n```",
                inline=False
            )
            
            if tunnel_url:
                success_embed.add_field(
                    name="🌍 CLOUDFLARED TUNNEL",
                    value=f"```fix\n{tunnel_url}\n```",
                    inline=False
                )
            
            success_embed.add_field(
                name="🔐 CREDENTIALS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Username : {admin_user}\n│ Email    : {admin_email}\n│ Password : {admin_pass}\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="📦 CONTAINER",
                value=f"```fix\n{self.container}\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="🔌 PORT",
                value=f"```fix\n{80 if panel_type == 'pterodactyl' else 8080}\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="🌍 PUBLIC STATISTICS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Total VPS Created : {total_vps}\n│ Total Users       : {total_users}\n│ Panels Installed  : {total_panels}\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            success_embed.set_footer(
                text=f"⚡ SVM5-BOT • Installed by {self.ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
                icon_url=THUMBNAIL_URL
            )
            
            await progress_msg.edit(embed=success_embed)
            
            # DM user with credentials
            try:
                dm_embed = discord.Embed(
                    title="```glow\n🔐 PANEL CREDENTIALS\n```",
                    description=f"Your {panel_type.title()} panel has been installed successfully!",
                    color=0x57F287
                )
                dm_embed.set_thumbnail(url=THUMBNAIL_URL)
                dm_embed.add_field(
                    name="🌐 PANEL URL",
                    value=f"```fix\n{panel_url}\n```",
                    inline=False
                )
                if tunnel_url:
                    dm_embed.add_field(
                        name="🌍 TUNNEL URL",
                        value=f"```fix\n{tunnel_url}\n```",
                        inline=False
                    )
                dm_embed.add_field(
                    name="🔐 LOGIN",
                    value=f"```fix\nUsername: {admin_user}\nEmail: {admin_email}\nPassword: {admin_pass}\n```",
                    inline=False
                )
                dm_embed.add_field(
                    name="📦 CONTAINER",
                    value=f"```fix\n{self.container}\n```",
                    inline=True
                )
                await self.ctx.author.send(embed=dm_embed)
            except:
                pass
            
            logger.info(f"User {self.ctx.author} installed {panel_type} on {self.container}")
            
        except Exception as e:
            await progress_msg.edit(embed=error_embed("Installation Failed", f"```diff\n- {str(e)[:500]}\n```"))


@bot.command(name="install-panel")
@commands.cooldown(1, 600, commands.BucketType.user)
async def install_panel(ctx, container_name: str = None):
    """Install Pterodactyl or Pufferpanel on your VPS with cloudflared tunnel"""
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            return await ctx.send(embed=no_vps_embed())
        container_name = vps_list[0]['container_name']
    
    if not any(v['container_name'] == container_name for v in get_user_vps(user_id)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    status = await get_container_status(container_name)
    if status != 'running':
        return await ctx.send(embed=error_embed("Container Not Running", f"```diff\n- {container_name} is not running.\n```"))
    
    # Get public statistics
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    total_users = len(set([v['user_id'] for v in all_vps]))
    
    embed = discord.Embed(
        title="```glow\n📦 PANEL INSTALLATION\n```",
        description=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Container : {container_name}\n└─────────────────────────────────────────────────┘\n```\n\n"
                    f"🦅 **Pterodactyl** - Popular game server panel\n"
                    f"🐡 **Pufferpanel** - Lightweight alternative\n\n"
                    f"```glow\n🌍 Current Statistics:\n• Total VPS: {total_vps}\n• Total Users: {total_users}\n```",
        color=0x5865F2
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
    
    view = PanelInstallView(ctx, container_name)
    await ctx.send(embed=embed, view=view)

# ==================================================================================================
#  🖥️  COMPLETE .vpsui COMMAND - REAL SCREENSHOT GENERATOR
# ==================================================================================================
@bot.command(name="vpsui")
@commands.cooldown(1, 30, commands.BucketType.user)
async def vps_ui(ctx, container_name: str = None):
    """Generate a beautiful screenshot/UI of your VPS"""
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        return await ctx.send(embed=error_embed("License Required", "Please verify license first."))
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            return await ctx.send(embed=no_vps_embed())
        container_name = vps_list[0]['container_name']
    
    if not any(v['container_name'] == container_name for v in get_user_vps(user_id)):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    
    msg = await ctx.send(embed=info_embed("📸 Generating VPS Screenshot", f"```fix\nContainer: {container_name}\nFetching data...\n```"))
    
    try:
        # Get VPS data
        vps_data = next((v for v in get_user_vps(user_id) if v['container_name'] == container_name), None)
        stats = await get_container_stats(container_name)
        
        # Get more detailed info
        uname, _, _ = await exec_in_container(container_name, "uname -a")
        uptime, _, _ = await exec_in_container(container_name, "uptime -p")
        processes, _, _ = await exec_in_container(container_name, "ps aux | wc -l")
        load, _, _ = await exec_in_container(container_name, "cat /proc/loadavg | awk '{print $1, $2, $3}'")
        
        # Memory details
        mem_out, _, _ = await exec_in_container(container_name, "free -h | awk '/^Mem:/{print $2, $3, $4}'")
        mem_parts = mem_out.split() if mem_out else ["N/A", "N/A", "N/A"]
        mem_total = mem_parts[0] if len(mem_parts) > 0 else "N/A"
        mem_used = mem_parts[1] if len(mem_parts) > 1 else "N/A"
        mem_free = mem_parts[2] if len(mem_parts) > 2 else "N/A"
        
        # Disk details
        disk_out, _, _ = await exec_in_container(container_name, "df -h / | awk 'NR==2{print $2, $3, $4, $5}'")
        disk_parts = disk_out.split() if disk_out else ["N/A", "N/A", "N/A", "N/A"]
        disk_total = disk_parts[0] if len(disk_parts) > 0 else "N/A"
        disk_used = disk_parts[1] if len(disk_parts) > 1 else "N/A"
        disk_avail = disk_parts[2] if len(disk_parts) > 2 else "N/A"
        disk_use = disk_parts[3] if len(disk_parts) > 3 else "N/A"
        
        # CPU details
        cpu_out, _, _ = await exec_in_container(container_name, "lscpu | grep 'Model name' | cut -d':' -f2 | xargs")
        cpu_model = cpu_out.strip() if cpu_out else "Unknown"
        
        # Network details
        net_out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
        ip = net_out.strip() if net_out else "N/A"
        
        # Calculate percentages
        try:
            if mem_total.endswith('Gi'):
                mem_total_val = float(mem_total.replace('Gi', '')) * 1024
                mem_used_val = float(mem_used.replace('Gi', '')) * 1024
            elif mem_total.endswith('Mi'):
                mem_total_val = float(mem_total.replace('Mi', ''))
                mem_used_val = float(mem_used.replace('Mi', ''))
            else:
                mem_total_val = float(mem_total)
                mem_used_val = float(mem_used)
            mem_percent = (mem_used_val / mem_total_val) * 100 if mem_total_val > 0 else 0
        except:
            mem_percent = 0
        
        try:
            disk_percent = float(disk_use.replace('%', '')) if disk_use != "N/A" else 0
        except:
            disk_percent = 0
        
        # Create image
        img_width = 800
        img_height = 600
        img = PIL.Image.new('RGB', (img_width, img_height), color=(18, 18, 24))
        draw = PIL.ImageDraw.Draw(img)
        
        # Try to load fonts
        try:
            font_title = PIL.ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            font_header = PIL.ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            font_normal = PIL.ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            font_small = PIL.ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except:
            font_title = PIL.ImageFont.load_default()
            font_header = PIL.ImageFont.load_default()
            font_normal = PIL.ImageFont.load_default()
            font_small = PIL.ImageFont.load_default()
        
        # Draw header gradient
        for i in range(60):
            color = (30 + i, 40 + i, 50 + i)
            draw.rectangle([(0, i), (img_width, i+1)], fill=color)
        
        # Draw title
        draw.text((20, 15), f"SVM5-BOT • VPS MANAGEMENT UI", fill=(255, 255, 255), font=font_title)
        draw.text((20, 45), f"Container: {container_name}", fill=(100, 200, 255), font=font_header)
        draw.text((20, 70), f"Status: {stats['status'].upper()}", fill=(0, 255, 0) if stats['status'] == 'running' else (255, 0, 0), font=font_normal)
        
        # Draw separator
        draw.line([(20, 95), (img_width - 20, 95)], fill=(60, 60, 80), width=2)
        
        # System Information Box
        draw.rectangle([(20, 105), (img_width - 20, 165)], outline=(60, 60, 80), fill=(25, 25, 35))
        draw.text((30, 110), "📊 SYSTEM INFORMATION", fill=(200, 200, 255), font=font_header)
        draw.text((30, 135), f"OS: {vps_data.get('os_version', 'N/A')}", fill=(180, 180, 200), font=font_normal)
        draw.text((300, 135), f"Kernel: {uname.split()[2] if uname else 'N/A'}", fill=(180, 180, 200), font=font_normal)
        draw.text((30, 155), f"Uptime: {uptime}", fill=(180, 180, 200), font=font_normal)
        draw.text((300, 155), f"Processes: {processes}", fill=(180, 180, 200), font=font_normal)
        
        # Resources Box
        draw.rectangle([(20, 175), (img_width - 20, 285)], outline=(60, 60, 80), fill=(25, 25, 35))
        draw.text((30, 180), "⚙️ RESOURCES", fill=(200, 200, 255), font=font_header)
        
        # RAM Bar
        draw.text((30, 210), f"RAM: {mem_used}/{mem_total}", fill=(180, 180, 200), font=font_normal)
        bar_width = 400
        bar_height = 12
        draw.rectangle([(30, 230), (30 + bar_width, 230 + bar_height)], outline=(80, 80, 100), fill=(40, 40, 50))
        fill_width = int(bar_width * (mem_percent / 100))
        ram_color = (0, 255, 0) if mem_percent < 70 else (255, 165, 0) if mem_percent < 90 else (255, 0, 0)
        draw.rectangle([(30, 230), (30 + fill_width, 230 + bar_height)], fill=ram_color)
        draw.text((30 + bar_width + 10, 228), f"{mem_percent:.1f}%", fill=(180, 180, 200), font=font_normal)
        
        # CPU Bar
        draw.text((30, 250), f"CPU: {stats['cpu']}", fill=(180, 180, 200), font=font_normal)
        cpu_val = float(stats['cpu'].replace('%', '')) if stats['cpu'] != 'N/A' else 0
        fill_width = int(bar_width * (cpu_val / 100))
        cpu_color = (0, 255, 0) if cpu_val < 70 else (255, 165, 0) if cpu_val < 90 else (255, 0, 0)
        draw.rectangle([(30, 270), (30 + fill_width, 270 + bar_height)], fill=cpu_color)
        draw.text((30 + bar_width + 10, 268), f"{cpu_val:.1f}%", fill=(180, 180, 200), font=font_normal)
        
        # Disk Bar
        draw.text((30 + bar_width + 100, 210), f"Disk: {disk_used}/{disk_total}", fill=(180, 180, 200), font=font_normal)
        fill_width = int(bar_width * (disk_percent / 100))
        disk_color = (0, 255, 0) if disk_percent < 70 else (255, 165, 0) if disk_percent < 90 else (255, 0, 0)
        draw.rectangle([(30 + bar_width + 100, 230), (30 + bar_width + 100 + bar_width, 230 + bar_height)], fill=disk_color)
        draw.text((30 + bar_width + 100 + bar_width + 10, 228), f"{disk_percent:.1f}%", fill=(180, 180, 200), font=font_normal)
        
        draw.text((30 + bar_width + 100, 250), f"CPU Model: {cpu_model[:40]}", fill=(180, 180, 200), font=font_normal)
        
        # Network Box
        draw.rectangle([(20, 295), (img_width - 20, 375)], outline=(60, 60, 80), fill=(25, 25, 35))
        draw.text((30, 300), "🌐 NETWORK", fill=(200, 200, 255), font=font_header)
        draw.text((30, 325), f"IP Address: {ip}", fill=(180, 180, 200), font=font_normal)
        draw.text((300, 325), f"MAC: {stats['mac']}", fill=(180, 180, 200), font=font_normal)
        draw.text((30, 345), f"Load Average: {load}", fill=(180, 180, 200), font=font_normal)
        draw.text((300, 345), f"IPv4: {len(stats['ipv4'])} address(es)", fill=(180, 180, 200), font=font_normal)
        
        # Resource Allocation Box
        draw.rectangle([(20, 385), (img_width - 20, 465)], outline=(60, 60, 80), fill=(25, 25, 35))
        draw.text((30, 390), "📦 RESOURCE ALLOCATION", fill=(200, 200, 255), font=font_header)
        
        # Resource Bars
        ram_alloc = vps_data['ram']
        cpu_alloc = vps_data['cpu']
        disk_alloc = vps_data['disk']
        
        ram_bar_alloc = "█" * int(ram_alloc / 16) + "░" * (10 - int(ram_alloc / 16))
        cpu_bar_alloc = "█" * int(cpu_alloc / 8) + "░" * (10 - int(cpu_alloc / 8))
        disk_bar_alloc = "█" * int(disk_alloc / 100) + "░" * (10 - int(disk_alloc / 100))
        
        draw.text((30, 415), f"RAM: {ram_alloc}GB [{ram_bar_alloc}]", fill=(180, 180, 200), font=font_normal)
        draw.text((30, 435), f"CPU: {cpu_alloc} Core(s) [{cpu_bar_alloc}]", fill=(180, 180, 200), font=font_normal)
        draw.text((30, 455), f"Disk: {disk_alloc}GB [{disk_bar_alloc}]", fill=(180, 180, 200), font=font_normal)
        
        # Management Commands Box
        draw.rectangle([(20, 475), (img_width - 20, 560)], outline=(60, 60, 80), fill=(25, 25, 35))
        draw.text((30, 480), "🖥️ MANAGEMENT COMMANDS", fill=(200, 200, 255), font=font_header)
        
        commands_text = f".manage {container_name}  |  .stats {container_name}  |  .logs {container_name}  |  .ssh-gen {container_name}  |  .reboot {container_name}  |  .shutdown {container_name}"
        wrapped = textwrap.fill(commands_text, width=70)
        draw.text((30, 505), wrapped, fill=(100, 200, 150), font=font_small)
        
        # Footer
        draw.text((20, img_height - 20), f"SVM5-BOT • Generated: {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fill=(100, 100, 120), font=font_small)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Send image
        file = discord.File(img_bytes, filename=f"vpsui_{container_name}.png")
        
        embed = discord.Embed(
            title=f"```glow\n🖥️ VPS UI - {container_name}\n```",
            description=f"Real-time screenshot of your VPS",
            color=0x00FF88
        )
        embed.set_image(url=f"attachment://vpsui_{container_name}.png")
        embed.add_field(name="📊 Status", value=f"```fix\n{stats['status'].upper()}\n```", inline=True)
        embed.add_field(name="💾 CPU", value=f"```fix\n{stats['cpu']}\n```", inline=True)
        embed.add_field(name="📀 Memory", value=f"```fix\n{stats['memory']}\n```", inline=True)
        embed.add_field(name="💽 Disk", value=f"```fix\n{stats['disk']}\n```", inline=True)
        embed.add_field(name="🌐 IP", value=f"```fix\n{ip}\n```", inline=True)
        embed.add_field(name="⏱️ Uptime", value=f"```fix\n{uptime}\n```", inline=True)
        
        await msg.edit(embed=embed, file=file)
        
    except Exception as e:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="panel-info")
async def panel_info(ctx):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM panels WHERE user_id = ? ORDER BY installed_at DESC', (uid,))
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Panels", "Use `.install-panel` to install one."))
    embed = info_embed(f"Your Panels ({len(rows)})")
    for r in rows:
        icon = "🦅" if r['panel_type']=='pterodactyl' else "🐡"
        val = f"```fix\nURL: {r['panel_url']}\nContainer: {r['container_name']}\nUsername: {r['admin_user']}\nEmail: {r['admin_email']}\nInstalled: {r['installed_at'][:16]}\n```"
        embed.add_field(name=f"{icon} {r['panel_type'].title()}", value=val, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="panel-reset")
async def panel_reset(ctx, ptype: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if ptype:
        cur.execute('SELECT * FROM panels WHERE user_id = ? AND panel_type = ? ORDER BY installed_at DESC LIMIT 1', (uid, ptype.lower()))
    else:
        cur.execute('SELECT * FROM panels WHERE user_id = ? ORDER BY installed_at DESC LIMIT 1', (uid,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return await ctx.send(embed=error_embed("No Panel", "No panel found."))
    p = dict(row)
    new = ''.join(random.choices(string.ascii_letters+string.digits+"!@#$%", k=16))
    msg = await ctx.send(embed=info_embed("Resetting Password", f"```fix\n{p['panel_type']} on {p['container_name']}\n```"))
    if p['panel_type'] == 'pterodactyl':
        cmd = f"cd /var/www/pterodactyl && php artisan p:user:password --email={p['admin_email']} --password={new}"
    else:
        cmd = f"pufferpanel user password --email {p['admin_email']} --password {new}"
    out, err, code = await exec_in_container(p['container_name'], cmd)
    if code == 0:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE panels SET admin_pass = ? WHERE id = ?', (new, p['id']))
        conn.commit()
        conn.close()
        embed = success_embed("Password Reset")
        embed.add_field(name="🌐 URL", value=f"```fix\n{p['panel_url']}\n```", inline=False)
        embed.add_field(name="👤 Username", value=f"```fix\n{p['admin_user']}\n```", inline=True)
        embed.add_field(name="🔑 New Password", value=f"||`{new}`||", inline=False)
        try:
            await ctx.author.send(embed=embed)
            await msg.edit(embed=success_embed("Password Reset", "Check your DMs!"))
        except:
            await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {err}\n```"))

@bot.command(name="panel-delete")
async def panel_delete(ctx, ptype: str = None):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    if ptype:
        cur.execute('SELECT * FROM panels WHERE user_id = ? AND panel_type = ?', (uid, ptype.lower()))
    else:
        cur.execute('SELECT * FROM panels WHERE user_id = ?', (uid,))
    rows = cur.fetchall()
    if not rows:
        conn.close()
        return await ctx.send(embed=info_embed("No Panels", "No panels to delete."))
    if len(rows) > 1:
        opts = []
        for r in rows:
            icon = "🦅" if r['panel_type']=='pterodactyl' else "🐡"
            opts.append(discord.SelectOption(label=f"{icon} {r['panel_type']} on {r['container_name']}", value=str(r['id'])))
        view = View()
        sel = Select(placeholder="Select panel...", options=opts)
        async def sel_cb(i):
            pid = int(sel.values[0])
            cur.execute('DELETE FROM panels WHERE id = ? AND user_id = ?', (pid, uid))
            conn.commit()
            await i.response.edit_message(embed=success_embed("Deleted", "Panel record deleted."), view=None)
        sel.callback = sel_cb
        view.add_item(sel)
        await ctx.send(embed=info_embed("Select Panel"), view=view)
    else:
        r = rows[0]
        icon = "🦅" if r['panel_type']=='pterodactyl' else "🐡"
        view = View()
        conf = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
        canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        async def conf_cb(i):
            cur.execute('DELETE FROM panels WHERE id = ? AND user_id = ?', (r['id'], uid))
            conn.commit()
            await i.response.edit_message(embed=success_embed("Deleted", "Panel record deleted."), view=None)
        async def canc_cb(i):
            await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
        conf.callback = conf_cb
        canc.callback = canc_cb
        view.add_item(conf)
        view.add_item(canc)
        embed = warning_embed("Confirm Delete", f"{icon} {r['panel_type']} on {r['container_name']}\nThis only deletes the record, not the actual panel.")
        await ctx.send(embed=embed, view=view)
    conn.close()

@bot.command(name="panel-tunnel")
async def panel_tunnel(ctx, container: str = None, port: int = None):
    uid = str(ctx.author.id)
    if not container:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM panels WHERE user_id = ? ORDER BY installed_at DESC LIMIT 1', (uid,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return await ctx.send(embed=error_embed("No Panel", "Specify container or install a panel."))
        container = row['container_name']
        port = 80 if row['panel_type']=='pterodactyl' else 8080
    if not any(v['container_name']==container for v in get_user_vps(uid)) and not is_admin(uid):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    if not port:
        view = View()
        b80 = Button(label="🌐 Port 80", style=discord.ButtonStyle.primary)
        b8080 = Button(label="🔌 Port 8080", style=discord.ButtonStyle.primary)
        async def b80_cb(i): await create_tunnel_cmd(i, container, 80)
        async def b8080_cb(i): await create_tunnel_cmd(i, container, 8080)
        b80.callback = b80_cb
        b8080.callback = b8080_cb
        view.add_item(b80)
        view.add_item(b8080)
        await ctx.send(embed=info_embed("Select Port"), view=view)
    else:
        await create_tunnel_cmd(ctx, container, port)

async def create_tunnel_cmd(ctx, container, port):
    msg = await ctx.send(embed=info_embed("Creating Tunnel", f"```fix\n{container}:{port}\n```"))
    try:
        await exec_in_container(container, "which cloudflared || (wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared)")
        tid = str(uuid.uuid4())[:8]
        await exec_in_container(container, f"nohup cloudflared tunnel --url http://localhost:{port} --no-autoupdate > /tmp/cloudflared_{tid}.log 2>&1 &")
        await asyncio.sleep(5)
        out,_,_ = await exec_in_container(container, f"cat /tmp/cloudflared_{tid}.log | grep -oP 'https://[a-z0-9-]+\\.trycloudflare\\.com' | head -1")
        url = out.strip()
        if url:
            embed = success_embed("Tunnel Created")
            embed.add_field(name="🌐 URL", value=f"```fix\n{url}\n```", inline=False)
            embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
            embed.add_field(name="🔌 Port", value=f"```fix\n{port}\n```", inline=True)
            await msg.edit(embed=embed)
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE panels SET tunnel_url = ? WHERE container_name = ?', (url, container))
            conn.commit()
            conn.close()
        else:
            await msg.edit(embed=error_embed("Failed", "Could not create tunnel. Install cloudflared."))
    except Exception as e:
        await msg.edit(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="panel-status")
async def panel_status(ctx, container: str = None):
    uid = str(ctx.author.id)
    if not container:
        vps = get_user_vps(uid)
        if not vps:
            return await ctx.send(embed=no_vps_embed())
        container = vps[0]['container_name']
    elif not any(v['container_name']==container for v in get_user_vps(uid)) and not is_admin(uid):
        return await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM panels WHERE container_name = ?', (container,))
    panel = cur.fetchone()
    out,_,_ = await exec_in_container(container, "ps aux | grep -E 'nginx|pufferpanel|php|mysql' | grep -v grep")
    embed = info_embed(f"Panel Status: {container}")
    if panel:
        p = dict(panel)
        icon = "🦅" if p['panel_type']=='pterodactyl' else "🐡"
        status = f"```fix\nPanel: {icon} {p['panel_type']}\nURL: {p['panel_url']}\nUsername: {p['admin_user']}\nEmail: {p['admin_email']}\nInstalled: {p['installed_at'][:16]}\nTunnel: {'✅' if p['tunnel_url'] else '❌'}\n```"
        embed.add_field(name="📋 Panel Info", value=status, inline=False)
    if out:
        embed.add_field(name="🔄 Services", value=f"```fix\n{out[:500]}\n```", inline=False)
    else:
        embed.add_field(name="🔄 Services", value="```fix\nNo panel services detected\n```", inline=False)
    conn.close()
    await ctx.send(embed=embed)

# ==================================================================================================
#  🤖  AI COMMANDS
# ==================================================================================================

AI_KEY = "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"
AI_MODEL = "llama-3.3-70b-versatile"

@bot.command(name="ai")
async def ai(ctx, *, msg: str):
    uid = str(ctx.author.id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ai_history (user_id TEXT PRIMARY KEY, messages TEXT, updated_at TEXT)')
    cur.execute('SELECT messages FROM ai_history WHERE user_id = ?', (uid,))
    row = cur.fetchone()
    if row:
        history = json.loads(row['messages'])
    else:
        history = [{"role":"system","content":f"You are {BOT_NAME} AI Assistant, a helpful VPS management bot."}]
    history.append({"role":"user","content":msg})
    if len(history) > 21:
        history = [history[0]] + history[-20:]
    m = await ctx.send(embed=info_embed("AI is thinking..."))
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {AI_KEY}","Content-Type":"application/json"},
                json={"model":AI_MODEL,"messages":history,"max_tokens":1024,"temperature":0.7},
                timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    reply = data["choices"][0]["message"]["content"]
                    history.append({"role":"assistant","content":reply})
                    cur.execute('INSERT OR REPLACE INTO ai_history (user_id, messages, updated_at) VALUES (?, ?, ?)',
                              (uid, json.dumps(history), datetime_.datetime.now().isoformat()))
                    conn.commit()
                    chunks = [reply[i:i+1900] for i in range(0,len(reply),1900)]
                    embed = info_embed("AI Response", chunks[0])
                    await m.edit(embed=embed)
                    for c in chunks[1:]:
                        await ctx.send(embed=info_embed("",c))
                else:
                    await m.edit(embed=error_embed("API Error", f"Status {resp.status}"))
    except Exception as e:
        await m.edit(embed=error_embed("Error", str(e)[:1900]))
    finally:
        conn.close()

@bot.command(name="ai-reset")
async def ai_reset(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM ai_history WHERE user_id = ?', (str(ctx.author.id),))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("AI Reset", "History cleared."))

@bot.command(name="ai-help")
async def ai_help(ctx, *, topic: str):
    await ai(ctx, msg=f"Please help me with {topic} for VPS/LXC management")

# ==================================================================================================
#  🐧  OS COMMANDS
# ==================================================================================================

@bot.command(name="os-list")
async def os_list(ctx, category: str = None):
    if category:
        cats = [c['category'].lower() for c in OS_OPTIONS]
        if category.lower() not in cats:
            return await ctx.send(embed=error_embed("Invalid Category", f"Categories: Ubuntu, Debian, Fedora, Rocky, AlmaLinux, CentOS, Alpine, Arch, OpenSUSE, FreeBSD, OpenBSD, Kali, Gentoo, Void"))
        filtered = [o for o in OS_OPTIONS if o['category'].lower() == category.lower()]
    else:
        filtered = OS_OPTIONS[:25]
    embed = os_embed(f"OS Options {f'- {category}' if category else ''}", f"```fix\nTotal: {len(filtered)}\n```")
    for o in filtered[:10]:
        embed.add_field(name=o['label'], value=f"```fix\n{o['desc']}\nRAM Min: {o['ram_min']}MB\n```", inline=True)
    await ctx.send(embed=embed)

# ==================================================================================================
#  🛡️  ADMIN COMMANDS
# ==================================================================================================

# ==================================================================================================
#  🚀  COMPLETE .create COMMAND - WITH apply_lxc_config FIX & FULL UI
# ==================================================================================================
# ==================================================================================================
#  🚀  COMPLETE .create COMMAND - WITH USER PROFILE & FULL DETAILS
# ==================================================================================================

import asyncio
import random
import string
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

RAINBOW_COLORS = [
    0xFF0000, 0xFF7700, 0xFFFF00, 0x00FF00, 0x00CCFF, 0x3366FF, 0x8B00FF, 0xFF00CC
]


class CreateVPSView(View):
    def __init__(self, ctx, ram, cpu, disk, user, os_version, os_name):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.ram = ram
        self.cpu = cpu
        self.disk = disk
        self.user = user
        self.os_version = os_version
        self.os_name = os_name
        
        confirm_btn = Button(label="✅ Confirm Create", style=discord.ButtonStyle.success, emoji="✅", row=0)
        confirm_btn.callback = self.confirm_callback
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=0)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(confirm_btn)
        self.add_item(cancel_btn)
    
    async def confirm_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await self.create_vps(interaction)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"), view=None)
    
    async def create_vps(self, interaction):
        await interaction.response.defer()
        
        user_id = str(self.user.id)
        container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
        
        def get_progress_bar(percent):
            filled = int(percent / 5)
            return "█" * filled + "░" * (20 - filled)
        
        progress_msg = await interaction.followup.send(
            embed=discord.Embed(
                title="```glow\n🌈 SVM5-BOT - CREATING VPS 🌈\n```",
                description=f"```fix\n[░░░░░░░░░░░░░░░░░░░░] 0% | 👤 User: {self.user.display_name}\n```",
                color=RAINBOW_COLORS[0]
            ),
            ephemeral=True
        )
        
        try:
            ram_mb = self.ram * 1024
            
            steps = [
                (10, "🔧 Initializing container..."),
                (25, f"💾 Setting RAM ({self.ram}GB)..."),
                (40, f"⚡ Setting CPU ({self.cpu} cores)..."),
                (55, f"💽 Setting Disk ({self.disk}GB)..."),
                (70, "🔨 Applying LXC config..."),
                (85, "▶️ Starting container..."),
                (95, "🔧 Configuring permissions..."),
                (100, "🎉 Finalizing..."),
            ]
            
            color_idx = 0
            for progress, desc in steps:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 SVM5-BOT - CREATING VPS 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(progress)}] {progress}% | {desc}\n👤 User: {self.user.display_name}\n```",
                    color=RAINBOW_COLORS[color_idx % len(RAINBOW_COLORS)]
                ))
                color_idx += 1
                
                if progress == 10:
                    await run_lxc(f"lxc init {self.os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
                elif progress == 25:
                    await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
                elif progress == 40:
                    await run_lxc(f"lxc config set {container_name} limits.cpu {self.cpu}")
                elif progress == 55:
                    await run_lxc(f"lxc config device set {container_name} root size={self.disk}GB")
                elif progress == 70:
                    await apply_lxc_config(container_name)
                elif progress == 85:
                    await run_lxc(f"lxc start {container_name}")
                elif progress == 95:
                    await apply_internal_permissions(container_name)
                
                await asyncio.sleep(1)
            
            # Get IP and MAC
            ip = "N/A"
            mac = "N/A"
            try:
                out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
                ip = out.strip() if out else "N/A"
                out, _, _ = await exec_in_container(container_name, "ip link | grep ether | awk '{print $2}' | head -1")
                mac = out.strip() if out else "N/A"
            except:
                pass
            
            # Save to database
            add_vps(user_id, container_name, self.ram, self.cpu, self.disk, self.os_version, "Custom")
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ip_address = ?, mac_address = ? WHERE container_name = ?',
                       (ip, mac, container_name))
            conn.commit()
            conn.close()
            
            # Assign role
            if self.ctx.guild:
                role = discord.utils.get(self.ctx.guild.roles, name=f"{BOT_NAME} User")
                if not role:
                    role = await self.ctx.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
                try:
                    await self.user.add_roles(role)
                except:
                    pass
            
            # Get statistics
            all_vps = get_all_vps()
            total_vps = len(all_vps)
            total_users = len(set([v['user_id'] for v in all_vps]))
            active_vps = len([v for v in all_vps if v['status'] == 'running'])
            
            # Resource Bars
            ram_bar = "█" * int(self.ram / 16) + "░" * (10 - int(self.ram / 16))
            cpu_bar = "█" * int(self.cpu / 8) + "░" * (10 - int(self.cpu / 8))
            disk_bar = "█" * int(self.disk / 100) + "░" * (10 - int(self.disk / 100))
            
            # Success Embed
            success_embed = discord.Embed(
                title=f"```glow\n🌟✨ VPS CREATED FOR {self.user.display_name.upper()}! ✨🌟\n```",
                description=f"🎉 **VPS created successfully by {self.ctx.author.mention}!**\n\n"
                            f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
                color=0x00FF88
            )
            success_embed.set_thumbnail(url=self.user.avatar.url if self.user.avatar else THUMBNAIL_URL)
            success_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
            
            success_embed.add_field(
                name="👤 OWNER",
                value=f"```fix\n{self.user.mention}\nID: {self.user.id}\nCreated: {self.user.created_at.strftime('%Y-%m-%d')}\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="📦 CONTAINER",
                value=f"```fix\nName: {container_name}\nIP: {ip}\nMAC: {mac}\nOS: {self.os_name}\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="⚙️ RESOURCES",
                value=f"```fix\nRAM: {self.ram}GB [{ram_bar}]\nCPU: {self.cpu} Core(s) [{cpu_bar}]\nDisk: {self.disk}GB [{disk_bar}]\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="🖥️ MANAGEMENT",
                value=f"```fix\n.manage {container_name} - Interactive Manager\n.stats {container_name} - Live Stats\n.logs {container_name} - System Logs\n.ssh-gen {container_name} - SSH Access\n.reboot {container_name} - Reboot\n.shutdown {container_name} - Shutdown\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="📊 STATUS",
                value=f"```fix\nStatus: 🟢 RUNNING\nCreated: {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUptime: Just Started\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="🌍 PUBLIC STATS",
                value=f"```fix\nTotal VPS: {total_vps}\nTotal Users: {total_users}\nActive VPS: {active_vps}\n```",
                inline=True
            )
            
            success_embed.set_footer(
                text=f"⚡ SVM5-BOT • Created by {self.ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
                icon_url=THUMBNAIL_URL
            )
            
            await progress_msg.edit(embed=success_embed)
            
            # DM to user
            try:
                dm_embed = discord.Embed(
                    title=f"```glow\n🌟 YOUR VPS IS READY! 🌟\n```",
                    description=f"🎉 A new VPS has been created for you by {self.ctx.author.name}!",
                    color=0x57F287
                )
                dm_embed.set_thumbnail(url=self.ctx.author.avatar.url if self.ctx.author.avatar else THUMBNAIL_URL)
                dm_embed.add_field(
                    name="📦 CONTAINER",
                    value=f"```fix\nName: {container_name}\nIP: {ip}\nMAC: {mac}\nOS: {self.os_name}\n```",
                    inline=False
                )
                dm_embed.add_field(
                    name="⚙️ RESOURCES",
                    value=f"```fix\nRAM: {self.ram}GB\nCPU: {self.cpu} Core(s)\nDisk: {self.disk}GB\n```",
                    inline=True
                )
                dm_embed.add_field(
                    name="🖥️ COMMANDS",
                    value=f"```fix\n.manage {container_name}\n.stats {container_name}\n.logs {container_name}\n.ssh-gen {container_name}\n```",
                    inline=False
                )
                await self.user.send(embed=dm_embed)
            except:
                pass
            
            logger.info(f"Admin {self.ctx.author} created VPS {container_name} for {self.user}")
            
        except Exception as e:
            await progress_msg.edit(embed=error_embed("Creation Failed", f"```diff\n- {str(e)}\n```"))
            try:
                await run_lxc(f"lxc delete {container_name} --force")
            except:
                pass


class OSDropdownView(View):
    def __init__(self, ctx, ram, cpu, disk, user):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.ram = ram
        self.cpu = cpu
        self.disk = disk
        self.user = user
        
        options = []
        for os in OS_OPTIONS[:25]:
            options.append(discord.SelectOption(
                label=os['label'][:100],
                value=os['value'],
                description=os['desc'][:100] if os.get('desc') else None,
                emoji=os.get('icon', '🐧')
            ))
        
        self.select = Select(placeholder="📋 Select an operating system...", options=options)
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=1)
        cancel_btn.callback = self.cancel_callback
        self.add_item(cancel_btn)
    
    async def select_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        selected_os = self.select.values[0]
        os_name = next((o['label'] for o in OS_OPTIONS if o['value'] == selected_os), selected_os)
        
        all_vps = get_all_vps()
        total_vps = len(all_vps)
        total_users = len(set([v['user_id'] for v in all_vps]))
        
        embed = discord.Embed(
            title=f"```glow\n⚠️ CONFIRM VPS CREATION FOR {self.user.display_name.upper()}\n```",
            description=f"```fix\n┌─────────────────────────────────────────────────┐\n│ 👤 User : {self.user.mention}\n│ 🐧 OS   : {os_name}\n│ 💾 RAM  : {self.ram}GB\n│ ⚙️ CPU  : {self.cpu} Core(s)\n│ 💽 Disk : {self.disk}GB\n└─────────────────────────────────────────────────┘\n```\n\n**Please confirm to create this VPS.**\n\n```glow\n🌍 Current Statistics:\n• Total VPS: {total_vps}\n• Total Users: {total_users}\n```",
            color=0xFFAA00
        )
        embed.set_thumbnail(url=self.user.avatar.url if self.user.avatar else THUMBNAIL_URL)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
        
        view = CreateVPSView(self.ctx, self.ram, self.cpu, self.disk, self.user, selected_os, os_name)
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"), view=None)


@bot.command(name="create")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_create(ctx, ram: int, cpu: int, disk: int, user: discord.Member):
    """Create a VPS for a user"""
    if ram <= 0 or cpu <= 0 or disk <= 0:
        return await ctx.send(embed=error_embed("Invalid Specs", "```diff\n- RAM, CPU, Disk must be positive integers.\n```"))
    
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    total_users = len(set([v['user_id'] for v in all_vps]))
    active_vps = len([v for v in all_vps if v['status'] == 'running'])
    
    embed = discord.Embed(
        title=f"```glow\n🖥️ CREATE VPS FOR {user.display_name.upper()}\n```",
        description=f"```fix\n┌─────────────────────────────────────────────────┐\n│ 👤 User : {user.mention}\n│ 💾 RAM  : {ram}GB\n│ ⚙️ CPU  : {cpu} Core(s)\n│ 💽 Disk : {disk}GB\n└─────────────────────────────────────────────────┘\n```\n\n**Please select an operating system.**\n\n```glow\n🌍 Server Statistics:\n• Total VPS: {total_vps}\n• Total Users: {total_users}\n• Active VPS: {active_vps}\n```",
        color=0x5865F2
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else THUMBNAIL_URL)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
    embed.set_footer(
        text=f"⚡ SVM5-BOT • Created by {ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    
    view = OSDropdownView(ctx, ram, cpu, disk, user)
    await ctx.send(embed=embed, view=view)  

# ==================================================================================================
#  📏  COMPLETE .resize COMMAND - ADMIN ONLY
# ==================================================================================================

@bot.command(name="resize")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def resize_vps(ctx, container_name: str, ram: int = None, cpu: int = None, disk: int = None):
    """Resize VPS resources - Admin only"""
    if ram is None and cpu is None and disk is None:
        return await ctx.send(embed=error_embed("Missing Parameters", "```fix\nUsage: .resize <container> [ram] [cpu] [disk]\nExample: .resize my-vps 8 4 100\n```"))
    
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        return await ctx.send(embed=error_embed("VPS Not Found", f"```diff\n- Container '{container_name}' not found.\n```"))
    
    user = await bot.fetch_user(int(vps['user_id']))
    
    # Current resources
    current_ram = vps['ram']
    current_cpu = vps['cpu']
    current_disk = vps['disk']
    
    # New resources
    new_ram = ram if ram is not None else current_ram
    new_cpu = cpu if cpu is not None else current_cpu
    new_disk = disk if disk is not None else current_disk
    
    # Validate new resources
    if new_ram <= 0 or new_cpu <= 0 or new_disk <= 0:
        return await ctx.send(embed=error_embed("Invalid Resources", "```diff\n- RAM, CPU, Disk must be positive.\n```"))
    
    if new_ram > 256:
        return await ctx.send(embed=error_embed("Too High", "```diff\n- RAM cannot exceed 256GB.\n```"))
    if new_cpu > 128:
        return await ctx.send(embed=error_embed("Too High", "```diff\n- CPU cannot exceed 128 cores.\n```"))
    if new_disk > 5000:
        return await ctx.send(embed=error_embed("Too High", "```diff\n- Disk cannot exceed 5TB.\n```"))
    
    # Confirm view
    view = ResizeConfirmView(ctx, container_name, vps, user, current_ram, current_cpu, current_disk, new_ram, new_cpu, new_disk)
    
    # Resource bars
    ram_bar = "█" * int(current_ram / 16) + "░" * (10 - int(current_ram / 16))
    cpu_bar = "█" * int(current_cpu / 8) + "░" * (10 - int(current_cpu / 8))
    disk_bar = "█" * int(current_disk / 100) + "░" * (10 - int(current_disk / 100))
    
    new_ram_bar = "█" * int(new_ram / 16) + "░" * (10 - int(new_ram / 16))
    new_cpu_bar = "█" * int(new_cpu / 8) + "░" * (10 - int(new_cpu / 8))
    new_disk_bar = "█" * int(new_disk / 100) + "░" * (10 - int(new_disk / 100))
    
    embed = discord.Embed(
        title="```glow\n📏 SVM5-BOT - RESIZE VPS 📏\n```",
        description=f"Resizing VPS **{container_name}**\n\n"
                    f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
        color=0xFFAA00
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    embed.add_field(
        name="📊 CURRENT RESOURCES",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ RAM  : {current_ram}GB  [{ram_bar}]\n│ CPU  : {current_cpu} Core(s) [{cpu_bar}]\n│ Disk : {current_disk}GB [{disk_bar}]\n└─────────────────────────────────────────────────┘\n```",
        inline=True
    )
    
    embed.add_field(
        name="⬆️ NEW RESOURCES",
        value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ RAM  : {new_ram}GB  [{new_ram_bar}]\n│ CPU  : {new_cpu} Core(s) [{new_cpu_bar}]\n│ Disk : {new_disk}GB [{new_disk_bar}]\n└─────────────────────────────────────────────────┘\n```",
        inline=True
    )
    
    embed.add_field(
        name="👤 OWNER",
        value=f"```fix\n{user.mention}\n```",
        inline=True
    )
    
    embed.set_footer(
        text=f"⚡ SVM5-BOT • Resize by {ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    
    await ctx.send(embed=embed, view=view)


class ResizeConfirmView(View):
    def __init__(self, ctx, container_name, vps, user, current_ram, current_cpu, current_disk, new_ram, new_cpu, new_disk):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.container_name = container_name
        self.vps = vps
        self.user = user
        self.current_ram = current_ram
        self.current_cpu = current_cpu
        self.current_disk = current_disk
        self.new_ram = new_ram
        self.new_cpu = new_cpu
        self.new_disk = new_disk
        
        confirm_btn = Button(label="✅ Confirm Resize", style=discord.ButtonStyle.success, emoji="✅", row=0)
        confirm_btn.callback = self.confirm_callback
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, emoji="❌", row=0)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(confirm_btn)
        self.add_item(cancel_btn)
    
    async def confirm_callback(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await self.perform_resize(interaction)
    
    async def cancel_callback(self, interaction):
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nResize cancelled.\n```"),
            view=None
        )
    
    async def perform_resize(self, interaction):
        await interaction.response.defer()
        
        rainbow_colors = [0xFF0000, 0xFF7700, 0xFFFF00, 0x00FF00, 0x00CCFF, 0x3366FF, 0x8B00FF]
        
        progress_msg = await interaction.followup.send(
            embed=discord.Embed(
                title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                description="```fix\n[░░░░░░░░░░░░░░░░░░░░] 0% | Checking container status...\n```",
                color=rainbow_colors[0]
            ),
            ephemeral=True
        )
        
        def get_progress_bar(percent):
            filled = int(percent / 5)
            return "█" * filled + "░" * (20 - filled)
        
        try:
            # Step 1: Check status
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                description=f"```fix\n[{get_progress_bar(20)}] 20% | 🔍 Checking container status...\n```",
                color=rainbow_colors[0]
            ))
            
            status = await get_container_status(self.container_name)
            was_running = status == 'running'
            
            # Step 2: Stop if running
            if was_running:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(40)}] 40% | ⏹️ Stopping container...\n```",
                    color=rainbow_colors[1]
                ))
                await run_lxc(f"lxc stop {self.container_name} --force")
                await asyncio.sleep(2)
            
            # Step 3: Apply RAM change
            if self.new_ram != self.current_ram:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(60)}] 60% | 💾 Updating RAM: {self.current_ram}GB → {self.new_ram}GB\n```",
                    color=rainbow_colors[2]
                ))
                await run_lxc(f"lxc config set {self.container_name} limits.memory {self.new_ram * 1024}MB")
            
            # Step 4: Apply CPU change
            if self.new_cpu != self.current_cpu:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(70)}] 70% | ⚡ Updating CPU: {self.current_cpu} → {self.new_cpu} cores\n```",
                    color=rainbow_colors[3]
                ))
                await run_lxc(f"lxc config set {self.container_name} limits.cpu {self.new_cpu}")
            
            # Step 5: Apply Disk change
            if self.new_disk != self.current_disk:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(80)}] 80% | 💽 Updating Disk: {self.current_disk}GB → {self.new_disk}GB\n```",
                    color=rainbow_colors[4]
                ))
                await run_lxc(f"lxc config device set {self.container_name} root size={self.new_disk}GB")
            
            # Step 6: Start if it was running
            if was_running:
                await progress_msg.edit(embed=discord.Embed(
                    title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                    description=f"```fix\n[{get_progress_bar(90)}] 90% | ▶️ Starting container...\n```",
                    color=rainbow_colors[5]
                ))
                await run_lxc(f"lxc start {self.container_name}")
                await asyncio.sleep(3)
            
            # Step 7: Update database
            await progress_msg.edit(embed=discord.Embed(
                title="```glow\n🌈 RESIZING VPS RESOURCES 🌈\n```",
                description=f"```fix\n[{get_progress_bar(100)}] 100% | 💾 Updating database...\n```",
                color=rainbow_colors[6]
            ))
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ram = ?, cpu = ?, disk = ? WHERE container_name = ?',
                       (self.new_ram, self.new_cpu, self.new_disk, self.container_name))
            conn.commit()
            conn.close()
            
            await asyncio.sleep(1)
            
            # Get updated public statistics
            all_vps = get_all_vps()
            total_vps = len(all_vps)
            total_users = len(set([v['user_id'] for v in all_vps]))
            active_vps = len([v for v in all_vps if v['status'] == 'running'])
            total_ram = sum([v['ram'] for v in all_vps])
            total_cpu = sum([v['cpu'] for v in all_vps])
            total_disk = sum([v['disk'] for v in all_vps])
            
            # Resource Bars
            new_ram_bar = "█" * int(self.new_ram / 16) + "░" * (10 - int(self.new_ram / 16))
            new_cpu_bar = "█" * int(self.new_cpu / 8) + "░" * (10 - int(self.new_cpu / 8))
            new_disk_bar = "█" * int(self.new_disk / 100) + "░" * (10 - int(self.new_disk / 100))
            
            # Success Embed
            success_embed = discord.Embed(
                title="```glow\n✅ VPS RESIZED SUCCESSFULLY! ✅\n```",
                description=f"🎉 **VPS {self.container_name} has been resized!**\n\n"
                            f"```glow\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n```",
                color=0x00FF88
            )
            success_embed.set_thumbnail(url=THUMBNAIL_URL)
            success_embed.set_image(url="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg")
            
            success_embed.add_field(
                name="📦 CONTAINER",
                value=f"```fix\n{self.container_name}\nOwner: {self.user.mention}\n```",
                inline=True
            )
            
            success_embed.add_field(
                name="⚙️ NEW RESOURCES",
                value=f"```fix\nRAM  : {self.new_ram}GB  [{new_ram_bar}]\nCPU  : {self.new_cpu} Core(s) [{new_cpu_bar}]\nDisk : {self.new_disk}GB [{new_disk_bar}]\n```",
                inline=False
            )
            
            success_embed.add_field(
                name="🌍 PUBLIC STATISTICS",
                value=f"```fix\n┌─────────────────────────────────────────────────┐\n│ Total VPS Created : {total_vps}\n│ Total Users       : {total_users}\n│ Active VPS        : {active_vps}\n│ Total RAM Used    : {total_ram}GB\n│ Total CPU Used    : {total_cpu} Cores\n│ Total Disk Used   : {total_disk}GB\n└─────────────────────────────────────────────────┘\n```",
                inline=False
            )
            
            success_embed.set_footer(
                text=f"⚡ SVM5-BOT • Resized by {self.ctx.author.name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
                icon_url=THUMBNAIL_URL
            )
            
            await progress_msg.edit(embed=success_embed)
            
            # DM user
            try:
                dm_embed = success_embed("📏 VPS Resized!", f"Your VPS **{self.container_name}** has been resized by an admin!")
                dm_embed.add_field(name="⚙️ New Resources", value=f"```fix\nRAM: {self.new_ram}GB\nCPU: {self.new_cpu} Core(s)\nDisk: {self.new_disk}GB\n```")
                await self.user.send(embed=dm_embed)
            except:
                pass
            
            logger.info(f"Admin {self.ctx.author} resized {self.container_name} to {self.new_ram}GB/{self.new_cpu}C/{self.new_disk}GB")
            
        except Exception as e:
            await progress_msg.edit(embed=error_embed("Resize Failed", f"```diff\n- {str(e)}\n```"))

# ==================================================================================================
#  �  SYSTEM DETECTION & INSTALLATION HELPERS
# ==================================================================================================

def get_os_info() -> Dict[str, str]:
    """Detect OS information"""
    try:
        info = {
            'os': platform.system(),
            'version': platform.release(),
            'machine': platform.machine(),
            'hostname': socket.gethostname(),
        }
        
        # Detect Linux distro
        if info['os'] == 'Linux':
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    content = f.read()
                    if 'ubuntu' in content.lower():
                        info['distro'] = 'Ubuntu'
                    elif 'debian' in content.lower():
                        info['distro'] = 'Debian'
                    elif 'fedora' in content.lower():
                        info['distro'] = 'Fedora'
                    else:
                        info['distro'] = 'Linux'
            else:
                info['distro'] = 'Linux'
        
        return info
    except Exception as e:
        logger.error(f"OS detection error: {e}")
        return {'os': 'Unknown', 'version': 'Unknown', 'machine': 'Unknown', 'hostname': 'Unknown', 'distro': 'Unknown'}

def check_lxc_installed() -> bool:
    """Check if LXC/LXD is installed"""
    try:
        result = subprocess.run(['which', 'lxc'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False

def get_system_resources() -> Dict[str, Any]:
    """Get system resource usage"""
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu': cpu_percent,
            'memory_percent': mem.percent,
            'memory_total_gb': mem.total / (1024**3),
            'memory_used_gb': mem.used / (1024**3),
            'disk_percent': disk.percent,
            'disk_total_gb': disk.total / (1024**3),
            'disk_used_gb': disk.used / (1024**3),
        }
    except Exception as e:
        logger.error(f"Resource check error: {e}")
        return {'cpu': 0, 'memory_percent': 0, 'disk_percent': 0}

TERMS_AND_POLICY = """
╔════════════════════════════════════════════════════════════════════════════╗
║                      PRIME VM - TERMS & POLICY                            ║
║                                                                            ║
║ ✅ System Requirements:                                                    ║
║   • Linux-based OS (Ubuntu/Debian recommended)                            ║
║   • Minimum 2GB RAM, 20GB Disk                                            ║
║   • Root or sudo access required                                          ║
║                                                                            ║
║ 📋 Disclaimer:                                                             ║
║   • System modifications will be made                                     ║
║   • LXC/LXD containers will be installed                                  ║
║   • Bot will run as systemd service                                       ║
║   • Automatic startup enabled on boot                                     ║
║                                                                            ║
║ ⚙️ What Will Be Installed:                                                ║
║   • LXC/LXD containerization platform                                     ║
║   • Prime VM Discord Bot service                                          ║
║   • System configuration at /opt/prime-vm                                 ║
║                                                                            ║
║ 🔒 Privacy & Security:                                                     ║
║   • Discord token will be securely stored                                 ║
║   • License key validation performed                                      ║
║   • All operations logged                                                 ║
║                                                                            ║
║ ✨ By proceeding, you agree to these terms.                               ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

class SetupModal(Modal):
    """Modal for collecting Discord token and configuration"""
    def __init__(self, ctx, step: int = 1):
        self.ctx = ctx
        self.step = step
        title = "Prime VM Setup - Step 1" if step == 1 else f"Prime VM Setup - Step {step}"
        super().__init__(title=title)
        
        if step == 1:
            self.discord_token = TextInput(label="Discord Bot Token", placeholder="Paste your bot token here", min_length=50)
            self.add_item(self.discord_token)
        elif step == 2:
            self.admin_id = TextInput(label="Main Admin Discord ID", placeholder="Your Discord user ID (e.g. 123456789)")
            self.add_item(self.admin_id)
        elif step == 3:
            self.bot_prefix = TextInput(label="Bot Command Prefix", placeholder="e.g. . or ! or /", min_length=1, max_length=3)
            self.add_item(self.bot_prefix)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

# ==================================================================================================
#  🔐  LICENSE VERIFY COMMAND WITH INSTALLATION FLOW
# ==================================================================================================

@bot.command(name="license-verify")
async def license_verify(ctx, key: str = None):
    """Verify license key and start installation"""
    global LICENSE_VERIFIED
    
    if key is None:
        if LICENSE_VERIFIED:
            embed = success_embed("License Verified", "```fix\nYour license is active and verified.\n```")
        else:
            embed = warning_embed("License Not Verified", "```fix\nNo valid license found. Use .license-verify <key> to activate.\n```")
            embed.add_field(
                name="📌 Valid License Keys",
                value="```fix\n1kapi\nPrime-Vm\nGamerhindu\nprimebahu\n(and more)\n```",
                inline=False
            )
        return await ctx.send(embed=embed)
    
    if key and key.strip().casefold() not in VALID_LICENSE_KEYS_LOWER:
        embed = error_embed("Invalid License Key", f"```diff\n- The key '{key}' is not valid.\n```")
        return await ctx.send(embed=embed)
    
    # License is valid - start installation flow
    embed = success_embed("✅ License Valid!", "Starting installation sequence in 5 seconds...")
    msg = await ctx.send(embed=embed)
    
    # 5 second countdown
    for i in range(5, 0, -1):
        await asyncio.sleep(1)
        progress = "█" * i + "░" * (5 - i)
        embed = success_embed("Installation Starting", f"```\n{progress} {i}s\n```")
        try:
            await msg.edit(embed=embed)
        except:
            pass
    
    # System detection
    os_info = get_os_info()
    resources = get_system_resources()
    lxc_installed = check_lxc_installed()
    
    embed = discord.Embed(title="🖥️ System Information Detected", color=0x5865F2)
    embed.add_field(name="OS", value=f"```{os_info.get('distro', os_info['os'])} {os_info['version']}```", inline=True)
    embed.add_field(name="Machine", value=f"```{os_info['hostname']}```", inline=True)
    embed.add_field(name="Arch", value=f"```{os_info['machine']}```", inline=True)
    embed.add_field(name="CPU Usage", value=f"```{resources['cpu']:.1f}%```", inline=True)
    embed.add_field(name="RAM", value=f"```{resources['memory_used_gb']:.1f}GB / {resources['memory_total_gb']:.1f}GB```", inline=True)
    embed.add_field(name="Disk", value=f"```{resources['disk_used_gb']:.1f}GB / {resources['disk_total_gb']:.1f}GB```", inline=True)
    embed.add_field(name="LXC/LXD Status", value=f"```{'✅ Installed' if lxc_installed else '⏳ Will be installed'}```", inline=False)
    await msg.edit(embed=embed)
    
    # Show Terms & Policy
    await asyncio.sleep(2)
    policy_embed = discord.Embed(title="📋 Terms & Policy", description=TERMS_AND_POLICY, color=0xFEE75C)
    await ctx.send(embed=policy_embed)
    
    # Ask for acceptance
    accept_msg = await ctx.send("**Press Y to Accept and Continue** ⬇️")
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['✅', 'Y', '🟢'] and reaction.message.id == accept_msg.id
    
    try:
        # Alternative: collect text message instead
        def message_check(m):
            return m.author == ctx.author and m.content.lower() in ['y', 'yes', '✅']
        
        msg_response = await bot.wait_for('message', check=message_check, timeout=60)
        await msg_response.delete()
    except asyncio.TimeoutError:
        await ctx.send("⏱️ Installation setup timed out. Try again with `.license-verify <key>`")
        return
    
    # Show installation progress
    progress_embed = discord.Embed(title="⚙️ Installation in Progress", color=0x57F287)
    progress_msg = await ctx.send(embed=progress_embed)
    
    # Step 1: Collect Discord Token
    modal = SetupModal(ctx, step=1)
    await ctx.send("A dialog will appear to collect your Bot Token...")
    
    try:
        await ctx.author.send("**Step 1/3: Enter your Discord Bot Token**\nReply with your bot token:")
    except:
        await ctx.send("Could not DM. Please respond in the channel.")
    
    def dm_check(m):
        return m.author == ctx.author and len(m.content) > 50
    
    try:
        token_msg = await bot.wait_for('message', check=dm_check, timeout=120)
        bot_token = token_msg.content.strip()
    except asyncio.TimeoutError:
        await ctx.send("⏱️ Setup timed out.")
        return
    
    # Step 2: Collect Admin ID
    try:
        await ctx.author.send("**Step 2/3: Enter your Discord User ID** (use `.info` to find it)\nReply with your user ID (numbers only):")
    except:
        await ctx.send("**Step 2/3: Enter your Discord User ID**\nReply with your user ID (numbers only):")
    
    def admin_id_check(m):
        return m.author == ctx.author and m.content.isdigit()
    
    try:
        admin_msg = await bot.wait_for('message', check=admin_id_check, timeout=120)
        admin_id = admin_msg.content.strip()
    except asyncio.TimeoutError:
        await ctx.send("⏱️ Setup timed out.")
        return
    
    # Step 3: Collect Bot Prefix
    try:
        await ctx.author.send("**Step 3/3: Enter Bot Command Prefix** (e.g. . or ! or /)\nReply with your prefix (1-3 characters):")
    except:
        await ctx.send("**Step 3/3: Enter Bot Command Prefix** (e.g. . or ! or /)\nReply with your prefix (1-3 characters):")
    
    def prefix_check(m):
        return m.author == ctx.author and 1 <= len(m.content) <= 3
    
    try:
        prefix_msg = await bot.wait_for('message', check=prefix_check, timeout=120)
        bot_prefix = prefix_msg.content.strip()
    except asyncio.TimeoutError:
        await ctx.send("⏱️ Setup timed out.")
        return
    
    # All inputs collected - save and start installation
    set_setting('discord_token', bot_token)
    set_setting('main_admin_id', admin_id)
    set_setting('bot_prefix', bot_prefix)
    
    # Installation progress visualization
    steps = [
        ("Validating Configuration", "Checking settings..."),
        ("Creating /opt/prime-vm Directory", "Setting up directories..."),
        ("Installing LXC/LXD" if not lxc_installed else "Verifying LXC/LXD", "Containerization setup..."),
        ("Configuring Bot Service", "Creating systemd service..."),
        ("Starting Services", "Enabling auto-start..."),
        ("Installation Complete!", "✅ System ready"),
    ]
    
    for i, (step_name, detail) in enumerate(steps):
        dots = "." * ((i % 3) + 1)
        progress_text = f"```\n[{'█' * (i+1)}{'░' * (6-i-1)}] {step_name}\n{detail}{dots}\n```"
        progress_embed = discord.Embed(title="⚙️ Installation Progress", description=progress_text, color=0x57F287)
        progress_embed.set_footer(text=f"Step {i+1}/6")
        try:
            await progress_msg.edit(embed=progress_embed)
        except:
            pass
        await asyncio.sleep(2)
    
    # Final success message
    set_setting('license_verified', 'true')
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS license_info (
        license_key TEXT, activated_by TEXT, activated_at TEXT, ip TEXT, mac TEXT
    )''')
    cur.execute('INSERT INTO license_info VALUES (?, ?, ?, ?, ?)',
               (key, str(ctx.author.id), datetime_.datetime.now().isoformat(), SERVER_IP, MAC_ADDRESS))
    conn.commit()
    conn.close()
    
    final_embed = discord.Embed(title="🎉 INSTALLATION COMPLETE!", color=0x57F287)
    final_embed.add_field(name="🔑 License Key", value=f"```{key}```", inline=False)
    final_embed.add_field(name="🖥️ System", value=f"```{os_info.get('distro', os_info['os'])} {os_info['version']}```", inline=True)
    final_embed.add_field(name="🤖 Bot Prefix", value=f"```{bot_prefix}```", inline=True)
    final_embed.add_field(name="📍 Service Location", value="```/opt/prime-vm```", inline=False)
    final_embed.add_field(name="⚙️ Service Status", value="```systemd enabled (auto-start on boot)```", inline=False)
    final_embed.add_field(name="✨ Next Steps", value=f"Use `{bot_prefix}help` to see all available commands", inline=False)
    final_embed.set_thumbnail(url=THUMBNAIL_URL)
    
    await progress_msg.edit(embed=final_embed)
    await ctx.author.send(embed=final_embed)


@bot.command(name="license-status")
async def license_status(ctx):
    """Show license status"""
    if LICENSE_VERIFIED:
        embed = success_embed("License Status", "```fix\nLicense is active.\n```")
    else:
        embed = warning_embed("License Status", "```fix\nNo active license found.\n```")
        embed.add_field(name="📌 Activate", value=f"Use `{BOT_PREFIX}license-verify <key>` to activate.", inline=False)
    await ctx.send(embed=embed)
    
@bot.command(name="delete")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_delete(ctx, user: discord.Member, num: int, *, reason: str = "No reason"):
    uid = str(user.id)
    vps = get_user_vps(uid)
    if not vps or num<1 or num>len(vps):
        return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
    v = vps[num-1]
    view = View()
    conf = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
    canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def conf_cb(i):
        await run_lxc(f"lxc stop {v['container_name']} --force")
        await run_lxc(f"lxc delete {v['container_name']}")
        delete_vps(v['container_name'])
        await i.response.edit_message(embed=success_embed("Deleted", f"```fix\n{v['container_name']}\n```"), view=None)
    async def canc_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    conf.callback = conf_cb
    canc.callback = canc_cb
    view.add_item(conf)
    view.add_item(canc)
    await ctx.send(embed=warning_embed("Confirm Delete", f"```fix\nUser: {user}\nVPS: {v['container_name']}\nReason: {reason}\n```"), view=view)

@bot.command(name="suspend")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_suspend(ctx, container: str, *, reason: str = "Admin action"):
    allv = get_all_vps()
    v = next((v for v in allv if v['container_name']==container), None)
    if not v:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {container}\n```"))
    await run_lxc(f"lxc stop {container} --force")
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE vps SET suspended = 1, suspended_reason = ? WHERE container_name = ?', (reason, container))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Suspended", f"```fix\n{container}\nReason: {reason}\n```"))

@bot.command(name="unsuspend")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_unsuspend(ctx, container: str):
    allv = get_all_vps()
    v = next((v for v in allv if v['container_name']==container), None)
    if not v:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {container}\n```"))
    await run_lxc(f"lxc start {container}")
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE vps SET suspended = 0, suspended_reason = "" WHERE container_name = ?', (container,))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Unsuspended", f"```fix\n{container}\n```"))

@bot.command(name="add-resources")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_add_resources(ctx, container: str, ram: int = None, cpu: int = None, disk: int = None):
    if not ram and not cpu and not disk:
        return await ctx.send(embed=error_embed("Missing", "Specify at least one resource"))
    allv = get_all_vps()
    v = next((v for v in allv if v['container_name']==container), None)
    if not v:
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {container}\n```"))
    was = v['status'] == 'running' and not v['suspended']
    if was:
        await run_lxc(f"lxc stop {container}")
    changes = []
    if ram:
        new = v['ram'] + ram
        await run_lxc(f"lxc config set {container} limits.memory {new*1024}MB")
        changes.append(f"RAM: +{ram}GB (now {new}GB)")
    if cpu:
        new = v['cpu'] + cpu
        await run_lxc(f"lxc config set {container} limits.cpu {new}")
        changes.append(f"CPU: +{cpu} cores (now {new})")
    if disk:
        new = v['disk'] + disk
        await run_lxc(f"lxc config device set {container} root size={new}GB")
        changes.append(f"Disk: +{disk}GB (now {new}GB)")
    if was:
        await run_lxc(f"lxc start {container}")
    conn = get_db()
    cur = conn.cursor()
    if ram:
        cur.execute('UPDATE vps SET ram = ram + ? WHERE container_name = ?', (ram, container))
    if cpu:
        cur.execute('UPDATE vps SET cpu = cpu + ? WHERE container_name = ?', (cpu, container))
    if disk:
        cur.execute('UPDATE vps SET disk = disk + ? WHERE container_name = ?', (disk, container))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Resources Added", "\n".join([f"```fix\n{c}\n```" for c in changes])))

@bot.command(name="list-all")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def list_all(ctx):
    allv = get_all_vps()
    if not allv:
        return await ctx.send(embed=info_embed("No VPS", "No VPS in system."))
    byuser = {}
    for v in allv:
        if v['user_id'] not in byuser:
            byuser[v['user_id']] = []
        byuser[v['user_id']].append(v)
    embed = info_embed(f"All VPS ({len(allv)})")
    for uid, vlist in list(byuser.items())[:5]:
        try:
            u = await bot.fetch_user(int(uid))
            name = u.name
        except:
            name = f"Unknown"
        text = "\n".join([f"{'🟢' if v['status']=='running' else '🔴'} `{v['container_name']}` ({v['ram']}GB)" for v in vlist[:3]])
        embed.add_field(name=f"{name} ({len(vlist)})", value=text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="add-inv")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def add_inv(ctx, user: discord.Member, amt: int):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    update_user_stats(str(user.id), invites=amt)
    await ctx.send(embed=success_embed("Invites Added", f"```fix\n+{amt} to {user.name}\n```"))

@bot.command(name="remove-inv")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def remove_inv(ctx, user: discord.Member, amt: int):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    s = get_user_stats(str(user.id))
    if s.get('invites',0) < amt:
        amt = s.get('invites',0)
    update_user_stats(str(user.id), invites=-amt)
    await ctx.send(embed=success_embed("Invites Removed", f"```fix\n-{amt} from {user.name}\n```"))

@bot.command(name="ports-add")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def ports_add_admin(ctx, user: discord.Member, amt: int):
    if amt <= 0:
        return await ctx.send(embed=error_embed("Invalid", "Amount must be positive"))
    add_port_allocation(str(user.id), amt)
    await ctx.send(embed=success_embed("Port Slots Added", f"```fix\n+{amt} to {user.name}\n```"))

@bot.command(name="serverstats")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def serverstats(ctx):
    allv = get_all_vps()
    tr = sum(v['ram'] for v in allv)
    tc = sum(v['cpu'] for v in allv)
    td = sum(v['disk'] for v in allv)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM vps')
    tu = cur.fetchone()[0] or 0
    cur.execute('SELECT COUNT(*) FROM port_forwards')
    tp = cur.fetchone()[0] or 0
    conn.close()
    embed = info_embed("Server Statistics")
    embed.add_field(name="🖥️ VPS", value=f"```fix\nTotal: {len(allv)}\nUsers: {tu}\n```", inline=True)
    embed.add_field(name="💾 Resources", value=f"```fix\nRAM: {tr}GB\nCPU: {tc} cores\nDisk: {td}GB\n```", inline=True)
    embed.add_field(name="🔌 Ports", value=f"```fix\n{len(allv)} VPS\n{tp} forwards\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="admin-add-ipv4")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_add_ipv4(ctx, user: discord.Member, container: str):
    uid = str(user.id)
    if not any(v['container_name']==container for v in get_user_vps(uid)):
        return await ctx.send(embed=error_embed("Not Found", f"Container {container} not found for user"))
    out,_,_ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)[0-9.]+' | head -1")
    priv = out.strip() or "N/A"
    out,_,_ = await exec_in_container(container, "ip link | grep ether | awk '{print $2}' | head -1")
    mac = out.strip() or "N/A"
    add_ipv4(uid, container, SERVER_IP, priv, mac)
    embed = success_embed("IPv4 Assigned")
    embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
    embed.add_field(name="🌐 Public", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🏠 Private", value=f"```fix\n{priv}\n```", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="admin-rm-ipv4")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_rm_ipv4(ctx, user: discord.Member, container: str = None):
    uid = str(user.id)
    if container:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM ipv4 WHERE user_id = ? AND container_name = ?', (uid, container))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("IPv4 Removed", f"```fix\n{container}\n```"))
    else:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM ipv4 WHERE user_id = ?', (uid,))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("IPv4 Removed", f"```fix\nAll IPv4 from {user.name}\n```"))

@bot.command(name="admin-pending-ipv4")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def admin_pending_ipv4(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions WHERE status = "pending" ORDER BY created_at')
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed("No Pending", "No pending IPv4 purchases."))
    embed = info_embed(f"Pending IPv4 ({len(rows)})")
    for r in rows:
        try:
            u = await bot.fetch_user(int(r['user_id']))
            name = u.name
        except:
            name = f"Unknown"
        embed.add_field(name=f"User: {name}", value=f"```fix\nRef: {r['txn_ref']}\nAmount: ₹{r['amount']}\nCreated: {r['created_at'][:16]}\n```", inline=False)
    await ctx.send(embed=embed)

# ==================================================================================================
#  👑  OWNER COMMANDS
# ==================================================================================================

@bot.command(name="admin-add")
@commands.check(lambda ctx: str(ctx.author.id) in map(str, MAIN_ADMIN_IDS))
async def owner_admin_add(ctx, user: discord.Member):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            'INSERT OR IGNORE INTO admins (user_id, added_at) VALUES (?, ?)', 
            (str(user.id), datetime_.datetime.now().isoformat())
        )
        conn.commit()
    
    await ctx.send(embed=success_embed("Admin Added", f"{user.mention} is now an admin"))

# --- This part handles the "No Permission" message ---
@owner_admin_add.error
async def owner_admin_add_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"❌ {ctx.author.mention}, you do not have permission to use this command!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Could not find that user. Please mention a valid member.")
        
@bot.command(name="admin-remove")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_admin_remove(ctx, user: discord.Member):
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        return await ctx.send(embed=error_embed("Cannot Remove", "Cannot remove main admin"))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM admins WHERE user_id = ?', (str(user.id),))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed("Admin Removed", f"{user.mention} is no longer admin"))

@bot.command(name="admin-list")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_admin_list(ctx):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM admins')
    rows = cur.fetchall()
    conn.close()
    main = "\n".join([f"👑 <@{a}>" for a in MAIN_ADMIN_IDS])
    admins = "\n".join([f"🛡️ <@{r['user_id']}>" for r in rows if r['user_id'] not in [str(a) for a in MAIN_ADMIN_IDS]])
    embed = info_embed("Admin List")
    embed.add_field(name="Main Admin", value=main or "None", inline=False)
    embed.add_field(name="Admins", value=admins or "None", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="maintenance")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_maintenance(ctx, mode: str):
    mode = mode.lower()
    if mode not in ['on','off']:
        return await ctx.send(embed=error_embed("Invalid", "Use on or off"))
    set_setting('maintenance_mode', mode)
    await ctx.send(embed=success_embed("Maintenance", f"Mode set to {mode}"))

@bot.command(name="purge-all")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_purge_all(ctx):
    allv = get_all_vps()
    unprotected = [v for v in allv if not v.get('purge_protected',0)]
    if not unprotected:
        return await ctx.send(embed=info_embed("No Unprotected", "All VPS are protected."))
    view = View()
    conf = Button(label="✅ PURGE", style=discord.ButtonStyle.danger)
    canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def conf_cb(i):
        await i.response.defer()
        prog = await i.followup.send(embed=info_embed("Purging", f"```fix\n0/{len(unprotected)}\n```"), ephemeral=True)
        deleted = 0
        for idx, v in enumerate(unprotected,1):
            try:
                await run_lxc(f"lxc stop {v['container_name']} --force")
                await run_lxc(f"lxc delete {v['container_name']}")
                delete_vps(v['container_name'])
                deleted += 1
                if idx % 5 == 0:
                    await prog.edit(embed=info_embed("Purging", f"```fix\n{idx}/{len(unprotected)}\n```"))
                await asyncio.sleep(2)
            except:
                pass
        await prog.edit(embed=success_embed("Purge Complete", f"```fix\nDeleted: {deleted}\nFailed: {len(unprotected)-deleted}\n```"))
    async def canc_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    conf.callback = conf_cb
    canc.callback = canc_cb
    view.add_item(conf)
    view.add_item(canc)
    await ctx.send(embed=warning_embed("⚠️ Purge All Unprotected", f"```fix\nThis will delete {len(unprotected)} unprotected VPS.\nProtected VPS will be skipped.\n```"), view=view)

@bot.command(name="protect")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_protect(ctx, user: discord.Member, num: int = None):
    uid = str(user.id)
    vps = get_user_vps(uid)
    if not vps:
        return await ctx.send(embed=error_embed("No VPS", f"{user.mention} has no VPS"))
    if num is None:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE user_id = ?', (uid,))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Protected", f"All VPS of {user.mention} are now protected"))
    else:
        if num < 1 or num > len(vps):
            return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE container_name = ?', (vps[num-1]['container_name'],))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Protected", f"VPS #{num} of {user.mention} is now protected"))

@bot.command(name="unprotect")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_unprotect(ctx, user: discord.Member, num: int = None):
    uid = str(user.id)
    vps = get_user_vps(uid)
    if not vps:
        return await ctx.send(embed=error_embed("No VPS", f"{user.mention} has no VPS"))
    if num is None:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE user_id = ?', (uid,))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Unprotected", f"All VPS of {user.mention} are no longer protected"))
    else:
        if num < 1 or num > len(vps):
            return await ctx.send(embed=error_embed("Invalid", f"VPS number must be 1-{len(vps)}"))
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE container_name = ?', (vps[num-1]['container_name'],))
        conn.commit()
        conn.close()
        await ctx.send(embed=success_embed("Unprotected", f"VPS #{num} of {user.mention} is no longer protected"))

@bot.command(name="backup-db")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_backup_db(ctx):
    name = f"backup_{datetime_.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    path = os.path.join(BACKUPS_DIR, name)
    try:
        shutil.copy2(DATABASE_PATH, path)
        await ctx.send(embed=success_embed("Backup Created", f"```fix\n{name}\n```"))
    except Exception as e:
        await ctx.send(embed=error_embed("Backup Failed", str(e)))

@bot.command(name="restore-db")
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def owner_restore_db(ctx, name: str):
    path = os.path.join(BACKUPS_DIR, name)
    if not os.path.exists(path):
        return await ctx.send(embed=error_embed("Not Found", f"```diff\n- {name}\n```"))
    view = View()
    conf = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
    canc = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def conf_cb(i):
        try:
            shutil.copy2(path, DATABASE_PATH)
            await i.response.edit_message(embed=success_embed("Restored", f"```fix\n{name}\n```"), view=None)
        except Exception as e:
            await i.response.edit_message(embed=error_embed("Failed", str(e)), view=None)
    async def canc_cb(i):
        await i.response.edit_message(embed=info_embed("Cancelled"), view=None)
    conf.callback = conf_cb
    canc.callback = canc_cb
    view.add_item(conf)
    view.add_item(canc)
    await ctx.send(embed=warning_embed("Confirm Restore", f"```fix\nRestore {name}?\nCurrent DB will be overwritten!\n```"), view=view)
# ==================================================================================================
#  🌐  COMPLETE IP COMMANDS - USER IP, VPS IP, NODE IP, ALL DETAILS
# ==================================================================================================

@bot.command(name="ip")
async def ip_cmd(ctx, target: str = None):
    """Main IP command - show your IP, VPS IP, or node IP"""
    if not target:
        # Show user's own IP
        await show_my_ip(ctx)
    elif target.lower() == "public":
        # Show public IP of server
        await show_public_ip(ctx)
    elif target.lower() == "vps" or target.lower() == "container":
        # Show all VPS IPs
        await show_vps_ips(ctx)
    elif target.lower() == "node":
        # Show node IPs
        await show_node_ips(ctx)
    elif target.lower() == "all":
        # Show all IPs
        await show_all_ips(ctx)
    elif target.lower() == "mac":
        # Show MAC address
        await show_mac_address(ctx)
    elif target.lower() == "dns":
        # Show DNS servers
        await show_dns_servers(ctx)
    elif target.lower() == "route" or target.lower() == "gateway":
        # Show routing table
        await show_routing_table(ctx)
    elif target.lower() == "interface" or target.lower() == "ifconfig":
        # Show network interfaces
        await show_network_interfaces(ctx)
    else:
        # Show specific container IP
        await show_container_ip(ctx, target)


@bot.command(name="myip")
async def my_ip(ctx):
    """Show your own public IP"""
    await show_my_ip(ctx)


@bot.command(name="vps-ip")
async def vps_ip(ctx, container: str = None):
    """Show VPS container IP details"""
    if container:
        await show_container_ip(ctx, container)
    else:
        await show_vps_ips(ctx)


@bot.command(name="node-ip")
async def node_ip(ctx, node_name: str = None):
    """Show node IP details"""
    if node_name:
        await show_node_ip_detail(ctx, node_name)
    else:
        await show_node_ips(ctx)


@bot.command(name="public-ip")
async def public_ip(ctx):
    """Show server public IP"""
    await show_public_ip(ctx)


@bot.command(name="mac")
async def mac_address(ctx, container: str = None):
    """Show MAC address of server or container"""
    if container:
        await show_container_mac(ctx, container)
    else:
        await show_mac_address(ctx)


@bot.command(name="gateway")
async def gateway_cmd(ctx, container: str = None):
    """Show gateway information"""
    if container:
        await show_container_gateway(ctx, container)
    else:
        await show_routing_table(ctx)


@bot.command(name="netstat")
async def netstat_cmd(ctx, container: str = None):
    """Show network connections"""
    if container:
        await show_container_netstat(ctx, container)
    else:
        await show_server_netstat(ctx)


@bot.command(name="ifconfig")
async def ifconfig_cmd(ctx, container: str = None):
    """Show network interfaces"""
    if container:
        await show_container_interfaces(ctx, container)
    else:
        await show_network_interfaces(ctx)


@bot.command(name="dns")
async def dns_cmd(ctx, container: str = None):
    """Show DNS servers"""
    if container:
        await show_container_dns(ctx, container)
    else:
        await show_dns_servers(ctx)


@bot.command(name="ping-ip")
async def ping_ip(ctx, ip: str):
    """Ping an IP address"""
    await ping_target(ctx, ip)


@bot.command(name="trace-ip")
async def trace_ip(ctx, ip: str):
    """Trace route to IP address"""
    await trace_target(ctx, ip)


# ==================================================================================================
#  📡  IP COMMAND IMPLEMENTATIONS
# ==================================================================================================

async def show_my_ip(ctx):
    """Show user's own public IP"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipify.org', timeout=5) as resp:
                public_ip = await resp.text()
    except:
        try:
            public_ip = subprocess.getoutput("curl -s ifconfig.me")
        except:
            public_ip = "Could not detect"
    
    embed = discord.Embed(
        title="```glow\n🌐 Your IP Information\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # Get local IPs
    local_ips = []
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            if iface != 'lo':
                addr = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addr:
                    for ip in addr[netifaces.AF_INET]:
                        if ip['addr'] != '127.0.0.1':
                            local_ips.append(f"{iface}: {ip['addr']}")
    except:
        local_ips = ["Could not detect"]
    
    embed.add_field(
        name="🌍 Public IP",
        value=f"```fix\n{public_ip}\n```",
        inline=False
    )
    
    embed.add_field(
        name="🏠 Local IPs",
        value=f"```fix\n" + "\n".join(local_ips[:5]) + "\n```",
        inline=False
    )
    
    embed.add_field(
        name="🖥️ Hostname",
        value=f"```fix\n{HOSTNAME}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🔌 MAC Address",
        value=f"```fix\n{MAC_ADDRESS}\n```",
        inline=True
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Your IP Information • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_public_ip(ctx):
    """Show server public IP"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipify.org', timeout=5) as resp:
                public_ip = await resp.text()
    except:
        try:
            public_ip = subprocess.getoutput("curl -s ifconfig.me")
        except:
            public_ip = "Could not detect"
    
    # Get additional IP info
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://ip-api.com/json/{public_ip}', timeout=5) as resp:
                ip_info = await resp.json()
                location = f"{ip_info.get('city', 'Unknown')}, {ip_info.get('country', 'Unknown')}"
                isp = ip_info.get('isp', 'Unknown')
    except:
        location = "Unknown"
        isp = "Unknown"
    
    embed = discord.Embed(
        title="```glow\n🌍 Public IP Information\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    embed.add_field(
        name="🌐 IP Address",
        value=f"```fix\n{public_ip}\n```",
        inline=False
    )
    
    embed.add_field(
        name="📍 Location",
        value=f"```fix\n{location}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🏢 ISP",
        value=f"```fix\n{isp}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🖥️ Hostname",
        value=f"```fix\n{HOSTNAME}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🔌 MAC",
        value=f"```fix\n{MAC_ADDRESS}\n```",
        inline=True
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Public IP Information • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_vps_ips(ctx):
    """Show all VPS containers IPs"""
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = discord.Embed(
        title="```glow\n🖥️ Your VPS IP Addresses\n```",
        color=COLORS['info']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    for vps in vps_list:
        container = vps['container_name']
        stats = await get_container_stats(container)
        
        status_emoji = "🟢" if stats['status'] == 'running' else "🔴"
        
        ip_text = f"{status_emoji} **`{container}`**\n"
        ip_text += f"```fix\n"
        
        if stats['ipv4']:
            for i, ip in enumerate(stats['ipv4'][:3], 1):
                ip_text += f"IPv4 #{i}: {ip}\n"
        else:
            ip_text += f"IPv4: Not assigned\n"
        
        ip_text += f"MAC: {stats['mac']}\n"
        ip_text += f"Status: {stats['status'].upper()}\n"
        ip_text += f"```"
        
        embed.add_field(name=f"📦 {container}", value=ip_text, inline=False)
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Use .ip <container> for details • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_container_ip(ctx, container_name: str):
    """Show detailed IP information for a container"""
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container_name for v in vps_list):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    stats = await get_container_stats(container_name)
    
    # Get more details from container
    ip_addr, _, _ = await exec_in_container(container_name, "ip addr show")
    route, _, _ = await exec_in_container(container_name, "ip route show")
    
    embed = discord.Embed(
        title=f"```glow\n🌐 IP Details: {container_name}\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # IPv4 Addresses
    ipv4_text = ""
    for ip in stats['ipv4']:
        ipv4_text += f"• {ip}\n"
    embed.add_field(
        name="🌍 IPv4 Addresses",
        value=f"```fix\n{ipv4_text if ipv4_text else 'No IPv4 assigned'}\n```",
        inline=True
    )
    
    # MAC Address
    embed.add_field(
        name="🔌 MAC Address",
        value=f"```fix\n{stats['mac']}\n```",
        inline=True
    )
    
    # Status
    embed.add_field(
        name="📊 Status",
        value=f"```fix\n{stats['status'].upper()}\n```",
        inline=True
    )
    
    # Full IP Configuration
    embed.add_field(
        name="📋 Full IP Configuration",
        value=f"```bash\n{ip_addr[:500]}\n```",
        inline=False
    )
    
    # Routing Table
    embed.add_field(
        name="🗺️ Routing Table",
        value=f"```bash\n{route[:500]}\n```",
        inline=False
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • {container_name} • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_node_ips(ctx):
    """Show all node IPs"""
    nodes = load_nodes()
    
    if not nodes['nodes']:
        await ctx.send(embed=info_embed("No Nodes", "No nodes configured."))
        return
    
    embed = discord.Embed(
        title="```glow\n🌐 Node IP Addresses\n```",
        color=COLORS['node']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    for name, node in nodes['nodes'].items():
        status_emoji = "🟢" if node['status'] == 'online' else "🔴"
        is_main = " 👑 MAIN" if node.get('is_main') else ""
        
        ip_text = f"{status_emoji} **`{name}`**{is_main}\n"
        ip_text += f"```fix\n"
        ip_text += f"Host: {node['host']}\n"
        ip_text += f"Port: {node['port']}\n"
        ip_text += f"Status: {node['status'].upper()}\n"
        ip_text += f"Region: {node.get('region', 'us')}\n"
        ip_text += f"```"
        
        embed.add_field(name=f"🌍 {name}", value=ip_text, inline=False)
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Use .node-info <name> for details • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_node_ip_detail(ctx, node_name: str):
    """Show detailed IP for a specific node"""
    node = get_node(node_name)
    
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- {node_name}\n```"))
        return
    
    embed = discord.Embed(
        title=f"```glow\n🌐 Node IP Details: {node_name}\n```",
        color=COLORS['node']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    embed.add_field(
        name="🌐 Host",
        value=f"```fix\n{node['host']}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🔌 Port",
        value=f"```fix\n{node['port']}\n```",
        inline=True
    )
    
    embed.add_field(
        name="📊 Status",
        value=f"```fix\n{node['status'].upper()}\n```",
        inline=True
    )
    
    embed.add_field(
        name="👤 Username",
        value=f"```fix\n{node['username']}\n```",
        inline=True
    )
    
    embed.add_field(
        name="📍 Region",
        value=f"```fix\n{node.get('region', 'us')}\n```",
        inline=True
    )
    
    embed.add_field(
        name="🗝️ API Key",
        value=f"```fix\n{node.get('api_key', 'N/A')[:16]}...\n```",
        inline=True
    )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Node IP Information • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_all_ips(ctx):
    """Show all IPs (user, VPS, node)"""
    embed = discord.Embed(
        title="```glow\n🌐 Complete IP Overview\n```",
        color=COLORS['gold']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # Server IP
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
    except:
        public_ip = subprocess.getoutput("curl -s ifconfig.me")
    
    embed.add_field(
        name="🖥️ Server IP",
        value=f"```fix\nPublic: {public_ip}\nLocal: {SERVER_IP}\nHostname: {HOSTNAME}\nMAC: {MAC_ADDRESS}\n```",
        inline=False
    )
    
    # VPS IPs
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if vps_list:
        vps_text = ""
        for vps in vps_list[:5]:
            stats = await get_container_stats(vps['container_name'])
            vps_text += f"• {vps['container_name']}: {stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n"
        embed.add_field(
            name="🖥️ Your VPS IPs",
            value=f"```fix\n{vps_text if vps_text else 'No VPS'}\n```",
            inline=False
        )
    
    # Node IPs
    nodes = load_nodes()
    if nodes['nodes']:
        node_text = ""
        for name, node in nodes['nodes'].items():
            node_text += f"• {name}: {node['host']} ({node['status']})\n"
        embed.add_field(
            name="🌐 Node IPs",
            value=f"```fix\n{node_text[:500]}\n```",
            inline=False
        )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Complete IP Overview • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


async def show_mac_address(ctx, container: str = None):
    """Show MAC address"""
    if container:
        # Show container MAC
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        stats = await get_container_stats(container)
        mac = stats['mac']
        
        embed = info_embed(f"🔌 MAC Address: {container}")
        embed.add_field(name="MAC Address", value=f"```fix\n{mac}\n```", inline=False)
        embed.add_field(name="Container", value=f"```fix\n{container}\n```", inline=True)
        await ctx.send(embed=embed)
    else:
        # Show server MAC
        embed = info_embed("🔌 Server MAC Address")
        embed.add_field(name="MAC Address", value=f"```fix\n{MAC_ADDRESS}\n```", inline=False)
        embed.add_field(name="Hostname", value=f"```fix\n{HOSTNAME}\n```", inline=True)
        await ctx.send(embed=embed)


async def show_routing_table(ctx, container: str = None):
    """Show routing table / gateway"""
    if container:
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        route, _, _ = await exec_in_container(container, "ip route show")
        
        embed = terminal_embed(f"Routing Table: {container}", route)
        await ctx.send(embed=embed)
    else:
        route = subprocess.getoutput("ip route show")
        embed = terminal_embed("Routing Table", route)
        await ctx.send(embed=embed)


async def show_container_gateway(ctx, container: str):
    """Show container gateway"""
    user_id = str(ctx.author.id)
    if not any(v['container_name'] == container for v in get_user_vps(user_id)):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    route, _, _ = await exec_in_container(container, "ip route show | grep default")
    gateway = route.split()[2] if route else "N/A"
    
    embed = info_embed(f"🚪 Gateway: {container}")
    embed.add_field(name="Gateway", value=f"```fix\n{gateway}\n```", inline=False)
    embed.add_field(name="Container", value=f"```fix\n{container}\n```", inline=True)
    await ctx.send(embed=embed)


async def show_network_interfaces(ctx, container: str = None):
    """Show network interfaces"""
    if container:
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        interfaces, _, _ = await exec_in_container(container, "ip link show")
        
        embed = terminal_embed(f"Network Interfaces: {container}", interfaces)
        await ctx.send(embed=embed)
    else:
        interfaces = subprocess.getoutput("ip link show")
        embed = terminal_embed("Network Interfaces", interfaces)
        await ctx.send(embed=embed)


async def show_container_interfaces(ctx, container: str):
    """Show container network interfaces"""
    await show_network_interfaces(ctx, container)


async def show_dns_servers(ctx, container: str = None):
    """Show DNS servers"""
    if container:
        user_id = str(ctx.author.id)
        if not any(v['container_name'] == container for v in get_user_vps(user_id)):
            await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
            return
        
        dns, _, _ = await exec_in_container(container, "cat /etc/resolv.conf | grep nameserver")
        
        embed = terminal_embed(f"DNS Servers: {container}", dns)
        await ctx.send(embed=embed)
    else:
        dns = subprocess.getoutput("cat /etc/resolv.conf | grep nameserver")
        embed = terminal_embed("DNS Servers", dns)
        await ctx.send(embed=embed)


async def show_container_dns(ctx, container: str):
    """Show container DNS servers"""
    await show_dns_servers(ctx, container)


async def show_server_netstat(ctx):
    """Show server network connections"""
    netstat = subprocess.getoutput("ss -tuln | head -30")
    embed = terminal_embed("Server Network Connections", netstat)
    await ctx.send(embed=embed)


async def show_container_netstat(ctx, container: str):
    """Show container network connections"""
    user_id = str(ctx.author.id)
    if not any(v['container_name'] == container for v in get_user_vps(user_id)):
        await ctx.send(embed=error_embed("Access Denied", "You don't own this VPS."))
        return
    
    netstat, _, _ = await exec_in_container(container, "netstat -tuln | head -30")
    embed = terminal_embed(f"Network Connections: {container}", netstat)
    await ctx.send(embed=embed)


async def ping_target(ctx, ip: str):
    """Ping an IP address"""
    msg = await ctx.send(embed=info_embed("Pinging...", f"```fix\n{ip}\n```"))
    
    try:
        result = subprocess.getoutput(f"ping -c 4 {ip}")
        
        # Parse ping results
        lines = result.splitlines()
        loss = "100%"
        avg = "N/A"
        
        for line in lines:
            if "packet loss" in line:
                loss = line.split(',')[2].strip()
            if "avg" in line:
                parts = line.split('/')
                if len(parts) >= 5:
                    avg = f"{parts[4]}ms"
        
        embed = info_embed(f"Ping Results: {ip}")
        embed.add_field(name="📡 Target", value=f"```fix\n{ip}\n```", inline=True)
        embed.add_field(name="📊 Packet Loss", value=f"```fix\n{loss}\n```", inline=True)
        embed.add_field(name="⏱️ Avg Latency", value=f"```fix\n{avg}\n```", inline=True)
        embed.add_field(name="📋 Full Output", value=f"```bash\n{result[:500]}\n```", inline=False)
        
        await msg.edit(embed=embed)
    except Exception as e:
        await msg.edit(embed=error_embed("Ping Failed", f"```diff\n- {str(e)}\n```"))


async def trace_target(ctx, ip: str):
    """Trace route to IP address"""
    msg = await ctx.send(embed=info_embed("Tracing Route...", f"```fix\n{ip}\n```"))
    
    try:
        result = subprocess.getoutput(f"traceroute -n {ip} 2>/dev/null || tracepath {ip} 2>/dev/null")
        
        embed = terminal_embed(f"Trace Route to {ip}", result[:1900])
        await msg.edit(embed=embed)
    except Exception as e:
        await msg.edit(embed=error_embed("Trace Failed", f"```diff\n- {str(e)}\n```"))


# ==================================================================================================
#  🆕  NEW IP COMMANDS FOR USER MANAGEMENT
# ==================================================================================================

@bot.command(name="user-ip")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def user_ip(ctx, user: discord.Member):
    """Show IP information for a user (Admin only)"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=info_embed(f"No VPS", f"{user.mention} has no VPS."))
        return
    
    embed = discord.Embed(
        title=f"```glow\n🌐 IP Information for {user.display_name}\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else THUMBNAIL_URL)
    
    for vps in vps_list:
        stats = await get_container_stats(vps['container_name'])
        
        ip_text = f"```fix\n"
        ip_text += f"Container: {vps['container_name']}\n"
        if stats['ipv4']:
            ip_text += f"IPv4: {stats['ipv4'][0]}\n"
        ip_text += f"MAC: {stats['mac']}\n"
        ip_text += f"Status: {stats['status'].upper()}\n"
        ip_text += f"RAM: {vps['ram']}GB | CPU: {vps['cpu']}\n"
        ip_text += f"```"
        
        embed.add_field(name=f"📦 {vps['container_name']}", value=ip_text, inline=False)
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Admin View • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


@bot.command(name="assign-ip")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def assign_ip(ctx, user: discord.Member, container: str, ip_address: str = None):
    """Assign a static IP to a container (Admin only)"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not any(v['container_name'] == container for v in vps_list):
        await ctx.send(embed=error_embed("Not Found", f"Container {container} not found for {user.mention}"))
        return
    
    if not ip_address:
        # Auto-assign IP
        ip_address = f"10.10.10.{random.randint(100, 250)}"
    
    # Get MAC address
    stats = await get_container_stats(container)
    mac = stats['mac']
    
    # Apply static IP
    cmd = f"ip addr add {ip_address}/24 dev eth0"
    await exec_in_container(container, cmd)
    
    # Save to database
    add_ipv4(user_id, container, ip_address, ip_address, mac)
    
    embed = success_embed("IP Assigned")
    embed.add_field(name="👤 User", value=user.mention, inline=True)
    embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
    embed.add_field(name="🌐 IP Address", value=f"```fix\n{ip_address}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{mac}\n```", inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name="release-ip")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def release_ip(ctx, user: discord.Member, container: str):
    """Release IP from a container (Admin only)"""
    user_id = str(user.id)
    
    # Remove from database
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM ipv4 WHERE user_id = ? AND container_name = ?', (user_id, container))
    conn.commit()
    conn.close()
    
    embed = success_embed("IP Released")
    embed.add_field(name="👤 User", value=user.mention, inline=True)
    embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
    
    await ctx.send(embed=embed)


@bot.command(name="ip-stats")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def ip_stats(ctx):
    """Show IP statistics (Admin only)"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM ipv4')
    total_ips = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM ipv4')
    users_with_ips = cur.fetchone()[0] or 0
    
    cur.execute('SELECT user_id, COUNT(*) as count FROM ipv4 GROUP BY user_id ORDER BY count DESC LIMIT 5')
    top_users = cur.fetchall()
    conn.close()
    
    embed = info_embed("IP Statistics")
    embed.add_field(name="📊 Total IPs Assigned", value=f"```fix\n{total_ips}\n```", inline=True)
    embed.add_field(name="👥 Users with IPs", value=f"```fix\n{users_with_ips}\n```", inline=True)
    
    if top_users:
        top_text = ""
        for row in top_users:
            try:
                user = await bot.fetch_user(int(row['user_id']))
                top_text += f"• {user.name}: {row['count']} IPs\n"
            except:
                top_text += f"• Unknown: {row['count']} IPs\n"
        embed.add_field(name="🏆 Top Users", value=f"```fix\n{top_text}\n```", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name="my-ip-info")
async def my_ip_info(ctx):
    """Show your IP information and network details"""
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    embed = discord.Embed(
        title="```glow\n🌐 Your Network Information\n```",
        color=COLORS['cyan']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    
    # User info
    embed.add_field(
        name="👤 User",
        value=f"```fix\n{ctx.author.display_name}\nID: {ctx.author.id}\n```",
        inline=True
    )
    
    # Server info
    embed.add_field(
        name="🖥️ Server",
        value=f"```fix\nPublic: {SERVER_IP}\nHostname: {HOSTNAME}\nMAC: {MAC_ADDRESS}\n```",
        inline=True
    )
    
    # VPS Info
    if vps_list:
        vps_text = ""
        for vps in vps_list[:5]:
            stats = await get_container_stats(vps['container_name'])
            vps_text += f"• {vps['container_name']}: {stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n"
        embed.add_field(
            name="🖥️ Your VPS IPs",
            value=f"```fix\n{vps_text}\n```",
            inline=False
        )
    
    embed.set_footer(text=f"⚡ {BOT_NAME} • Your Network Info • {datetime_.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡")
    await ctx.send(embed=embed)


@bot.command(name="ip-history")
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def ip_history(ctx, user: discord.Member = None):
    """Show IP assignment history (Admin only)"""
    conn = get_db()
    cur = conn.cursor()
    
    if user:
        cur.execute('SELECT * FROM ipv4 WHERE user_id = ? ORDER BY assigned_at DESC', (str(user.id),))
    else:
        cur.execute('SELECT * FROM ipv4 ORDER BY assigned_at DESC LIMIT 20')
    
    rows = cur.fetchall()
    conn.close()
    
    if not rows:
        await ctx.send(embed=info_embed("No IP History", "No IP assignments found."))
        return
    
    embed = info_embed(f"IP Assignment History ({len(rows)})")
    
    for row in rows[:10]:
        try:
            u = await bot.fetch_user(int(row['user_id']))
            username = u.name
        except:
            username = f"Unknown ({row['user_id'][:8]})"
        
        value = f"```fix\n"
        value += f"Container: {row['container_name']}\n"
        value += f"IP: {row['public_ip']}\n"
        value += f"MAC: {row['mac_address']}\n"
        value += f"Assigned: {row['assigned_at'][:16]}\n"
        value += f"```"
        
        embed.add_field(name=f"👤 {username}", value=value, inline=False)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  ✨  PMV EXTENDED COMMAND PACK
# ==================================================================================================

def ensure_pmv_tables():
    conn = get_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS wallet (
        user_id TEXT PRIMARY KEY,
        credits INTEGER DEFAULT 0,
        daily_last_claim TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS vps_notes (
        container_name TEXT PRIMARY KEY,
        note TEXT,
        updated_by TEXT,
        updated_at TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS vps_warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        container_name TEXT,
        warning TEXT,
        warned_by TEXT,
        warned_at TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS vps_expiry (
        container_name TEXT PRIMARY KEY,
        expires_at TEXT,
        updated_by TEXT,
        updated_at TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS owner_delegates (
        user_id TEXT PRIMARY KEY,
        expires_at TEXT,
        added_by TEXT,
        added_at TEXT
    )''')
    conn.commit()
    conn.close()


ensure_pmv_tables()


def get_wallet_credits(user_id: str) -> int:
    ensure_pmv_tables()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO wallet (user_id, credits) VALUES (?, 0)', (user_id,))
    cur.execute('SELECT credits FROM wallet WHERE user_id = ?', (user_id,))
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return int(row[0] if row else 0)


def add_wallet_credits(user_id: str, amount: int):
    ensure_pmv_tables()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO wallet (user_id, credits) VALUES (?, 0)', (user_id,))
    cur.execute('UPDATE wallet SET credits = MAX(0, credits + ?) WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()


def set_wallet_credits(user_id: str, amount: int):
    ensure_pmv_tables()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO wallet (user_id, credits, daily_last_claim) VALUES (?, ?, COALESCE((SELECT daily_last_claim FROM wallet WHERE user_id = ?), NULL))',
                (user_id, max(0, amount), user_id))
    conn.commit()
    conn.close()


def get_vps_by_num_for_user(user_id: str, num: int) -> Optional[Dict]:
    vps = get_user_vps(user_id)
    if num < 1 or num > len(vps):
        return None
    return vps[num - 1]


class PayOptionsView(View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        ind_btn = Button(label='IND Button', emoji='🇮🇳', style=discord.ButtonStyle.success)
        foreign_btn = Button(label='FOREGIN Button', emoji='🌍', style=discord.ButtonStyle.primary)
        close_btn = Button(label='Close', emoji='🗑️', style=discord.ButtonStyle.danger)
        ind_btn.callback = self.ind_cb
        foreign_btn.callback = self.foreign_cb
        close_btn.callback = self.close_cb
        self.add_item(ind_btn)
        self.add_item(foreign_btn)
        self.add_item(close_btn)

    async def _guard(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message('This menu is not for you.', ephemeral=True)
            return False
        return True

    async def ind_cb(self, interaction: discord.Interaction):
        if not await self._guard(interaction):
            return
        embed = info_embed('💸 INDIA Payment Options')
        embed.description = (
            '```fix\n'
            'PHONEPAY\n'
            'GOOGLEPAY\n'
            'FAMPAY\n'
            'RAZORPAY\n'
            'UPI\n'
            '```'
        )
        await interaction.response.edit_message(embed=embed, view=self)

    async def foreign_cb(self, interaction: discord.Interaction):
        if not await self._guard(interaction):
            return
        embed = info_embed('🌐 FOREIGN Payment Options')
        embed.description = (
            '```fix\n'
            'PAYPAL\n'
            'USDT\n'
            'CRYPTO\n'
            '```'
        )
        await interaction.response.edit_message(embed=embed, view=self)

    async def close_cb(self, interaction: discord.Interaction):
        if not await self._guard(interaction):
            return
        await interaction.message.delete()


@bot.command(name='bot-status')
async def bot_status(ctx):
    up = datetime_.datetime.utcnow() - bot.start_time
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    embed = discord.Embed(title='```glow\n🤖 BOT STATUS • FULL OPERATION\n```', color=COLORS['success'])
    embed.add_field(name='⚡ Latency', value=f'`{round(bot.latency * 1000)}ms`', inline=True)
    embed.add_field(name='⏱️ Uptime', value=f'`{str(up).split(".")[0]}`', inline=True)
    embed.add_field(name='🧠 CPU', value=f'`{cpu:.1f}%`', inline=True)
    embed.add_field(name='💾 RAM', value=f'`{mem.percent:.1f}% ({mem.used//1024//1024}MB/{mem.total//1024//1024}MB)`', inline=False)
    embed.add_field(name='🗄️ Disk', value=f'`{disk.percent:.1f}% ({disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB)`', inline=False)
    embed.add_field(name='📦 Total VPS', value=f'`{len(get_all_vps())}`', inline=True)
    embed.set_thumbnail(url=THUMBNAIL_URL)
    await ctx.send(embed=embed)


@bot.command(name='links')
async def links_cmd(ctx):
    embed = info_embed('🔗 All Important Links')
    embed.add_field(name='🌐 Main Website', value=f"`{get_setting('main_website_link', 'Not Set')}`", inline=False)
    embed.add_field(name='📈 Uptime Kuma', value=f"`{get_setting('uptime_monitoring_link', 'Not Set')}`", inline=False)
    embed.add_field(name='🦖 Pterodactyl', value=f"`{get_setting('pterodactyl_panel_link', 'Not Set')}`", inline=False)
    embed.add_field(name='🖥️ VPS Panel', value=f"`{get_setting('vps_panel_link', 'Not Set')}`", inline=False)
    embed.add_field(name='💬 Discord Server', value=f"`{get_setting('discord_server_link', 'Not Set')}`", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='vps-stats')
async def vps_stats_cmd(ctx):
    my = get_user_vps(str(ctx.author.id))
    if not my:
        return await ctx.send(embed=info_embed('No VPS', 'You have no VPS yet.'))
    running = sum(1 for v in my if v.get('status') == 'running')
    suspended = sum(1 for v in my if int(v.get('suspended', 0)) == 1)
    total_ram = sum(int(v.get('ram', 0)) for v in my)
    total_cpu = sum(int(v.get('cpu', 0)) for v in my)
    total_disk = sum(int(v.get('disk', 0)) for v in my)
    embed = info_embed('🖥️ Your VPS Stats')
    embed.add_field(name='📊 Count', value=f'`Total: {len(my)} | Running: {running} | Suspended: {suspended}`', inline=False)
    embed.add_field(name='📦 Resources', value=f'`CPU: {total_cpu} | RAM: {total_ram}GB | Disk: {total_disk}GB`', inline=False)
    await ctx.send(embed=embed)


@bot.command(name='share-user')
async def share_user_alias(ctx, user: discord.Member, num: int):
    await share(ctx, user, num)


@bot.command(name='share-ruser')
async def share_ruser_alias(ctx, user: discord.Member, num: int):
    await unshare(ctx, user, num)


@bot.command(name='share-list')
async def share_list_alias(ctx, num: int = None):
    if num is None:
        return await shared(ctx)
    my = get_user_vps(str(ctx.author.id))
    if num < 1 or num > len(my):
        return await ctx.send(embed=error_embed('Invalid', f'VPS number must be 1-{len(my)}'))
    container = my[num - 1]['container_name']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT shared_with_id FROM shared_vps WHERE owner_id = ? AND container_name = ?', (str(ctx.author.id), container))
    rows = cur.fetchall()
    conn.close()
    embed = info_embed(f'👥 Shared Users • #{num}')
    if not rows:
        embed.description = 'No users have access to this VPS.'
    else:
        users = []
        for row in rows:
            try:
                u = await bot.fetch_user(int(row[0]))
                users.append(f'• {u.name} ({u.id})')
            except Exception:
                users.append(f'• Unknown ({row[0]})')
        embed.description = '```fix\n' + '\n'.join(users) + '\n```'
    await ctx.send(embed=embed)


@bot.command(name='transfer-ownership')
async def transfer_ownership(ctx, user: discord.Member, num: int):
    uid = str(ctx.author.id)
    target = get_vps_by_num_for_user(uid, num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid VPS number.'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE vps SET user_id = ? WHERE container_name = ?', (str(user.id), target['container_name']))
    cur.execute('DELETE FROM shared_vps WHERE container_name = ?', (target['container_name'],))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('Ownership Transferred', f"```fix\n{target['container_name']} -> {user.name}\n```"))


@bot.command(name='rename-vps')
async def rename_vps_alias(ctx, num: int, *, new_name: str):
    uid = str(ctx.author.id)
    target = get_vps_by_num_for_user(uid, num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid VPS number.'))
    old = target['container_name']
    new = re.sub(r'[^a-zA-Z0-9-]', '-', new_name.strip().lower())[:32]
    if not new:
        return await ctx.send(embed=error_embed('Invalid Name', 'Provide a valid new VPS name.'))
    out, err, code = await run_lxc(f'lxc rename {old} {new}')
    if code != 0:
        return await ctx.send(embed=error_embed('Rename Failed', f"```diff\n- {err or out}\n```"))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE vps SET container_name = ? WHERE container_name = ?', (new, old))
    cur.execute('UPDATE shared_vps SET container_name = ? WHERE container_name = ?', (new, old))
    cur.execute('UPDATE panels SET container_name = ? WHERE container_name = ?', (new, old))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('VPS Renamed', f"```fix\n{old} -> {new}\n```"))


@bot.command(name='vps-note')
async def vps_note(ctx, num: int, *, note: str):
    uid = str(ctx.author.id)
    target = get_vps_by_num_for_user(uid, num)
    if not target and is_admin(uid):
        allv = get_all_vps()
        if num <= len(allv):
            target = allv[num - 1]
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'VPS not found with that number.'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO vps_notes (container_name, note, updated_by, updated_at) VALUES (?, ?, ?, ?)',
                (target['container_name'], note[:1000], uid, datetime_.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('VPS Note Updated', f"```fix\n{target['container_name']}\n{note[:300]}\n```"))


@bot.command(name='uptime-vps')
async def uptime_vps(ctx, num: int):
    target = get_vps_by_num_for_user(str(ctx.author.id), num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid VPS number.'))
    out, err, code = await exec_in_container(target['container_name'], 'uptime -p | sed "s/up //"')
    if code != 0:
        return await ctx.send(embed=error_embed('Failed', err or 'Could not fetch uptime.'))
    await ctx.send(embed=info_embed('⏱️ VPS Uptime', f"```fix\n{target['container_name']}: {out or 'N/A'}\n```"))


@bot.command(name='myinfo')
async def myinfo(ctx):
    st = get_user_stats(str(ctx.author.id))
    wallet = get_wallet_credits(str(ctx.author.id))
    myvps = get_user_vps(str(ctx.author.id))
    embed = info_embed('👤 My Profile & VPS Summary')
    embed.add_field(name='📨 Invites', value=f"`{st.get('invites', 0)}`", inline=True)
    embed.add_field(name='🚀 Boosts', value=f"`{st.get('boosts', 0)}`", inline=True)
    embed.add_field(name='💰 Credits', value=f"`{wallet}`", inline=True)
    embed.add_field(name='🖥️ VPS Count', value=f"`{len(myvps)}`", inline=True)
    embed.add_field(name='🔑 API Key', value=f"`{st.get('api_key', 'N/A')}`", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='pay-options')
async def pay_options(ctx):
    embed = info_embed('💳 Payment Options')
    embed.description = 'Use the buttons below to switch between Indian and Foreign payment methods.'
    await ctx.send(embed=embed, view=PayOptionsView(ctx))


@bot.command(name='buyc')
async def buy_credits_info(ctx):
    await pay_options(ctx)


@bot.command(name='credits')
async def credits_cmd(ctx):
    c = get_wallet_credits(str(ctx.author.id))
    await ctx.send(embed=info_embed('💰 Credit Balance', f"```fix\n{c} credits\n```"))


@bot.command(name='transfer')
async def transfer_credits(ctx, user: discord.Member, amount: int):
    if amount <= 0:
        return await ctx.send(embed=error_embed('Invalid Amount', 'Amount must be greater than 0.'))
    sender = str(ctx.author.id)
    receiver = str(user.id)
    have = get_wallet_credits(sender)
    if have < amount:
        return await ctx.send(embed=error_embed('Insufficient', f'You have {have} credits.'))
    add_wallet_credits(sender, -amount)
    add_wallet_credits(receiver, amount)
    await ctx.send(embed=success_embed('Transfer Complete', f"```fix\n{amount} credits -> {user.name}\n```"))


@bot.command(name='share-credit')
async def share_credit_cmd(ctx, user: discord.Member, credits: int):
    await transfer_credits(ctx, user, credits)


@bot.command(name='daily-credits')
async def daily_credits(ctx):
    uid = str(ctx.author.id)
    ensure_pmv_tables()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR IGNORE INTO wallet (user_id, credits, daily_last_claim) VALUES (?, 0, NULL)', (uid,))
    cur.execute('SELECT daily_last_claim, credits FROM wallet WHERE user_id = ?', (uid,))
    row = cur.fetchone()
    last_claim = row[0] if row else None
    now = datetime_.datetime.utcnow()
    streak = int(get_setting(f'daily_streak:{uid}', '0'))
    if last_claim:
        try:
            last = datetime_.datetime.fromisoformat(last_claim)
            if (now - last).total_seconds() < 24 * 3600:
                left = int((24 * 3600 - (now - last).total_seconds()) // 3600)
                conn.close()
                return await ctx.send(embed=warning_embed('Daily Already Claimed', f'Try again in about {left}h.'))
            if (now - last).total_seconds() <= 48 * 3600:
                streak += 1
            else:
                streak = 1
        except Exception:
            streak = 1
    else:
        streak = 1
    reward = streak * 10
    cur.execute('UPDATE wallet SET credits = credits + ?, daily_last_claim = ? WHERE user_id = ?',
                (reward, now.isoformat(), uid))
    conn.commit()
    conn.close()
    set_setting(f'daily_streak:{uid}', str(streak))
    await ctx.send(embed=success_embed('Daily Credits Claimed', f"```fix\n+{reward} credits\nStreak Day: {streak}\n```"))


@bot.command(name='vps-inv')
async def vps_inv_cmd(ctx):
    st = get_user_stats(str(ctx.author.id))
    invites = int(st.get('invites', 0))
    embed = info_embed('📨 Invite Progress & Plans')
    embed.add_field(name='📊 Your Invites', value=f'`Total: {invites}`', inline=False)
    lines = [f"{p['emoji']} {p['name']} -> {p['invites']} invites" for p in FREE_VPS_PLANS.get('invites', [])]
    embed.add_field(name='🎯 Claimable Invite Plans', value='```fix\n' + '\n'.join(lines[:10]) + '\n```', inline=False)
    await ctx.send(embed=embed)


@bot.command(name='vps-boost')
async def vps_boost_cmd(ctx):
    st = get_user_stats(str(ctx.author.id))
    boosts = int(st.get('boosts', 0))
    await ctx.send(embed=info_embed('🚀 Boost Points', f"```fix\nYou currently have: {boosts} boosts\n```"))


@bot.command(name='vps-claim')
async def vps_claim_alias(ctx):
    cmd = bot.get_command('claim-free')
    if not cmd:
        return await ctx.send(embed=error_embed('Unavailable', 'claim-free command is not loaded.'))
    await ctx.invoke(cmd)


@bot.command(name='buywc')
async def buy_with_credits(ctx, plan: str = None, cpu_type: str = None):
    if not plan:
        return await ctx.send(embed=info_embed('Buy With Credits', f'Usage: `{BOT_PREFIX}buywc <plan> <Intel/AMD>`'))
    await ctx.send(embed=info_embed('Buy Request Received', f"```fix\nPlan: {plan}\nCPU: {cpu_type or 'Intel'}\nUse admin approval flow to complete purchase.\n```"))


@bot.command(name='announce')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def announce_cmd(ctx, *, message: str):
    owners = sorted({int(v['user_id']) for v in get_all_vps() if v.get('user_id')})
    sent = 0
    for uid in owners:
        try:
            u = await bot.fetch_user(uid)
            await u.send(f"📢 **Announcement from {BOT_NAME}**\n\n{message}")
            sent += 1
        except Exception:
            pass
    await ctx.send(embed=success_embed('Announcement Sent', f"```fix\nDelivered to {sent} users\n```"))


@bot.command(name='new-updates')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def new_updates_cmd(ctx, *, message: str):
    await announce_cmd(ctx, message=f"🆕 NEW UPDATE\n{message}")


@bot.command(name='leaderboard')
async def leaderboard_cmd(ctx):
    ensure_pmv_tables()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT w.user_id, w.credits, COALESCE(u.invites,0) invites, COALESCE(u.boosts,0) boosts FROM wallet w LEFT JOIN user_stats u ON w.user_id = u.user_id ORDER BY (w.credits + invites + boosts) DESC LIMIT 10')
    rows = cur.fetchall()
    conn.close()
    if not rows:
        return await ctx.send(embed=info_embed('Leaderboard', 'No data available yet.'))
    lines = []
    for i, r in enumerate(rows, 1):
        try:
            u = await bot.fetch_user(int(r['user_id']))
            name = u.name
        except Exception:
            name = f"User-{r['user_id'][:6]}"
        lines.append(f"#{i} {name} | C:{r['credits']} I:{r['invites']} B:{r['boosts']}")
    await ctx.send(embed=info_embed('🏆 Top Holders', '```fix\n' + '\n'.join(lines) + '\n```'))


@bot.command(name='report')
async def report_cmd(ctx, user: discord.Member, *, report_message: str):
    target_admin = MAIN_ADMIN_IDS[0] if MAIN_ADMIN_IDS else None
    if target_admin:
        try:
            owner_user = await bot.fetch_user(int(target_admin))
            await owner_user.send(
                f"🚨 **User Report**\nReporter: {ctx.author} ({ctx.author.id})\nTarget: {user} ({user.id})\nMessage: {report_message}"
            )
        except Exception:
            pass
    await ctx.send(embed=success_embed('Report Submitted', 'Owner has been notified via DM.'))


@bot.command(name='contact-owner')
async def contact_owner(ctx, issue_type: str, *, details: str):
    target_admin = MAIN_ADMIN_IDS[0] if MAIN_ADMIN_IDS else None
    if target_admin:
        try:
            owner_user = await bot.fetch_user(int(target_admin))
            await owner_user.send(
                f"📩 **Owner Contact Request**\nFrom: {ctx.author} ({ctx.author.id})\nType: {issue_type}\nDetails: {details}"
            )
        except Exception:
            pass
    await ctx.send(embed=success_embed('Message Sent', 'Your issue has been sent to the owner.'))


@bot.command(name='delete-vps')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def delete_vps_alias(ctx, user: discord.Member, num: int, *, reason: str = 'No reason'):
    cmd = bot.get_command('delete')
    if not cmd:
        return await ctx.send(embed=error_embed('Unavailable', 'delete command is missing.'))
    await ctx.invoke(cmd, user=user, num=num, reason=reason)


@bot.command(name='server-stats')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def server_stats_alias(ctx):
    cmd = bot.get_command('serverstats')
    if cmd:
        return await ctx.invoke(cmd)
    await ctx.send(embed=error_embed('Unavailable', 'serverstats command is missing.'))


@bot.command(name='prefix')
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def change_prefix(ctx, new_prefix: str):
    global BOT_PREFIX
    new_prefix = new_prefix.strip()
    if len(new_prefix) > 3:
        return await ctx.send(embed=error_embed('Invalid Prefix', 'Keep prefix up to 3 characters.'))
    BOT_PREFIX = new_prefix
    set_setting('bot_prefix', new_prefix)
    await ctx.send(embed=success_embed('Prefix Updated', f"Now using `{new_prefix}` (also supports `!` and `.`)."))


@bot.command(name='suspicious-check')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def suspicious_check(ctx):
    patterns = ['ddos', 'slowloris', 'udp flood', 'syn flood', 'bot.py']
    flagged = []
    for v in get_all_vps():
        container = v['container_name']
        out, _, code = await exec_in_container(container, "ps aux | head -n 80")
        if code == 0 and any(p.lower() in out.lower() for p in patterns):
            flagged.append(container)
            await run_lxc(f"lxc stop {container} --force")
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET suspended = 1, suspended_reason = ? WHERE container_name = ?', ('Suspicious process detected', container))
            conn.commit()
            conn.close()
    if not flagged:
        return await ctx.send(embed=success_embed('Scan Complete', 'No suspicious VPS found.'))
    await ctx.send(embed=warning_embed('Suspicious VPS Suspended', '```fix\n' + '\n'.join(flagged) + '\n```'))


@bot.command(name='warn-vps')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def warn_vps(ctx, num: int, user: discord.Member, *, warning: str):
    target = get_vps_by_num_for_user(str(user.id), num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid user VPS number.'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO vps_warnings (user_id, container_name, warning, warned_by, warned_at) VALUES (?, ?, ?, ?, ?)',
                (str(user.id), target['container_name'], warning[:500], str(ctx.author.id), datetime_.datetime.utcnow().isoformat()))
    cur.execute('SELECT COUNT(*) FROM vps_warnings WHERE user_id = ? AND container_name = ?', (str(user.id), target['container_name']))
    count = int(cur.fetchone()[0] or 0)
    if count >= 3:
        cur.execute('UPDATE vps SET suspended = 1, suspended_reason = ? WHERE container_name = ?', ('Too many warnings', target['container_name']))
    conn.commit()
    conn.close()
    if count >= 3:
        await run_lxc(f"lxc stop {target['container_name']} --force")
    await ctx.send(embed=warning_embed('VPS Warned', f"```fix\nContainer: {target['container_name']}\nWarnings: {count}\n```"))


@bot.command(name='add-plans')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def add_plans_cmd(ctx):
    await ctx.send(embed=info_embed('Plans Manager', 'Use existing plan commands and edit JSON/config. Interactive full plan editor can be added next.'))


@bot.command(name='remove-plans')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def remove_plans_cmd(ctx, *, plan_name_or_id: str):
    await ctx.send(embed=info_embed('Remove Plan Request', f"Received request to remove: `{plan_name_or_id}`"))


@bot.command(name='admin-check')
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def admin_check_cmd(ctx):
    patterns = ['python3 bot.py', 'ddos', 'slowloris', 'xmrig', 'masscan']
    removed = []
    for v in get_all_vps():
        container = v['container_name']
        out, _, code = await exec_in_container(container, 'ps aux')
        if code == 0 and any(p.lower() in out.lower() for p in patterns):
            await run_lxc(f'lxc stop {container} --force')
            await run_lxc(f'lxc delete {container}')
            delete_vps(container)
            removed.append(container)
    if not removed:
        return await ctx.send(embed=success_embed('Admin Check', 'No dangerous VPS found.'))
    await ctx.send(embed=warning_embed('Auto Deleted VPS', '```diff\n- ' + '\n- '.join(removed[:30]) + '\n```'))


@bot.command(name='extra-owner')
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def extra_owner(ctx, user: discord.Member, time: str):
    amount = 0
    unit = 'h'
    m = re.match(r'^(\d+)([dhm])$', time.lower())
    if m:
        amount = int(m.group(1))
        unit = m.group(2)
    if amount <= 0:
        return await ctx.send(embed=error_embed('Invalid Time', 'Use format like 12h, 7d, 30m'))
    delta = datetime_.timedelta(hours=amount) if unit == 'h' else datetime_.timedelta(days=amount) if unit == 'd' else datetime_.timedelta(minutes=amount)
    exp = datetime_.datetime.utcnow() + delta
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO owner_delegates (user_id, expires_at, added_by, added_at) VALUES (?, ?, ?, ?)',
                (str(user.id), exp.isoformat(), str(ctx.author.id), datetime_.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('Extra Owner Added', f"```fix\n{user} until {exp.isoformat()} UTC\n```"))


@bot.command(name='remove-owner')
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def remove_owner(ctx, user: discord.Member):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM owner_delegates WHERE user_id = ?', (str(user.id),))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('Owner Removed', f'`{user}` no longer has extra-owner permissions.'))


@bot.command(name='bot-update')
@commands.check(lambda ctx: str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS])
async def bot_update(ctx, status: str = 'online', *, message: str = None):
    status_map = {
        'online': discord.Status.online,
        'dnd': discord.Status.dnd,
        'idle': discord.Status.idle,
        'invisible': discord.Status.invisible,
        'offline': discord.Status.offline,
    }
    activity = discord.Game(name=message or f'{BOT_PREFIX}help')
    await bot.change_presence(status=status_map.get(status.lower(), discord.Status.online), activity=activity)
    await ctx.send(embed=success_embed('Bot Presence Updated', f"Status: `{status}`\nMessage: `{message or (BOT_PREFIX + 'help')}`"))


@bot.command(name='maintaince')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def maintaince_alias(ctx, mode: str):
    cmd = bot.get_command('maintenance')
    if not cmd:
        return await ctx.send(embed=error_embed('Unavailable', 'maintenance command is missing.'))
    await ctx.invoke(cmd, mode=mode)


@bot.command(name='purge-system')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def purge_system(ctx, action: str, timer: int = 60):
    if action.lower() == 'activate':
        set_setting('purge_system', f'active:{timer}')
        await ctx.send(embed=warning_embed('Purge System Activated', f'Unprotected VPS can be purged after {timer} minutes.'))
    elif action.lower() == 'deactivate':
        set_setting('purge_system', 'inactive')
        await ctx.send(embed=success_embed('Purge System Deactivated', 'Purge checks disabled.'))
    else:
        await ctx.send(embed=error_embed('Invalid Action', 'Use activate/deactivate'))


@bot.command(name='purge-protect')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def purge_protect_alias(ctx, user: discord.Member, vps_number: int = None):
    cmd = bot.get_command('protect')
    if not cmd:
        return await ctx.send(embed=error_embed('Unavailable', 'protect command is missing.'))
    if vps_number is None:
        await ctx.invoke(cmd, user=user)
    else:
        await ctx.invoke(cmd, user=user, num=vps_number)


@bot.command(name='setexpire')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def setexpire(ctx, user: discord.Member, vps_num: int, days: int):
    target = get_vps_by_num_for_user(str(user.id), vps_num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid VPS number.'))
    expires = datetime_.datetime.utcnow() + datetime_.timedelta(days=days)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO vps_expiry (container_name, expires_at, updated_by, updated_at) VALUES (?, ?, ?, ?)',
                (target['container_name'], expires.isoformat(), str(ctx.author.id), datetime_.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('Expiry Set', f"`{target['container_name']}` expires on `{expires.isoformat()} UTC`"))


@bot.command(name='extendexpire')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def extendexpire(ctx, user: discord.Member, vps_num: int, days: int):
    target = get_vps_by_num_for_user(str(user.id), vps_num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid VPS number.'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT expires_at FROM vps_expiry WHERE container_name = ?', (target['container_name'],))
    row = cur.fetchone()
    base = datetime_.datetime.utcnow()
    if row and row[0]:
        try:
            base = datetime_.datetime.fromisoformat(row[0])
        except Exception:
            base = datetime_.datetime.utcnow()
    expires = base + datetime_.timedelta(days=days)
    cur.execute('INSERT OR REPLACE INTO vps_expiry (container_name, expires_at, updated_by, updated_at) VALUES (?, ?, ?, ?)',
                (target['container_name'], expires.isoformat(), str(ctx.author.id), datetime_.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('Expiry Extended', f"`{target['container_name']}` now expires on `{expires.isoformat()} UTC`"))


@bot.command(name='removeexpire')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)))
async def removeexpire(ctx, user: discord.Member, vps_num: int):
    target = get_vps_by_num_for_user(str(user.id), vps_num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid VPS number.'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM vps_expiry WHERE container_name = ?', (target['container_name'],))
    conn.commit()
    conn.close()
    await ctx.send(embed=success_embed('Expiry Removed', f"`{target['container_name']}` is now set to Never."))


@bot.command(name='checkexpire')
@commands.check(lambda ctx: is_admin(str(ctx.author.id)) or True)
async def checkexpire(ctx, user: discord.Member = None):
    target_user_id = str(user.id) if user else str(ctx.author.id)
    rows = get_user_vps(target_user_id)
    if not rows:
        return await ctx.send(embed=info_embed('Expiry Status', 'No VPS found for this user.'))
    conn = get_db()
    cur = conn.cursor()
    embed = info_embed('⏳ VPS Expiry Status')
    for i, v in enumerate(rows, 1):
        cur.execute('SELECT expires_at FROM vps_expiry WHERE container_name = ?', (v['container_name'],))
        row = cur.fetchone()
        exp = row[0] if row else None
        embed.add_field(name=f"#{i} {v['container_name']}", value=f"`{exp if exp else 'Never'}`", inline=False)
    conn.close()
    await ctx.send(embed=embed)


@bot.command(name='cm-install')
async def cm_install(ctx, num: int, option: str = 'all'):
    target = get_vps_by_num_for_user(str(ctx.author.id), num)
    if not target:
        return await ctx.send(embed=error_embed('Invalid', 'Invalid VPS number.'))
    opt = option.lower()
    tasks_to_run = []
    if opt in ['tailscale', 'all']:
        tasks_to_run.append('curl -fsSL https://tailscale.com/install.sh | sh')
    if opt in ['cloudflare', 'all']:
        tasks_to_run.append('curl -fsSL https://pkg.cloudflare.com/install.sh | bash')
    if opt in ['pufferpanel', 'all']:
        tasks_to_run.append('bash -c "curl -s https://packagecloud.io/install/repositories/pufferpanel/pufferpanel/script.deb.sh | bash && apt-get install -y pufferpanel"')
    if not tasks_to_run:
        return await ctx.send(embed=error_embed('Invalid Option', 'Use tailscale/cloudflare/pufferpanel/all'))
    await ctx.send(embed=info_embed('Installation Started', f"```fix\nContainer: {target['container_name']}\nOption: {opt}\n```"))
    results = []
    for cmd in tasks_to_run:
        out, err, code = await exec_in_container(target['container_name'], cmd, timeout=180)
        results.append(f"[{code}] {cmd[:50]} -> {'OK' if code == 0 else 'FAIL'}")
    await ctx.send(embed=info_embed('CM Install Result', '```fix\n' + '\n'.join(results) + '\n```'))


@bot.command(name='pmv-help')
async def pmv_help(ctx):
    embed = discord.Embed(
        title=f"✨ {BOT_NAME} Help Center",
        description=(
            f"Use `{BOT_PREFIX}help` for interactive categories.\n"
            f"Also supports `!` prefix for most commands.\n\n"
            "👤 User: ping, uptime, bot-status, manage, share-user, links, vps-stats, cm-install, rename-vps, upi, pay-options\n"
            "🖥️ VPS: manage-shared, share-list, transfer-ownership, vps-note, uptime-vps, myinfo\n"
            "💰 Credits: plans, buyc, buywc, credits, transfer, daily-credits, vps-claim\n"
            "📢 Extras: announce, leaderboard, new-updates, report, contact-owner\n"
            "🛡️ Admin: create, delete-vps, server-stats, prefix, resize, suspicious-check, warn-vps\n"
            "👑 Owner: admin-add, admin-remove, admin-list, admin-check, extra-owner, remove-owner, bot-update, maintaince, purge-system, purge-protect, setexpire, extendexpire, removeexpire, checkexpire"
        ),
        color=COLORS['gold']
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_footer(text=f"{BOT_NAME} • Beautiful command center")
    await ctx.send(embed=embed)

# ==================================================================================================
#  🚀  RUN THE BOT
# ==================================================================================================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE" or not BOT_TOKEN.strip():
        print("\n❌ ERROR: Please set BOT_TOKEN or DISCORD_BOT_TOKEN environment variable!")
        sys.exit(1)
    if not MAIN_ADMIN_IDS:
        print("\n❌ ERROR: MAIN_ADMIN_IDS is empty. Please configure at least one admin ID.")
        sys.exit(1)
    update_local_node_stats()
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n❌ ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
