## @package wininfparser
#  @author Arsen Arutyunyan arutar@bk.ru 2022
#  wininfparser - module for working with Windows INF files
#
#  wininfparser - module that can create, open, save, edit Windows INF files (Driver Files).
#  It easy to understand and use
#
import re
import sys

## @mainpage
#  Main Classes
#  =================================================
#  - \ref wininfparser.INFsection "INFsection"
#  - \ref wininfparser.WinINF "WinINF"
#
#  List of basic functions for working with wininfparser
#  =================================================
#  Save, Open INF Files
#  -------------------------------
#  - \ref wininfparser.WinINF.ParseFile "WinINF.ParseFile"
#  - \ref wininfparser.WinINF.Save "WinINF.Save"
#
#  WinINF Class
#  =================================================
#  - \ref wininfparser.WinINF.AddSection "WinINF.AddSection"
#  - \ref wininfparser.WinINF.RemoveSection "WinINF.RemoveSection"
#  - \ref wininfparser.WinINF.GetSection "WinINF.GetSection"
#  - \ref wininfparser.WinINF.__getitem__ "WinINF.operator[]"
#  - \ref wininfparser.WinINF.__next__ "WinINF.__next__"
#  - \ref wininfparser.WinINF.__iter__ "WinINF.__iter__"
#
#  INFsection Class
#  =================================================
#  - \ref wininfparser.INFsection.__getitem__ "operator[]"
#  - \ref wininfparser.INFsection.GetKeyIndex "GetKeyIndex"
#  - \ref wininfparser.INFsection.FindKey "FindKey"
#  - \ref wininfparser.INFsection.__next__ "__next__"
#  - \ref wininfparser.INFsection.Next "Next"
#  - \ref wininfparser.INFsection.Previous "Previous"
#  - \ref wininfparser.INFsection.AddData "AddData"
#  - \ref wininfparser.INFsection.AddDataP "AddDataP"
#  - \ref wininfparser.INFsection.FindKey "FindKey"
#  - \ref wininfparser.INFsection.FindValueIndex "FindValueIndex"
#  - \ref wininfparser.INFsection.FindValue "FindValue"
#  - \ref wininfparser.INFsection.FindKey "FindKey"


