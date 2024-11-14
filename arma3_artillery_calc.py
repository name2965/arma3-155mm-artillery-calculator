from fractions import Fraction
import numpy as np
import sympy as s

artillery_type_table = ['Exit Program', 'M109A6 & Sholef', 'Panzerhaubitze2000', 'M252 (81mm)', 'M119A2 (105mm)']
min_distance_table   = [0, 300, 400, 50, 300] # vel_charge_calc 로직과 함께 추후 수정 필요

# 포 종류(art_type)와 거리(rx)를 입력 받아, 포구 속도(V)와 장약(charge_level) 결정
# 수정 필요
def vel_charge_calc(rx, art_type): 
    if art_type == 1: # M109A6(Paladin) & Sholef
        velocity_table = [153.9, 243, 388.8, 648, 810]
        if rx < 300 or rx > 29900:
            return -1, -1
        elif rx >= 300 and rx < 2500:
            charge_level = 0
        elif rx >= 2500 and rx < 6100:
            charge_level = 1
        elif rx >= 6100 and rx < 15500:
            charge_level = 2
        elif rx >= 15500 and rx <= 29900:
            charge_level = 3
        v = velocity_table[charge_level]
    elif art_type == 2: # Panzerhaubitze2000(PzH2000)
        velocity_table = [222.8, 259.2, 291.6, 344.3, 405.0, 477.9, 550.8]
        if rx < 400 or rx > 29900:
            return -1, -1
        elif rx >= 400 and rx < 5100:
            charge_level = 0
        elif rx >= 5100 and rx < 6900:
            charge_level = 1
        elif rx >= 6900 and rx < 8700:
            charge_level = 2
        elif rx >= 8700 and rx < 12100:
            charge_level = 3
        elif rx >= 12100 and rx < 16800:
            charge_level = 4
        elif rx >= 16800 and rx < 23300:
            charge_level = 5
        elif rx >= 23300 and rx < 29900:
            charge_level = 6
        v = velocity_table[charge_level]
    elif art_type == 3: # M252 (81mm)
        velocity_table = [70, 140, 200]
        if rx <50 or rx > 4050:
            return -1, -1
        elif rx >= 50 and rx < 450:
            charge_level = 0
        elif rx >= 450 and rx < 1950:
            charge_level = 1
        elif rx >= 1950 and rx < 4050:
            charge_level = 2
        v = velocity_table[charge_level]
    elif art_type == 4: # M119A2 (105mm)
        velocity_table = [153.9, 243, 388.8]
        if rx < 300 or rx > 15400:
            return -1, -1
        elif rx >= 300 and rx < 2500:
            charge_level = 0
        elif rx >= 2500 and rx < 6100:
            charge_level = 1
        elif rx >= 6100 and rx < 154000:
            charge_level = 2
        v = velocity_table[charge_level]
    else:
        return -2, -2
    
    return v, charge_level

# 사용자가 number 타입만 입력하도록 안내
# isCoordinate = True 일 경우만 5자리 입력하도록 추가 안내
def get_number_input(prompt, isCoordinate = False):
    while True:
        try:
            if isCoordinate:
                axis_input = input(prompt)
                if len(axis_input) == 5:
                    return int(axis_input)
                else:
                    print("[Error] invalid value")
                    print("[Error] input 5 number (ex. 12300)")
            else :
                return int(input(prompt))
        except ValueError:
            print("[Error] invalid value")
            print("[Error] input number value")

def artillery_calc_mod1(art_type):

    print('\n[+] please input 10 step coordinates (ex. 123 456 => 12300 45600)')
    x1 = get_number_input('your x-axis coordinate > ', True)
    y1 = get_number_input('your y-axis coordinate > ', True)
    z1 = get_number_input('your altitude > ')
    x2 = get_number_input('target x-axis coordinate > ', True)
    y2 = get_number_input('target y-axis coordinate > ', True)
    z2 = get_number_input('target altitude > ')

    angle = s.atan2((x1 - x2), (y1 - y2)) * float(Fraction(180, Fraction(np.pi)) * Fraction(6400, 360))
    rx = round(np.sqrt(((x1 - x2)**2) + ((y1 - y2)**2)))
    v, charge_level = vel_charge_calc(rx, art_type)
    if v == -1:
        print('[Error] invalid distance')
        print('[Error] distance : ' + str(rx))
        return

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

    print('============================================')
    print('[+] Shooting Angle : ' + str(round(angle)))
    print('[+] Low angle elevation : ' + str(round(sk)))
    print('[+] Low ELEV ETA : ' + str(eta_l))
    print('[+] High angle elevation : ' + str(round(sa)))
    print('[+] High ELEV ETA : ' + str(eta_h))
    print('[+] Charge level : ' + str(charge_level))
    print('============================================')

def artillery_calc_mod2(art_type):

    rx = get_number_input('distance between you and the target (minimum = ' + str(min_distance_table[art_type]) + ') > ')
    z1 = get_number_input('your altitude > ')
    z2 = get_number_input('target altitude > ')
    v, charge_level = vel_charge_calc(rx, art_type)
    if v == -1:
        print('[Error] invalid distance')
        print('[Error] distance : ' + str(rx))
        return

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

    print('============================================')
    print('[+] Low angle elevation : ' + str(round(sk)))
    print('[+] Low ELEV ETA : ' + str(eta_l))
    print('[+] High angle elevation : ' + str(round(sa)))
    print('[+] High ELEV ETA : ' + str(eta_h))
    print('[+] Charge level : ' + str(charge_level))
    print('============================================')

# 포 종류(art_type) 선택 시 0번 입력하여 프로그램 종료하지 않는 이상 계속 반복
if __name__ == '__main__':
    while True:
        print('\nArma3 Artillery Calculator')
        print('Select type of artillery')
        for idx, val in enumerate(artillery_type_table):
            print(f'{idx}. {val}')
        art_type = get_number_input('> ')
        if art_type == 0:
            break
        elif art_type > len(artillery_type_table) - 1:
            print('[Error] invalid type')
            print('[Error] please input 1 ~ ' + str(len(artillery_type_table) - 1))
            continue
        print('Select calculate mode')
        print('1. coordinate-based calculation mode')
        print('2. distance-based calculation mode')

        mode = get_number_input('> ')

        if mode == 1:
            artillery_calc_mod1(art_type)
        elif mode == 2:
            artillery_calc_mod2(art_type)
        else:
            print('[Error] invalid input')
            print('[Error] please input 1 or 2')