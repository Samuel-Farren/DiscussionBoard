import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.DataOutputStream;
import java.io.IOException;
import java.util.Date;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class NewMessage extends JPanel {
	
	private static final long serialVersionUID = 7073812287815887367L;
	
	private JTextField subjectField;
	private JTextArea bodyField;
	private JButton submitButton;

	public NewMessage(final JFrame frame, final DataOutputStream writer, final String username, final String groupname) {
		super(new BorderLayout());
		
		// Subject line field
		subjectField = new JTextField("Subject");
		
		// Message body input field
		bodyField = new JTextArea();
		bodyField.setPreferredSize(new Dimension(200,100));
		bodyField.setLineWrap(true);
		
		// Submit button
		submitButton = new JButton("Submit");
		submitButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// Build message
				String message = "\r\n";
				message += "POST\r\n";
				message += groupname + "\r\n";
				message += username + "\r\n";
				message += new Date().toString() + "\r\n";
				message += subjectField.getText() + "\r\n";
				message += bodyField.getText() + "\r\n\r\n";
					
				// Send message to server with socket
				System.out.println(message);
				try {
					writer.writeUTF(message);
				} catch (IOException e1) {
					e1.printStackTrace();
				}
				
				// Close the new message pane
				frame.dispose();
			}
		});
		
		// Add view objects to the panel
		this.add(BorderLayout.NORTH, subjectField);
		this.add(BorderLayout.CENTER, bodyField);
		this.add(BorderLayout.SOUTH, submitButton);
	}

}
