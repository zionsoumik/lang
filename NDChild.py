class NDChild(object):
    def __init__ (self, learningrate, conslearningrate,language,sets):

        self.grammar = {"lang":language,"SP": .5, "HIP": .5, "HCP": .5, "OPT": .5, "NS": .5, "NT": .5,"WHM": .5, "PI": .5, "TM": .5, "VtoI": .5, "ItoC": .5,"AH": .5, "QInv": .5}
        self.r = learningrate #simulation will pass child a learning rate
        self.conservativerate = conslearningrate
        self.sets=sets

    def consumeSentence(self, s): #child is fed a list containing [lang, inflec, sentencestring]
        self.spEtrigger(s)    #parameter 1
        self.hipEtrigger(s)   #parameter 2
        self.hcpEtrigger(s)   #parameter 3
        #self.optEtrigger(s)  #parameter 4
        self.nsEtrigger(s)    #parameter 5
        self.ntEtrigger(s)    #parameter 6
        self.whmEtrigger(s)   #parameter 7
        self.piEtrigger(s)    #parameter 8
        self.tmEtrigger(s)    #parameter 9
        self.VtoIEtrigger(s)  #parameter 10
        #self.ItoCEtrigger(s) #parameter 11
        self.ahEtrigger(s)    #parameter 12
        #self.QInvEtrigger(s) #parameter 13

    #etriggers for parameters
    # first parameter Subject Position
    def spEtrigger(self, s):
        # Check if O1 and S are in the sentence and sent is declarative
        if "O1" in s.sentenceList and "S" in s.sentenceList and s.inflection == "DEC":
            O1index = s.sentenceList.index("O1")
            Sindex = s.sentenceList.index("S") # Sindex is position of S in sentList
            # Make sure O1 is non-sentence-initial and before S
            if O1index > 0 and O1index < s.sentenceList.index("S"):
                # set towards Subject final
                self.adjustweight ("SP",1, self.r)
                self.sets[0][1].append(s.sentenceList)
                #print(set(s.sentenceList))
            # S occurs before 01
            elif Sindex > 0 and O1index > s.sentenceList.index("S"): # S cannot be Sent initial
                # set towards Subject initial
                self.adjustweight("SP",0,self.r)
                self.sets[0][0].append(s.sentenceList)

    # second parameter Head IP, VP, PP, etc
    def hipEtrigger(self, s):
        if "O3" in s.sentenceList and "P" in s.sentenceList:
            O3index = s.sentenceList.index("O3")
            Pindex = s.sentenceList.index("P")
            # O3 followed by P and not topicalized
            if O3index > 0 and Pindex == O3index + 1:
                self.adjustweight ("HIP", 1, self.r)
                self.sets[1][1].append(s.sentenceList)
            elif O3index > 0 and Pindex == O3index - 1:
                self.adjustweight ("HIP", 0, self.r)
                self.sets[1][0].append(s.sentenceList)

        # If imperative, make sure Verb directly follows O1
        elif s.inflection == "IMP" and "O1" in s.sentenceList and "Verb" in s.sentenceList:
            if s.sentenceList.index("O1") == s.sentenceList.index("Verb") - 1:
                self.adjustweight ("HIP", 1, self.r)
                self.sets[2][1].append(s.sentenceList)
            elif s.sentenceList.index("Verb") == (s.sentenceList.index("O1") - 1):
                self.adjustweight("HIP", 0, self.r)
                self.sets[2][0].append(s.sentenceList)

    # third parameter Head in CP
    def hcpEtrigger(self, s):
        if s.inflection == "Q":
            # ka or aux last in question
            if s.sentenceList[-1] == 'ka' or ("ka" not in s.sentenceList and s.sentenceList[-1] == "Aux"):
                self.adjustweight("HCP", 1, self.r)
                self.sets[3][1].append(s.sentenceList)

            # ka or aux first in question
            elif s.sentenceList[0] == "ka" or ("ka" not in s.sentenceList and s.sentenceList[0]=="Aux"):
                self.adjustweight("HCP", 0, self.r)
                self.sets[3][0].append(s.sentenceList)


    def nsEtrigger(self, s):
        if s.inflection == "DEC" and "S" not in s.sentenceStr and s.outOblique():
            self.adjustweight("NS",1,self.r)
            self.sets[4][1].append(s.sentenceList)
        elif s.inflection == "DEC" and "S" in s.sentenceStr and s.outOblique():
            self.adjustweight("NS",0,self.conservativerate)
            self.sets[4][0].append(s.sentenceList)

    def ntEtrigger(self, s):
        if s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" not in s.sentenceStr:
            self.adjustweight("NT",1,self.r)
            self.sets[5][1].append(s.sentenceList)

        elif s.inflection == "DEC" and "O2" in s.sentenceStr and "O1" in s.sentenceStr and "O3" in s.sentenceStr and "S" in s.sentenceStr and "Adv" in s.sentenceStr:
            self.adjustweight("NT",0,self.conservativerate)
            self.sets[5][0].append(s.sentenceList)
        #if all possible complements of VP are in sentence, then the sentence is not Null Topic

    def whmEtrigger(self, s):
        if s.inflection == "Q" and "+WH" in s.sentenceStr:
            if ("+WH" in s.sentenceList[0]) or ("P" in s.sentenceList[0] and "O3[+WH]" == s.sentenceList[1]):
                self.adjustweight("WHM",1,self.conservativerate)
                self.sets[6][1].append(s.sentenceList)
            else:
                self.adjustweight("WHM",0,self.r)
                self.sets[6][0].append(s.sentenceList)

    def piEtrigger(self, s):
        pIndex = s.indexString("P")
        O3Index = s.indexString("O3")
        if pIndex > -1 and O3Index > -1:
            if abs(pIndex - O3Index) > 1:
                self.adjustweight("PI", 1, self.r)
                self.sets[7][1].append(s.sentenceList)

            elif ((pIndex + O3Index) == 1):
                self.adjustweight ("PI",0,self.conservativerate)
                self.sets[7][0].append(s.sentenceList)

    def tmEtrigger(self, s):
        if "[+WA]" in s.sentenceStr:
            self.adjustweight("TM",1,self.r)
            self.sets[8][1].append(s.sentenceList)
        elif "O1" in s.sentenceList and "O2" in s.sentenceList and (abs(s.sentenceList.index("O1")-s.sentenceList.index("O2")) > 1):
            self.adjustweight("TM",0,self.r)
            self.sets[8][0].append(s.sentenceList)

    def VtoIEtrigger(self, s):
        if "Verb" in s.sentenceStr and "O1" in s.sentenceStr:
            o1index = s.indexString("O1")
            if o1index != 0 and abs(s.indexString("Verb") - o1index) > 1:
                self.adjustweight("VtoI", 1, self.r)
                self.sets[9][1].append(s.sentenceList)
                self.adjustweight("AH", 0, self.r)
                self.sets[11][0].append(s.sentenceList)

        #no need to explicitly check inflection because only Q and DEC have AUX
        elif "Aux" in s.sentenceList:
            self.adjustweight("VtoI", 0, self.conservativerate)
            self.sets[9][0].append(s.sentenceList)


    def ItoCEtrigger(self, s):
        sp = self.grammar['SP']
        hip = self.grammar['HIP']
        hcp = self.grammar['HCP']

        if sp < 0.5 and hip < 0.5: # (Word orders 1, 5)
            Sindex = s.sentenceList.index("S")
            if (Sindex > 0 and s.inflection == "DEC") and s.sentenceList.index("Aux") == Sindex + 1:
                self.adjustweight("ItoC", 0, self.r)
                self.sets[10][0].append(s.sentenceList)

        elif sp > 0.5 and hip > 0.5: # (Word orders 2, 6)
            if (s.inflection == "DEC"):
                AuxIndex = s.sentenceList.index("Aux")
                if (AuxIndex > 0 and s.sentenceList.index("S") == AuxIndex + 1):
                    self.adjustweight("ItoC", 0, self.r)
                    self.sets[10][0].append(s.sentenceList)

        elif sp > 0.5 and hip < 0.5 and hcp > 0.5 and s.inflection == "DEC":
            if s.sentenceList.index("Verb") == s.sentenceList.index("Aux") + 1:
                self.adjustweight("ItoC", 0, self.r)
                self.sets[10][0].append(s.sentenceList)

        elif sp < 0.5 and hip > 0.5 and hcp < 0.5 and s.inflection == "DEC":
            if s.sentenceList.index("Aux") == s.sentenceList.index("Verb") + 1:
                self.adjustweight("ItoC", 0, self.r)
                self.sets[10][0].append(s.sentenceList)

        elif sp > 0.5 and hip < 0.5 and hcp < 0.5 and ('ka' in s.sentenceList):
            if s.inflection == "DEC" and "Aux" not in s.sentence:
                if (s.sentenceList.index("Verb") == s.sentenceList.index("Never") + 1):
                    self.adjustweight("ItoC", 0, self.r)
                    self.sets[10][0].append(s.sentenceList)

        elif sp < 0.5 and hip > 0.5 and hcp > 0.5 and ('ka' in s.sentenceList):
            if s.inflection == "DEC" and "Aux" not in s.sentence:
                if s.sentenceList.index("Never") == s.sentenceList.index("Verb") + 1:
                    self.adjustweight("ItoC", 0, self.r)
                    self.sets[10][0].append(s.sentenceList)

    def ahEtrigger(self, s):
        if (s.inflection == "DEC" or s.inflection == "Q") and ("Aux" not in s.sentenceStr and "Never" in s.sentenceStr and "Verb" in s.sentenceStr and "O1" in s.sentenceStr):
            neverPos = s.indexString("Never")
            verbPos = s.indexString("Verb")
            O1Pos = s.indexString("O1")

            if (neverPos > -1 and verbPos == neverPos+1 and O1Pos == verbPos+1) or (O1Pos > -1 and verbPos == O1Pos+1 and neverPos == verbPos + 1):
                self.adjustweight("AH", 1, self.r)
                self.sets[11][1].append(s.sentenceList)
                self.adjustweight("VtoI", 0, self.r)
                self.sets[9][0].append(s.sentenceList)

        elif "Aux" in s.sentenceStr and self.grammar["AH"] <= 0.5:
            self.adjustweight ("AH",0,self.conservativerate)
            self.sets[11][0].append(s.sentenceList)
            #if self.grammar["VtoI"] > 0.5: #If not affix hopping language, vtoi is either 0 or 1, but if evidence of vtoi towards 1 has alreadybeen observed, increase confidence 1VtoI given 0AH
                #self.adjustweight("VtoI", 1, self.conservativerate)

    def adjustweight(self, parameter, direction, rate):
        if direction == 0:
            self.grammar[parameter] -= rate*self.grammar[parameter]
        elif direction == 1:
            self.grammar[parameter] += rate*(1-self.grammar[parameter])
