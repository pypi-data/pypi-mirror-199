#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
if int(str(range(3))[-2]) == 2:
  sys.stderr.write("You need python 3.0 or later to run this script\n")
  exit(1)

import cmd, inspect, math, sys
import Microfire_Mod_EC

ec = Microfire_Mod_EC.i2c()
fw_compatible = 1
hw_compatible = 1

class Mod_EC_Shell(cmd.Cmd):
    intro="Type `help` for a list of commands\n`enter` repeats the last command"
    prompt = '> '

    def do_config(self, a):
        """prints out all the configuration data\nparameters: none"""
        print("Mod-EC Config: ", end='')
        if ec.connected():
            print_green('connected')
            ec.getDeviceInfo()
            if (ec.fwVersion != fw_compatible) or (ec.hwVersion != hw_compatible):
                print_red("*This version of shell was designed for a different hardware revision or firmware version*")

            print("Calibration:")
            print(" low reference / read: ", end='')
            if math.isnan(ec.calibrationLowReference):
                print("-", end='')
            else:
                print("{:.2f}".format(ec.calibrationLowReference), end='')
            print(" / ", end='')
            if math.isnan(ec.calibrationLowReading):
                print("-")
            else:
                print("{:.2f}".format(ec.calibrationLowReading))

            print(" middle reference / read: ", end='')
            if math.isnan(ec.calibrationMidReference):
                print("-", end='')
            else:
                print("{:.2f}".format(ec.calibrationMidReference), end='')
            print(" / ", end='')
            if math.isnan(ec.calibrationMidReading):
                print("-")
            else:
                print("{:.2f}".format(ec.calibrationMidReading)) 

            print(" high reference / read: ", end='')
            if math.isnan(ec.calibrationHighReference):
                print("-", end='')
            else:
                print("{:.2f}".format(ec.calibrationHighReference), end='')
            print(" / ", end='')
            if math.isnan(ec.calibrationHighReading):
                print("-")
            else:
                print("{:.2f}".format(ec.calibrationHighReading)) 

            print(" single point: ", end='')
            if math.isnan(ec.calibrationSingleOffset):
                print("-")
            else:
                print("{:.2f}".format(ec.calibrationSingleOffset)) 

            print("hardware:firmware version: ", end='')
            print(ec.hwVersion, end='')
            print(":", end='')
            print(ec.fwVersion)
        else:
             print_red('**disconnected**')


    def do_reset(self, a):
        """reset all saved values\nparameters: none"""
        ec.reset()
        self.do_config(self)

    def do_ec(self, line):
        """starts an EC measurement\nparameters: tempC[25.0], tempCoef[0.019], tempConst[25.0], K[1.0]"""
        data = [s for s in line.split()]
        if len(data) >= 1:
            tempC = float(data[0]) 
        else:
            tempC = 25.0
        tempCoef = float(data[1]) if len(data) >= 2 else 0.019
        tempConst = float(data[2]) if len(data) >= 3 else 25.0
        k = float(data[3]) if len(data) >= 4 else 1.0

        ec.measureEC(tempC, tempCoef, tempConst, k, 0, True)
        if ec.mS <= 1.0:
            print("{:.2f}".format(ec.uS), end='')
            print(" µS/cm @ " + str("{:.2f}".format(tempC)) + "°C")
        else:
            print("{:.2f}".format(ec.mS), end='')
            print(" mS/cm @ " + str("{:.2f}".format(tempC)) + "°C")

        if ec.status:
            print_red(ec.status_string[ec.status])

    def do_single(self, line):
        """Single point calibration\nparameters: solution_mS, tempC[25.0], tempCoef[0.019], tempConst[25.0], K[1.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0
        tempCoef = float(data[2]) if len(data) >= 3 else 0.019
        tempConst = float(data[3]) if len(data) >= 4 else 25.0
        k = float(data[4]) if len(data) >= 5 else 1.0

        ec.calibrateSingle(float(data[0]), tempC, tempCoef, tempConst, k, True)
        if ec.status:
            print_red(ec.status_string[ec.status])

        self.do_config(self)

    def do_low(self, line):
        """Low point calibration\nparameters: solution_mS, tempC[25.0], tempCoef[0.019], tempConst[25.0], K[1.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0
        tempCoef = float(data[2]) if len(data) >= 3 else 0.019
        tempConst = float(data[3]) if len(data) >= 4 else 25.0
        k = float(data[4]) if len(data) >= 5 else 1.0

        ec.calibrateLow(float(data[0]), tempC, tempCoef, tempConst, k, True)
        if ec.status:
            print_red(ec.status_string[ec.status])
        
        self.do_config(self)

    def do_mid(self, line):
        """Mid point calibration\nparameters: solution_mS, tempC[25.0], tempCoef[0.019], tempConst[25.0], K[1.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0
        tempCoef = float(data[2]) if len(data) >= 3 else 0.019
        tempConst = float(data[3]) if len(data) >= 4 else 25.0
        k = float(data[4]) if len(data) >= 5 else 1.0

        ec.calibrateMid(float(data[0]), tempC, tempCoef, tempConst, k, True)
        if ec.status:
            print_red(ec.status_string[ec.status])
        
        self.do_config(self)

    def do_high(self, line):
        """High point calibration\nparameters: solution_mS, tempC[25.0], tempCoef[0.019], tempConst[25.0], K[1.0]"""
        data = [s for s in line.split()]
        if len(data) >= 2:
            tempC = float(data[1]) 
        else:
            tempC = 25.0
        tempCoef = float(data[2]) if len(data) >= 3 else 0.019
        tempConst = float(data[3]) if len(data) >= 4 else 25.0
        k = float(data[4]) if len(data) >= 5 else 1.0

        ec.calibrateHigh(float(data[0]), tempC, tempCoef, tempConst, k, True)
        if ec.status:
            print_red(ec.status_string[ec.status])
        
        self.do_config(self)

    def do_i2c(self, line):
        """changes the I2C address"""
        i2c_address = int(line, 16)

        if ((i2c_address <= 0x07) or (i2c_address > 0x7f)):
            print("Error: I2C address not in valid range")
        else:
            ec.setI2CAddress(i2c_address);

    def do_exit(self, s):
        """Exits\nparameters: none"""
        return True

def print_red(txt): print("\033[91m {}\033[00m" .format(txt)) 
def print_green(txt): print("\033[92m {}\033[00m" .format(txt)) 


ec.begin()
Mod_EC_Shell().cmdloop()