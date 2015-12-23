#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

from __future__ import print_function
from six.moves  import input           # use raw_input when I say input
from os.path    import expanduser      # Cross-platform home directory finder

__appname__    = "Specification validator"
__author__     = "Kevin Cole"
__copyright__  = "Copyright 2015, NOVA Web Development, LLC"
__credits__    = ["Kevin Cole"]  # Authors and bug reporters
__license__    = "GPL"
__version__    = "0.1"
__maintainer__ = "Kevin Cole"
__email__      = "dc.loco@gmail.com"
__status__     = "Prototype"  # "Prototype", "Development" or "Production"
__module__     = ""


#    def __init__(self):
#        self.Column_for_Excel_Format = "Index,"      \
#                                       "Length,"     \
#                                       "Start,"      \
#                                       "Stop,"       \
#                                       "Reqd,"       \
#                                       "Type,"       \
#                                       "Field Name," \
#                                       "Count"
#
#    def Column_for_Excel_Format(self):
#        return munge("Indexa,Length,Start,Stop,Reqd,Type,Field_Name,Count")


class Typo(Exception):
    def __init__(self, value, source):
        self.value = value
        self.source = source

    def __str__(self):
        message  = "Invalid field type: '{0}' in\n  '{1}'\n"
        message += "  (Not 'N', 'A' or 'AN')"
        return message.format(self.value, self.source)

recordOut = {}


class Field:

    def __init__(self, specs):
        length, start, stop, reqd, type1, type2, x, order = specs.split(",")
        self.length = int(length)
        self.start  = int(start) - 1
        self.stop   = int(stop)
        self.order  = int(order)
        self.x      = x
        self.reqd   = reqd
        if type1 == "N":                       # Set output format string
            self.type = "int"
            self.fmt = "{0}d".format(length)
        elif type1 == "AN" or type1 == "A":
            self.type = "str"
            self.fmt = "{0}s".format(length)
        else:
            raise Typo(type1, specs)
        self.value = None

    def getval(self, recordIn):
        soup = recordIn[self.start:self.stop]  # Primordial soup
        if self.reqd == "O" and soup != "":
            if self.type == "int":
                try:
                    self.value = int(soup)
                except:
                    self.error(soup)
            elif self.type == "str":
                self.value = soup
        elif self.reqd == "R":
            if len(soup.strip()):
                if self.type == "int":
                    try:
                        self.value = int(soup)
                    except:
                        self.error(soup)
                elif self.type == "str":
                    self.value = soup
        recordOut[self.order] = [self.fmt, self.value]

    def error(self, source):
        size = "(" + str(self.length) + ")"
        message  = "ERROR: "
        message += "{0:3d}: [{1:4d} - {2:4d}]  {3:>5s}  {4:2s}"
        message += "  {5}  {6}  |  value = '{7}'"
        print(message
              .format(self.order, self.start, self.stop,
                      size, self.x, self.reqd,
                      self.type, source))

class Record:
    def __init__(self):
        pass

