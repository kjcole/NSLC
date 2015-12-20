#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# The includes:
import os
import re
import sys
import stat
import optparse
import subprocess
import signal
import time
import io
import csv
import string
import openpyxl
#
from subprocess import call
#
# Boilerplate imports for Python 2 / Python 3 mutual compatiibility
#
# from __future__ import print_function  # Make print a function
from six.moves  import input           # Use raw_input when I say input
from os.path    import expanduser      # Cross-platform home directory finder
#
# This is completely stolen from Kevin Cole, as he is the master... 
__author__     = "Flint"
__copyright__  = "Copyright 2015, Goddard College (12/09/2015)"
__credits__    = ["Flint"]  # Authors and bug reporters
__license__    = "GPL"
__version__    = "0.01"
__maintainer__ = "Flint"
__email__      = "flint@flint.com"
__status__     = "Prototype"  # "Prototype", "Development" or "Production"
__appname__    = "NSLC file utililty"
#
# Comment lines: Lines beginning with "#" will be stripped of leading
# and trailing spaces (as well as the "#"  and inserted wholesale onto
# a 1250 print "hello world"  # uncomment line 7 to make your life a living hell..character line.
#
# Read a CSV file with many rows, and 110 columns.
#     # Each row represents a student.
#     # Each column represents parameter from the 9-4-14_New_EnrollRept_ProgrammingandTestingGuide.pdf.
#     # http://import opeglobalnpyxlwww.studentclearinghouse.org/colleges/files/EnrollRept_ProgrammingandTestingGuide.pdf#page=15
#         * The constraints of this guideance are included in the class "drl".(detailed record length)
#    www.studentclearinghouse.org/colleges/files/EnrollRept_ProgrammingandTestingGuide.pdf     * The goal is to use this class to operate on the 1250 byte list.
#         * CSV Data from the input is identified and punched into the list at appropriate spacing 
#     # Examples:
#         * >> print drl.RecordType .
#         * >> [2,1,2,"R","AN"] .
#         * >> print drl.StudentSSN .
#         * >> [9,3,11,"R","N"] .
#         * >> print drl.FirstName .
#         * >> [import openpyxl=0,12,31,"R","AN"] .
#
# Set up an object called drl and populate this with spreadsheet data
# this data is a direct copy of the publication data from page 15.
#
# Load landers
# Column for Excel Format Index 
length = 0 
start = 1 
stop = 2
reqd = 3
type = 4
fieldname = 6
count = 7
spreadsheet = "example.xlsx"
#
# Establish global string variable
# global outlist
#
class drl:
	Line = 2	# starting line for data
	def __init__(self):
		self.Column_for_Excel_Format = "Index,Length,Start,Stop,Reqd,Type,Field Name,Count"
        def hi(self):
		fm = " From Object Land..."
		return 'Hello World'+fm
	def Column_for_Excel_Format(self): 
		return munge("Index,Length,Start,Stop,Reqd,Type,Field_Name,Count")
	def Record_Type(self): 
		return munge("2,1,2,R,AN,AN,A,1")
	def Student_SSN(self): 
		return munge("9,3,11,R,N,N,B,2")
	def First_Name(self): 
		return munge("20,12,31,R,AN,AN,C,3")
	def Middle_Initial(self): 
		return munge("1,32,32,O,AN,AN,D,4")
	def Last_Name(self): 
		return munge("20,33,52,R,AN,AN,E,5")
	def Name_Suffix(self): 
		return munge("5,53,57,O,AN,AN,F,6")
	def Previous_SSN(self): 
		return munge("9,58,66,O,N,N,G,7")
	def Previous_Last_Name(self): 
		return munge("20,67,86,O,AN,AN,H,8")
	def Degree_Concentration(self): 
		return munge("9,1,87,87,R,A,I,9")
	def Enrollment_Status(self): 
		return munge("1,87,87,R,A,N,J,10")
	def Status_Start_Date(self): 
		return munge("8,88,95,C,N,AN,K,11")
	def Street_Line_1(self): 
		return munge("30,96,125,R,AN,AN,L,12")
	def Street_Line_2(self): 
		return munge("30,126,155,O,AN,A,M,13")
	def City(self): 
		return munge("20,156,175,R,A,A,N,14")
	def State(self): 
		return munge("2,176,177,R,A,AN,O,15")
	def Zip(self): 
		return munge("9,178,186,C,AN,AN,P,16")
	def Country(self): 
		return munge("15,187,201,C,AN,N,Q,17")
	def Anticipated_Graduation_Date(self): 
		return munge("8,202,209,C,N,N,R,18")
	def Date_of_Birth(self): 
		return munge("8,210,217,R,N,N,S,19")
	def Term_Begin_Date(self): 
		return munge("8,218,225,R,N,N,T,20")
	def Term_End_Date(self): 
		return munge("8,226,233,R,N,AN,U,21")
	def Filler(self): 
		return munge("1,234,234,R,AN,A,V,22")
	def Directory_Block_Indicator(self): 
		return munge("1,235,235,R,A,N,W,23")
	def NCES_CIP_Code_for_Major_1(self): 
		return munge("6,236,241,O,N,N,X,24")
	def NCES_CIP_Code_for_Major_2(self): 
		return munge("6,242,247,O,N,AN,Y,25")
	def Major_Course_of_Study_1(self): 
		return munge("80,248,327,O,AN,AN,Z,26")
	def Major_Course_of_Study_2(self): 
		return munge("80,328,407,O,AN,A,AA,27")
	def Class_Credential(self): 
		return munge("1,408,408,C,A,A,AB,28")
	def First_Time_Full_Time(self): 
		return munge("1,409,409,O,A,A,AC,29")
	def Degree_Seeking(self): 
		return munge("1,410,410,O,A,N,AD,30")
	def High_School_Code(self): 
		return munge("6,411,416,O,N,A,AE,31")
	def Gender(self): 
		return munge("1,417,417,O,A,A,AF,32")
	def Race_Ethnicity(self): 
		return munge("2,418,419,O,A,AN,AG,33")
	def College_Student_ID(self): 
		return munge("20,420,439,O,AN,AN,AH,34")
	def State_Student_ID(self): 
		return munge("30,440,469,O,AN,AN,AI,35")
	def Email(self): 
		return munge("128,470,597,O,AN,A,AJ,36")
	def Good_Student(self): 
		return munge("1,598,598,O,A,AN,AK,37")
	def Middle_Name(self): 
		return munge("35,599,633,O,AN,A,AL,38")
	def Veterans_Status_Indicator_(self): 
		return munge("1,634,634,O,A,AN,AM,39")
	def Reserved_for_CommIT_ID(self): 
		return munge("12,635,646,O,AN,A,AN,40")
	def Pell_Grant_Recipient_Flag(self): 
		return munge("1,647,647,O,A,A,AO,41")
	def Remedial_Flag(self): 
		return munge("1,648,648,O,A,A,AP,42")
	def Citizenship_Flag(self): 
		return munge("1,649,649,O,A,A,AQ,43")
	def Student_Phone_Type(self): 
		return munge("1,650,650,O,A,A,AR,44")
	def Preferred_Phone_Number_Flag(self): 
		return munge("1,651,651,O,A,N,AS,45")
	def Student_Phone_Country_Code(self): 
		return munge("3,652,654,O,N,N,AT,46")
	def Student_Phone_Number(self): 
		return munge("11,655,665,O,N,N,AU,47")
	def Reserved_for_Move_To_OPEID_Future_CH_Functionality(self): 
		return munge("8,666,673,O,N,A,AV,48")
	def Program_Indicator(self): 
		return munge("1,674,674,R,A,N,AW,49")
	def Program_1_CIP_Code(self): 
		return munge("6,675,680,C,N,N,AX,50")
	def CIP_Year(self): 
		return munge("4,681,684,C,N,N,AY,51")
	def Program_1_Credential_Level(self): 
		return munge("2,685,686,C,N,N,AZ,52")
	def Published_Program_1_Length(self): 
		return munge("6,687,692,C,N,A,BA,53")
	def Published_Program_1_Length_Measurement(self): 
		return munge("1,693,693,C,A,N,BB,54")
	def Weeks_Program_1_Title_IV_Academic_Year(self): 
		return munge("6,694,699,C,N,N,BC,55")
	def Program_1_Begin_Date(self): 
		return munge("8,700,707,C,N,A,BD,56")
	def Special_Program_Indicator(self): 
		return munge("1,708,708,C,A,A,BE,57")
	def Program_1_Enrollment_Status(self): 
		return munge("1,709,709,C,A,N,BF,58")
	def Program_1_Enrollment_Status_Effective_Date(self): 
		return munge("8,710,717,C,N,N,BG,59")
	def Program_2_CIP_Code(self): 
		return munge("6,718,723,O,N,N,BH,60")
	def CIP_Year(self): 
		return munge("4,724,727,C,N,N,BI,61")
	def Program_2_Credential_Level(self): 
		return munge("2,728,729,C,N,N,BJ,62")
	def Published_Program_2_Length(self): 
		return munge("6,730,735,C,N,A,BK,63")
	def Published_Program_2_Length_Measurement(self): 
		return munge("1,736,736,C,A,N,BL,64")
	def Weeks_Program_2_Title_IV_Academic_Year(self): 
		return munge("6,737,742,C,N,N,BM,65")
	def Program_2_Begin_Date(self): 
		return munge("8,743,750,C,N,A,BN,66")
	def Special_Program_Indicator(self): 
		return munge("1,751,751,C,A,A,BO,67")
	def Program_2_Enrollment_Status(self): 
		return munge("1,752,752,C,A,N,BP,68")
	def Program_2_Enrollment_Status_Effective_Date(self): 
		return munge("8,753,760,C,N,N,BQ,69")
	def Program_3_CIP_Code(self): 
		return munge("6,761,766,O,N,N,BR,70")
	def CIP_Year(self): 
		return munge("4,767,770,C,N,N,BS,71")
	def Program_3_Credential_Level(self): 
		return munge("2,771,772,C,N,N,BT,72")
	def Published_Program_3_Length(self): 
		return munge("6,773,778,C,N,A,BU,73")
	def Published_Program_3_Length_Measurement(self): 
		return munge("1,779,779,C,A,N,BV,74")
	def Weeks_Program_3_Title_IV_Academic_Year(self): 
		return munge("6,780,785,C,N,N,BW,75")
	def Program_3_Begin_Date(self): 
		return munge("8,786,793,C,N,A,BX,76")
	def Special_Program_Indicator(self): 
		return munge("1,794,794,C,A,A,BY,77")
	def Program_3_Enrollment_Status(self): 
		return munge("1,795,795,C,A,N,BZ,78")
	def Program_3_Enrollment_Status_Effective_Date(self): 
		return munge("8,796,803,C,N,N,CA,79")
	def Program_4_CIP_Code(self): 
		return munge("6,804,809,O,N,N,CB,80")
	def CIP_Year(self): 
		return munge("4,810,813,C,N,N,CC,81")
	def Program_4_Credential_Level(self): 
		return munge("2,814,815,C,N,N,CD,82")
	def Published_Program_4_Length(self): 
		return munge("6,816,821,C,N,A,CE,83")
	def Published_Program_4_Length_Measurement(self): 
		return munge("1,822,822,C,A,N,CF,84")
	def Weeks_Program_4_Title_IV_Academic_Year(self): 
		return munge("6,823,828,C,N,N,CG,85")
	def Program_4_Begin_Date(self): 
		return munge("8,829,836,C,N,A,CH,86")
	def Special_Program_Indicator(self): 
		return munge("1,837,837,bin,A,A,CI,87")
	def Program_4_Enrollment_Status(self): 
		return munge("1,838,838,C,A,N,CJ,88")
	def Program_4_Enrollment_Status_Effective_Date(self): 
		return munge("8,839,846,C,N,N,CK,89")
	def Program_5_CIP_Code(self): 
		return munge("6,847,852,O,N,N,CL,90")
	def CIP_Year(self): 
		return munge("4,853,856,C,N,N,CM,91")
	def Program_5_Credential_Level(self): 
		return munge("2,857,858,C,N,N,CN,92")
	def Published_Program_5_Length(self): 
		return munge("6,859,864,C,N,A,CO,93")
	def Published_Program_5_Length_Measurement(self): 
		return munge("1,865,865,C,A,N,CP,94")
	def Weeks_Program_5_Title_IV_Academic_Year(self): 
		return munge("6,866,871,C,N,N,CQ,95")
	def Program_5_Begin_Date(self): 
		return munge("8,872,879,C,N,A,CR,96")
	def Special_Program_Indicator(self): 
		return munge("1,880,880,C,A,A,CS,97")
	def Program_5_Enrollment_Status(self): 
		return munge("1,881,881,C,A,N,CT,98")
	def Program_5_Enrollment_Status_Effective_Date(self): 
		return munge("8,882,889,C,N,N,CU,99")
	def Program_6_CIP_Code(self): 
		return munge("6,890,895,O,N,N,CV,100")
	def CIP_Year(self): 
		return munge("4,896,899,C,N,N,CW,101")
	def Program_6_Credential_Level(self): 
		return munge("2,900,901,C,N,N,CX,102")
	def Published_Program_6_Length(self): 
		return munge("6,902,907,C,N,A,CY,103")
	def Published_Program_6_Length_Measurement(self): 
		return munge("1,908,908,C,A,N,CZ,104")
	def Weeks_Program_6_Title_IV_Academic_Year(self): 
		return munge("6,909,914,C,N,N,DA,105")
	def Program_6_Begin_Date(self): 
		return munge("8,915,922,C,N,A,DB,106")
	def Special_Program_Indicator(self): 
		return munge("1,923,923,C,A,A,DC,107")
	def Program_6_Enrollment_Status(self): 
		return munge("1,924,924,C,A,N,DD,108")
	def Program_6_Enrollment_Status_Effective_Date(self): 
		return munge("8,925,932,C,N,AN,DE,109")
	def Filler(self): 
		return munge("318,933,1250,R,AN,,DF,110")

