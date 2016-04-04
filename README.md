Networking Project 2: Discussion Board

Sam Farren
farren.19@osu.edu

Griffin Solimini
solimini.1@osu.edu

#############################################################################

CLIENT

Client is written in Java using Swing for the graphic interface. If using ssh
to run, will need to use ssh -X.

Instructions to compile client:
'cd' to project directory
run 'make'

Instructions to run client:
run 'java Main'

#############################################################################

SERVER

Server is written in python.

Instructions to compile server:
N/A

Instructions to run server
run 'python DiscussionBoard.py'

#############################################################################

PROTOCOL

JOIN sent from client to server to join user to group

\r\n
JOIN\r\n
username\r\n
group\r\n
\r\n

UNJOIN sent from client to server to unjoin user from group

\r\n
UNJOIN\r\n
username\r\n
group\r\n
\r\n

USERS sent from client to server to get a list of all users in a group

\r\n
USERS\r\n
group\r\n
\r\n

GET sent from client to server to get a message of specific id from a group

\r\n
GET\r\n
username\r\n
group\r\n
messageId\r\n
\r\n

POST sent from client to server to post a message to the server

\r\n
POST\r\n
groupname\r\n
username\r\n
date\r\n
subject\r\n
body\r\n
\r\n

GROUPS sent from server to client to list available groups.

GROUPS\r\n
group1\r\n
group2\r\n
group3\r\n
group4\r\n
group5\r\n
\r\n

MESSAGE sent from server to client when a message has been sent to a group

MESSAGE\r\n
group\r\n
id\r\n
user\r\n
date\r\n
subject\r\n
body\r\n
\r\n

GETMESSAGE sent from server to client as a response to client GET request

GETMESSAGE\r\n
group\r\n
id\r\n
user\r\n
date\r\n
subject\r\n
body\r\n

USERSINGROUP sent from server to client as response to client USERS request

USERSINGROUP\r\n
group\r\n
user1\r\n
user2\r\n
...
...
userN\r\n
\r\n

USERJOINED sent from server to client to notify that a user has joined a group

USERJOINED\r\n
group\r\n
user\r\n
\r\n

USERUNJOINED sent from server to client to notify that a user has unjoined a group

USERUNJOINED\r\n
group\r\n
user\r\n
\r\n
