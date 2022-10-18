###############################################################################
###### Windows INF file parser Version 1.0
###### by Arsen Arutyunyan arutar@bk.ru 2022
###### Python module that can open, save, edit Windows INF files (Driver Files)
###############################################################################

import re
import sys

class INFsection:
    comment=1
    single_line=2
    key_pair=3

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


    def __iter__(self):
        self.__CurrentIndex=None
        return self

    def __next__(self):
        if self.__CurrentIndex is not None:
            if len(self.__KeyList) <  self.__CurrentIndex+1:
                self.__CurrentIndex+=1
                if len(self.__ValueList):
                    return self.__KeyList[self.__CurrentIndex],self.__ValueList[self.__CurrentIndex],self.__Comments[self.__CurrentIndex]
                else:
                    return self.__KeyList[self.__CurrentIndex],"",self.__Comments[self.__CurrentIndex]
            else:
                self.__CurrentIndex=None
                raise StopIteration
        else:
            if self.Head is None:
                raise StopIteration
            else:
                self.__CurrentIndex = 0
                if len(self.__ValueList):
                    return self.__KeyList[self.__CurrentIndex],self.__ValueList[self.__CurrentIndex],self.__Comments[self.__CurrentIndex]
                else:
                    return self.__KeyList[self.__CurrentIndex],"",self.__Comments[self.__CurrentIndex]

    def Next(self):
        return self.__NextSection

    def SetNext(self, n):
        if n is not None:
            n.__PreviousSection=self
        self.__NextSection=n

    def SetPrevious(self, p):
        if p is not None:
            p.__NextSection=self
        self.__PreviousSection=p

    def CheckSection(self):
        if not self.__Name.rstrip() and not len(self.__KeyList):
            return False
        else:
            return True

    def Previous(self):
        self.__PreviousSection

    def SetType(self,t):
        self.__Type=t

    def GetType(self):
        return self.__Type

    def SetIndent(self,i: int):
        self.__Indent=i

    def GetIndent(self):
        return self.__Indent

    def SetName(self,NewName):
        self.__Name=NewName

    def SetNameComment(self,NewNameComment):
        self.__NameComment=NewNameComment

    def GetName(self):
        return self.__Name

    def SetValid(self):
        if not self.CheckSection():
            return

        if not self.__Name.rstrip():
            self.__Type=INFsection.comment
        elif len(self.__ValueList):
            self.__Type = INFsection.key_pair
        else:
            self.__Type = INFsection.single_line

        self.__Valid=True

    def IsValid(self):
        return self.__Valid

    def GetNext(self):
        return self.__NextSection

    def GetPrevious(self):
        return self.__PreviousSection

    def AddEmptyStrings(self):
        for i in range(self.__Indent-1):
            self.__KeyList.append('')
            if len(self.__ValueList):
                self.__ValueList.append('')
            self.__Comments.append('\n')

        self.__Indent = 0

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


    def RemoveKey(self, k):
        try:
            CurrentIndex=self.__KeyList.index(k)

            self.__KeyList.pop(CurrentIndex)
            self.__Comments.pop(CurrentIndex)
            if len(self.__ValueList):
                self.__ValueList.pop(CurrentIndex)
        except:
            pass

    def RemoveValue(self, v):
        try:
            CurrentIndex = self.__ValueList.index(v)

            self.__KeyList.pop(CurrentIndex)
            self.__ValueList.pop(CurrentIndex)
            self.__Comments.pop(CurrentIndex)
        except:
            pass

    def RemoveComment(self, c):
        try:
            CurrentIndex = self.__Comments.index(c)

            self.__Comments[CurrentIndex]=""
        except:
            pass

    def __getitem__(self, Index: int):
        return self.__KeyList[Index]

    def __getitem__(self, k: str):
        KeyInd=self.GetKeyIndex(k)
        if len(self.__ValueList):
            return self.__ValueList[KeyInd]
        else:
            return self.FindValue(k)

    def __setitem__(self,k,v):
        self.__KeyList.append(k)
        self.__Comments.append("")
        if v is not None:
            self.__ValueList.append(v)


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
                    print(key, "=", self.__ValueList[CurrentIndex],self.__Comments[CurrentIndex],end="")
                else:
                    print(self.__Comments[CurrentIndex], end="")
        else:
            for CurrentIndex, key in enumerate(self.__KeyList):
                if key:
                    print(key,self.__Comments[CurrentIndex],end="")
                else:
                    print(self.__Comments[CurrentIndex], end="")

        for i in range(self.__Indent-1):
            print("")

    def Save(self):
        Returner=""
        if self.__Name != "":
            Returner="[{0}]{1}\n".format(self.__Name,self.__NameComment)

        if len(self.__ValueList):
            for CurrentIndex, key in enumerate(self.__KeyList):
                if key:
                    Returner += (key + "=" + self.__ValueList[CurrentIndex] + self.__Comments[CurrentIndex])
                else:
                    Returner += (self.__Comments[CurrentIndex])
        else:
            for CurrentIndex, key in enumerate(self.__KeyList):
                if key:
                    Returner += (key + self.__Comments[CurrentIndex])
                else:
                    Returner += (self.__Comments[CurrentIndex])

        for i in range(self.__Indent-1):
            Returner+="\n"

        return Returner




class WinINF:
    def __init__(self):
        self.__FileName=""
        self.__Head=None
        self.__Tail=None
        self.__Current=None
        self.__ItemCount=0
        self.__SectionsDict={}

    def __iter__(self):
        self.__Current=None
        return self

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

    def Sections(self):
        return self.__SectionsDict.keys()

    def GetFileName(self):
        return self.__FileName

    def Count(self):
        return self.__ItemCount

    def __getitem__(self, k: str):
        return self.GetSection(k)

    def GetSection(self,Name):
        return self.__SectionsDict.get(Name)

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

    def Save(self, Name=None):
        if Name is not None:
            self.__FileName=Name

        if self.__Head is None:
            return

        f=open(self.__FileName,"w")

        for Current in self:
            f.write(Current.Save())

        f.close()








