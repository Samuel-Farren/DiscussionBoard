#Assignment 2
#Sam Farren & Griffin Solomini

from socket import *
import thread

def main():
    CRLF = '\r\n'

    #keep track of current usernames in the discussion board
    usernames = []

    #Keep track of the two current discussion posts
    discussionPosts = []

    #local host that is accessed from web
    HOST = '127.0.0.1'
    serverPort = 6789

    #Create TCP socket (IPv4 and of type SOCK_STREAM)
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Associate server port number (serverPort) with this socket
    #serverSocket is our welcoming socket, wait for a client to make TCP request
    serverSocket.bind((HOST,serverPort))

    #has server listen for TCP requests from client
    #The parameter "1" specifies the max number of queued connections (at least 1)
    serverSocket.listen(5)
    print 'The server is ready to receive'
    while 1:

        #Set up TCP connection between the clients clientSocket and the servers
        #connectionSocket. Client and server can now send bytes over the connection
        connectionSocket, addr = serverSocket.accept()
        #Start new thread and have it listen for another connection
        thread.start_new_thread(serverSocket.listen,(5, ) )

        #retrieve request message
        message = connectionSocket.recv(1024)

        if len(discussionPosts) <= 2:
            discussionPosts.append(message)

        print message

        connectionSocket.send('userName cleared, you can now post to the discussion board.')
main()
