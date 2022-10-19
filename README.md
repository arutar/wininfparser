# wininfparser

wininfparser Python module that can open, save, edit Windows INF files (Driver Files) 

## Usage
opening an inf file, viewing the list of sections, viewing the contents of a section

```python
from wininfparser import WinINF, INFsection

InfFile = WinINF()
InfFile.ParseFile("с:\\path_to_inf\\Intel.inf")

print(InfFile.Sections())
#
#dict_keys(['Version', 'DestinationDirs', 'Manufacturer', 'Intel.Mfg'])

VersionSection=InfFile["Version"]

VersionSection.Info()
#[Version]
#Signature = "$WINDOWS NT$"
# Provider = %Intel%
# ClassGUID = {4D36E968-E325-11CE-BFC1-08002BE10318}
# Class = Display
# CatalogFile = i830mnt5.cat
# 
#DriverVer = 08/20/2004,6.14.10.3889

##
# k - key 
# v - value 
# c - comment
for k,v,c in VersionSection:
    print("Key: ", k, " Value: ", v)
 
#Key: Signature  Value: "$WINDOWS NT$"
#Key: Provider  Value: %Intel%
#Key: ClassGUID  Value: {4D36E968-E325-11CE-BFC1-08002BE10318}
#Key: Class  Value: Display
#Key: CatalogFile  Value: i830mnt5.cat
#Key:   Value: Key: DriverVer  Value: 08/20/2004,6.14.10.3889
#

VersionSection['ClassGUID']
#{4D36E968-E325-11CE-BFC1-08002BE10318}
```
