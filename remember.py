#!/usr/bin/python3

import csv
import sys
import signal
import readline

facts = {}

beVerbs=["am","are","is","be"]
ignoredKeyPrefix=["the ","a "]
questionWords=["what","who"]
defaultMemoryFile=".rememberFacts.csv"
unknownAnswer="I don't know."
trueAnswer="Correct"
falseAnswer="Wrong"
invalidSentence="That's not a valid sentence"
sessionExitCode=["exit","bye","goodbye","adios"]
sessionRememberCode="remember"
instructions="type "+sessionExitCode[0]+" to leave session."
learnSuccessful="Okay"
learnFailed="I do not understand"
myReminders="my reminders"
saveConstantly=True;
helpText="commands: "
helpText+="\n"
helpText+="\n[key] is [attribute]."
helpText+="\n    -adds attrubute to key in the facts list"
helpText+="\n"
helpText+="\nWhat is [key]?"
helpText+="\n    -lists the attributes for a given key"
helpText+="\n"
helpText+="\nforget [key]."
helpText+="\n    -discards the key and it's attributes"
helpText+="\n"
helpText+="\nremind me [event]."
helpText+="\n    -adds to the \""+myReminders+"\" key shown at startup"
helpText+="\n"
helpText+="\nls"
helpText+="\n    -prints all of the known facts"
helpText+="\n"
helpText+="\n    This program is designed to help you remember things."
helpText+="\nTo do this, start by telling the program how things are."
helpText+="\nuse the words \"is\" and \"are\" to say things like:"
helpText+="\n\"Ron's number is 555-6666\" or \"smurfs are blue people\""
helpText+="\nThen, when you are done, ask who or what questions like:"
helpText+="\n\"what is my phone number?\" or \"who are smurfs?\""
helpText+="\nIf you have explained the things you asked for already,"
helpText+="\nthe program will recite what it remembers."
helpText+="\n"
helpText+="\n    You may also wish to be reminded of things."
helpText+="\nTo do this, use \"remind me\" like so:"
helpText+="\n\"remind me to leave\" or \"remind me to do the thing\""
helpText+="\nLater, when you open this script again, your reminders"
helpText+="\nwill be shown to you.  Your reminders are stored just like"
helpText+="\nany other thing under the label \""+myReminders+"\". Thus,"
helpText+="\nyou may view, add to, and forget your reminders just like"
helpText+="\nanything else"
helpText+="\n"

def runRemember():
    temp=remember()
    if (not temp):
        print("No memories found, making new ones")
    if (myReminders in facts):
        print(consider("what are "+myReminders+"?"))
    #if there are arguments, just evaluate that argument
    arguments = (" ".join(sys.argv[1:]))
    if len(arguments)>0:
        if (arguments in facts):
            if arguments[len(arguments)-1]=="s":
                print(consider("what are "+arguments))
            else:
                print (consider("what is "+arguments))
        elif arguments[:3]=="to ":
            print (consider("remind me "+arguments))
            saveMemories()
        else:
            print (consider(arguments))
            saveMemories()
    #else open a session
    else:
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)
        readline.set_completer_delims('/n');
        userSentence=''
        while (userSentence not in sessionExitCode):
            if (len(userSentence)>0):
                print(consider(userSentence))
            userSentence=input()
        saveMemories()

def completer(text, state):
    options = {}

    #handle a forget command autocompete
    if text.lower().startswith('forget '):
        forgetfulText=text[len('forget '):]
        if forgetfulText.lower().startswith('to '):
            options = ['Forget '+i for i in facts[myReminders] if i.startswith(forgetfulText)]
        else:
            [fsub,fverb,fpred]=splitSentence(forgetfulText)
            if len(fverb)==0:
                options = ['Forget '+i for i in facts.keys() if i.startswith(fsub)]
            else:
                options = ['Forget '+fsub+fverb+i for i in facts[fsub] if i.startswith(fpred)]
    #handle a non-foget autocomplete
    else:
        #print(text.lower());
        [sub,verb,pred]=splitSentence(text)
        if len(verb)==0:
            #sets the options to the relavent question words
            options = [i for i in questionWords if i.lower().startswith(sub)]
        else:
            if sub in questionWords:
                options = [sub+verb+i for i in facts.keys() if i.startswith(pred)]
            else:
                options = [sub+verb+i for i in facts[sub] if i.startswith(pred)]
    if state < len(options):
        return options[state]
    else:
        return None

def saveMemories(filename=defaultMemoryFile):
    writer = csv.writer(open(filename, "w"))
    for word, definition in facts.items():
        csvList=[word]
        for description in definition:
            csvList.append(description)
        writer.writerow(csvList)