sdata = drl() 				# instantiate the drl class to sdata

# print sdata.Filler			# view a particular attribute
# sdata.__dict__.keys()			# example of  combined output
# dir(sdata)				# prints keys as list
# sdata.__dict__  			# prints the class as a dictionary
# sdata.__dict__.keys() 		# prints the keys as a list
# out=sdata 				# assign the instance optional
# print out.Filler			# view a particular attribute
#  type(out.Filler)			# Determine type
# print sdata.Filler.split(",")	`	# output as a list of strings
# print sdata.Filler.split(",")[2]	# a particular value
# print dir(Filler)
# print dline.readline()

#
##
def munge(index):
	''' munges the object '''
	# Test this with: "20,33,52,R,AN,AN,E,5"
	stuff = rsheet("A1")
	if stuff != "Record Type":
		return "error sheet must be in Upper Right Corner"
	length = int(index.split(",")[0])
	begin = int(index.split(",")[1])-1
	end = int(index.split(",")[2])
	# print sdata.Line
	# countr =  str(int(index.split(",")[7])+0)
	# cell = index.split(",")[6]+str(Line)
	cell = index.split(",")[6]+str(sdata.Line)
	# stuff = r#sheet(cell)
	istuff = rsheet(cell)
	if not istuff:
		istuff = " "
	if len(istuff) < 1:
		istuff = " "
	stuff = istuff.ljust(length)
	# print stuff+"  "+str(len(stuff))
	result = [length,begin,end,stuff,cell]
	return result