## Can return values, keys, and section comments of INF files.
#  Allows you to navigate through the contents of a section. Able to add and remove values.
#  Can search for keys and values within a section
#  variable       |  description                                        |  Value       |
#  -------------  |---------------------------                          |------------- |
#  comment        |typicali header section with \n comments ony content |    1         |
#  single_line    |section that contains only \n values                 |    2         |
#  key_pair       |section that contains key \n value pairs             |    3         |
#
class INFsection:
    comment=1
    single_line=2
    key_pair=3

    ## Default constructor
    def __init__(self):
        self.__Name=''
        self.__NameComment=''
        self.__Valid=False
        self.__KeyList=[]
        self.__ValueList=[]
        self.__Comments=[]
        self.__NextSection=None
        self.__PreviousSection=None
        self.__Indent=0
        self.__EmptyCount = 0
        self.__CurrentIndex = None
        self.__Type=None

    ## Lets go through the section content!
    #  @return INFsection
    def __iter__(self):
        self.__CurrentIndex=None
        return self

    ## Lets go through the section content!
    #  returns k - key
    #  returns v - value
    #  returns c - comment
    #  \code{.py}
    #  for k,v,c in VersionSection:
    #      print("Key:{0:12}".format(k), " Value:", v, " Comment:", c)
    #  \endcode
    #  @return str,str,str
    def __next__(self):
        if self.__CurrentIndex is not None:
            if len(self.__KeyList) >  self.__CurrentIndex+1:
                self.__CurrentIndex+=1
                if len(self.__ValueList):
                    return self.__KeyList[self.__CurrentIndex],self.__ValueList[self.__CurrentIndex],self.__Comments[self.__CurrentIndex]
                else:
                    return self.__KeyList[self.__CurrentIndex],"",self.__Comments[self.__CurrentIndex]
            else:
                self.__CurrentIndex=None
                raise StopIteration
        else:
            if not len(self.__KeyList):
                raise StopIteration
            else:
                self.__CurrentIndex = 0
                if len(self.__ValueList):
                    return self.__KeyList[self.__CurrentIndex],self.__ValueList[self.__CurrentIndex],self.__Comments[self.__CurrentIndex]
                else:
                    return self.__KeyList[self.__CurrentIndex],"",self.__Comments[self.__CurrentIndex]

    ## Returns next Section
    #  @return INFsection
    def Next(self):
        return self.__NextSection

    ## Sets next Section
    #  @param n (INFsection) must be Invalid
    def SetNext(self, n):
        if n is not None:
            n.__PreviousSection=self
        self.__NextSection=n

    ## Sets previous Section
    #  @param p (INFsection) must be Invalid
    def SetPrevious(self, p):
        if p is not None:
            p.__NextSection=self
        self.__PreviousSection=p

    ## Checks if a section can be added to an inf file
    #  @return bool
    def CheckSection(self):
        if not self.__Name.rstrip() and not len(self.__KeyList):
            return False
        else:
            return True

    ## Returns previous Section
    #  @return INFsection
    def Previous(self):
        self.__PreviousSection

    ## Sets sction type must be INFsection.comment or INFsection.single_line or INFsection.key_pair
    def SetType(self,t):
        self.__Type=t

    ## Returns Section type
    #  @return int (INFsection.comment or INFsection.single_line or INFsection.key_pair)
    def GetType(self):
        return self.__Type

    ## Sets indent after section
    #  @param i (int)
    def SetIndent(self,i: int):
        self.__Indent=i

    ## returns indent after section
    #  @return int
    def GetIndent(self):
        return self.__Indent

    ## Sets section name
    #  @param NewName (str)
    def SetName(self,NewName):
        self.__Name=NewName

    ## Sets comment to section name
    #  @param NewNameComment (str)
    def SetNameComment(self,NewNameComment):
        self.__NameComment=NewNameComment

    ## returns section name
    #  @param NewName (str)
    def GetName(self):
        return self.__Name

    ## Sets section to valid state
    def SetValid(self):
        if not self.CheckSection():
            return

        if not self.__Name:
            self.__Type=INFsection.comment
        elif len(self.__ValueList):
            self.__Type = INFsection.key_pair
        else:
            self.__Type = INFsection.single_line

        self.__Valid=True

    ## Checks if section valid
    #  @return bool
    def IsValid(self):
        return self.__Valid

    ## Function required for parser
    #  inserts empty laines
    def AddEmptyStrings(self):
        for i in range(self.__Indent-1):
            self.__KeyList.append('')
            if len(self.__ValueList):
                self.__ValueList.append('')
            self.__Comments.append('')

        self.__Indent = 0

    ## Adds k,v,c paramentrs to the end of the section
    #  @param k key (str)
    #  @param v value (str)
    #  @param c comment (str)
    def AddData(self,k,v=None,c=None):
        if not self.__Valid:
            self.AddEmptyStrings()

        self.__KeyList.append(k)

        if v is not None:
            if self.__EmptyCount:
                self.__ValueList=['' for i in range(self.__EmptyCount)]
                self.__EmptyCount=0
            self.__ValueList.append(v)
        elif len(self.__ValueList) and v is None:
            self.__ValueList.append('')

        if c is not None:
            self.__Comments.append(c)
        else:
            self.__Comments.append('')

    ## Adds comment to the end of the section
    #  @param c (str)
    def AddComment(self,c=None):
        if not len(self.__ValueList):
            self.__EmptyCount+=1

        if c is not None and ";" in c:
            self.AddEmptyStrings()

            self.__KeyList.append('')
            if len(self.__ValueList):
                self.__ValueList.append('')
            self.__Comments.append(c)

        else:
            self.__Indent+=1

    ## Adds k,v,c parameters to the selected position of the section
    #  @param pos position (int)
    #  @param k key (str)
    #  @param v value (str)
    #  @param c comment (str)
    def AddDataP(self,pos: int,k,v=None,c=None):
        if len(self.__KeyList) < pos or pos < 0:
            self.AddData(k,v,c)
            return
        else:
            if not self.__Valid:
                self.AddEmptyStrings()

            self.__KeyList.insert(pos,k)

            if v is not None:
                if self.__EmptyCount:
                    self.__ValueList = ['' for i in range(self.__EmptyCount)]
                    self.__EmptyCount = 0
                self.__ValueList.insert(pos,v)
            elif len(self.__ValueList) and v is None:
                self.__ValueList.insert(pos,'')

            if c is not None:
                self.__Comments.insert(pos,c)
            else:
                self.__Comments.insert(pos,'')


    ## Removes first matched key of the section
    #  @param k key (str)
    def RemoveKey(self, k):
        try:
            CurrentIndex=self.__KeyList.index(k)

            self.__KeyList.pop(CurrentIndex)
            self.__Comments.pop(CurrentIndex)
            if len(self.__ValueList):
                self.__ValueList.pop(CurrentIndex)
        except:
            pass

    ## Removes first matched value of the section
    #  @param v value (str)
    def RemoveValue(self, v):
        try:
            CurrentIndex = self.__ValueList.index(v)

            self.__KeyList.pop(CurrentIndex)
            self.__ValueList.pop(CurrentIndex)
            self.__Comments.pop(CurrentIndex)
        except:
            pass

    ## Removes first matched comment of the section
    #  @param c comment (str)
    def RemoveComment(self, c):
        try:
            CurrentIndex = self.__Comments.index(c)

            self.__Comments[CurrentIndex]=""
        except:
            pass

    ## Returns key with selected index
    #  @param Index (int)
    #  @return str
    def __getitem__(self, Index: int):
        return self.__KeyList[Index]

    ## Returns key with selected key
    #  @param k (str)
    #  @return str
    def __getitem__(self, k: str):
        KeyInd=self.GetKeyIndex(k)
        if len(self.__ValueList):
            return self.__ValueList[KeyInd]
        else:
            return self.FindValue(k)

    ## Sets key value pair
    #  @param k (str)
    #  @param v (str)
    def __setitem__(self,k,v):
        i=self.GetKeyIndex(k)
        if i < 0:
            if len(self.__KeyList):
                if len(self.__ValueList):
                    self.__ValueList.append(v)
            else:
                self.__ValueList.append(v)
            self.__KeyList.append(k)
            self.__Comments.append("")

        else:
            if len(self.__ValueList):
                self.__KeyList[i]=v


    def GetKeyIndex(self,k,p=0):
        for CurrentIndex, key in enumerate(self.__KeyList):
            if CurrentIndex>=p and k in key:
                return CurrentIndex
        return -1

    def FindKey(self,k,p=0):
        for CurrentIndex, key in enumerate(self.__KeyList):
            if CurrentIndex>=p and k in key:
                return key
        return ""

    def FindValueIndex(self,v,p=0):
        for CurrentIndex, val in enumerate(self.__ValueList):
            if CurrentIndex>=p and v in val:
                return CurrentIndex
        return -1

    def FindValue(self,v,p=0):
        for CurrentIndex, val in enumerate(self.__ValueList):
            if CurrentIndex>=p and v in val:
                return val
        return ""

    def GetValue(self,Index):
        return self.__ValueList[Index]

    def Info(self):
        if self.__Name != "":
            print("[{0}]{1}".format(self.__Name,self.__NameComment))

        if len(self.__ValueList):
            for CurrentIndex, key in enumerate(self.__KeyList):
                if key:
                    print(key, "=", self.__ValueList[CurrentIndex],self.__Comments[CurrentIndex])
                else:
                    print(self.__Comments[CurrentIndex])
        else:
            for CurrentIndex, key in enumerate(self.__KeyList):
                if key:
                    print(key,self.__Comments[CurrentIndex])
                else:
                    print(self.__Comments[CurrentIndex])

        for i in range(self.__Indent-1):
            print("")

    def Save(self):
        Returner=""
        if self.__Name != "":
            Returner="[{0}]{1}\n".format(self.__Name,self.__NameComment)

        if len(self.__ValueList):
            for CurrentIndex, key in enumerate(self.__KeyList):
                if key:
                    Returner += (key + "=" + self.__ValueList[CurrentIndex] + self.__Comments[CurrentIndex] + "\n")
                else:
                    Returner += (self.__Comments[CurrentIndex] + "\n")
        else:
            for CurrentIndex, key in enumerate(self.__KeyList):
                if key:
                    Returner += (key + self.__Comments[CurrentIndex] + "\n")
                else:
                    Returner += (self.__Comments[CurrentIndex] + "\n")

        for i in range(self.__Indent-1):
            Returner+="\n"

        return Returner



