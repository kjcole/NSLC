#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

from __future__ import print_function
from six.moves  import input           # use raw_input when I say input
from os.path    import expanduser      # Cross-platform home directory finder

import sys

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


class TypoError(Exception):
    """Syntax error: Attempted to define a Field with an invalid data type"""
    def __init__(self, data_type, definition_string):
        self.data_type = data_type
        self.definition_string = definition_string

    def __str__(self):
        message  = "Invalid field type: '{0}' in\n  '{1}'\n"
        message += "  (Not 'N', 'A' or 'AN')"
        return message.format(self.data_type, self.definition_string)


class SizeError(Exception):
    """Syntax error: Supplied length != computed length"""
    def __init__(self, stop, start, length, definition_string):
        self.stop   = stop
        self.start  = start
        self.length = length
        self.definition_string = definition_string

    def __str__(self):
        message  = "Something doesn't add up: (Stop - Start) + 1 != Length\n"
        message += "  (({0} - {1}) + 1) != {2} in\n"
        message += "  '{3}'"
        return message.format(self.stop, self.start, self.length,
                              self.definition_string)


class DataError(Exception):
    def __init__(self, field, fault, source):
        self.field = field
        self.fault = fault
        self.source = source

    def __str__(self):
        self.size = "(" + str(self.field.length) + ")"
        message  = "Invalid data: {0}\n"
        message += "  Col: [Start - End]   (Size)  Cell  Req'd  Type  |  "
        message += "          Value\n"
        message += "  ---- -------------   ------  ----  -----  ----  |  "
        message += ("-" * 25) + "\n"
        message += "  {1:3d}: [{2:4d} - {3:4d}]    {4:>5s}    {5:2s}"
        message += "    {6}     {7}  |  '{8}'"
        return message.format(self.fault,
                              self.field.order,
                              self.field.start, self.field.stop, self.size,
                              self.field.cell, self.field.reqd,
                              self.field.type,
                              self.source)


class Field:
    def __init__(self, specs):
        """Build a self-aware field"""
        length, start, stop, reqd, type1, type2, cell, order = specs.split(",")
        self.length = int(length)     # Field length
        self.start  = int(start) - 1  # Starting column
        self.stop   = int(stop)       # Ending column
        self.order  = int(order)      # Order w/i record
        self.cell   = cell            # Spreadsheet cell
        self.reqd   = reqd            # Required, Optional, Conditional
        if (self.stop - self.start) != self.length:
            raise SizeError(stop, start, length, specs)
        if type1 == "N":              # Data type is Numeric...
            self.type = "int"         # ...i.e. integer
            self.fmt = "{0}d".format(length)  # Output format
        elif type1 in ("A", "AN"):    # Data type is alpha-numeric...
            self.type = "str"         # ...i.e. string
            self.fmt = "{0}s".format(length)  # Output format
        else:                                 # Data type is WACKY!!!
            raise TypoError(type1, specs)     # ...i.e. ERROR!!!
        self.value = ""           # Initialize to no value

    def load(self, row):
        """Set field's value to content from input record"""
        soup = row[self.start:self.stop]       # Primordial soup
        soup = soup.strip()                    # Safe for every field?
        if self.reqd in ("O", "C"):            # If optional or conditional...
            if soup != "":                     # ...and soup has stones...
                if self.type == "int":
                    try:
                        self.value = int(soup)
                    except:
                        raise DataError(self, "Not a number", soup)
                elif self.type == "str":
                    self.value = soup
            else:                              # ...soup has no stones
                self.fmt = "{0}s".format(self.length)
        elif self.reqd == "R":                 # If required...
            if soup != "":                     # ...and soup has stones...
                if self.type == "int":
                    try:
                        self.value = int(soup)
                    except:
                        raise DataError(self, "Not a number", soup)
                elif self.type == "str":
                    self.value = soup
            else:                              # ...soup has no stones
                raise DataError(self, "Required field empty", soup)

    def __repr__(self):
        """See __repr__ documentation"""
        return "{0}".format(self.value)

    def __str__(self):
        """A formatted representation of the field"""
        fmt = "".join(("{0:", self.fmt, "}"))
        return fmt.format(self.value)

    def setval(self, value):
        if self.type == "int":
            self.value = int(value)
        else:
            self.value = value