##
def swib(fobj):
	''' Does the substution '''
	index = fobj()
	length = index[0]
	begin = index[1]
	end = index[2]
	stuff = index[3]
	# print index.split(",")
	# inlist = list(stuff) 				# change data into a list element
	outlist[begin:end] = stuff 			# place data in the list in the correct place
	# print stuff+"  "+str(len(stuff))
	#
	# next 
	outstr = "".join(outlist) 
	# print outstr
	# print len(outstr)
	# of.write(outstr)
##
def openf():
	''' currently unused '''
	global outlist
	# of = open('workfile', 'w')
	# of.write('This is a test\n')
	# of.write(outlist)
	# print outlist
	outlist = list(outstr)
	print len(outlist)
	print type(outlist)

#
##iloop
def iloop():
	''' Loop through the object variables for whatever reason you want'''
	''' they are in no particular order'''
	for attr, value in sdata.__dict__.iteritems():
		print attr, value
##
def outb():
	''' The output file is born all 1250 characters'''
	# make the record string
	global outlist 
	global outstr
	outstr = 1250 * " "
	# print outstr
	# print len(outstr)
	outlist = list(outstr) 				# change this into a list
##
def outw():
	''' Writes the output to a file, all 1250 characters'''
	# make the record string
	# ok, pack em up...
	outstr = "".join(outlist) 
	print outstr
	print len(outstr)
	# of = open('workfile', 'w')
	of = open('workfile', 'a')
	# of.write(\n)
	of.write(outstr)
	of.close()
