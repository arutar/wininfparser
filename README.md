# wininfparser v1.0

INF files parser for python

wininfparser Python module that can open, save, edit Windows INF files (Driver Files)

Full documentation [here](https://arutar.github.io/wininfparser/).



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
