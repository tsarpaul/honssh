from docker import Client
from time import sleep
from honssh.config import Config

client = Client()
conf = Config.getInstance()
honssh_guest_image = conf.get(['honeypot-docker', 'image'])
print("[cleanupd.py][+ ] HONSSH_GUEST_IMAGE = " + honssh_guest_image)

while True:
    print("[cleanupd.py][+ ] Polling!")
    containers = client.containers()
    for container in containers:
        if not honssh_guest_image in container['Image']:
            continue
        time = 0
        time_unit = ''
        try:
            # expect status to be in format of 'up <time> <time_unit>'; time=int, time_unit=seconds/minutes/hours
            status = container['Status']
            _, time, time_unit = status.split(' ')
            time = int(time)
        except:
            continue
        if time > 5 and time_unit == 'minutes':
            print("[cleanupd.py][+ ] Killing container " + container['Names'][0])
            client.kill(container['Id'])
    sleep(30)
