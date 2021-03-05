from time import sleep
import subprocess

# command = 'scrapy crawl enigma'
# subprocess.run(command, shell=True)

timeout = 30

while True:
    command = 'scrapy crawl enigma'
    subprocess.run(command, shell=True)
    sleep(timeout)