# Create a boatload (record-load?) of fields
#
Record_Type = Field("2,1,2,R,AN,AN,A,1")
Student_SSN = Field("9,3,11,R,N,N,B,2")
First_Name = Field("20,12,31,R,AN,AN,C,3")
Middle_Initial = Field("1,32,32,O,AN,AN,D,4")
Last_Name = Field("20,33,52,R,AN,AN,E,5")
Name_Suffix = Field("5,53,57,O,AN,AN,F,6")
Previous_SSN = Field("9,58,66,O,N,N,G,7")
Previous_Last_Name = Field("20,67,86,O,AN,AN,H,8")
Degree_Concentration = Field("9,1,87,87,R,A,I,9")
Enrollment_Status = Field("1,87,87,R,A,N,J,10")
Status_Start_Date = Field("8,88,95,C,N,AN,K,11")
Street_Line_1 = Field("30,96,125,R,AN,AN,L,12")
Street_Line_2 = Field("30,126,155,O,AN,A,M,13")
City = Field("20,156,175,R,A,A,N,14")
State = Field("2,176,177,R,A,AN,O,15")
Zip = Field("9,178,186,C,AN,AN,P,16")
Country = Field("15,187,201,C,AN,N,Q,17")
Anticipated_Graduation_Date = Field("8,202,209,C,N,N,R,18")
Date_of_Birth = Field("8,210,217,R,N,N,S,19")
Term_Begin_Date = Field("8,218,225,R,N,N,T,20")
Term_End_Date = Field("8,226,233,R,N,AN,U,21")
Filler = Field("1,234,234,R,AN,A,V,22")
Directory_Block_Indicator = Field("1,235,235,R,A,N,W,23")
NCES_CIP_Code_for_Major_1 = Field("6,236,241,O,N,N,X,24")
NCES_CIP_Code_for_Major_2 = Field("6,242,247,O,N,AN,Y,25")
Major_Course_of_Study_1 = Field("80,248,327,O,AN,AN,Z,26")
Major_Course_of_Study_2 = Field("80,328,407,O,AN,A,AA,27")
Class_Credential = Field("1,408,408,C,A,A,AB,28")
First_Time_Full_Time = Field("1,409,409,O,A,A,AC,29")
Degree_Seeking = Field("1,410,410,O,A,N,AD,30")
High_School_Code = Field("6,411,416,O,N,A,AE,31")
Gender = Field("1,417,417,O,A,A,AF,32")
Race_Ethnicity = Field("2,418,419,O,A,AN,AG,33")
College_Student_ID = Field("20,420,439,O,AN,AN,AH,34")
State_Student_ID = Field("30,440,469,O,AN,AN,AI,35")
Email = Field("128,470,597,O,AN,A,AJ,36")
Good_Student = Field("1,598,598,O,A,AN,AK,37")
Middle_Name = Field("35,599,633,O,AN,A,AL,38")
Veterans_Status_Indicator_ = Field("1,634,634,O,A,AN,AM,39")
Reserved_for_CommIT_ID = Field("12,635,646,O,AN,A,AN,40")
Pell_Grant_Recipient_Flag = Field("1,647,647,O,A,A,AO,41")
Remedial_Flag = Field("1,648,648,O,A,A,AP,42")
Citizenship_Flag = Field("1,649,649,O,A,A,AQ,43")
Student_Phone_Type = Field("1,650,650,O,A,A,AR,44")
Preferred_Phone_Number_Flag = Field("1,651,651,O,A,N,AS,45")
Student_Phone_Country_Code = Field("3,652,654,O,N,N,AT,46")
Student_Phone_Number = Field("11,655,665,O,N,N,AU,47")
Reserved_for_Move_To_OPEID_Future_CH_Functionality = Field("8,666,673,O,N,A,AV,48")
Program_Indicator = Field("1,674,674,R,A,N,AW,49")
Program_1_CIP_Code = Field("6,675,680,C,N,N,AX,50")
CIP_Year = Field("4,681,684,C,N,N,AY,51")
Program_1_Credential_Level = Field("2,685,686,C,N,N,AZ,52")
Published_Program_1_Length = Field("6,687,692,C,N,A,BA,53")
Published_Program_1_Length_Measurement = Field("1,693,693,C,A,N,BB,54")
Weeks_Program_1_Title_IV_Academic_Year = Field("6,694,699,C,N,N,BC,55")
Program_1_Begin_Date = Field("8,700,707,C,N,A,BD,56")
Special_Program_Indicator = Field("1,708,708,C,A,A,BE,57")
Program_1_Enrollment_Status = Field("1,709,709,C,A,N,BF,58")
Program_1_Enrollment_Status_Effective_Date = Field("8,710,717,C,N,N,BG,59")
Program_2_CIP_Code = Field("6,718,723,O,N,N,BH,60")
CIP_Year = Field("4,724,727,C,N,N,BI,61")
Program_2_Credential_Level = Field("2,728,729,C,N,N,BJ,62")
Published_Program_2_Length = Field("6,730,735,C,N,A,BK,63")
Published_Program_2_Length_Measurement = Field("1,736,736,C,A,N,BL,64")
Weeks_Program_2_Title_IV_Academic_Year = Field("6,737,742,C,N,N,BM,65")
Program_2_Begin_Date = Field("8,743,750,C,N,A,BN,66")
Special_Program_Indicator = Field("1,751,751,C,A,A,BO,67")
Program_2_Enrollment_Status = Field("1,752,752,C,A,N,BP,68")
Program_2_Enrollment_Status_Effective_Date = Field("8,753,760,C,N,N,BQ,69")
Program_3_CIP_Code = Field("6,761,766,O,N,N,BR,70")
CIP_Year = Field("4,767,770,C,N,N,BS,71")
Program_3_Credential_Level = Field("2,771,772,C,N,N,BT,72")
Published_Program_3_Length = Field("6,773,778,C,N,A,BU,73")
Published_Program_3_Length_Measurement = Field("1,779,779,C,A,N,BV,74")
Weeks_Program_3_Title_IV_Academic_Year = Field("6,780,785,C,N,N,BW,75")
Program_3_Begin_Date = Field("8,786,793,C,N,A,BX,76")
Special_Program_Indicator = Field("1,794,794,C,A,A,BY,77")
Program_3_Enrollment_Status = Field("1,795,795,C,A,N,BZ,78")
Program_3_Enrollment_Status_Effective_Date = Field("8,796,803,C,N,N,CA,79")
Program_4_CIP_Code = Field("6,804,809,O,N,N,CB,80")
CIP_Year = Field("4,810,813,C,N,N,CC,81")
Program_4_Credential_Level = Field("2,814,815,C,N,N,CD,82")
Published_Program_4_Length = Field("6,816,821,C,N,A,CE,83")
Published_Program_4_Length_Measurement = Field("1,822,822,C,A,N,CF,84")
Weeks_Program_4_Title_IV_Academic_Year = Field("6,823,828,C,N,N,CG,85")
Program_4_Begin_Date = Field("8,829,836,C,N,A,CH,86")
Special_Program_Indicator = Field("1,837,837,bin,A,A,CI,87")
Program_4_Enrollment_Status = Field("1,838,838,C,A,N,CJ,88")
Program_4_Enrollment_Status_Effective_Date = Field("8,839,846,C,N,N,CK,89")
Program_5_CIP_Code = Field("6,847,852,O,N,N,CL,90")
CIP_Year = Field("4,853,856,C,N,N,CM,91")
Program_5_Credential_Level = Field("2,857,858,C,N,N,CN,92")
Published_Program_5_Length = Field("6,859,864,C,N,A,CO,93")
Published_Program_5_Length_Measurement = Field("1,865,865,C,A,N,CP,94")
Weeks_Program_5_Title_IV_Academic_Year = Field("6,866,871,C,N,N,CQ,95")
Program_5_Begin_Date = Field("8,872,879,C,N,A,CR,96")
Special_Program_Indicator = Field("1,880,880,C,A,A,CS,97")
Program_5_Enrollment_Status = Field("1,881,881,C,A,N,CT,98")
Program_5_Enrollment_Status_Effective_Date = Field("8,882,889,C,N,N,CU,99")
Program_6_CIP_Code = Field("6,890,895,O,N,N,CV,100")
CIP_Year = Field("4,896,899,C,N,N,CW,101")
Program_6_Credential_Level = Field("2,900,901,C,N,N,CX,102")
Published_Program_6_Length = Field("6,902,907,C,N,A,CY,103")
Published_Program_6_Length_Measurement = Field("1,908,908,C,A,N,CZ,104")
Weeks_Program_6_Title_IV_Academic_Year = Field("6,909,914,C,N,N,DA,105")
Program_6_Begin_Date = Field("8,915,922,C,N,A,DB,106")
Special_Program_Indicator = Field("1,923,923,C,A,A,DC,107")
Program_6_Enrollment_Status = Field("1,924,924,C,A,N,DD,108")
Program_6_Enrollment_Status_Effective_Date = Field("8,925,932,C,N,AN,DE,109")
Filler = Field("318,933,1250,R,AN,,DF,110")


