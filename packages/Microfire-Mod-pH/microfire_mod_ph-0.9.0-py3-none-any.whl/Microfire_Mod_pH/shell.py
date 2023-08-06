#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
if int(str(range(3))[-2]) == 2:
  sys.stderr.write("You need python 3.0 or later to run this script\n")
  exit(1)

import cmd, inspect, math, sys
import Microfire_Mod_pH
ph = Microfire_Mod_pH.i2c()

fw_compatible = 1
hw_compatible = 2

class Mod_pH_Shell(cmd.Cmd):
    intro="Type `help` for a list of commands\n`enter` repeats the last command"
    prompt = '> '

    def do_config(self, a):
        """prints out all the configuration data\nparameters: none"""
        print("Mod-pH Config: ", end='')
        if ph.connected():
            print_green('connected')
            ph.getDeviceInfo()
            if (ph.fwVersion != fw_compatible) or (ph.hwVersion != hw_compatible):
                print_red("*This version of shell was designed for a different hardware revision or firmware version*")

            print("Calibration:")
            print(" low reference / read: ", end='')
            if math.isnan(ph.calibrationLowReference):
                print("-", end='')
            else:
                print("{:.2f}".format(ph.calibrationLowReference), end='')
            print(" / ", end='')
            if math.isnan(ph.calibrationLowReading):
                print("-")
            else:
                print("{:.2f}".format(ph.calibrationLowReading))

            print(" middle reference / read: ", end='')
            if math.isnan(ph.calibrationMidReference):
                print("-", end='')
            else:
                print("{:.2f}".format(ph.calibrationMidReference), end='')
            print(" / ", end='')
            if math.isnan(ph.calibrationMidReading):
                print("-")
            else:
                print("{:.2f}".format(ph.calibrationMidReading)) 

            print(" high reference / read: ", end='')
            if math.isnan(ph.calibrationHighReference):
                print("-", end='')
            else:
                print("{:.2f}".format(ph.calibrationHighReference), end='')
            print(" / ", end='')
            if math.isnan(ph.calibrationHighReading):
                print("-")
            else:
                print("{:.2f}".format(ph.calibrationHighReading)) 

            print(" single point: ", end='')
            if math.isnan(ph.calibrationSingleOffset):
                print("-")
            else:
                print("{:.2f}".format(ph.calibrationSingleOffset))

            print(" calibration temperature: ", end='')
            if math.isnan(ph.calibrationTemperature):
                print("-")
            else:
                print("{:.2f}".format(ph.calibrationTemperature)) 

            print("hardware:firmware version: ", end='')
            print(ph.hwVersion, end='')
            print(":", end='')
            print(ph.fwVersion)
        else:
             print_red('**disconnected**')


    def do_reset(self, a):
        """reset all saved values\nparameters: none"""
        ph.reset()
        self.do_config(self)

    def do_ph(self, line):
        """starts a pH measurement\nparameters: tempC[25.0]"""
        data = [s for s in line.split()]
        if len(data) >= 1:
            tempC = float(data[0]) 
        else:
            tempC = 25.0

        ph.measurepH(tempC)

        print("{:.2f}".format(ph.pH), end='')
        print(" pH @ " + str("{:.2f}".format(tempC)) + "°C")

        if ph.status:
            print_red(ph.status_string[ph.status])

    def do_single(self, line):
        """Single point calibration\nparameters: solution_pH, tempC[25.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0

        ph.calibrateSingle(float(data[0]), tempC, True)
        if ph.status:
            print_red(ph.status_string[ph.status])

        self.do_config(self)

    def do_low(self, line):
        """Low point calibration\nparameters: solution_pH, tempC[25.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0

        ph.calibrateLow(float(data[0]), tempC, True)
        if ph.status:
            print_red(ph.status_string[ph.status])
        
        self.do_config(self)

    def do_mid(self, line):
        """Mid point calibration\nparameters: solution_pH, tempC[25.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0

        ph.calibrateMid(float(data[0]), tempC, True)
        if ph.status:
            print_red(ph.status_string[ph.status])
        
        self.do_config(self)

    def do_high(self, line):
        """High point calibration\nparameters: solution_pH, tempC[25.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0

        ph.calibrateHigh(float(data[0]), tempC, True)
        if ph.status:
            print_red(ph.status_string[ph.status])
        
        self.do_config(self)

    def do_i2c(self, line):
        """changes the I2C address"""
        i2c_address = int(line, 16)

        if ((i2c_address <= 0x07) or (i2c_address > 0x7f)):
            print("Error: I2C address not in valid range")
        else:
            ph.setI2CAddress(i2c_address);

    def do_exit(self, s):
        """Exits\nparameters: none"""
        return True

def print_red(txt): print("\033[91m {}\033[00m" .format(txt)) 
def print_green(txt): print("\033[92m {}\033[00m" .format(txt)) 

ph.begin()
Mod_pH_Shell().cmdloop()