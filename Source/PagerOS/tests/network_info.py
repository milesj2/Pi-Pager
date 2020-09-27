import psutil


ADDRESS_LOCAL = "127.0.0.1"
LAN = "eth0"

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# Network information
print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        if str(address.family) != 'AddressFamily.AF_INET':
            continue
        if address.address == ADDRESS_LOCAL:
            continue
        print(f"=== Interface: {interface_name} ===")
        print(f"  IP Address: {address.address}")
        print(f"  Netmask: {address.netmask}")
        print(f"  Broadcast IP: {address.broadcast}")

# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

print(__name__)
print(__file__)