## Class WinINF - Can open INF files, allows you to get a section by its name,
#  can save INF files, and allows you to walk through all sections of a file
#
class WinINF:
    ## Default constructor
    def __init__(self):
        self.__FileName=""
        self.__Head=None
        self.__Tail=None
        self.__Current=None
        self.__ItemCount=0
        self.__SectionsDict={}

    ## Lets go through the sections!
    #  @return WinINF
    def __iter__(self):
        self.__Current=None
        return self

    ## Lets go through the sections!
    #  @return INFsection
    def __next__(self):
        if self.__Current is not None:
            if self.__Current.Next() is not None:
                self.__Current=self.__Current.Next()
                return self.__Current
            else:
                self.__Current=None
                raise StopIteration
        else:
            if self.__Head is None:
                raise StopIteration
            else:
                self.__Current = self.__Head
                return self.__Current

    ## Returns section names.
    #  @return list
    def Sections(self):
        return self.__SectionsDict.keys()

    ## Returns file name.
    #  @return str
    def GetFileName(self):
        return self.__FileName

    ## Returns section count/
    #  @return int
    def Count(self):
        return self.__ItemCount

    ## Returns section by name. If section not present None returned.
    #  `InfFile['Name']`
    #  @param k (str)
    #  @return INFsection
    def __getitem__(self, k: str):
        return self.GetSection(k)

    ## Returns section by name. If section not present None returned.
    #  @param Name (str)
    #  @return INFsection
    def GetSection(self,Name):
        return self.__SectionsDict.get(Name)

    ## Adds section
    #  @param Section (INFsection)
    def AddSection(self, Section: INFsection):
        if Section.IsValid():
            print("Yo can add only invalid sections!")
            return
        if not Section.CheckSection():
            print("Error: Can't add emty section!")
            return

        Section.SetValid()

        if self.__Head is None:
            self.__Head = Section
            self.__Tail = Section
        else:
            self.__Tail.SetNext(Section)
            self.__Tail = Section

        if Section.GetName().rstrip():
            self.__SectionsDict[Section.GetName()] = Section
        self.__ItemCount += 1

    ## Removes selected section!
    #  @param Section (INFsection)
    def RemoveSection(self, Section: INFsection):
        if not Section.IsValid():
            return

        p=Section.Previous()
        n=Section.Next()

        if p is not None:
            if n is not None:
                p.SetNext(n)
            else:
                p.SetNext(None)
                self.__Tail=p
        else:
            if n is not None:
                n.SetPrevious(None)
                self.__Head = n
            else:
                self.__Tail = p
                self.__Head = n

    ## Opens INF file.
    #  If Name Full faile path to inf file
    #  @param Name (str)
    def ParseFile(self,Name):
        self.__Head=None
        self.__Tail=None
        self.__Current=None
        self.__ItemCount=0
        self.__SectionsDict = {}

        self.__FileName=Name
        f=open(Name)

        SepRE=re.compile('[^";=]*("|;|=)?')
        KeyRE = re.compile('[^"]*(")')
        ValueRE = re.compile('[^";=]*("|;)?')

        EmptyRE = re.compile('\\s*$')
        CommentRE = re.compile("\\s*(;.*)?$")
        SectRE = re.compile(" *\\[([^]]*)\\](\\s*;.*)?")

        for line in f:
            line = line.rstrip()
            if line == "" or EmptyRE.match(line) is not None:
                if self.__Tail is not None:
                    self.__Tail.AddComment()
                else:
                    continue

            ms = CommentRE.match(line)
            if ms is not None:
                if self.__Head is None:
                    NewSection = INFsection()
                    NewSection.AddComment(line)
                    self.__Head=NewSection
                    self.__Tail=NewSection
                    self.__ItemCount += 1
                else:
                    self.__Tail.AddComment(line)

                continue

            ms = SectRE.match(line)
            if ms is not None:
                NewSection=INFsection()
                NewSection.SetName(ms.group(1).lstrip().rstrip())

                if ms.group(2) is not None:
                    NewSection.SetNameComment(ms.group(2))

                if self.__Head is None:
                    self.__Head=NewSection
                    self.__Tail=NewSection
                else:
                    self.__Tail.SetNext(NewSection)
                    self.__Tail.SetValid()
                    self.__Tail=NewSection

                self.__SectionsDict[NewSection.GetName()]=NewSection
                self.__ItemCount+=1
                continue

            SeparatorRE = SepRE
            p=0
            fv=False
            f_open=False
            k=""
            v=""
            c=""
            while p != len(line):
                ma = SeparatorRE.match(line,pos=p)
                if ma is None:
                    if v:
                        v += line[p:]
                    else:
                        k += line[p:]
                    p=len(line)
                    continue

                if ma.group(1) is None:
                    if not fv:
                        k+=ma.group(0)
                        p = ma.span()[1]
                    else:
                        v+=ma.group(0)
                        p = ma.span()[1]
                else:
                    if not fv:
                        if ma.group(0)[-1] != '"':
                            k+=ma.group(0)[:-1]

                            if ma.group(0)[-1] == "=":
                                fv=True
                                SeparatorRE=ValueRE
                            else:
                                c=line[ma.span()[1]-1:]
                                p=len(line)
                                continue
                        else:
                            k += ma.group(0)
                            if f_open:
                                f_open=False;
                                SeparatorRE=SepRE
                            else:
                                f_open = True;
                                SeparatorRE = KeyRE
                        p = ma.span()[1]
                    else:
                        if ma.group(0)[-1] != '"':
                            v+=ma.group(0)[:-1]

                            c = line[ma.span()[1] - 1:]
                            p = len(line)

                            continue
                        else:
                            v += ma.group(0)
                            if f_open:
                                f_open=False;
                                SeparatorRE=ValueRE
                            else:
                                f_open = True;
                                SeparatorRE = KeyRE
                        p = ma.span()[1]

            if self.__Tail is not None:
                if v:
                    self.__Tail.AddData(k,v,c)
                else:
                    self.__Tail.AddData(k, None, c)

        if self.__Tail is not None:
            self.__Tail.SetValid()
        f.close()

    ## Saves INF file.
    #  If Name argument is None, then data saved to current file and overwrite information on it
    #  @param Name (str)
    def Save(self, Name=None):
        if Name is not None:
            self.__FileName=Name

        if self.__Head is None:
            return

        f=open(self.__FileName,"w")

        for Current in self:
            f.write(Current.Save())

        f.close()







