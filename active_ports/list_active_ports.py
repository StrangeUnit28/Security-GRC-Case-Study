import psutil

print("Active (listening) ports:")
for conn in psutil.net_connections(kind="inet"):
    if conn.status == psutil.CONN_LISTEN:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
        proto = "TCP" if conn.type == 1 else "UDP"
        print(f"{proto} {laddr}")