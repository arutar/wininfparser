# wininfparser

INF files parser for python

wininfparser Python module that can open, save, edit Windows INF files (Driver Files)

Full documentation [here](https://arutar.github.io/wininfparser/).

## Install
```Batchfile
pip install wininfparser
```
##### Upgrade
```Batchfile
pip install wininfparser --upgrade
```

## Usage
- #### Open and save inf files

```python
from wininfparser import WinINF, INFsection

InfFile = WinINF()

#Open Intel.inf
InfFile.ParseFile("./Intel.inf")

#Save Intel.inf on th same place
InfFile.Save()
```

- #### Create new inf file

```python
from wininfparser import WinINF, INFsection

InfFile = WinINF()

h="""##########################

 Header data 07/11/2023
 Other data
 Some very important information

##########################"""

# Creates a header and sets an indent of 3 after it 
n=INFsection()
n.SetHeader(h)
n.SetIndent(3)

# Add header to the inf file
InfFile.AddSection(n)

n=INFsection()

# Enable key alignment
# set indent after key 1
# set indent before value 1
# set indent before comment 4
n.SetKeyAutoSize(True,1,1,4)
#
# also n.SetIndents(1,1,4) can be used

#Add key/value/comment data to the section
n.SetName("New_Section")
n.AddData("Path","./somepath")
n.AddData("Version","2.34.57","megatest")
n["TestKey"]="TestValue"
#Add comment
n.AddComment(" some comment")
#Add two empty lines
n.AddComment()
n.AddComment()
#Add comment
n.AddComment(" some comment 2")

#Add section to the end of the inf file
InfFile.AddSection(n)

#Save inf file
InfFile.Save(./new_file.inf)
```
##### Otput:  ./new_file.inf
```dosini
;##########################
;
; Header data 07/11/2023
; Other data
; Some very important information
;
;##########################



[New_Section]
Path    = ./somepath
Version = 2.34.57    ;megatest
TestKey = TestValue
; some comment


; some comment 2
```

- #### Section management
```python
InfFile = WinINF()
InfFile.ParseFile("./Intel.inf")

# print section names
print(InfFile.Sections())

# iterate over sections
for s in InfFile:
    print(s.GetName())

#Find section by name
s=InfFile['Manufacturer']
if s is not None:
    print(s.GetName())

#Sets number of white spaces to the last section
InfFile.Last().SetIndent(3)

#Create new section, and set section name 
n=INFsection()
n.SetName("New_Section")

# Enable key alignment
# set indent after key 1
# set indent before value 1
n.SetKeyAutoSize(True,1,1)

#Add key/value data to the section
n.AddData("Path","./somepath")
n.AddData("Version","2.34.57")
n["TestKey"]="TestValue"

#Add section to the end of the inf file
InfFile.AddSection(n)

#Save Intel.inf on th same place
InfFile.Save()
```

- #### Remove sections

```python
InfFile = WinINF()
InfFile.ParseFile("./Intel.inf")

#Find and remove New_Section
s=InfFile['New_Section']
if s is not None:
    InfFile.RemoveSection(s)

    #Save Intel.inf on th same place
    InfFile.Save()
```


- #### Section content view and search

```python
InfFile = WinINF()
InfFile.ParseFile("./Intel.inf")

# Get "Intel.Mfg" section
s=InfFile['Intel.Mfg']
if s is None:
    print("Error: section not found!")
    sys.exit(-10)

#Get key with index 2
Key=s[2]
print(Key)

# Finds the first key containing "iBKDG" and return its value
Value=s.Find("iBKDG")
print(Value)

# Finds the first key exactly matching "%iBKDG%" and return its value
Value=s["%iBKDG%"]
print(Value)

#Searches for keys that contain "i830M" and returns their values
for k,v,c in s.SearchKeyIter("i830M"):
    print(v)

#Print all section content
for k,v,c in s:
    print(v)
```

### Windows INF File Example
```dosini
;=============================================================================
;
; Copyright (c) Intel Corporation (2002).
;
; INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS
; LICENSED ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT,
; ASSISTANCE, INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT
; PROVIDE ANY UPDATES, ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY
; DISCLAIMS ANY WARRANTY OF MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY
; PARTICULAR PURPOSE, OR ANY OTHER WARRANTY.  Intel disclaims all liability,
; including liability for infringement of any proprietary rights, relating to
; use of the code. No license, express or implied, by estoppel or otherwise,
; to any intellectual property rights is granted herein.
;
;=============================================================================

; Installation inf for the Intel Corporation graphics adapter.

[Version]
Signature="$WINDOWS NT$"
Provider=%Intel%
ClassGUID={4D36E968-E325-11CE-BFC1-08002BE10318}
Class=Display
CatalogFile=i830mnt5.cat

DriverVer=08/20/2004,6.14.10.3889

[DestinationDirs]
DefaultDestDir   = 11
ialm.Miniport  = 12  ; drivers
ialm.Display   = 11  ; system32
Help.Copy = 11
CUI.Copy = 11
Uninstall_Copy = 11

OpenGL.Copy    = 11  ; OpenGL Drivers in System32

;
; Driver information
;

[Manufacturer]
%Intel%   = Intel.Mfg

[Intel.Mfg]
;830
;%i830M% = i830M, PCI\VEN_8086&DEV_3577
%i830M% = i830M, PCI\VEN_8086&DEV_3577&SUBSYS_00C81028
%i830M% = i830M, PCI\VEN_8086&DEV_3577&SUBSYS_01221028
%i830M% = i830M, PCI\VEN_8086&DEV_3577&SUBSYS_00B81028
%i830M% = i830M, PCI\VEN_8086&DEV_3577&SUBSYS_00B91028
%i830M% = i830M, PCI\VEN_8086&DEV_3577&SUBSYS_00F51028

;845
;%iBKDG% = i845G, PCI\VEN_8086&DEV_2562
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_013D1028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01471028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_03011028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_013A1028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01481028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01381028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01261028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01271028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01331028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_014B1028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01601028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01611028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01291028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_01461028
%iBKDG% = i845G, PCI\VEN_8086&DEV_2562&SUBSYS_03031028

;845GM
%iBKDGM% = i845GM, PCI\VEN_8086&DEV_2562&SUBSYS_01491028
```