##
def swtchro():
	inlist = list("hello world") 			# change data into a list element
	outlist[9:20] = inlist 				# place data in the list in the correct place
	# print "".join(outlist)  			# see result
	outstr = "".join(outlist) 
	print outstr
	print len(outstr)
##
def swtest():
	# print "".join(outlist)  			# see result
	print outstr
	print len(outstr)
##
##
def alom():
	''' puts beginning and end on file, keeps size right at 1250 bytes'''
	#
	# this is the alpha
	inlist = list("begin") 				# change data into a list element
	outlist[0:5] = inlist 				# place data in the list in the correct place
	# print "".join(outlist)  			# see result
	#	
	# this is the omega
	inlist = list("end")
	# 				
	# change data into a list element
	outlist[1247:1250] = inlist 			# place data in the list in the correct place
	outstr = "".join(outlist) 
	print outstr
	print len(outstr)
	# of = open('workfile', 'w')
	# of.write(outstr)
##
def dend():
	''' puts an end on file, keeps size right at 1250 bytes'''
	#
	# this is the omega
	inlist = list("end"+"\n")
	# 				
	# change data into a list element
	outlist[1247:1250] = inlist 			# place data in the list in the correct place
	outstr = "".join(outlist) 
	# print outstr
	# print len(outstr)
	# of = open('workfile', 'w')
	# of.write(outstr)