def remember(filename=defaultMemoryFile):
    try:
        for data in csv.reader(open(filename)):
            if (data[0] in facts):
                for attribute in data[1:]:
                    if (not attribute in facts[data[0]]):
                        facts[data[0]].append(attribute)
            else:
                facts[data[0]]=data[1:]
        return True
    except IOError:
        return False

def consider(sentence):
    #check for some built in commands first
    #help
    if sentence.lower()=="help":
        return helpText
    #list facts
    elif sentence.lower()=="ls":
        return ", ".join(facts.keys())
    #forget a fact
    elif sentence.lower().startswith("forget "):
        forgetwords=sentence[7:]
        if forgetwords.endswith('.'):
            forgetwords=forgetwords[:len(forgetwords)-1]
        return forget(forgetwords);
    #add a reminder.  Reminders are forced to begin with "to "
    elif sentence.startswith("remind me"):
        if sentence[10:13]!="to ":
            sentence=sentence[0:10]+"to "+sentence[10:]
        if "." in sentence:
            return learn(myReminders+" are "+sentence[10:sentence.index(".")])
        else:
            return learn(myReminders+" are "+sentence[10:])
    #check for a question
    elif "?" in sentence or sentence.startswith("what ") or sentence.startswith("who "):
        words=sentence
        if "?" in words:
            words=sentence[: sentence.index("?")]
        return answer(words)
    #If all else fails, this is a new fact to learn.
    else:
        words=sentence
        if "." in words:
            words=sentence[: sentence.index(".")]
        return learn(words)

def forget(words):
    if words[:3]=="to ":
        return forget("my reminders are "+words);
    [subject, verb, predicate]=splitSentence(words)
    if verb=="":
        if words in facts:
            print("Are you sure you want to forget "+words+"?")
            if (input().lower()=="yes"):
                print (answer("what are "+words))
                facts.pop(words)
                if saveConstantly:
                    saveMemories()
                return (words+" has been forgotten.")
            else:
                return "I have not forgotten."
        else:
            return "I already don't know of "+words
    else:
        if (subject in facts and predicate in facts[subject]):
            print("Are you sure you want to forget "+words+"?")
            if input().lower()=="yes":
                facts[subject].remove(predicate)
                if saveConstantly:
                    saveMemories()
                return (words+" has been forgotten.")
            else:
                return "I have not forgotten."
        else:
            return "I don't know of "+words


def learn(words):
    [subject,verb,predicate]=splitSentence(words)
    if len(verb)==0:
        return learnFailed
    for pre in ignoredKeyPrefix:
        if (subject.startswith(pre)):
            subject=subject[len(pre):]
    if (subject in facts and not predicate in facts[subject] and len(predicate)>0):
        facts[subject].append(predicate)
    else:
        if len(predicate)>0:
            facts[subject]=[predicate]
        else:
            facts[subject]={}
    if saveConstantly:
        saveMemories();
    return learnSuccessful

def answer(words):
    [subject,verb,predicate]=splitSentence(words)
    if len(verb)==0:
        return learnFailed
    if (subject.lower() == "what" or subject.lower() == "who"):
        ignore=""
        for pre in ignoredKeyPrefix:
            if (predicate.startswith(pre)):
                predicate=predicate[len(pre):]
                ignore=pre
        if (predicate in facts):
            return ignore+predicate+verb+addGrammar(facts[predicate])+"."
        else:
            return unknownAnswer
    else:
        if (subject in facts and predicate in facts[subject]):
            return trueAnswer
        else:
            return falseAnswer

def addGrammar(wordList):
    if (len(wordList)==0):
        return ""
    answer=wordList[0]
    for nextWord in wordList[1:len(wordList)-1]:
        answer+=(", "+nextWord)
    if (len(wordList)>2):
        answer+=(", and "+wordList[len(wordList)-1])
    elif (len(wordList)==2):
        answer+=(" and "+wordList[len(wordList)-1])
    return answer

#splits a sentence with a be verb into a subject, predicate, and verb
def splitSentence(sentence):
    verb=''
    for v in beVerbs:
        if " "+v+" " in sentence:
            verb=" "+v+" "
    if (len(verb)==0):
        return (sentence,'','')
    else:
        [subject,predicate]=sentence.split(verb)
        return (subject,verb,predicate)

def gracefulClose(signal,frame):
    saveMemories()
    sys.exit(0)

signal.signal(signal.SIGINT, gracefulClose)

runRemember()
