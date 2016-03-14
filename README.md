# DiscussionBoard

Griffin Solomini and Sam Farren
Discussion board implemented in Python to service clients who want to connect to certain groups and post messages.

## Part 1
One unique Group for the server: 
In the first part of this project, you will consider that all clients belong to one and only one group.  A client joins
by connecting to a dedicated server (a standalone process) and is prompted to enter a non-existent user name in
that  group.   Note:  in  this  project,  you  are not required  to  implement  any  user  authentication  mechanisms.   The
server listens on a specic non-system port endlessly.  The server keeps track of all users that join or leave the group.
When a user joins or leaves the group, all other connected clients get notied by the server.  When a user (or client)
joins the group, he/she can only see the last 2 messages that were posted on the board by other clients who joined
earlier.  A list of users belonging to the group is displayed once a new user joins (in this part, the list represents all
users/clients that have joined earlier).  When a user posts a new message, other users in the same group should see
the posted message.  Messages are displayed in the following format:  \Message ID, Sender, Post Date, Subject."  A
user can retrieve the content of a message by contacting the server and providing the message ID as a parameter.
Your client program should also provide the option to leave the group.  Once a user leaves the group,  the server
noties all other users in the same group of this event.

## Part 2
  Extend Part 1 to allow users to join multiple discussion groups.  Once a user is connected to the server, the server
provides a list of 5 groups.  The user can then select the desired group by id or by name.  A user can join multiple
groups at the same time.  Remember that a user in one group cannot see users in other groups as well as the messages
they have posted
