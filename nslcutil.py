#!/usr/bin/python
# -*- coding: utf-8 -*-
#

# Boilerplate inports for Python 2 / Python 3 mutual compatiibility
#
from __future__ import print_function  # Make print a function
from six.moves  import input           # Use raw_input when I say input
from os.path    import expanduser      # Cross-platform home directory finder

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
# a 1250 print("hello world")  # uncomment line 7 to make your life a
# living hell..character line.
#
# Read a CSV file with many rows, and 110 columns.
#
#     # Each row represents a student.
#     # Each column represents parameter from the
#       9-4-14_New_EnrollRept_ProgrammingandTestingGuide.pdf.
#     # http://www.studentclearinghouse.org/colleges/files/EnrollRept_ProgrammingandTestingGuide.pdf#page=15
#         * The constraints of this guideance are included in the class
#           "drl" (detailed record length).
#         * The goal is to use this class to operate on the 1250 byte list.
#         * CSV Data from the input is identified and punched into the
#           list at appropriate spacing
#     # Examples:
#         * >> print(drl.RecordType) .
#         * >> [2, 1, 2, "R", "AN"] .
#         * >> print(drl.StudentSSN) .
#         * >> [9, 3, 11, "R", "N"] .
#         * >> print(drl.FirstName) .
#         * >> [20, 12, 31, "R", "AN"] .
#
# Set up an object called drl and populate this with spreadsheet data
# this data is a direct copy of the publication data from page 15.
#
# Load landers
# Column for Excel Format Index
length    = 0
start     = 1
stop      = 2
reqd      = 3
type      = 4
fieldname = 6
#
#
# Variable List
#
# Column for Excel FormatIndex =
# ["Length", "Start", "Stop", "Reqd", "Type", "Field Name"]
A1    = [  "2",   "1",   "2", "R", "AN", "A", "Record Type"]
B2    = [  "9",   "3",   "11", "R", "N",  "B", "Student SSN"]
C3    = [ "20",  "12",   "31", "R", "AN", "C", "First Name"]
D4    = [  "1",  "32",   "32", "O", "AN", "D", "Middle Initial"]
E5    = [ "20",  "33",   "52", "R", "AN", "E", "Last Name"]
F6    = [  "5",  "53",   "57", "O", "AN", "F", "Name Suffix"]
G7    = [  "9",  "58",   "66", "O", "N",  "G", "Previous SSN"]
H8    = [ "20",  "67",   "86", "O", "AN", "H", "Previous Last Name"]
I9    = [  "1",  "87",   "87", "R", "A",  "I", "Degree Concentration"]
J10   = [  "8",  "88",   "95", "C", "N",  "J", "Enrollment Status"]
K11   = [ "30",  "96",  "125", "R", "AN", "K", "Status Start Date"]
L12   = [ "30", "126",  "155", "O", "AN", "L", "Street Line 1"]
M13   = [ "20", "156",  "175", "R", "A",  "M", "Street Line 2"]
N14   = [  "2", "176",  "177", "R", "A",  "N", "City"]
O15   = [  "9", "178",  "186", "C", "AN", "O", "State"]
P16   = [ "15", "187",  "201", "C", "AN", "P", "Zip"]
Q17   = [  "8", "202",  "209", "C", "N",  "Q", "Country"]
R18   = [  "8", "210",  "217", "R", "N",  "R", "Anticipated Graduation Date"]
S19   = [  "8", "218",  "225", "R", "N",  "S", "Date of Birth"]
T20   = [  "8", "226",  "233", "R", "N",  "T", "Term Begin Date"]
U21   = [  "1", "234",  "234", "R", "AN", "U", "Term End Date"]
V22   = [  "1", "235",  "235", "R", "A",  "V", "Filler"]
W23   = [  "6", "236",  "241", "O", "N",  "W", "Directory Block Indicator"]
X24   = [  "6", "242",  "247", "O", "N",  "X", "NCES CIP Code for Major 1"]
Y25   = [ "80", "248",  "327", "O", "AN", "Y", "NCES CIP Code for Major 2"]
Z26   = [ "80", "328",  "407", "O", "AN", "Z", "Major Course of Study 1"]
AA27  = [  "1", "408",  "408", "C", "A",  "AA", "Major Course of Study 2"]
AB28  = [  "1", "409",  "409", "O", "A",  "AB", "Class/ Credential"]
AC29  = [  "1", "410",  "410", "O", "A",  "AC", "First Time Full Time"]
AD30  = [  "6", "411",  "416", "O", "N",  "AD", "Degree Seeking"]
AE31  = [  "1", "417",  "417", "O", "A",  "AE", "High School Code"]
AF32  = [  "2", "418",  "419", "O", "A",  "AF", "Gender"]
AG33  = [ "20", "420",  "439", "O", "AN", "AG", "Race/ Ethnicity"]
AH34  = [ "30", "440",  "469", "O", "AN", "AH", "College Student ID"]
AI35  = ["128", "470",  "597", "O", "AN", "AI", "State Student ID"]
AJ36  = [  "1", "598",  "598", "O", "A",  "AJ", "Email"]
AK37  = [ "37", "35", "599", "633", "O", "AN", "Good Student"]
AL38  = [  "1", "634",  "634", "O", "A",  "AL", "Middle Name"]
AM39  = [ "12", "635",  "646", "O", "AN", "AM", "Veteran's Status Indicator"]
AN40  = [  "1", "647",  "647", "O", "A",  "AN", "Reserved for CommIT ID"]
AO41  = [  "1", "648",  "648", "O", "A",  "AO", "Pell Grant Recipient Flag"]
AP42  = [  "1", "649",  "649", "O", "A",  "AP", "Remedial Flag"]
AQ43  = [  "1", "650",  "650", "O", "A",  "AQ", "Citizenship Flag"]
AR44  = [  "1", "651",  "651", "O", "A",  "AR", "Student Phone Type"]
AS45  = [  "3", "652",  "654", "O", "N",  "AS", "Preferred Phone Number Flag"]
AT46  = [ "11", "655",  "665", "O", "N",  "AT", "Student Phone Country Code"]
AU47  = [  "8", "666",  "673", "O", "N",  "AU", "Student Phone Number"]
AV48  = [  "1", "674",  "674", "R", "A",  "AV", "Reserved for Move To OPEID Future CH Functionality"]
AW49  = [  "6", "675",  "680", "C", "N",  "AW", "Program Indicator"]
AX50  = [  "4", "681",  "684", "C", "N",  "AX", "Program 1 CIP Code"]
AY51  = [  "2", "685",  "686", "C", "N",  "AY", "Program 1 CIP Year"]
AZ52  = [  "6", "687",  "692", "C", "N",  "AZ", "Program 1 Credential Level"]
BA53  = [  "1", "693",  "693", "C", "A",  "BA", "Published Program 1 Length"]
BB54  = [  "6", "694",  "699", "C", "N",  "BB", "Published Program 1 Length Measurement"]
BC55  = [  "8", "700",  "707", "C", "N",  "BC", "Weeks Program 1 Title IV Academic Year"]
BD56  = [  "1", "708",  "708", "C", "A",  "BD", "Program 1 Begin Date"]
BE57  = [  "1", "709",  "709", "C", "A",  "BE", "Program 1 Special Program Indicator"]
BF58  = [  "8", "710",  "717", "C", "N",  "BF", "Program 1 Enrollment Status"]
BG59  = [  "6", "718",  "723", "O", "N",  "BG", "Program 1 Enrollment Status Effective Date"]
BH60  = [  "4", "724",  "727", "C", "N",  "BH", "Program 2 CIP Code"]
BI61  = [  "2", "728",  "729", "C", "N",  "BI", "Program 2 CIP Year"]
BJ62  = [  "6", "730",  "735", "C", "N",  "BJ", "Program 2 Credential Level"]
BK63  = [  "1", "736",  "736", "C", "A",  "BK", "Published Program 2 Length"]
BL64  = [  "6", "737",  "742", "C", "N",  "BL", "Published Program 2 Length Measurement"]
BM65  = [  "8", "743",  "750", "C", "N",  "BM", "Weeks Program 2 Title IV Academic Year"]
BN66  = [  "1", "751",  "751", "C", "A",  "BN", "Program 2 Begin Date"]
BO67  = [  "1", "752",  "752", "C", "A",  "BO", "Program 2 Special Program Indicator"]
BP68  = [  "8", "753",  "760", "C", "N",  "BP", "Program 2 Enrollment Status"]
BQ69  = [  "6", "761",  "766", "O", "N",  "BQ", "Program 2 Enrollment Status Effective Date"]
BR70  = [  "4", "767",  "770", "C", "N",  "BR", "Program 3 CIP Code"]
BS71  = [  "2", "771",  "772", "C", "N",  "BS", "Program 3 CIP Year"]
BT72  = [  "6", "773",  "778", "C", "N",  "BT", "Program 3 Credential Level"]
BU73  = [  "1", "779",  "779", "C", "A",  "BU", "Published Program 3 Length"]
BV74  = [  "6", "780",  "785", "C", "N",  "BV", "Published Program 3 Length Measurement"]
BW75  = [  "8", "786",  "793", "C", "N",  "BW", "Weeks Program 3 Title IV Academic Year"]
BX76  = [  "1", "794",  "794", "C", "A",  "BX", "Program 3 Begin Date"]
BY77  = [  "1", "795",  "795", "C", "A",  "BY", "Program 3 Special Program Indicator"]
BZ78  = [  "8", "796",  "803", "C", "N",  "BZ", "Program 3 Enrollment Status"]
CA79  = [  "6", "804",  "809", "O", "N",  "CA", "Program 3 Enrollment Status Effective Date"]
CB80  = [  "4", "810",  "813", "C", "N",  "CB", "Program 4 CIP Code"]
CC81  = [  "2", "814",  "815", "C", "N",  "CC", "Program 4 CIP Year"]
CD82  = [  "6", "816",  "821", "C", "N",  "CD", "Program 4 Credential Level"]
CE83  = [  "1", "822",  "822", "C", "A",  "CE", "Published Program 4 Length"]
CF84  = [  "6", "823",  "828", "C", "N",  "CF", "Published Program 4 Length Measurement"]
CG85  = [  "8", "829",  "836", "C", "N",  "CG", "Weeks Program 4 Title IV Academic Year"]
CH86  = [  "1", "837",  "837", "C", "A",  "CH", "Program 4 Begin Date"]
CI87  = [  "1", "838",  "838", "C", "A",  "CI", "Program 4 Special Program Indicator"]
CJ88  = [  "8", "839",  "846", "C", "N",  "CJ", "Program 4 Enrollment Status"]
CK89  = [  "6", "847",  "852", "O", "N",  "CK", "Program 4 Enrollment Status Effective Date"]
CL90  = [  "4", "853",  "856", "C", "N",  "CL", "Program 5 CIP Code"]
CM91  = [  "2", "857",  "858", "C", "N",  "CM", "Program 5 CIP Year"]
CN92  = [  "6", "859",  "864", "C", "N",  "CN", "Program 5 Credential Level"]
CO93  = [  "1", "865",  "865", "C", "A",  "CO", "Published Program 5 Length"]
CP94  = [  "6", "866",  "871", "C", "N",  "CP", "Published Program 5 Length Measurement"]
CQ95  = [  "8", "872",  "879", "C", "N",  "CQ", "Weeks Program 5 Title IV Academic Year"]
CR96  = [  "1", "880",  "880", "C", "A",  "CR", "Program 5 Begin Date"]
CS97  = [  "1", "881",  "881", "C", "A",  "CS", "Program 5 Special Program Indicator"]
CT98  = [  "8", "882",  "889", "C", "N",  "CT", "Program 5 Enrollment Status"]
CU99  = [  "6", "890",  "895", "O", "N",  "CU", "Program 5 Enrollment Status Effective Date"]
CV100 = [  "4", "896",  "899", "C", "N",  "CV", "Program 6 CIP Code"]
CW101 = [  "2", "900",  "901", "C", "N",  "CW", "Program 6 CIP Year"]
CX102 = [  "6", "902",  "907", "C", "N",  "CX", "Program 6 Credential Level"]
CY103 = [  "1", "908",  "908", "C", "A",  "CY", "Published Program 6 Length"]
CZ104 = [  "6", "909",  "914", "C", "N",  "CZ", "Published Program 6 Length Measurement"]
DA105 = [  "8", "915",  "922", "C", "N",  "DA", "Weeks Program 6 Title IV Academic Year"]
DB106 = [  "1", "923",  "923", "C", "A",  "DB", "Program 6 Begin Date"]
DC107 = [  "1", "924",  "924", "C", "A",  "DC", "Program 6 Special Program Indicator"]
DD108 = [  "8", "925",  "932", "C", "N",  "DD", "Program 6 Enrollment Status"]
DE109 = ["318", "933", "1250", "R", "AN", "DE", "Program 6 Enrollment Status Effective Date"]
#
print(DE109)
print(DE109[6])
print(DE109[fieldname])
#
print("Start " + __appname__)  # uncomment line 7 to make your life a living hell...
outstr = 1250 * " "
print(outstr)
print(len(outstr))
outlist = list(outstr)                          # change this into a list
#
inlist = list("hello world")                    # change data into a list element
outlist[10:19] = inlist                         # place data in the list in the correct place
print("".join(outlist))                         # see result


