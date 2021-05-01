import wifi

networks = []

#cells = wifi.Cell.all('wlp8s0')

cells = wifi.Scheme.all()

for cell in cells:
    networks.append(cell)
    print(cell.ssid)
