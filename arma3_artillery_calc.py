from fractions import Fraction
import numpy as np
import sympy as s

velocity_table = [153.9,243,388.8,648,810]
charge_level = -1

def artillery_calc_mod1():

    print('\n[+] please input 10 step coordinates (ex. 123 456 => 12300 45600)')
    x1 = int(input('your x-axis coordinate > '))
    y1 = int(input('your y-axis coordinate > '))
    z1 = int(input('your altitude > '))
    x2 = int(input('target x-axis coordinate > '))
    y2 = int(input('target y-axis coordinate > '))
    z2 = int(input('target altitude > '))

    angle = s.atan2((x1 - x2), (y1 - y2)) * float(Fraction(180, Fraction(np.pi)) * Fraction(6400, 360))
    rx = round(np.sqrt(((x1 - x2)**2) + ((y1 - y2)**2)))

    if rx < 300 or rx > 29900:
        print('invalid distance')
        print('distance : ' + str(rx))
        return
    elif rx >= 300 and rx < 2500:
        charge_level = 0
        v = velocity_table[charge_level]
    elif rx >= 2500 and rx < 6100:
        charge_level = 1
        v = velocity_table[charge_level]
    elif rx >= 6100 and rx < 15500:
        charge_level = 2
        v = velocity_table[charge_level]
    elif rx >= 15500 and rx <= 29900:
        charge_level = 3
        v = velocity_table[charge_level]

    v2 = v*v
    v4 = v2*v2
    rx2 = rx*rx
    g = 9.80665
    ry = z1 - z2

    res_h = s.atan((v2 + s.sqrt(v4 - g * ((g * rx2) + (2 * ry * v2)))) / (g * rx))
    res_l = s.atan((v2 - s.sqrt(v4 - g * ((g * rx2) + (2 * ry * v2)))) / (g * rx))

    sa = res_h * 180 / np.pi
    sk = res_l * 180 / np.pi
    eta_l = round((rx / (v * s.cos(sk*np.pi/180))), 1)
    eta_h = round((rx / (v * s.cos(sa*np.pi/180))), 1)

    if angle > 0:
        an = 3200 - angle
        angle = 6400 - an
    elif angle < 0:
        angle = 3200 + angle

    sk *= (6400/360)
    sa *= (6400/360)

    print()
    print('[+] Shooting Angle : ' + str(round(angle)))
    print('[+] Low angle elevation : ' + str(round(sk)))
    print('[+] Low ELEV ETA : ' + str(eta_l))
    print('[+] High angle elevation : ' + str(round(sa)))
    print('[+] High ELEV ETA : ' + str(eta_h))
    print('[+] Charge level : ' + str(charge_level))
    print()

def artillery_calc_mod2():

    rx = int(input('distance between you and the target (minimum = 300) > '))
    z1 = int(input('your altitude > '))
    z2 = int(input('target altitude > '))

    if rx < 300 or rx > 29900:
        print('invalid distance')
        print('distance : ' + str(rx))
        return
    elif rx >= 300 and rx < 2500:
        charge_level = 0
        v = velocity_table[charge_level]
    elif rx >= 2500 and rx < 6100:
        charge_level = 1
        v = velocity_table[charge_level]
    elif rx >= 6100 and rx < 15500:
        charge_level = 2
        v = velocity_table[charge_level]
    elif rx >= 15500 and rx <= 29900:
        charge_level = 3
        v = velocity_table[charge_level]

    v2 = v*v
    v4 = v2*v2
    rx2 = rx*rx
    g = 9.80665
    ry = z1 - z2

    res_h = s.atan((v2 + s.sqrt(v4 - g * ((g * rx2) + (2 * ry * v2)))) / (g * rx))
    res_l = s.atan((v2 - s.sqrt(v4 - g * ((g * rx2) + (2 * ry * v2)))) / (g * rx))

    sa = res_h * 180 / np.pi
    sk = res_l * 180 / np.pi
    eta_l = round((rx / (v * s.cos(sk*np.pi/180))), 1)
    eta_h = round((rx / (v * s.cos(sa*np.pi/180))), 1)

    sk *= (6400/360)
    sa *= (6400/360)

    print()
    print('[+] Low angle elevation : ' + str(round(sk)))
    print('[+] Low ELEV ETA : ' + str(eta_l))
    print('[+] High angle elevation : ' + str(round(sa)))
    print('[+] High ELEV ETA : ' + str(eta_h))
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
