from fractions import Fraction
import numpy as np
import sympy as s
import math as m

velocity_table = [242.9,388.8,649]
charge_level = -1
t = s.Symbol('t', real=True)
theta = s.Symbol('theta', real=True)

def artillery_calc_mod1():

    print('\n[+] please input 10 step coordinates (ex. 123 456 => 12300 45600)')
    x1 = int(input('your x-axis coordinate > '))
    y1 = int(input('your y-axis coordinate > '))
    z1 = int(input('your altitude > '))
    x2 = int(input('target x-axis coordinate > '))
    y2 = int(input('target y-axis coordinate > '))
    z2 = int(input('target altitude > '))

    angle = m.atan2((x1 - x2), (y1 - y2)) * float(Fraction(180, Fraction(np.pi)) * Fraction(6400, 360))
    rx = round(np.sqrt(((x1 - x2)**2) + ((y1 - y2)**2)))

    if rx % 10 != 0:
        rx += 10 - (rx%10)

    if rx < 1400 or rx > 29900:
        print('invalid distance')
        return
    elif rx >= 1400 and rx < 6000:
        charge_level = 1
        v = velocity_table[charge_level-1]
    elif rx >= 6000 and rx < 15400:
        charge_level = 2
        v = velocity_table[charge_level-1]   
    elif rx >= 15400 and rx <= 29900:
        charge_level = 3
        v = velocity_table[charge_level-1]

    if angle > 0:
        an = 3200 - angle
        angle = 6400 - an
    elif angle < 0:
        angle = 3200 + angle

    ax = np.pi * 0.00085 * 1.225 * 0.155**2 * float(Fraction(Fraction(v**2), (8 * 45)))
    ay = np.pi * 0.00085 * 1.225 * 0.155**2 * float(Fraction(Fraction(v**2), (8 * 45)))

    eq1 = rx - (5 * s.cos(theta) + v * s.cos(theta) * t - (1/2) * ax * s.cos(theta) * t**2)
    eq2 = z2 - ((z1 + 5*s.sin(theta)) + v * s.sin(theta) * t - (1/2) * (ay * s.sin(theta) + (980665/100000)) * t**2)

    res = s.solve((eq1, eq2), (theta, t), dict=True)
    
    for i in range(len(res)):
        if res[i][t] >= 50.0 or res[i][t] < 1:
            continue
        sk = res[i][theta] * float(Fraction(180, Fraction(np.pi)) * Fraction(6400, 360))
        sa = 1600 - sk

        if sk >= sa:
            continue

        print()
        print('[+] Shooting Angle : ' + str(round(angle)))
        print('[+] Low angle elevation : ' + str(round(sk, 1)))
        print('[+] ETA : ' + str(round(res[i][t], 1)))
        print('[+] Charge level : ' + str(charge_level))
        print()


def artillery_calc_mod2():

    rx = int(input('distance between you and the target (minimum = 1400) > '))
    z1 = int(input('your altitude > '))
    z2 = int(input('target altitude > '))

    if rx % 10 != 0:
        rx += 10 - (rx%10)

    if rx < 1400 or rx > 29900:
        print('invalid distance')
        return
    elif rx >= 1400 and rx < 6000:
        charge_level = 1
        v = velocity_table[charge_level-1]
    elif rx >= 6000 and rx < 15400:
        charge_level = 2
        v = velocity_table[charge_level-1]   
    elif rx >= 15400 and rx <= 29900:
        charge_level = 3
        v = velocity_table[charge_level-1]

    ax = np.pi * 0.00085 * 1.225 * 0.155**2 * float(Fraction(Fraction(v**2), (8 * 45)))
    ay = np.pi * 0.00085 * 1.225 * 0.155**2 * float(Fraction(Fraction(v**2), (8 * 45)))

    eq1 = rx - (5 * s.cos(theta) + v * s.cos(theta) * t - (1/2) * ax * s.cos(theta) * t**2)
    eq2 = z2 - ((z1 + 5*s.sin(theta)) + v * s.sin(theta) * t - (1/2) * (ay * s.sin(theta) + (980665/100000)) * t**2)

    res = s.solve((eq1, eq2), (theta, t), dict=True)

    for i in range(len(res)):
        if res[i][t] >= 50.0 or res[i][t] < 1:
            continue
        sk = res[i][theta] * float(Fraction(180, Fraction(np.pi)) * Fraction(6400, 360))
        sa = 1600 - sk

        if sk >= sa:
            continue

        print()
        print('[+] Low angle elevation : ' + str(round(sk,8)))
        print('[+] ETA : ' + str(round(res[i][t], 1)))
        print('[+] Charge level : ' + str(charge_level))
        print()

if __name__ == '__main__':

    print('\narma3 M4 Scorcher 155mm artillery calculator\n')
    print('select calculate mode')
    print('1. coordinate-based calculation mode')
    print('2. distance-based calculation mode')

    mode = int(input('> '))

    if mode == 1:
        artillery_calc_mod1()
    elif mode == 2:
        artillery_calc_mod2()
    else:
        print('[+] invalid input')
        print('[+] please input 1 or 2')
