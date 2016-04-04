from socket import *
from mimetypes import *
import thread

port1 = 6789

class Group:
    def __init__(self, groupName):
        self.name = groupName
        self.messages=[]
        self.clients = []
        #self.connections = []

class Message:
    def __init__(self,userName,postDate,subject,body):
        self.userName = userName
        self.postDate = postDate
        self.subject = subject
        self.body = body
        self.id = uniqueMessageID

class Client:
    def __init__(self, connection):
        self.userName = ''
        self.connection = connection
        self.groups = []

#init(): initializes a list of five groups that users can join upon request
def init():
        g0 = Group('House Gossip')
        groups.append(g0)
        g1 = Group('Real Talk')
        groups.append(g1)
        g2 = Group('Street Dope')
        groups.append(g2)
        g3 = Group('Fun Tymez')
        groups.append(g3)
        g4 = Group('Networking')
        groups.append(g4)

def findClient(username,groupID):
    for client in groups[groupID].clients:
        if client.userName==username:
            return client
    return -1

def findGroupByUserName(userName):
    i=0
    for group in groups:
        for client in group.clients:
            if client.userName == userName:
                return i
        i=i+1
    return -1

def findMessage(messageID):
    for group in groups:
        for message in group.messages:
            if message.id == messageID:
                return message
    return -1

def initMessages(connection,groupID,groupName):
    messageLen = len(groups[groupID].messages)
    if messageLen == 0:
        print "no posts in group yet, don't send anything"
    elif messageLen == 1:
        connection.send("JOINMESSAGE\r\n" + groupName + "\r\n" + str(groups[groupID].messages[messageLen-1].id) + "\r\n" + groups[groupID].messages[messageLen-1].userName + "\r\n" + groups[groupID].messages[messageLen-1].postDate + "\r\n" + groups[groupID].messages[messageLen-1].subject
        + "\r\n" + groups[groupID].messages[messageLen-1].body + "\r\n\r\n")
    else:
        connection.send("JOINMESSAGE\r\n" + groupName + "\r\n" + str(groups[groupID].messages[messageLen-1].id) + "\r\n" + groups[groupID].messages[messageLen-1].userName + "\r\n" + groups[groupID].messages[messageLen-1].postDate + "\r\n" + groups[groupID].messages[messageLen-1].subject
        + "\r\n" + groups[groupID].messages[messageLen-1].body + "\r\n\r\n")
        connection.send("JOINMESSAGE\r\n" + groupName + "\r\n" + str(groups[groupID].messages[messageLen-2].id) + "\r\n" + groups[groupID].messages[messageLen-2].userName + "\r\n" + groups[groupID].messages[messageLen-2].postDate + "\r\n" + groups[groupID].messages[messageLen-2].subject
        + "\r\n" + groups[groupID].messages[messageLen-2].body + "\r\n\r\n")



#groups[] holds five group objects in a list that hold the name of the group
#the clients in the group, and the messages in the group
groups = []

#Initial group map to map group names to their associated index in the group array
groupMap = {'House Gossip'.strip():0,'Real Talk'.strip():1,'Street Dope'.strip():2,'Fun Tymez'.strip():3,'Networking'.strip():4}

#global userNames array that hold all userNames in disscussion board
userNames = []
#global messageID counter to keep track of all messages added to the group
uniqueMessageID = 0

