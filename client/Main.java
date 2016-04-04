import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.Executors;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.ListSelectionModel;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

public class Main extends JPanel {

	private static final long serialVersionUID = -8562111201061094266L;

	private JList<String> list;
	private DefaultListModel<String> listModel;

	private JTextField userNameField;
	private JTextField messageIdField;

	private JScrollPane scrollPane;
	private JTextArea messages;

	private JButton loginButton;
	private JButton joinButton;
	private JButton unjoinButton;
	private JButton postButton;
	private JButton getButton;

	private Socket socket;

	private BufferedReader socketReader;
	private DataOutputStream socketWriter;

	String username;

	Set<String> groups;

	public Main() {
		super(new BorderLayout());

		// Holds the groups the user is subscribed to
		groups = new HashSet<String>();

		listModel = new DefaultListModel<String>();

		list = new JList<String>(listModel);
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		list.setSelectedIndex(-1);
		list.setVisibleRowCount(5);
		list.setPreferredSize(new Dimension(150, 200));

		// Sets the user's username for joining, posting, etc.
		loginButton = new JButton("Login");
		loginButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String userNameRequest = userNameField.getText();
				if (userNameRequest.length() != 0) {
					// Build message
					String message = "\r\n";
					message += "LOGIN\r\n";
					message += userNameRequest + "\r\n";

					// Write the message to the server
					try {
						socketWriter.writeUTF(message);
					} catch (IOException e1) {
						e1.printStackTrace();
					}
					System.out.println(message);
				}
			}
		});

		// Joins a user to group(s)
		joinButton = new JButton("Join");
		joinButton.setEnabled(false);
		joinButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					// Get the group name
					String group = list.getSelectedValue();
					if (group != null) {
						// Check if user belongs to group
						if (!groups.contains(group)) {
							// Build message
							String message = "\r\n";
							message += "JOIN\r\n";
							message += username + "\r\n";
							message += group + "\r\n\r\n";

							// Write the message to the server
							socketWriter.writeUTF(message);
							System.out.println(message);
						} else {
							messages.append("Already joined " + group + ".\n\n");
						}
					}
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		});

		// Removes a user from group(s)
		unjoinButton = new JButton("Unjoin");
		unjoinButton.setEnabled(false);
		unjoinButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// Get group name
				String group = list.getSelectedValue();
				if (group != null) {
					// Check if user belongs to group
					if (groups.contains(group)) {
						try {
							// Build message
							String message = "\r\nUNJOIN\r\n" + username
									+ "\r\n" + group + "\r\n\r\n";

							// Write message to server
							socketWriter.writeUTF(message);
							System.out.println(message);
							messages.append(username + " unjoined " + group
									+ "\n\n");

							// remove joined groups from list of joined groups
							groups.remove(group);
						} catch (IOException e1) {
							e1.printStackTrace();
						}
					} else {
						messages.append("Cannot unjoin " + group
								+ ", don't belong.\n\n");
					}
				}
			}
		});

		// Requests a list of the users in certain group(s) from the server
		JButton usersButton = new JButton("Users");
		usersButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					String group = list.getSelectedValue();
					if (group != null) {
						// Build message
						String message = "\r\nUSERS\r\n" + group + "\r\n\r\n";

						// Write message to server
						socketWriter.writeUTF(message);
						System.out.println(message);
					}
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		});

		// Opens a new window to handle writing a message
		postButton = new JButton("Post");
		postButton.setEnabled(false);
		postButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String groupname = list.getSelectedValue();
				if (groupname != null) {

					// Create new window
					JFrame frame = new JFrame("New Message");
					frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

					// Pass data into new window
					JComponent newContentPane = new NewMessage(frame,
							socketWriter, username, groupname);

					newContentPane.setOpaque(true);
					frame.setContentPane(newContentPane);

					frame.pack();
					frame.setVisible(true);
				}
			}
		});

		// Requets a message based on id from the server
		getButton = new JButton("Get");
		getButton.setEnabled(false);
		getButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// Get the id of the message from the user
				String id = messageIdField.getText();
				if (id.length() != 0) {
					// Build message
					String message = "\r\nGET\r\n";
					message += username + "\r\n";
					message += id + "\r\n\r\n";

					// Write message to server
					System.out.println(message);
					try {
						socketWriter.writeUTF(message);
					} catch (IOException e1) {
						e1.printStackTrace();
					}
				}
			}
		});

		// Text fields
		userNameField = new JTextField(10);
		messageIdField = new JTextField(1);

		// Build a button pane and add all buttons to it
		JPanel buttonPane = new JPanel();
		buttonPane.setLayout(new BoxLayout(buttonPane, BoxLayout.LINE_AXIS));
		buttonPane.add(userNameField);
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(new JSeparator(SwingConstants.VERTICAL));
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(loginButton);
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(joinButton);
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(unjoinButton);
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(usersButton);
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(postButton);
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(getButton);
		buttonPane.add(Box.createHorizontalStrut(5));
		buttonPane.add(messageIdField);
		buttonPane.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

		// Create the messages window
		messages = new JTextArea(30,50);
		messages.setEditable(false);
		messages.setLineWrap(true);
		messages.setWrapStyleWord(true);

		// Make text area scrollable
		scrollPane = new JScrollPane(messages);
		scrollPane
				.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		scrollPane
				.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);

		// Add messages window to panel
		this.add(scrollPane, BorderLayout.EAST);

		// Add grouplist to panel
		this.add(list, BorderLayout.CENTER);

		// Add button panel to main panel
		this.add(buttonPane, BorderLayout.PAGE_END);

		// Connect to server and start listening on the server socket in the
		// background
		connectToServer();
		setupBackgroundListening();
	}

	// Connect to server and setup reader and writer for the socket input
	// and output streams
	private void connectToServer() {
		try {
			socket = new Socket("192.168.1.17", 6789);
			socketReader = new BufferedReader(new InputStreamReader(
					socket.getInputStream()));
			socketWriter = new DataOutputStream(socket.getOutputStream());
		} catch (IOException e1) {
			System.out.println("Cannot connect to server.");
			System.exit(0);
		}
	}

	// Setup a background thread to continuously check if the
	// server has sent any response or updates
	private void setupBackgroundListening() {
		Executors.newSingleThreadExecutor().execute(new Runnable() {
			@Override
			public void run() {
				try {
					// Constantly check stream
					while (true) {
						// Read from stream
						String response;
						while ((response = socketReader.readLine()) != null) {
							response.trim();
							System.out.println(response);

							// Server sent a list of the available groups
							if (response.equals("GROUPS")) {
								for (int i = 0; i < 5; i++) {
									listModel.addElement(socketReader
											.readLine().trim());
								}
							}
							
							if (response.equals("USERNAMELOGIN")) {
								String user = socketReader.readLine().trim();
								String success = socketReader.readLine().trim();
								
								if (success.equals("YES")) {
									// Lock the text field and login button
									userNameField.setEditable(false);
									loginButton.setEnabled(false);

									// Enable action buttons
									getButton.setEnabled(true);
									joinButton.setEnabled(true);
									unjoinButton.setEnabled(true);
									postButton.setEnabled(true);

									// Set username
									username = user;
									
									messages.append("Logged in as: " + username + "\n\n");
								} else {
									messages.append("Unable to login as: " + user + ", username taken.\n\n");
								}
							}

							// Server sent the data corresponding to a message
							if (response.equals("MESSAGE")) {
								// Get message from socket
								String group = socketReader.readLine().trim();
								String id = socketReader.readLine().trim();
								String user = socketReader.readLine().trim();
								String date = socketReader.readLine().trim();
								String subject = socketReader.readLine().trim();
								String body = socketReader.readLine().trim();

								// Update the view with the new message
								messages.append(user + " posted in " + group
										+ "\n");
								messages.append("ID: " + id + "\n");
								messages.append("Date: " + date + "\n");
								messages.append("Subject: " + subject + "\n");
								messages.append(body + "\n\n");
							}

							// Server sent data for most recent messages in
							// group
							if (response.equals("JOINMESSAGE")) {
								// Get message from socket
								String group = socketReader.readLine().trim();
								String id = socketReader.readLine().trim();
								String user = socketReader.readLine().trim();
								String date = socketReader.readLine().trim();
								String subject = socketReader.readLine().trim();
								String body = socketReader.readLine().trim();

								// Update the view with the new message
								messages.append("Recent message in " + group
										+ ":\n");
								messages.append(user + " posted in " + group
										+ "\n");
								messages.append("ID: " + id + "\n");
								messages.append("Date: " + date + "\n");
								messages.append("Subject: " + subject + "\n");
								messages.append(body + "\n\n");
							}

							// Server found message for "GET" request
							if (response.equals("GETMESSAGE")) {
								// Get message from socket
								String group = socketReader.readLine().trim();
								String id = socketReader.readLine().trim();
								String user = socketReader.readLine().trim();
								String date = socketReader.readLine().trim();
								String subject = socketReader.readLine().trim();
								String body = socketReader.readLine().trim();

								// Update the view with the new message
								messages.append("Retreived message for id: "
										+ id + "\n");
								messages.append(user + " posted in " + group
										+ "\n");
								messages.append("ID: " + id + "\n");
								messages.append("Date: " + date + "\n");
								messages.append("Subject: " + subject + "\n");
								messages.append(body + "\n\n");
							}

							// Server response with all users in group
							if (response.equals("USERSINGROUP")) {
								String group = socketReader.readLine().trim();
								String user;
								messages.append("Users in group " + group
										+ ":\n");
								while (!(user = socketReader.readLine()).equals("END")) {
									user.trim();
									messages.append(user + "\t");
								}
								socketReader.readLine();
								messages.append("\n\n");
							}

							// Server notifying a user has joined
							if (response.equals("USERJOINED")) {
								String group = socketReader.readLine().trim();
								String user = socketReader.readLine().trim();
								messages.append(user + " joined " + group
										+ "\n\n");

								// If user is self, add joined groups to list of
								// joined groups
								if (user.equals(username))
									groups.add(group.trim());
							}

							// Server notifying a user has joined
							if (response.equals("USERUNJOINED")) {
								String group = socketReader.readLine().trim();
								String user = socketReader.readLine().trim();
								messages.append(user + " unjoined " + group
										+ "\n\n");
							}
							
							// Response when requesting a message in a group a user is not in
							if (response.equals("NOTINGROUP")) {
								String id = socketReader.readLine().trim();
								messages.append("Do not belong to the group message " + id + " is in\n\n");
							}
							
							// Response when message doesn't exist
							if (response.equals("MESSAGEDNE")) {
								String id = socketReader.readLine().trim();
								messages.append("Message " + id + " does not exist.\n\n");
							}
						}
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	// Setup Main window 
    private static void createGUI() {
        JFrame frame = new JFrame("Discussion Board");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        JComponent newContentPane = new Main();
        newContentPane.setOpaque(true);
        frame.setContentPane(newContentPane);
 
        frame.pack();
        frame.setVisible(true);
    }
 
    // Main method for program
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createGUI();
            }
        });
    }
}
