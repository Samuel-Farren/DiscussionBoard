JFLAGS = -g
JC = javac
JR = java
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
Main.java \
Login.java \
NewMessage.java

default: classes

classes: $(CLASSES:.java=.class)

clean:
	$(RM) *.class

run:
	$(JR) Main
