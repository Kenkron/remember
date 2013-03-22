#!/usr/bin/python3

import csv
import sys

facts = {}

beVerbs=["am","are","is"]
defaultMemoryFile=".rememberFacts.csv"
unknownAnswer="I don't know."
trueAnswer="Correct"
falseAnswer="Wrong"
invalidSentence="That's not a valid sentence"
sessionExitCode="exit"
sessionRememberCode="remember"
instructions="type "+sessionExitCode+" to leave session."
learnSuccessful="Okay"
learnFailed="I do not understand"
myReminders="my reminders"
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

def startSession():
    print (" ".join(sys.argv[1:]))
    temp=remember()
    if (temp):
        print("I remember")
    else:
        print("No memories found, making new ones")
    if (myReminders in facts):
        print(consider("what are "+myReminders+"?"))
    userSentence=""
    while (userSentence!=sessionExitCode):
        if (len(userSentence)>0):
            print(consider(userSentence))
        userSentence=input()
    saveMemories()
        
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
    if sentence.lower()=="help":
        return helpText
    elif sentence[0:7].lower()=="forget ":
        forgetwords=sentence[7:]
        if "." in forgetwords:
            forgetwords=forgetwords[: forgetwords.index(".")]
        forget(forgetwords);
    elif sentence[0:10].lower()=="remind me ":
        if "." in sentence:
            return learn(myReminders+" are "+sentence[10:sentence.index(".")])
        else:
            return learn(myReminders+" are "+sentence[10:])
    elif "?" in sentence or sentence[:5].lower()=="what ":
        words=sentence
        if "?" in words:
            words=sentence[: sentence.index("?")]
        return answer(words)
    else:
        words=sentence
        if "." in words:
            words=sentence[: sentence.index(".")]
        return learn(words)

def forget(words):
    verb=""
    for v in beVerbs:
        if " "+v+" " in words:
            verb=" "+v+" "
    if verb=="":
        if words in facts:
            print("Are you sure you want to forget "+words+"?")
            if (input().lower()=="yes"):
                print (answer("what is "+words))
                facts.pop(words)
                return (words+" has been forgotten.")
            else:
                return "I have not forgotten."
        else:
            return "I already don't know of "+words
    else:
        [subject,predicate]=words.split(verb)
        if (subject in facts and predicate in facts[subject]):
            print("Are you sure you want to forget "+words+"?")
            if input().lower()=="yes":
                facts[subject].remove(predicate)
                return (words+"has been forgotten.")
            else:
                return "I have not forgotten."
        else:
            return "I already don't know of "+words
            

def learn(words):
    verb=""
    if (" is " in words):
        verb=" is "
    elif (" are " in words):
        verb=" are "
    elif (" am " in words):
        verb=" am "
    else:
        return learnFailed
    
    [subject,predicate]=words.split(verb)
    if (subject in facts and not predicate in facts[subject]):
        facts[subject].append(predicate)
    else:
        facts[subject]=[predicate]
    saveMemories();
    return learnSuccessful

def answer(words):
    if (" is " in words):
        verb=" is "
    elif (" are " in words):
        verb=" are "
    elif (" am " in words):
        verb=" am "
    else:
        return unknownAnswer

    [subject,predicate]=words.split(verb)
    
    if (subject.lower() == "what" or subject.lower() == "who"):
        if (predicate in facts):
            return predicate+verb+addGrammar(facts[predicate])+"." 
        else:
            return unknownAnswer
    else:
        if (subject in facts and predicate in facts[subject]):
            return trueAnswer;
        else:
            return falseAnswer;

def addGrammar(wordList):
    answer=wordList[0]
    for nextWord in wordList[1:len(wordList)-1]:
        answer+=(", "+nextWord)
    if (len(wordList)>2):
        answer+=(", and "+wordList[len(wordList)-1])
    elif (len(wordList)==2):
        answer+=(" and "+wordList[len(wordList)-1])
    return answer

startSession()
