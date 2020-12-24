from hunting_fishbrain.hunting_fishbrain.TwoTargets import TwoTargets


#create a dummy targets object so we can test
targets = TwoTargets(0,0,0,0,0,0)

CLsum = 0
CRsum = 0
ERsum = 0
ELsum = 0

for k in range(0,200):
    hunt, pose, state, block, elapsed = targets.update(False)
    if targets.state=="target":
        if(targets.trialTypes[targets.trial_ind]=="CL"):
            CLsum+=1
        elif(targets.trialTypes[targets.trial_ind]=="CR"):
            CRsum+=1
        elif(targets.trialTypes[targets.trial_ind]=="EL"):
            ELsum+=1
        elif(targets.trialTypes[targets.trial_ind]=="ER"):
            ERsum+=1
        print block,targets.trialTypes[targets.trial_ind],targets.trial_ind,targets.state


print "totals:"
print "CL: "+str(CLsum)
print "CR: "+str(CRsum)
print "EL: "+str(ELsum)
print "ER: "+str(ERsum)