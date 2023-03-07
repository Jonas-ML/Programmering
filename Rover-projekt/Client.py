import socket, pygame

print("Kører klienten\n")
skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Laver en socket
host = "192.168.1.145" # Dette er IP-adressen for Raspberry Pi
port = 3000

pygame.init()
screen = pygame.display.set_mode((300,200))

while True:
    events = pygame.event.get()
    for event in events:
       
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            data="forwards"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
        elif event.type == pygame.KEYUP and event.key == pygame.K_UP:
            data="stop"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            data="backwards"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            data="stop"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            data="left"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            data="cutl"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            data="right"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            data="cutr"
            indkodet_data = data.encode("UTF-8")
            skt.sendto(indkodet_data,(host, port))