class Record:
    """Create a boatload (record-load?) of fields"""
    def __init__(self):
        self.Record_Type = Field("2,1,2,R,AN,AN,A,1")
        self.Student_SSN = Field("9,3,11,R,N,N,B,2")
        self.First_Name = Field("20,12,31,R,AN,AN,C,3")
        self.Middle_Initial = Field("1,32,32,O,AN,AN,D,4")
        self.Last_Name = Field("20,33,52,R,AN,AN,E,5")
        self.Name_Suffix = Field("5,53,57,O,AN,AN,F,6")
        self.Previous_SSN = Field("9,58,66,O,N,N,G,7")
        self.Previous_Last_Name = Field("20,67,86,O,AN,AN,H,8")
        #self.Degree_Concentration = Field("9,1,87,87,R,A,I,9")
        self.Enrollment_Status = Field("1,87,87,R,A,N,J,10")
        self.Status_Start_Date = Field("8,88,95,C,N,AN,K,11")
        self.Street_Line_1 = Field("30,96,125,R,AN,AN,L,12")
        self.Street_Line_2 = Field("30,126,155,O,AN,A,M,13")
        self.City = Field("20,156,175,R,A,A,N,14")
        self.State = Field("2,176,177,R,A,AN,O,15")
        self.Zip = Field("9,178,186,C,AN,AN,P,16")
        self.Country = Field("15,187,201,C,AN,N,Q,17")
        self.Anticipated_Graduation_Date = Field("8,202,209,C,N,N,R,18")
        self.Date_of_Birth = Field("8,210,217,R,N,N,S,19")
        self.Term_Begin_Date = Field("8,218,225,R,N,N,T,20")
        self.Term_End_Date = Field("8,226,233,R,N,AN,U,21")
        self.Filler = Field("1,234,234,R,AN,A,V,22")
        self.Directory_Block_Indicator = Field("1,235,235,R,A,N,W,23")
        self.NCES_CIP_Code_for_Major_1 = Field("6,236,241,O,N,N,X,24")
        self.NCES_CIP_Code_for_Major_2 = Field("6,242,247,O,N,AN,Y,25")
        self.Major_Course_of_Study_1 = Field("80,248,327,O,AN,AN,Z,26")
        self.Major_Course_of_Study_2 = Field("80,328,407,O,AN,A,AA,27")
        self.Class_Credential = Field("1,408,408,C,A,A,AB,28")
        self.First_Time_Full_Time = Field("1,409,409,O,A,A,AC,29")
        self.Degree_Seeking = Field("1,410,410,O,A,N,AD,30")
        self.High_School_Code = Field("6,411,416,O,N,A,AE,31")
        self.Gender = Field("1,417,417,O,A,A,AF,32")
        self.Race_Ethnicity = Field("2,418,419,O,A,AN,AG,33")
        self.College_Student_ID = Field("20,420,439,O,AN,AN,AH,34")
        self.State_Student_ID = Field("30,440,469,O,AN,AN,AI,35")
        self.Email = Field("128,470,597,O,AN,A,AJ,36")
        self.Good_Student = Field("1,598,598,O,A,AN,AK,37")
        self.Middle_Name = Field("35,599,633,O,AN,A,AL,38")
        self.Veterans_Status_Indicator_ = Field("1,634,634,O,A,AN,AM,39")
        self.Reserved_for_CommIT_ID = Field("12,635,646,O,AN,A,AN,40")
        self.Pell_Grant_Recipient_Flag = Field("1,647,647,O,A,A,AO,41")
        self.Remedial_Flag = Field("1,648,648,O,A,A,AP,42")
        self.Citizenship_Flag = Field("1,649,649,O,A,A,AQ,43")
        self.Student_Phone_Type = Field("1,650,650,O,A,A,AR,44")
        self.Preferred_Phone_Number_Flag = Field("1,651,651,O,A,N,AS,45")
        self.Student_Phone_Country_Code = Field("3,652,654,O,N,N,AT,46")
        self.Student_Phone_Number = Field("11,655,665,O,N,N,AU,47")
        self.Reserved_for_Move_To_OPEID_Future_CH_Functionality = Field("8,666,673,O,N,A,AV,48")
        self.Program_Indicator = Field("1,674,674,R,A,N,AW,49")
        self.Program_1_CIP_Code = Field("6,675,680,C,N,N,AX,50")
        self.CIP_Year = Field("4,681,684,C,N,N,AY,51")
        self.Program_1_Credential_Level = Field("2,685,686,C,N,N,AZ,52")
        self.Published_Program_1_Length = Field("6,687,692,C,N,A,BA,53")
        self.Published_Program_1_Length_Measurement = Field("1,693,693,C,A,N,BB,54")
        self.Weeks_Program_1_Title_IV_Academic_Year = Field("6,694,699,C,N,N,BC,55")
        self.Program_1_Begin_Date = Field("8,700,707,C,N,A,BD,56")
        self.Special_Program_Indicator = Field("1,708,708,C,A,A,BE,57")
        self.Program_1_Enrollment_Status = Field("1,709,709,C,A,N,BF,58")
        self.Program_1_Enrollment_Status_Effective_Date = Field("8,710,717,C,N,N,BG,59")
        self.Program_2_CIP_Code = Field("6,718,723,O,N,N,BH,60")
        self.CIP_Year = Field("4,724,727,C,N,N,BI,61")
        self.Program_2_Credential_Level = Field("2,728,729,C,N,N,BJ,62")
        self.Published_Program_2_Length = Field("6,730,735,C,N,A,BK,63")
        self.Published_Program_2_Length_Measurement = Field("1,736,736,C,A,N,BL,64")
        self.Weeks_Program_2_Title_IV_Academic_Year = Field("6,737,742,C,N,N,BM,65")
        self.Program_2_Begin_Date = Field("8,743,750,C,N,A,BN,66")
        self.Special_Program_Indicator = Field("1,751,751,C,A,A,BO,67")
        self.Program_2_Enrollment_Status = Field("1,752,752,C,A,N,BP,68")
        self.Program_2_Enrollment_Status_Effective_Date = Field("8,753,760,C,N,N,BQ,69")
        self.Program_3_CIP_Code = Field("6,761,766,O,N,N,BR,70")
        self.CIP_Year = Field("4,767,770,C,N,N,BS,71")
        self.Program_3_Credential_Level = Field("2,771,772,C,N,N,BT,72")
        self.Published_Program_3_Length = Field("6,773,778,C,N,A,BU,73")
        self.Published_Program_3_Length_Measurement = Field("1,779,779,C,A,N,BV,74")
        self.Weeks_Program_3_Title_IV_Academic_Year = Field("6,780,785,C,N,N,BW,75")
        self.Program_3_Begin_Date = Field("8,786,793,C,N,A,BX,76")
        self.Special_Program_Indicator = Field("1,794,794,C,A,A,BY,77")
        self.Program_3_Enrollment_Status = Field("1,795,795,C,A,N,BZ,78")
        self.Program_3_Enrollment_Status_Effective_Date = Field("8,796,803,C,N,N,CA,79")
        self.Program_4_CIP_Code = Field("6,804,809,O,N,N,CB,80")
        self.CIP_Year = Field("4,810,813,C,N,N,CC,81")
        self.Program_4_Credential_Level = Field("2,814,815,C,N,N,CD,82")
        self.Published_Program_4_Length = Field("6,816,821,C,N,A,CE,83")
        self.Published_Program_4_Length_Measurement = Field("1,822,822,C,A,N,CF,84")
        self.Weeks_Program_4_Title_IV_Academic_Year = Field("6,823,828,C,N,N,CG,85")
        self.Program_4_Begin_Date = Field("8,829,836,C,N,A,CH,86")
        self.Special_Program_Indicator = Field("1,837,837,bin,A,A,CI,87")
        self.Program_4_Enrollment_Status = Field("1,838,838,C,A,N,CJ,88")
        self.Program_4_Enrollment_Status_Effective_Date = Field("8,839,846,C,N,N,CK,89")
        self.Program_5_CIP_Code = Field("6,847,852,O,N,N,CL,90")
        self.CIP_Year = Field("4,853,856,C,N,N,CM,91")
        self.Program_5_Credential_Level = Field("2,857,858,C,N,N,CN,92")
        self.Published_Program_5_Length = Field("6,859,864,C,N,A,CO,93")
        self.Published_Program_5_Length_Measurement = Field("1,865,865,C,A,N,CP,94")
        self.Weeks_Program_5_Title_IV_Academic_Year = Field("6,866,871,C,N,N,CQ,95")
        self.Program_5_Begin_Date = Field("8,872,879,C,N,A,CR,96")
        self.Special_Program_Indicator = Field("1,880,880,C,A,A,CS,97")
        self.Program_5_Enrollment_Status = Field("1,881,881,C,A,N,CT,98")
        self.Program_5_Enrollment_Status_Effective_Date = Field("8,882,889,C,N,N,CU,99")
        self.Program_6_CIP_Code = Field("6,890,895,O,N,N,CV,100")
        self.CIP_Year = Field("4,896,899,C,N,N,CW,101")
        self.Program_6_Credential_Level = Field("2,900,901,C,N,N,CX,102")
        self.Published_Program_6_Length = Field("6,902,907,C,N,A,CY,103")
        self.Published_Program_6_Length_Measurement = Field("1,908,908,C,A,N,CZ,104")
        self.Weeks_Program_6_Title_IV_Academic_Year = Field("6,909,914,C,N,N,DA,105")
        self.Program_6_Begin_Date = Field("8,915,922,C,N,A,DB,106")
        self.Special_Program_Indicator = Field("1,923,923,C,A,A,DC,107")
        self.Program_6_Enrollment_Status = Field("1,924,924,C,A,N,DD,108")
        self.Program_6_Enrollment_Status_Effective_Date = Field("8,925,932,C,N,AN,DE,109")
        self.Filler = Field("318,933,1250,R,AN,,DF,110")

    def __str__(self):
        record = {}
        # For each field, record[order] = field value
        for field in dir(self):
            if (not field.startswith("__")) and \
               (not callable(getattr(self, field))):
                record[eval("self." + field).order] = \
                       eval("self." + field)
        fields = list(record.keys())      # A list of field indexes
        fields.sort()                     # A SORTED list of field indexes
        output = ""
        for field in fields:              # For each field, in order...
            output += str(record[field])  # ...append to output string
        return output


def fetch(row):
    record = Record()
    [eval("record.{0}".format(field)).load(row)
     for field in dir(record)
     if (not field.startswith("__")) and
        (not callable(getattr(record, field)))]
    return record

def main():
    data = open("sample_data_2015-12-18.dat", "r")
    records = []
    for row in data:
        record = fetch(row)
        records.append(record)

    for record in records:
        print("\n{0}".format(record))
        while True:
            field = input("\nField to change ([ENTER] for next record, QUIT to abort): ")
            if field == "":
                break
            elif field == "QUIT":
                sys.exit()
            else:
                value = input("New value: ")
                if field in dir(record):
                    eval("record.{0}".format(field)).setval(value)
                    print("\n{0}".format(record))
                else:
                    print("'{0}' is not a valid field name".format(field))
    return 0

if __name__ == "__main__":
    main()
