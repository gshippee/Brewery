from __future__ import print_function  
import remi.gui as gui 
from remi.gui import * 
from remi import start, App 
from threading import Timer 
import hid  
import time  
import serial 
import struct 
import numpy as np 
from datetime import datetime, date, time 
from time import sleep 
import pandas as pd 
from pandas import ExcelWriter 
from pandas import ExcelFile 
 
data = serial.Serial(port='/dev/cu.SLAB_USBtoUART', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1) 
print("connected to: " + data.portstr) 

start_time = 0
start_time_second = 0
start_time_minute = 0
start_time_hour = 0
total_start_time = 0

continue_on = False
pause = False

target_temp1 = 0
target_temp2 = 0

instructions = 0
step = 0

heater1 = True
heater2 = True

first_loop = True

fileupload = False

class Brewery(App):
	def __init__(self, *args):
		super(Brewery, self).__init__(*args, static_file_path='./res/')

	def main(self):
		print("Opening app")
		verticalContainer = gui.Widget(style={'width': '100%', 'height': '100%','display': 'block', 'overflow': 'auto', 'text-align': 'center', 'background-color': '#2F4F4f', 'border-color': 'black', 'border-width': '2px', 'border-style' : 'solid', 'left':'20%' })

		self.relay_num = 0
		self.kettle1_time = 0
		self.kettle2_time = 0
		self.kettle2_time1 = 0
		self.kettle3_time = 0
		self.relay_time = 0
		self.check_on = False
		self.check_count = 0

		self.fire_img = gui.Image('res/blank.png', style = {'width':'16%', 'height':'8.0%', 'left': '6.5%', 'margin':'auto', 'top': '52%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
		self.kettle_img = gui.Image('res/kettle.png', style = {'width':'17.0%', 'height':'25.0%', 'left': '8%', 'margin':'auto', 'top': '32%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})

		self.kettle_img2 = gui.Image('res/second_kettle.png', style = {'width':'17.0%', 'height':'28.0%', 'left': '28%', 'margin':'auto', 'top': '34%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.kettle_img3 = gui.Image('res/monk-brewing-beer.png', style = {'width':'12.0%', 'height':'27.0%', 'left': '54%', 'margin':'auto', 'top': '31%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.kettle_img4 = gui.Image('res/beer_barrel.png', style = {'width':'17.0%', 'height':'23.0%', 'left': '74%', 'margin':'auto', 'top': '65%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.fire_img1 = gui.Image('res/blank.png', style = {'width':'16%', 'height':'8.0%', 'left': '50.5%', 'margin':'auto', 'top': '52%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
		self.water_pump1 = gui.Image('res/pump_static.png', style = {'width':'7.0%', 'height':'8.50%', 'left': '29%', 'margin':'auto', 'top': '60%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.water_pump2 = gui.Image('res/pump_static.png', style = {'width':'7.0%', 'height':'8.50%', 'left': '49%', 'margin':'auto', 'top': '60%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.water_pump3 = gui.Image('res/pipes.gif', style = {'width':'19.0%', 'height':'35.0%', 'left': '37.5%', 'filter':'flipH', 'margin':'auto', 'top': '33.5%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.water_pump4 = gui.Image('res/pipes.gif', style = {'width':'19.0%', 'height':'35.0%', 'left': '37.5%', 'filter':'flipH', 'margin':'auto', 'top': '33.5%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.heat_exchanger = gui.Image('res/heat_exchanger.png', style = {'width':'9.0%', 'height':'10.50%', 'left': '69%', 'margin':'auto', 'top': '58%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.faucet = gui.Image('res/blank.png', style = {'width':'7.0%', 'height':'8.50%', 'left': '65%', 'margin':'auto', 'top': '66%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.cup = gui.Image('res/blank.png', style = {'width':'8.0%', 'height':'8.0%', 'left': '48%', 'margin':'auto', 'top': '28%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.sign = gui.Image('res/sign2.png', style = {'width':'28.0%', 'height':'24.0%', 'left': '36%', 'margin':'auto', 'top': '72%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.pipe = gui.Image('res/pipe-only1.png', style = {'width':'14.0%', 'height':'24.0%', 'left': '59%', 'margin':'auto', 'top': '48%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})
		self.pipe_right = gui.Image('res/pipes-right-only-static.png', style = {'width':'19.0%', 'height':'35.0%', 'left': '17.5%', 'filter':'flipH', 'margin':'auto', 'top': '33.5%', 'display' : 'block', 'position' : 'absolute', 'z-index' : '0'})


		self.counter = gui.Label('', style = {'width' : '24%', 'height' : '10%', 'padding-top' : '1%', 'color': 'green', 'left' : '3%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '2.5vw', 'top' : '82%', 'text-align':'center', 'z-index' : '0'})

		self.target_temp1 = gui.Label(' Target temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'red', 'left' : '3%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
		self.target_temp1_val = gui.TextInput(style = {'width' : '8%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '16%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '0%', 'z-index' : '1'})
		self.target_temp1_val.set_text('250 \u2103')

		self.current_temp1 = gui.Label(' Current temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': '#75e7ff', 'left' : '3%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
		self.current_temp1_val = gui.Label('0 \u2103', style = {'width' : '8%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '16%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '0%', 'z-index' :'1'})

		self.kettle1_time_lab = gui.Label(' Pump 1->2 Time (s):', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '3%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '23%', 'text-align':'left', 'padding-left': '0.8%', 'z-index' :'0'})
		self.kettle1_time = gui.TextInput(style = {'width' : '5%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '19%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '23%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})
		self.kettle1_time.set_text("0")
		self.kettle1_time.set_on_change_listener(self.on_kettle1_area_change)

		self.kettle1_but = gui.Button(' GO', style = {'width' : '3%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'black', 'left' : '21%', 'background-color': "green", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '23%', 'text-align':'left', 'padding-left': '0.3%', 'z-index' :'2'})
		self.kettle1_but.set_on_click_listener(self.kettle1_go)

		self.kettle2_time_lab = gui.Label(' Pump 2->2 Time (s):', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '27%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '0.8%', 'z-index' :'0'})
		self.kettle2_time = gui.TextInput(style = {'width' : '5%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '43%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})
		self.kettle2_time.set_text("0")
		self.kettle2_time.set_on_change_listener(self.on_kettle2_area_change)

		self.kettle2_but = gui.Button(' GO', style = {'width' : '3%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'black', 'left' : '45%', 'background-color': "green", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '0.3%', 'z-index' :'2'})
		self.kettle2_but.set_on_click_listener(self.kettle2_go)

		self.kettle2_time_lab1 = gui.Label(' Pump 2->3 Time (s):', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '27%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '0.8%', 'z-index' :'0'})
		self.kettle2_time1 = gui.TextInput(style = {'width' : '5%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '43%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})
		self.kettle2_time1.set_text("0")
		self.kettle2_time1.set_on_change_listener(self.on_kettle2_area_change1)

		self.kettle2_but1 = gui.Button(' GO', style = {'width' : '3%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'black', 'left' : '45%', 'background-color': "green", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '0.3%', 'z-index' :'2'})
		self.kettle2_but1.set_on_click_listener(self.kettle2_go1)

		self.target_temp2 = gui.Label(' Target temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'red', 'left' : '51%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
		self.target_temp2_val = gui.TextInput(style = {'width' : '8%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '64%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '0%', 'z-index' : '1'})
		self.target_temp2_val.set_text('100 \u2103')

		self.current_temp2 = gui.Label(' Current temp:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': '#75e7ff', 'left' : '51%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
		self.current_temp2_val = gui.Label('0 \u2103', style = {'width' : '8%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '64%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '16%', 'text-align':'left', 'padding-left': '0%', 'z-index' :'1'})


		self.kettle3_time_lab = gui.Label(' Pump 3->4 Time (s):', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '51%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '23%', 'text-align':'left', 'padding-left': '0.8%', 'z-index' :'0'})
		self.kettle3_time = gui.TextInput(style = {'width' : '5%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '67%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '23%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})
		self.kettle3_time.set_text("0")
		self.kettle3_time.set_on_change_listener(self.on_kettle3_area_change)

		self.kettle3_but = gui.Button(' GO', style = {'width' : '3%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'black', 'left' : '69%', 'background-color': "green", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '23%', 'text-align':'left', 'padding-left': '0.3%', 'z-index' :'2'})
		self.kettle3_but.set_on_click_listener(self.kettle3_go)

		self.current_task = gui.Label(' Current Task:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '9%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
		self.current_task_val = gui.Label('Pending', style = {'width' : '20%', 'height' : '14%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '13%', 'text-align':'left', 'padding-left': '0.8%', 'z-index' :'1'})


		self.target_time = gui.Label(' Target time:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '32%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})
		self.target_time_val = gui.TextInput(style = {'width' : '8%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '86%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '32%', 'text-align':'left', 'padding-left': '0%', 'z-index' : '1'})


		self.current_time = gui.Label(' Time left:', style = {'width' : '20%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '30%', 'text-align':'left', 'padding-left': '.8%', 'z-index' : '0'})

		self.current_time_val = gui.Label('00:00:00', style = {'width' : '8%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '86%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.5vw', 'top' : '30%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})

		self.btUploadFile = gui.FileUploader('./',  style = {'width':'25%', 'color' :'white', 'background-color' :'black', 'white' : '2.5vw',  'height':'3.0%', 'left': '70%', 'margin':'auto', 'top': '92%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
		self.btUploadFile.set_on_success_listener(self.fileupload_on_success)
		self.btUploadFile.set_on_failed_listener(self.fileupload_on_failed)

		self.close = gui.Button('Reset',  style = {'width':'8%', 'color' :'black', 'background-color' :'red', 'font-size' : '2.5vw',  'height':'8.0%', 'left': '83%', 'margin':'auto', 'top': '87%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
		self.close.set_on_click_listener(self.on_button_pressed)

		delta_time = self.get_time()

		self.relay_lab = gui.Label(' Relay #', style = {'width' : '6%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.3vw', 'top' : '38%', 'text-align':'left', 'padding-left': '0.5%', 'z-index' :'0'})
		self.relay_txt = gui.TextInput(style = {'width' : '2.5%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '80.5%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.3vw', 'top' : '38%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})
		self.relay_txt.set_text("0")
		self.relay_txt.set_on_change_listener(self.on_relay_area_change)

		self.relay_t_lab = gui.Label('Time (s)', style = {'width' : '6%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '83%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.3vw', 'top' : '38%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'0'})
		self.relay_t = gui.TextInput(style = {'width' : '3%', 'height' : '3.9%', 'padding-top' : '.8%', 'color': 'grey', 'left' : '89%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.3vw', 'top' : '38%', 'text-align':'left', 'padding-left': '0.0%', 'z-index' :'1'})
		self.relay_t.set_text("0")
		self.relay_t.set_on_change_listener(self.on_relay_time_area_change)
		

		self.relay_but = gui.Button(' GO', style = {'width' : '3%', 'height' : '5%', 'padding-top' : '.8%', 'color': 'black', 'left' : '93%', 'background-color': "green", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.3vw', 'top' : '38%', 'text-align':'left', 'padding-left': '0.3%', 'z-index' :'1'})
		self.relay_but.set_on_click_listener(self.relay_go)

		self.continue_o = gui.Button('CONTINUE',  style = {'width':'20%', 'color' :'black', 'background-color' :'green', 'font-size' : '2.2vw',  'height':'4.0%', 'left': '75.5%', 'margin':'auto', 'top': '23.5%', 'display' : 'block', 'position' :'absolute', 'z-index' : '2'})
		self.continue_o.set_on_click_listener(self.on_continue_pressed)

		self.pause_off = gui.Button('Pause',  style = {'width':'8%', 'color' :'black', 'background-color' :'green', 'font-size' : '2.2vw',  'height':'4.0%', 'left': '75%', 'margin':'auto', 'top': '87%', 'display' : 'block', 'position' :'absolute', 'z-index' : '1'})
		self.pause_off.set_on_click_listener(self.on_unpause_pressed)

		self.check = gui.CheckBoxLabel('Board 2', False, style = {'width' : '6%', 'height' : '4%', 'padding-top' : '.8%', 'color': 'white', 'left' : '75%', 'background-color': "black", 'line-height' :'100%', 'position' : 'absolute', 'font-weight':'bold', 'font-size' : '1.3vw', 'top' : '44%', 'text-align':'left', 'padding-left': '0.5%', 'z-index' :'0'})
		#self.check = gui.CheckBoxLabel('Board 2', False, style = {'width' : '6%', 'height' : '4%', 'left' : '78%',  'position' : 'absolute', 'top' : '38%', 'z-index' : '2'})
		self.check.set_on_change_listener(self.on_check_change)

		self.counter.set_text('Running Time: ' + str(int(delta_time/3600)).zfill(2)+":"+ str(int(delta_time/60)%60).zfill(2)+":"+str(delta_time%60).zfill(2))
		verticalContainer.append(self.check)
		verticalContainer.append(self.relay_txt)
		verticalContainer.append(self.relay_lab)
		verticalContainer.append(self.relay_t_lab)
		verticalContainer.append(self.relay_t)
		verticalContainer.append(self.relay_but)
		verticalContainer.append(self.kettle1_time)
		verticalContainer.append(self.kettle1_time_lab)
		verticalContainer.append(self.kettle1_but)
		verticalContainer.append(self.kettle2_time)
		verticalContainer.append(self.kettle2_time_lab)
		verticalContainer.append(self.kettle2_but)
		verticalContainer.append(self.kettle2_time1)
		verticalContainer.append(self.kettle2_time_lab1)
		verticalContainer.append(self.kettle2_but1)
		verticalContainer.append(self.kettle3_time)
		verticalContainer.append(self.kettle3_time_lab)
		verticalContainer.append(self.kettle3_but)
		verticalContainer.append(self.continue_o)
		#verticalContainer.append(self.pause_off)
		verticalContainer.append(self.btUploadFile)
		verticalContainer.append(self.target_temp1)
		verticalContainer.append(self.current_temp1)
		verticalContainer.append(self.target_temp1_val)
		verticalContainer.append(self.current_temp1_val)
		#verticalContainer.append(self.target_time)
		#verticalContainer.append(self.target_time_val)
		verticalContainer.append(self.current_time)
		verticalContainer.append(self.current_time_val)
		verticalContainer.append(self.target_temp2)
		verticalContainer.append(self.current_temp2)
		verticalContainer.append(self.target_temp2_val)
		verticalContainer.append(self.current_temp2_val)
		verticalContainer.append(self.current_task)
		verticalContainer.append(self.current_task_val)
		verticalContainer.append(self.fire_img)
		verticalContainer.append(self.fire_img1)
		verticalContainer.append(self.kettle_img)
		verticalContainer.append(self.kettle_img2)
		verticalContainer.append(self.kettle_img3)
		verticalContainer.append(self.kettle_img4)
		verticalContainer.append(self.water_pump1)
		verticalContainer.append(self.water_pump2)
		verticalContainer.append(self.water_pump3)
		verticalContainer.append(self.water_pump4)
		verticalContainer.append(self.pipe)
		verticalContainer.append(self.pipe_right)
		verticalContainer.append(self.heat_exchanger)
		verticalContainer.append(self.faucet)
		verticalContainer.append(self.counter)
		verticalContainer.append(self.cup)
		verticalContainer.append(self.sign)
		#verticalContainer.append(self.close)

		# kick of regular display of counter
		self.run_brewery()

		# returning the root widget
		return verticalContainer

	def open_input_dialog(self):
		self.inputDialog = gui.InputDialog('Confirmation', 'Continue to Next Step?', width=500, height=160)
		self.inputDialog.set_on_confirm_value_listener(self.on_input_dialog_confirm)
		# here is returned the Input Dialog widget, and it will be shown
		self.inputDialog.show(self)

	def on_input_dialog_confirm(self, widget, value):
		print("Starting Step")

	def on_check_change(self, widget, newValue):
			self.check_on = newValue
			print(self.check_on)


	def fileupload_on_success(self, widget, filename):
		global instructions, fileupload, step
		fileupload = False
		try:
			print(str(filename))
			instructions = pd.read_excel(str(filename))
			step = 0
			print(instructions)
			fileupload=True
		except:
			print("not proper filetype")
	#               self.lbl.set_text('File upload success: ' + filename)

	def fileupload_on_failed(self, widget, filename):
	#               self.lbl.set_text('File upload failed: ' + filename)
		fileupload = False
		print("File upload failed")

	def on_kettle1_area_change(self, widget, newValue):
		self.kettle1_time = newValue

	def kettle1_go(self, _):
		self.turn_on_pump1()
		self.wait(int(self.kettle1_time))
		self.turn_off_pump1()

	def on_kettle2_area_change(self, widget, newValue):
		self.kettle2_time = newValue

	def kettle2_go(self, _):
		self.turn_on_pump2_path1()
		self.wait(int(self.kettle2_time))
		self.turn_off_pump2()

	def on_kettle2_area_change1(self, widget, newValue):
		self.kettle2_time1 = newValue

	def kettle2_go1(self, _):
		self.turn_on_pump2_path2()
		self.wait(int(self.kettle2_time1))
		self.turn_off_pump2()

	def on_kettle3_area_change(self, widget, newValue):
		self.kettle3_time = newValue

	def kettle3_go(self, _):
		self.turn_on_pump3()
		self.wait(int(self.kettle3_time))
		self.turn_off_pump3()

	def on_relay_area_change(self, widget, newValue):
		self.relay_num = newValue
		print(self.relay_num)

	def on_relay_time_area_change(self, widget, newValue):
		self.relay_time = newValue
		print(self.relay_time)

	def relay_go(self, _):
		if self.check_on == "true":
			try:
				v.write([0x00,0xff, int(self.relay_num,16)])
				self.wait(int(self.relay_time))
				v.write([0x00,0xfd,int(self.relay_num,16)])
			except:
				print("Step Failed")
		else: 
			try:
				h.write([0x00,0xff, int(self.relay_num,16)])
				self.wait(int(self.relay_time))
				h.write([0x00,0xfd,int(self.relay_num,16)])
			except:
				print("Step Failed")

	def get_time(self):
		global start_time_second
		global start_time_minute
		global start_time_hour
		global total_start_time

		current_time = datetime.now()
		current_time_second = current_time.second
		current_time_minute = current_time.minute
		current_time_hour = current_time.hour
		total_current_time = current_time.second + 60*current_time.minute + 3600*current_time.hour

		if (total_current_time < total_start_time):
			total_current_time += 12*3600

		delta_time = total_current_time - total_start_time

		return delta_time

	def on_continue_pressed(self, _):
		global continue_on
		continue_on = True
		print(continue_on)


	def on_unpause_pressed(self, _):
		global pause
		pause = False

	def on_button_pressed(self, _):
		print("3\n3\n3\n\n3\n3\n3\n")
		global delta_pump_time
		global first_loop


		global start_time
		global start_time_second
		global start_time_minute
		global start_time_hour
		global total_start_time
		
		global step
		global target_temp1
		global target_temp2

		step = 0

		target_temp1 = -999
		target_temp2 = -999
		start_time = datetime.now()
		start_time_second = start_time.second
		start_time_minute = start_time.minute
		start_time_hour = start_time.hour
		total_start_time = start_time_second + 60*start_time_minute+3600*start_time_hour
		delta_time = self.get_time()
		self.counter.set_text('Running Time: ' + str(int(delta_time/3600)).zfill(2)+":"+ str(int(delta_time/60)%60).zfill(2)+":"+str(delta_time%60).zfill(2))


		first_loop = True

		self.current_time_val.set_text('00:00:00')
		self.target_temp1_val.set_text('250 \u2103')
		self.target_temp2_val.set_text('100 \u2103')
		h.write([0x00,0xfc])
		self.fire_img.set_image('res/blank.png')
		self.kettle_img.set_image('res/kettle.png')
		self.kettle_img2.set_image('res/second_kettle.png')
		self.kettle_img3.set_image('res/monk-brewing-beer.png')
		self.kettle_img4.set_image('res/beer_barrel.png')
		self.fire_img1.set_image('res/blank.png')
		self.water_pump1.set_image('res/pump_static.png')
		self.water_pump2.set_image('res/pump_static.png')
		self.water_pump3.set_image('res/pipes.gif')
		self.water_pump4.set_image('res/pipes.gif')
		self.heat_exchanger.set_image('res/heat_exchanger.png')
		self.faucet.set_image('res/blank.png')
		self.cup.set_image('res/blank.png')
		self.sign.set_image('res/sign2.png')
		self.pipe.set_image('res/pipe-only1.png')
		self.pipe_right.set_image('res/pipes-right-only-static.png')
		self.turn_off_pump1()
		self.turn_off_pump2_path1()
		self.turn_off_pump3_path2()
		self.turn_off_pump3()
		self.turn_off_faucet()
		self.run_brewery()


	def maintain_temp(self):
		global heater1, heater2
		global target_temp1, target_temp2
		print(target_temp1)
		data.readline()
		current_temp1 = 0
		current_temp2 = 0
		try:
			data.write(struct.pack('>B',10))
			current_temp1 = float((data.readline()).decode('UTF-8')[-8:-1])
			current_temp2 = float((data.readline()).decode('UTF-8')[-8:-1])
			print(current_temp1)
			self.current_temp1_val.set_text(str(current_temp1)+"\u2103")
			self.current_temp2_val.set_text(str(current_temp2)+"\u2103")
		except:
			print("Error Reading Temp")
		if current_temp1 < target_temp1 and heater1 == False:
			heater1 = True
			self.fire_img.set_image('res/fire.png')
			try:
				# turn heater 1 on
				print("Turning on heater 1")
				h.write([0x00,0xff,0x06])
			except IOError as ex:
				print(ex)
				print("You probably don't have the hard coded device. Update the hid.device line")
				print("in this script with one from the enumeration list output above and try again.")
		if current_temp1 >= target_temp1 and heater1 == True:
			heater1 = False
			self.fire_img.set_image('res/blank.png')
			try:
				# turn heater 1 on
				print("Turning off heater 1")
				h.write([0x00,0xfd,0x06])
			except IOError as ex:
				print(ex)
				print("You probably don't have the hard coded device. Update the hid.device line")
				print("in this script with one from the enumeration list output above and try again.")


		if current_temp2 < (target_temp2-.4) and heater2 == False:
			self.fire_img1.set_image('res/fire.png')
			try:
				# turn heater 2 on
				print("Turning on heater 2")
				h.write([0x00,0xff,0x05])
			except IOError as ex:
				print(ex)
				print("You probably don't have the hard coded device. Update the hid.device line")
				print("in this script with one from the enumeration list output above and try again.")
			heater2 = True
		if current_temp2 >= target_temp2 and heater2 == True:
			self.fire_img1.set_image('res/blank.png')
			try:
				# turn heater 2 off
				print("Turning off heater 2")
				h.write([0x00,0xfd,0x05])
			except IOError as ex:
				print(ex)
				print("You probably don't have the hard coded device. Update the hid.device line")
				print("in this script with one from the enumeration list output above and try again.")
			heater2 = False



	def set_temp1(self):
		global target_temp1, heater1
		current_temp1 = 0
		current_temp2 = 0
		self.fire_img.set_image('res/fire.png')
		try:
			# turn heater 1 on
			print("Turning on heater 1")
			h.write([0x00,0xff,0x06])
			heater1 = True
		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")
		
		if current_temp1 >= target_temp1:
			try:
				# turn heater 1 off
				print("Turning off heater 1")
				h.write([0x00,0xfd,0x06])
				heater1 = True
			except IOError as ex:
				print(ex)
				print("You probably don't have the hard coded device. Update the hid.device line")
				print("in this script with one from the enumeration list output above and try again.")
			

		while current_temp1 < target_temp1:
			try:
				data.write(struct.pack('>B',10))
				current_temp1 = float((data.readline()).decode('UTF-8')[-8:-1])
				current_temp2 = float((data.readline()).decode('UTF-8')[-8:-1])
				#print(current_temp1, current_temp2)
				self.current_temp1_val.set_text(str(current_temp1)+"\u2103")
				self.current_temp2_val.set_text(str(current_temp2)+"\u2103")
			except:
				print("Error Reading Temp")
			sleep(1)

		return target_temp1


	def set_temp2(self):
		global target_temp2, heater2
		current_temp1 = 0
		current_temp2 = 0
		data.readline()
		self.fire_img1.set_image('res/fire.png')
		try:
			# turn heater 2 on
			print("Turning on heater 2")
			h.write([0x00,0xff,0x05])
			heater2 = True
		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")
	
		if current_temp2 >= target_temp2:
			try:
				# turn heater 2 off
				print("Turning off heater 2")
				h.write([0x00,0xfd,0x05])
				heater1 = True
			except IOError as ex:
				print(ex)
				print("You probably don't have the hard coded device. Update the hid.device line")
				print("in this script with one from the enumeration list output above and try again.")

		while current_temp2 < target_temp2:
			try:
				data.write(struct.pack('>B',10))
				current_temp1 = float((data.readline()).decode('UTF-8')[-8:-1])+10
				current_temp2 = float((data.readline()).decode('UTF-8')[-8:-1])
#				#data.readline()
				self.current_temp1_val.set_text(str(current_temp1)+"\u2103")
				self.current_temp2_val.set_text(str(current_temp2)+"\u2103")
			except:
				print("Error Reading Temp")
			sleep(1)

		return target_temp2

	def turn_on_pump1(self):
		try:
			#turn pump 1 on
			print("Turning on pump 1")
			h.write([0x00,0xff,0x02])
			self.water_pump1.set_image('res/Wassermotor-mit_Pfeilen_w_trans4.png.gif')
			self.pipe_right.set_image('res/pipes-right-only.gif')

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")

	def turn_off_pump1(self):
		try:
			#turn pump 1 off
			print("Turning off pump 1")
			h.write([0x00,0xfd,0x02])
			self.pipe_right.set_image('res/pipes-right-only-static.png')
			self.water_pump1.set_image('res/pump_static.png')

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")

	def turn_on_pump2_path1(self):
		try:
			print("Turning on pump 2, path 1")
			h.write([0x00,0xff,0x03])
			sleep(10)
			h.write([0x00,0xfd,0x03])
			h.write([0x00,0xff,0x08])
			self.water_pump2.set_image('res/Wassermotor-mit_Pfeilen_w_trans4.png.gif')
			self.water_pump3.set_image('res/pipes-left.gif')

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")

	def turn_off_pump2(self):
		try:
			print("Turning off pump 2")
			h.write([0x00,0xfd,0x08])
			self.water_pump2.set_image('res/pump_static.png')
			self.water_pump3.set_image('res/pipes.gif')
			self.water_pump4.set_image('res/pipes.gif')

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")

	def turn_on_pump2_path2(self):
		try:
			#turn pump 1 on
			print("Turning on pump 2, path 2")
			h.write([0x00,0xff,0x04])
			sleep(10)
			h.write([0x00,0xfd,0x04])
			h.write([0x00,0xff,0x08])
			self.water_pump2.set_image('res/Wassermotor-mit_Pfeilen_w_trans4.png.gif')
			self.water_pump4.set_image('res/pipes-right.gif')

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")


	def turn_on_pump3(self):
		try:
			print("Turning on pump 3")
			v.write([0x00,0xff,0x08])

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")

	def turn_off_pump3(self):
		try:
			print("Turning off pump 3")
			v.write([0x00,0xfd,0x08])

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")

	def turn_on_faucet(self):
		try:
			#turn pump 3 on
			print("Turning on faucet")
			h.write([0x00,0xff,0x07])
			self.pipe.set_image('res/pipe-only1.gif')

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")


	def turn_off_faucet(self):
		try:
			#turn pump 3 on
			print("Turning off faucet")
			h.write([0x00,0xfd,0x07])
			self.pipe.set_image('res/pipe-only1.png')

		except IOError as ex:
			print(ex)
			print("You probably don't have the hard coded device. Update the hid.device line")
			print("in this script with one from the enumeration list output above and try again.")

	def turn_cup(self):
		data.write(struct.pack('>B',170))
		self.cup.set_image('res/cup.gif')
		sleep(5)
		self.cup.set_image('res/blank.png')
		data.write(struct.pack('>B',10))

	def wait(self,target_time):
		global first_loop
		global target_temp1
		global target_temp2
		if first_loop == True:
			start_time = self.get_time()
			delta_time = self.get_time()-start_time
			first_loop == False
		while (delta_time < target_time):
			delta_time = self.get_time()-start_time
			self.maintain_temp()
			if (target_time-delta_time) < 0:
				self.current_time_val.set_text('00:00:00')
			else:
				self.current_time_val.set_text(str(int((target_time-delta_time)/3600)).zfill(2)+":"+ str(int((target_time-delta_time)/60)%60).zfill(2)+":"+str((target_time-delta_time)%60).zfill(2))
			running_time = self.get_time()
			self.counter.set_text('Running Time: ' + str(int(running_time/3600)).zfill(2)+":"+ str(int(running_time/60)%60).zfill(2)+":"+str(running_time%60).zfill(2))
			print(target_time)
			print(delta_time)
			sleep(1)

	def run_brewery(self):
		print("Running Brewery")
		global target_temp1, target_temp2, instructions, step, start_time, total_start_time, fileupload, pause, heater2, continue_on
		if(fileupload == True and continue_on == True):
			try:
				print("STEP")
				print(step)
				DESCRIPTOR = instructions['DESCRIPTOR'][step]
				ID = int(instructions['ID'][step])
				ARG = instructions['ARGUMENT'][step]
				print(ID, DESCRIPTOR, ARG)
				self.current_task_val.set_text(str(DESCRIPTOR))
				delta_time = self.get_time()
				self.counter.set_text('Running Time: ' + str(int(delta_time/3600)).zfill(2)+":"+ str(int(delta_time/60)%60).zfill(2)+":"+str(delta_time%60).zfill(2)) 
				print(step)
				if ID == 0:
					self.wait(int(ARG))
					self.target_time_val.set_text(str(int(ARG/3600)).zfill(2)+":"+ str(int(ARG/60)%60).zfill(2)+":"+str(ARG%60).zfill(2))
				if ID == 1:
					self.turn_on_pump1()
				if ID == 2:
					self.turn_off_pump1()
				if ID == 3:
					self.turn_on_pump2_path1()
				if ID == 4:
					self.turn_off_pump2()
				if ID == 5:
					self.turn_on_pump2_path2()
				if ID == 6:
					self.turn_on_pump3()
				if ID == 7:
					self.turn_off_pump3()
				if ID == 9:
					target_temp1 = float(ARG)
					self.target_temp1_val.set_text(str(target_temp1))
					self.set_temp1()
				if ID == 10:
					target_temp2 = float(ARG)
					self.target_temp2_val.set_text(str(target_temp2))
					self.set_temp2()
				if ID == 11:
					self.turn_cup()
				if ID == 12:
					self.turn_on_faucet()
				if ID == 13:
					self.turn_off_faucet()
				if ID == 14:
					target_temp1 = float(ARG)
					self.target_temp1_val.set_text(str(target_temp1))
					heater2 = False
				if ID == 15:
					target_temp2 = float(ARG)
					self.target_temp2_val.set_text(str(target_temp2))
					heater2 = False
				self.maintain_temp()
				if step < len(instructions['ID']):
					step+=1
					if ID == 16:
						continue_on = False
				if step == len(instructions['ID']):
					self.current_task_val.set_text("DONE!\nHOPE YOU ENJOY THE BEER!")
			except:
				print("Step failed")
				if step < len(instructions['ID']):
					step+=1
					continue_on = False
					print(continue_on)
				if step == len(instructions['ID']):
					self.current_task_val.set_text("DONE!\nHOPE YOU ENJOY THE BEER!")
		Timer(1, self.run_brewery).start()

if __name__ == "__main__":
        '''
        global start_time = 0
        global start_time_second = 0
        global start_time_minute = 0
        global start_time_hour = 0
        global total_start_time = 0
        '''
        start_time = datetime.now()
        start_time_second = start_time.second
        start_time_minute = start_time.minute
        start_time_hour = start_time.hour
        total_start_time = start_time_second + 60*start_time_minute+3600*start_time_hour

        print("Opening the device")
	        
        '''v = hid.device()
        v.open_path(b'IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/XHC1@14/XHC1@14000000/HS02@14200000/USB2.0 Hub@14200000/AppleUSB20Hub@14200000/AppleUSB20HubPort@14210000/USBRelay8@14210000/IOUSBHostInterface@0/IOUSBHostHIDDevice@14210000,0')

        h = hid.device()
        h.open_path(b'IOService:/AppleACPIPlatformExpert/PCI0@0/AppleACPIPCI/XHC1@14/XHC1@14000000/HS01@14100000/USBRelay8@14100000/IOUSBHostInterface@0/IOUSBHostHIDDevice@14100000,0')	
	
	#h.open_path(hid.enumerate(5824,1503)[0]['path'])
        #h.open(5824, 1503) # trezor vendorid/productid
        print("Manufacturer: %s" % h.get_manufacturer_string())
        print("Product: %s" % h.get_product_string())
        print("Serial No: %s" % h.get_serial_number_string())

        # enable non-blocking mode
        v.set_nonblocking(1)
        h.set_nonblocking(1)

        h.write([0x00,0xfc])
        v.write([0x00,0xfc])'''
#       filename = input("Enter a filename: ")
        instructions = '' 
        print("Done opening device")
        #start(Brewery, debug=False, address='127.0.0.1', port = 5000, start_browser=True)
        start(Brewery, debug=False, address='172.20.15.255', port = 5000, start_browser=True)
        #start(Brewery, debug=True, address='192.168.1.146', port = 5000, start_browser=True)

      #  h.write([0x00,0xfc])
      #  v.write([0x00,0xfc])
        print("Closing the device")
      #  h.close()
      #  v.close()
        ser.close()


