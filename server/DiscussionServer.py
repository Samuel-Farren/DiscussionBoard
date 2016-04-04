from socket import *
from mimetypes import *
import thread

#OSU IP: 172.28.25.174

#Port that is used to communicate between clients and this server
port1 = 6789

#Group Class that holds the name of the group, a list of messages in that group
#and a list of the clients in that group
class Group:
    def __init__(self, groupName):
        self.name = groupName
        self.messages=[]
        self.clients = []

#Message Class that holds the userName of who posted the message, date when the message was posted,
#subject of message, body content of message, and the Unique message ID of that message
class Message:
    def __init__(self,userName,postDate,subject,body):
        self.userName = userName
        self.postDate = postDate
        self.subject = subject
        self.body = body
        self.id = uniqueMessageID

#Client Class that holds the userName of that client, the connection(address) in
#order to send responses to that client, and a list contating all the groups the client has joined
class Client:
    def __init__(self, connection):
        self.userName = ''
        self.connection = connection
        self.groups = []

#init(): initializes a list of five groups that users can join upon request:
#These Groups are: House Gossip, Real Talk, Street Dope, Fun Tymez, and Networking
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

#Finds a user in a particular group based off the username given and the groupID given
def findClient(username,groupID):
    for client in groups[groupID].clients:
        if client.userName==username:
            return client
    return -1

#Finds a group based off the users username
#-1 is returned if a user doesn't belong
def findGroupByUserName(userName):
    i=0
    for group in groups:
        for client in group.clients:
            if client.userName == userName:
                return i
        i=i+1
    return -1

#Finds a message based off the ID of the message that the user wants
#if -1 is returned then that message doesn't exist
def findMessage(messageID,messageGroup):
    i=0
    for group in groups:
        for message in group.messages:
            if message.id == messageID:
                messageGroup.append(i)
                return message
        i=i+1
    messageGroup.append(-1)
    return -1

#This function is called when someone initially joins a group
#Nothing is sent if no one has posted in the group, if there is only one message in the group then only one is sent
#If there are more than one message in the group, the two most recent messages are sent
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
        request = connectionSocket.recv(4096)
        #if the user exits out of their GUI it sends a blank request(This test catches that scenario)
        if len(request)==0:
            print "User Closed GUI: "
            #Check if they logged in to the discussion board, if so remove their userName from the list
            if c.userName in userNames:
                print "User Closed GUI: " + str(c.userName)
                userNames.remove(c.userName)
            if len(c.groups) > 0:
                for groupID in c.groups:
                    client = findClient(c.userName,groupID)
                    print "before removed: " + str(groups[groupID].clients)
                    groups[groupID].clients.remove(client)
                    print "after removed: " + str(groups[groupID].clients)
                    #Let other people in group that the user left
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

#Obtain parsed tokens from the user request
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
#Update everyone in group that user joined
                try:
                    for client in groups[groupID].clients:
                        print "Sending to client: " + client.userName
                        client.connection.send("USERJOINED\r\n" + groupName + "\r\n" + userName + "\r\n\r\n")
                except serverSocket.error as msg:
                    print "msg is: " + msg
                print 'Number of clients is: ' + str(len(groups[groupID].clients))
                for x in groups[groupID].clients:
                    print x.userName

                #Send User that just joined the last two messages posted in the group
                initMessages(connectionSocket,groupID,groupName)

                #Send the user that just joined the list of users in that group
                users = "USERSINGROUP\r\n"
                users += groupName
                users += "\r\n"
                for client in groups[groupID].clients:
                    print "sending list of clients\n"
                    users += client.userName
                    users += "\r\n"
                users+= "END\r\n\r\n"
                connectionSocket.send(users)