def iloop():
    """ Loop through the input variables for whatever reason you want"""
    x = [    "A1",    "B2",    "C3",    "D4",    "E5",    "F6",    "G7",
             "H8",    "I9",   "J10",   "K11",   "L12",   "M13",   "N14",
            "O15",   "P16",   "Q17",   "R18",   "S19",   "T20",   "U21",
            "V22",   "W23",   "X24",   "Y25",   "Z26",  "AA27",  "AB28",
           "AC29",  "AD30",  "AE31",  "AF32",  "AG33",  "AH34",  "AI35",
           "AJ36",  "AK37",  "AL38",  "AM39",  "AN40",  "AO41",  "AP42",
           "AQ43",  "AR44",  "AS45",  "AT46",  "AU47",  "AV48",  "AW49",
           "AX50",  "AY51",  "AZ52",  "BA53",  "BB54",  "BC55",  "BD56",
           "BE57",  "BF58",  "BG59",  "BH60",  "BI61",  "BJ62",  "BK63",
           "BL64",  "BM65",  "BN66",  "BO67",  "BP68",  "BQ69",  "BR70",
           "BS71",  "BT72",  "BU73",  "BV74",  "BW75",  "BX76",  "BY77",
           "BZ78",  "CA79",  "CB80",  "CC81",  "CD82",  "CE83",  "CF84",
           "CG85",  "CH86",  "CI87",  "CJ88",  "CK89",  "CL90",  "CM91",
           "CN92",  "CO93",  "CP94",  "CQ95",  "CR96",  "CS97",  "CT98",
           "CU99", "CV100", "CW101", "CX102", "CY103", "CZ104", "DA105",
          "DB106", "DC107", "DD108", "DE109"]

    for i in range(len(x)):
        print(x[i])
        # return x[i]