##
def wline():
	''' puts beginning and end on file'''
	# this is the alpha
	inlist = list("begin") 				# change data into a list element
	outlist[0:5] = inlist 				# place data in the list in the correct place
	# print "".join(outlist)  			# see result
	# this is the omega
	inlist = list("end") 				# change data into a list element
	outlist[1247:1250] = inlist 				# place data in the list in the correct place
	# ok, pack em up...
	outstr = "".join(outlist) 
	print outstr
	# print "Length is "+lswtchro()en(outstr)
	print len(outstr)
	# of = open('workfile', 'w')
	of.write(outstr)
##
def gtest():
	'''	self.Column_for_Excel_Format '''
	print sdata.Column_for_Excel_Format 
	# print sdata.Column_for_Excel_Format(",")[6]
	# print sdata.Column_for_Excel_Format(",")[fieldname]
	print sdata.hi()
	#
#
def dtest():
	outb()		# a new output file is born
	# alom()	# checks beginning and end
	# swtchro()	# adds "hello world"
	swib(sdata.Record_Type)
	swib(sdata.Student_SSN)
	swib(sdata.First_Name)
	swib(sdata.Middle_Initial)
	swib(sdata.Last_Name)
	swib(sdata.Name_Suffix)
	swib(sdata.Previous_SSN)
	swib(sdata.Previous_Last_Name)
	swib(sdata.Enrollment_Status)
	swib(sdata.Status_Start_Date)
	swib(sdata.Street_Line_1)
	swib(sdata.Street_Line_2)
	swib(sdata.City)
	swib(sdata.State)
	swib(sdata.Zip)
	swib(sdata.Country)
	swib(sdata.Anticipated_Graduation_Date)
	swib(sdata.Date_of_Birth)
	swib(sdata.Term_Begin_Date)
	swib(sdata.Term_End_Date)
	swib(sdata.Filler)
	swib(sdata.Directory_Block_Indicator)
	swib(sdata.NCES_CIP_Code_for_Major_1)
	swib(sdata.NCES_CIP_Code_for_Major_2)
	swib(sdata.Major_Course_of_Study_1)
	swib(sdata.Major_Course_of_Study_2)
	swib(sdata.Class_Credential)
	swib(sdata.First_Time_Full_Time)
	swib(sdata.Degree_Seeking)
	swib(sdata.High_School_Code)
	swib(sdata.Gender)
	swib(sdata.Race_Ethnicity)
	swib(sdata.College_Student_ID)
	swib(sdata.State_Student_ID)
	swib(sdata.Email)
	swib(sdata.Good_Student)
	swib(sdata.Middle_Name)
	swib(sdata.Veterans_Status_Indicator_)
	swib(sdata.Reserved_for_CommIT_ID)
	swib(sdata.Pell_Grant_Recipient_Flag)
	swib(sdata.Remedial_Flag)
	swib(sdata.Citizenship_Flag)
	swib(sdata.Student_Phone_Type)
	swib(sdata.Preferred_Phone_Number_Flag)
	swib(sdata.Student_Phone_Country_Code)
	swib(sdata.Student_Phone_Number)
	swib(sdata.Reserved_for_Move_To_OPEID_Future_CH_Functionality)
	swib(sdata.Program_Indicator)
	swib(sdata.Program_1_CIP_Code)
	swib(sdata.CIP_Year)
	swib(sdata.Program_1_Credential_Level)
	swib(sdata.Published_Program_1_Length)
	swib(sdata.Published_Program_1_Length_Measurement)
	swib(sdata.Weeks_Program_1_Title_IV_Academic_Year)
	swib(sdata.Program_1_Begin_Date)
	swib(sdata.Special_Program_Indicator)
	swib(sdata.Program_1_Enrollment_Status)
	swib(sdata.Program_1_Enrollment_Status_Effective_Date)
	swib(sdata.Program_2_CIP_Code)
	swib(sdata.CIP_Year)
	swib(sdata.Program_2_Credential_Level)
	swib(sdata.Published_Program_2_Length)
	swib(sdata.Published_Program_2_Length_Measurement)
	swib(sdata.Weeks_Program_2_Title_IV_Academic_Year)
	swib(sdata.Program_2_Begin_Date)
	swib(sdata.Special_Program_Indicator)
	swib(sdata.Program_2_Enrollment_Status)
	swib(sdata.Program_2_Enrollment_Status_Effective_Date)
	swib(sdata.Program_3_CIP_Code)
	swib(sdata.CIP_Year)
	swib(sdata.Program_3_Credential_Level)
	swib(sdata.Published_Program_3_Length)
	swib(sdata.Published_Program_3_Length_Measurement)
	swib(sdata.Weeks_Program_3_Title_IV_Academic_Year)
	swib(sdata.Program_3_Begin_Date)
	swib(sdata.Special_Program_Indicator)
	swib(sdata.Program_3_Enrollment_Status)
	swib(sdata.Program_3_Enrollment_Status_Effective_Date)
	swib(sdata.Program_4_CIP_Code)
	swib(sdata.CIP_Year)
	swib(sdata.Program_4_Credential_Level)
	swib(sdata.Published_Program_4_Length)
	swib(sdata.Published_Program_4_Length_Measurement)
	swib(sdata.Weeks_Program_4_Title_IV_Academic_Year)
	swib(sdata.Program_4_Begin_Date)
	swib(sdata.Special_Program_Indicator)
	swib(sdata.Program_4_Enrollment_Status)
	swib(sdata.Program_4_Enrollment_Status_Effective_Date)
	swib(sdata.Program_5_CIP_Code)
	swib(sdata.CIP_Year)
	swib(sdata.Program_5_Credential_Level)
	swib(sdata.Published_Program_5_Length)
	swib(sdata.Published_Program_5_Length_Measurement)
	swib(sdata.Weeks_Program_5_Title_IV_Academic_Year)
	swib(sdata.Program_5_Begin_Date)
	swib(sdata.Special_Program_Indicator)
	swib(sdata.Program_5_Enrollment_Status)
	swib(sdata.Program_5_Enrollment_Status_Effective_Date)
	swib(sdata.Program_6_CIP_Code)
	swib(sdata.CIP_Year)
	swib(sdata.Program_6_Credential_Level)
	swib(sdata.Published_Program_6_Length)
	swib(sdata.Published_Program_6_Length_Measurement)
	swib(sdata.Weeks_Program_6_Title_IV_Academic_Year)
	swib(sdata.Program_6_Begin_Date)
	swib(sdata.Special_Program_Indicator)
	swib(sdata.Program_6_Enrollment_Status)
	swib(sdata.Program_6_Enrollment_Status_Effective_Date)
	swib(sdata.Filler)
	dend()
	# outw()		# writes the file to disk
	# swtest()	# switch test
	# openf()		# test writing
##
def rsheet(cell):
	'''Reads in a sheet'''
	wb = openpyxl.load_workbook(spreadsheet)
	ws =  "".join(wb.get_sheet_names()[0])
	sheet_ranges = wb[ws]
	return (sheet_ranges[cell].value)
##
def go():
	for i in range(2,13):
	     # of = open('workfile', 'a')
	     sdata.Line = i
	     dtest()
	     outw()			# write the line
	     # of.write(outstr)

print "Welcome to the "+__appname__  			# uncomment line 7 to make your life a living hell...
print "Counting the header we are currently at line "+str(sdata.Line)+" of the spreadsheet"+spreadsheet

