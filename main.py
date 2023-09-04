import subprocess
import time
from colour import Color
from sense_hat import SenseHat

# 100 color gradient from red to green
colors = list(Color('blue').range_to(Color("red"), 100))
# sense = SenseHat()
loop_condition = True

pixels = [
    (1, 1),  # down
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),  # right
    (2, 6),
    (3, 6),
    (4, 6),
    (5, 6),
    (6, 6),  # up
    (6, 5),
    (6, 4),
    (6, 3),
    (6, 2),
    (6, 1),  # left
    (5, 1),
    (4, 1),
    (3, 1),
    (2, 1)   # ultimate point

    # total pixels: 20
    # degree range: 1-100
    # so 5 degrees per pixel
]


def toggle_loop_condition():
    global loop_condition
    loop_condition = not loop_condition


def get_temp():
    # get temperature from system
    thermal_zone_temp = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp'])
    # convert to int, divide by 1000, and round to whole numbers
    # divide because the system value is wonky
    cpu_temp = round(int(thermal_zone_temp) / 1000)
    return cpu_temp


def get_elligible_pixels(temp):
    pixel_amount = round(temp / 5)
    return pixels[0:pixel_amount]


def get_color(temp):
    temp = temp - 1
    color = colors[temp].rgb
    return round(color[0]), round(color[1]), round(color[2])


def main():
    while True:
        temp = get_temp()
        color = get_color(temp)
        pxs = get_elligible_pixels(temp)

        for px in pxs:
            sense.set_pixel(x=px[0], y=px[1], pixel=color)

        if not loop_condition:
            sense.clear()
            break

        time.sleep(2)


sense.stick.direction_any = toggle_loop_condition

if __name__ == '__main__':
    main()
