import board
import busio
import digitalio
import adafruit_max31855
from time import sleep

import time
t0=time.time() #start time
print(t0)

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
max31855 = adafruit_max31855.MAX31855(spi,cs)

spi_2 = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs_2 = digitalio.DigitalInOut(board.D6)
max31855_2 = adafruit_max31855.MAX31855(spi_2,cs_2)

print('Temp/K,time/s')
f = open('test.txt', mode='a')
f.write('Temp/K,time/s\n')
f.close()

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#鍵
key_name = 'temperature-measurement60876-76ca5673b803.json'
sheet_name = '発表当日デモンストレーション'

#APIにログイン
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(key_name, scope)
gc = gspread.authorize(credentials)

#セル'A1'に'time/s','A2'に'Temp/K'と入力
try:
    cell_number1 = 'A1'
    input_value1 = 'time/s'
    wks = gc.open(sheet_name).sheet1
    wks.update_acell(cell_number1, input_value1)
    cell_number2 = 'B1'
    input_value2 = 'Temp/K'
    wks.update_acell(cell_number2, input_value2)
    cell_number3 = 'C1'
    input_value3 = 'Temp/K'
    wks.update_acell(cell_number3, input_value3)
    cell_number4 = 'D1'
    input_value4 = '温度変化'
    wks.update_acell(cell_number4, input_value4)
    cell_number5 = 'E1'
    input_value5 = '時間変化'
    wks.update_acell(cell_number5, input_value5)
    cell_number6 = 'F1'
    input_value6 = '昇温速度'
    wks.update_acell(cell_number6, input_value6)
except:
    pass
cell_list = wks.range('A2:F11')

sheet_pointer =2
list_pointer = 0

import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

from pygame.locals import *
import pygame
pygame.init()    # Pygameを初期化
screen = pygame.display.set_mode((400, 330))    # 画面を作成
pygame.display.set_caption("keyboard event")    # タイトルを作成

t1=0
T1=max31855.temperature
T3=max31855_2.temperature
keyFlag=False

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:  # キーを押したとき
            # ESCキーならスクリプトを終了
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            else:
                key = pygame.key.name(event.key)
                print("押されたキー = " + key)
                if key == 'a' :
                    GPIO.output(18,True)
                    print('手動加熱')
                    keyFlag=True
                elif key == 'b':
                    GPIO.output(18,False)
                    print('手動冷却')
                    keyFlag=True
                elif key == 'c':
                    print('auto')
                    keyFlag=False
                elif key == 'd':
                    print('done')
                    GPIO.output(18,False)
                    GPIO.cleanup()
                    sys.exit(0)                
    pygame.display.update()
    t2=time.time()
    dt=t2-t1-t0
    t1=t2-t0
    T2=max31855.temperature
    dT=T2-T1
    T1=T2
    if not keyFlag:
        if 60*dT/dt <= 5 :
             GPIO.output(18,True)
        else :
            GPIO.output(18,False)
    print('温度変化',dT,'時間変化',round(dt,3),'現在温度1',T2+273.15,'現在温度2',T3+273.15,'時刻',round(t1,2),'昇温速度',round(60*dT/dt,3))
    f = open('test.txt', mode='a')
    f.write(str(T2+273.15)+",")
    f.write(str(round(t1,3))+"\n")
    f.close()
    cell_list[list_pointer].value=t1
    cell_list[list_pointer+1].value=T2+273.15
    cell_list[list_pointer+2].value=T3+273.15
    cell_list[list_pointer+3].value=dT
    cell_list[list_pointer+4].value=dt
    cell_list[list_pointer+5].value=60*dT/dt
    list_pointer+=6
    if list_pointer > 54:
        print('upload')
        wks.update_cells(cell_list)
        list_pointer = 0
        sheet_pointer += 10
        cell_list = wks.range('A'+str(sheet_pointer)+':F'+str(sheet_pointer+9))

            
            
        
       
    


     


         





