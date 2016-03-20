from socket import *
serverName='127.0.0.1'
serverPort=6789
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print 'Connection Established! '
sentence=raw_input('Input userName: ')
clientSocket.send(sentence)
modifiedSentence=clientSocket.recv(1024)
print 'From Server: ', modifiedSentence
clientSocket.close()