#No one in group, add client to group and update username of client. Send 
#past two messages in group (if any) then send list of people in group(just himself since he's the only one in this group)
            else:
                c.userName = userName
                c.groups.append(groupID)
                groups[groupID].clients.append(c)
                print 'length was zero and added username: ' + groups[groupID].clients[0].userName
                print str(addr[0])
                connectionSocket.send("USERJOINED\r\n" + groupName + "\r\n" + userName + "\r\n\r\n")
                initMessages(connectionSocket,groupID,groupName)
                #send user his username saying he is the only one in the group
                users = "USERSINGROUP\r\n"
                users += groupName
                users += "\r\n"
                users += userName
                users += "\r\n"
                users += "END\r\n\r\n"
                connectionSocket.send(users)


#Checks userName that is provided by the client and make sure its not in use
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
            groups[groupID].messages.append(message)
            messageLen = len(groups[groupID].messages)
            print "Length of messages in group " + str(groupID) + " is " + str(messageLen)
#Send everyone in group the message that was just posted
            for client in groups[groupID].clients:
                print "sending to client\n\n\n"
                client.connection.send("MESSAGE\r\n" + groupName + "\r\n" + str(groups[groupID].messages[messageLen-1].id) + "\r\n" + groups[groupID].messages[messageLen-1].userName + "\r\n" + groups[groupID].messages[messageLen-1].postDate + "\r\n" + groups[groupID].messages[messageLen-1].subject
                + "\r\n" + groups[groupID].messages[messageLen-1].body + "\r\n\r\n")
            uniqueMessageID=uniqueMessageID + 1

        elif (tokens[1]=='GET'):
            userName = tokens[2]
            messageID = tokens[3]
            messageID = int(messageID)
            messageGroup = []
#Finds the message if it exists and updates the group that the message is found in and
            foundMessage = findMessage(messageID,messageGroup)
            groupID = findGroupByUserName(userName)

#checks if the message was found and if user belongs in the group that the message was found in
            if foundMessage != -1:
                if int(messageGroup[0]) in c.groups:
                    connectionSocket.send("GETMESSAGE\r\n" +groups[int(messageGroup[0])].name + "\r\n" + str(messageID) + "\r\n" + foundMessage.userName + "\r\n" + foundMessage.postDate + "\r\n" + foundMessage.subject + "\r\n" + foundMessage.body + "\r\n\r\n")
                else:
                    print "Cant find user in group"
                    connectionSocket.send("NOTINGROUP\r\n" +str(messageID) + "\r\n\r\n")
            else:
                print "Requested Message Does Not Exist"
                connectionSocket.send("MESSAGEDNE\r\n" + str(messageID) + "\r\n\r\n")
                
#Delete the user from the group they want to unjoin from 
        elif (tokens[1]=='UNJOIN'):
            userName = tokens[2]
            groupName = tokens[3].strip()
            groupID = groupMap[groupName]
            client = findClient(userName,groupID)
            print "before removed: " + str(groups[groupID].clients)
            groups[groupID].clients.remove(client)
            c.groups.remove(groupID)
            userNames.remove(userName)
            print "after removed: " + str(groups[groupID].clients)
            #Notify all users in the group that someone joined
            if len(groups[groupID].clients)>0:
                try:
                    for client in groups[groupID].clients:
                        print "Sending to client: " + client.userName
                        client.connection.send("USERUNJOINED\r\n" + groupName + "\r\n" + userName + "\r\n\r\n")
                except serverSocket.error as msg:
                    print "msg is: " + msg

#Sends the user a list of all the users in that group
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
serverSocket.listen(1)

#Initialize the groups(0,1,2,3,4) for the users to join
init()

print "\nStarted listening on port " + str(port1) + "\n"
while True:
    connectionSocket, addr = serverSocket.accept()
    print "accepted connection and client added"
    c=Client(connectionSocket)
#Initial list of groups that is sent to the user once the connection is accepted
    c.connection.send("GROUPS\r\nHouse Gossip\r\nReal Talk\r\nStreet Dope\r\nFun Tymez\r\nNetworking\r\n\r\n")

    #Starts a new thread for the current user that just connected to the server
    #Their client object, handler method, and connectionSocket and address are
    #passed into the new thread
    thread.start_new_thread(handler, (connectionSocket, addr,c))
