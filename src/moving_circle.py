from colorlog import ColorLog
import logging
from shell import Shell as shell

log = ColorLog(logging.getLogger("texture_compress__automatic"))  # remove __automatic (some day)
log.setLevel('INFO')
shell.setLogger(log)

for i in range(352//2):
    shell.run("convert -size 352x288 xc:skyblue "
              + "-fill white -stroke black -draw \"circle "
              + str(42+i) + ",42 " + str(74+i) + ",42\" /tmp/circle"
              + str('%03d' % i) + ".png")

shell.run("ffmpeg -i /tmp/circle%3d.png /tmp/out.avi")