def main():
    data = open("sample_data_2015-12-18.dat", "r")
    for row in data:
        Record_Type.getval(row)
        Student_SSN.getval(row)
        First_Name.getval(row)
        Middle_Initial.getval(row)
        Last_Name.getval(row)
        Name_Suffix.getval(row)
        Previous_SSN.getval(row)
        Previous_Last_Name.getval(row)
        Degree_Concentration.getval(row)
        Enrollment_Status.getval(row)
        Status_Start_Date.getval(row)
        Street_Line_1.getval(row)
        Street_Line_2.getval(row)
        City.getval(row)
        State.getval(row)
        Zip.getval(row)
        Country.getval(row)
        Anticipated_Graduation_Date.getval(row)
        Date_of_Birth.getval(row)
        Term_Begin_Date.getval(row)
        Term_End_Date.getval(row)
        Filler.getval(row)
        Directory_Block_Indicator.getval(row)
        NCES_CIP_Code_for_Major_1.getval(row)
        NCES_CIP_Code_for_Major_2.getval(row)
        Major_Course_of_Study_1.getval(row)
        Major_Course_of_Study_2.getval(row)
        Class_Credential.getval(row)
        First_Time_Full_Time.getval(row)
        Degree_Seeking.getval(row)
        High_School_Code.getval(row)
        Gender.getval(row)
        Race_Ethnicity.getval(row)
        College_Student_ID.getval(row)
        State_Student_ID.getval(row)
        Email.getval(row)
        Good_Student.getval(row)
        Middle_Name.getval(row)
        Veterans_Status_Indicator_.getval(row)
        Reserved_for_CommIT_ID.getval(row)
        Pell_Grant_Recipient_Flag.getval(row)
        Remedial_Flag.getval(row)
        Citizenship_Flag.getval(row)
        Student_Phone_Type.getval(row)
        Preferred_Phone_Number_Flag.getval(row)
        Student_Phone_Country_Code.getval(row)
        Student_Phone_Number.getval(row)
        Reserved_for_Move_To_OPEID_Future_CH_Functionality.getval(row)
        Program_Indicator.getval(row)
        Program_1_CIP_Code.getval(row)
        CIP_Year.getval(row)
        Program_1_Credential_Level.getval(row)
        Published_Program_1_Length.getval(row)
        Published_Program_1_Length_Measurement.getval(row)
        Weeks_Program_1_Title_IV_Academic_Year.getval(row)
        Program_1_Begin_Date.getval(row)
        Special_Program_Indicator.getval(row)
        Program_1_Enrollment_Status.getval(row)
        Program_1_Enrollment_Status_Effective_Date.getval(row)
        Program_2_CIP_Code.getval(row)
        CIP_Year.getval(row)
        Program_2_Credential_Level.getval(row)
        Published_Program_2_Length.getval(row)
        Published_Program_2_Length_Measurement.getval(row)
        Weeks_Program_2_Title_IV_Academic_Year.getval(row)
        Program_2_Begin_Date.getval(row)
        Special_Program_Indicator.getval(row)
        Program_2_Enrollment_Status.getval(row)
        Program_2_Enrollment_Status_Effective_Date.getval(row)
        Program_3_CIP_Code.getval(row)
        CIP_Year.getval(row)
        Program_3_Credential_Level.getval(row)
        Published_Program_3_Length.getval(row)
        Published_Program_3_Length_Measurement.getval(row)
        Weeks_Program_3_Title_IV_Academic_Year.getval(row)
        Program_3_Begin_Date.getval(row)
        Special_Program_Indicator.getval(row)
        Program_3_Enrollment_Status.getval(row)
        Program_3_Enrollment_Status_Effective_Date.getval(row)
        Program_4_CIP_Code.getval(row)
        CIP_Year.getval(row)
        Program_4_Credential_Level.getval(row)
        Published_Program_4_Length.getval(row)
        Published_Program_4_Length_Measurement.getval(row)
        Weeks_Program_4_Title_IV_Academic_Year.getval(row)
        Program_4_Begin_Date.getval(row)
        Special_Program_Indicator.getval(row)
        Program_4_Enrollment_Status.getval(row)
        Program_4_Enrollment_Status_Effective_Date.getval(row)
        Program_5_CIP_Code.getval(row)
        CIP_Year.getval(row)
        Program_5_Credential_Level.getval(row)
        Published_Program_5_Length.getval(row)
        Published_Program_5_Length_Measurement.getval(row)
        Weeks_Program_5_Title_IV_Academic_Year.getval(row)
        Program_5_Begin_Date.getval(row)
        Special_Program_Indicator.getval(row)
        Program_5_Enrollment_Status.getval(row)
        Program_5_Enrollment_Status_Effective_Date.getval(row)
        Program_6_CIP_Code.getval(row)
        CIP_Year.getval(row)
        Program_6_Credential_Level.getval(row)
        Published_Program_6_Length.getval(row)
        Published_Program_6_Length_Measurement.getval(row)
        Weeks_Program_6_Title_IV_Academic_Year.getval(row)
        Program_6_Begin_Date.getval(row)
        Special_Program_Indicator.getval(row)
        Program_6_Enrollment_Status.getval(row)
        Program_6_Enrollment_Status_Effective_Date.getval(row)
        Filler.getval(row)
        print(recordOut[0])

#   return 0

if __name__ == "__main__":
    main()
