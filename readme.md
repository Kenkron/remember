Remember
========

Description:
------------

This program is designed to help you remember things.  To do this, start by telling the program how things are.  Use the words `is` and `are` to say things like `Ron's number is 555-6666` or `smurfs are blue people`.  Then, when you are done, ask who or what questions like `what is my phone number?` or `who are the smurfs?`.  If you have explained the things you asked for already, the program will recite what it remembers.

You may also wish to be reminded of things.  To do this, use `remind me` as in `remind me to leave` or `remind me to do the thing`.  Later, when you open this script again, your reminders will be shown to you.  Your reminders are stored just like any other thing under the label `my reminders`. Thus, you may view, add to, and forget your reminders just like anything else.

If you can't remember what it is you are trying to remember, and want to see a big long list of all the facts your program has, ls will list everything it knows.

Commands: 
---------

`[key] is [attribute]`
* adds attrubute to key in the facts list

`What is [key]`
* lists the attributes for a given key

`forget [key]`
* discards the key and it's attributes

`forget [key] is [attribute]`
* discards the given attribute from the given key

`remind me [event]`
* adds to the "my reminders" key shown at startup

`ls`
* lists all known facts