#handler called when a connection is accepted and a new thread is Started
#handles all user requests from that thread
def handler(connectionSocket, addr,c):
    global uniqueMessageID
    global groups
    while 1:
        #updateSocket = socket(AF_INET, SOCK_STREAM)
        #updateSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #updateSocket.bind(("", port2))

        request = connectionSocket.recv(4096)
        #if the user exits out of their GUI it sends a blank request
        if len(request)==0:
            print "User Closed GUI: " + str(c.userName)
            if c.userName in userNames:
                userNames.remove(c.userName)
            if len(c.groups) > 0:
                for groupID in c.groups:
                    client = findClient(c.userName,groupID)
                    print "before removed: " + str(groups[groupID].clients)
                    groups[groupID].clients.remove(client)
                    print "after removed: " + str(groups[groupID].clients)
                    if len(groups[groupID].clients)>0:
                        try:
                            for updateClient in groups[groupID].clients:
                                print "Sending to client: " + updateClient.userName
                                updateClient.connection.send("USERUNJOINED\r\n" + groupName + "\r\n" + c.userName + "\r\n\r\n")
                        except serverSocket.error as msg:
                            print "msg is: " + msg

            connectionSocket.close()
            return

        print "request is: " + request

        tokens = request.split("\r\n")
        print tokens
        tokens[0].strip()

        if tokens[1]=='JOIN':
            print 'Request is JOIN, Inside JOIN'
            userName = tokens[2]
            groupName = tokens[3].strip()
            groupID = groupMap[groupName]
            print "groupID is: " + str(groupID)
            if len(groups[groupID].clients) > 0:
                c.userName = userName
                c.groups.append(groupID)
                print str(groups[groupID].clients)
                groups[groupID].clients.append(c)
                print str(groups[groupID].clients)
                try:
                    for client in groups[groupID].clients:
                        print "Sending to client: " + client.userName
                        client.connection.send("USERJOINED\r\n" + groupName + "\r\n" + userName + "\r\n\r\n")
                except serverSocket.error as msg:
                    print "msg is: " + msg
                print 'Number of clients is: ' + str(len(groups[groupID].clients))
                for x in groups[groupID].clients:
                    print x.userName
                initMessages(connectionSocket,groupID,groupName)

            else:
                c.userName = userName
                c.groups.append(groupID)
                groups[groupID].clients.append(c)
                print 'length was zero and added username: ' + groups[groupID].clients[0].userName
                print str(addr[0])
                connectionSocket.send("USERJOINED\r\n" + groupName + "\r\n" + userName + "\r\n\r\n")
                initMessages(connectionSocket,groupID,groupName)
                #updateSocket.connect((str(addr[0]),port2))
                #updateSocket.send("Real Talk YOLO\r\n")
                #updateSocket.close()

                #groups[groupID].users.append(userName)
                #print 'appended ' + groups[groupID].clients[len(groups[groupID].clients)].userName + ' to group ' + str(groupID)
                #print 'userName: ' + userName + ' already in group'

        elif tokens[1]=='LOGIN':
            userName = tokens[2]
            allowed = True
            if len(userNames) > 0:
                    for name in userNames:
                        if name == userName:
                            print "They are Equal"
                            allowed = False
            if allowed:
                userNames.append(userName)
                connectionSocket.send("USERNAMELOGIN\r\n" + userName + "\r\n" + "YES" + "\r\n\r\n")
            else:
                connectionSocket.send("USERNAMELOGIN\r\n" + userName + "\r\n" + "NO" + "\r\n\r\n")




        elif tokens[1]=='POST':
            groupName = tokens[2].strip()
            groupID = groupMap[groupName]
            sender = tokens[3]
            postDate = tokens[4]
            subject = tokens[5]
            content = tokens[6]
            message = Message(sender,postDate,subject,content)
            #print "message is: " + str(message)
            groups[groupID].messages.append(message)
            messageLen = len(groups[groupID].messages)
            print "Length of messages in group " + str(groupID) + " is " + str(messageLen)
            for client in groups[groupID].clients:
                print "sending to client\n\n\n"
                #client.connection.send("something stupid")
                client.connection.send("MESSAGE\r\n" + groupName + "\r\n" + str(groups[groupID].messages[messageLen-1].id) + "\r\n" + groups[groupID].messages[messageLen-1].userName + "\r\n" + groups[groupID].messages[messageLen-1].postDate + "\r\n" + groups[groupID].messages[messageLen-1].subject
                + "\r\n" + groups[groupID].messages[messageLen-1].body + "\r\n\r\n")
                     #client.connection.send("MESSAGE\r\n" + str(groups[groupID].messages[messageLen-1].id) + "\r\n" + groups[groupID].messages[messageLen-1].userName + "\r\n" + groups[groupID].messages[messageLen-1].postDate + "\r\n" + groups[groupID].messages[messageLen-1].subject
                     #+ "\r\n" + groups[groupID].messages[messageLen-1].body + "\r\n\r\n")
            uniqueMessageID=uniqueMessageID + 1

        elif (tokens[1]=='GET'):
            #check user is in group
            userName = tokens[2]
            messageID = tokens[3]
            messageID = int(messageID)
            foundMessage = findMessage(messageID)
            groupID = findGroupByUserName(userName)
            #client = findClient(userName,groupID)
            if foundMessage != -1:
                if groupID != -1:
                    connectionSocket.send("GETMESSAGE\r\n" +groups[groupID].name + "\r\n" + str(messageID) + "\r\n" + userName + "\r\n" + foundMessage.postDate + "\r\n" + foundMessage.subject + "\r\n" + foundMessage.body + "\r\n\r\n")
                else:
                    print "Cant find user in group"
                    connectionSocket.send("NOTINGROUP\r\n" +str(messageID) + "\r\n\r\n")
            else:
                print "Requested Message Does Not Exist"
                connectionSocket.send("MESSAGEDNE\r\n" + str(messageID) + "\r\n\r\n")


        elif (tokens[1]=='UNJOIN'):
            userName = tokens[2]
            groupName = tokens[3].strip()
            groupID = groupMap[groupName]
            client = findClient(userName,groupID)
            print "before removed: " + str(groups[groupID].clients)
            groups[groupID].clients.remove(client)
            userNames.remove(userName)
            print "after removed: " + str(groups[groupID].clients)
            if len(groups[groupID].clients)>0:
                try:
                    for client in groups[groupID].clients:
                        print "Sending to client: " + client.userName
                        client.connection.send("USERUNJOINED\r\n" + groupName + "\r\n" + userName + "\r\n\r\n")
                except serverSocket.error as msg:
                    print "msg is: " + msg

            #Notify other people in group when he leaves


        elif (tokens[1]=='USERS'):
            groupName = tokens[2].strip()
            groupID = groupMap[groupName]
            users = "USERSINGROUP\r\n"
            users += groupName
            users += "\r\n"
            for client in groups[groupID].clients:
                print "sending list of clients\n"
                users += client.userName
                users += "\r\n"
            users+= "END\r\n\r\n"
            connectionSocket.send(users)
        else:
            print "404 Not Found No matching Protocol"

# Setup socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", port1))

#serverSocket.bind(("", port2))
#serverSocket.bind(("", port2))
serverSocket.listen(1)

#Initialize the groups(0,1,2,3,4) for the users to join
init()

print "\nStarted listening on port " + str(port1) + "\n"
while True:
    connectionSocket, addr = serverSocket.accept()
    print "accepted connection and client added"
    #clients.append(connectionSocket)
    c=Client(connectionSocket)
    c.connection.send("GROUPS\r\nHouse Gossip\r\nReal Talk\r\nStreet Dope\r\nFun Tymez\r\nNetworking\r\n\r\n")
    thread.start_new_thread(handler, (connectionSocket, addr,c))
