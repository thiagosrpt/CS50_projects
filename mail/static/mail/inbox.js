document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email() {
  const compose_recipients = document.querySelector('#compose-recipients').value;
  const compose_subject = document.querySelector('#compose-subject').value;
  const compose_body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: compose_recipients,
      subject: compose_subject,
      body: compose_body
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
  });
  return false;
}

function load_mailbox(mailbox) {
    
  fetch(`/emails/${mailbox}`)
      .then(response => response.json())
      .then(emails => {
          console.log(emails.length)
          for (let i of Object.keys(emails)) {
              const elem_email = document.createElement('tr');
              elem_email.classList.add('email');
              if (emails[i].read) {
                  elem_email.classList.add('is_read');
              } else {
                elem_email.classList.add('new_email');
              }
              console.log(i)
              elem_email.innerHTML = `
                      <td>${emails[i].subject}</td>
                      <td>From: ${emails[i].sender}</td>
                      <td>Date: ${emails[i].timestamp}</td>
              `;
              console.log(emails[i].id)
              elem_email.addEventListener('click', () => email_content(emails[i].id, mailbox));

              console.log(elem_email)
              document.querySelector('#emails-view').append(elem_email);
          };
      });
      
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

}

function email_content(id, mailbox) {

  let sent = false;
  if (mailbox==="sent") {
    sent = true;
  }

  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      console.log(email);
      document.querySelector('#email-view').innerHTML = `
      <div>From: ${email.sender}</div>
      <div>To: ${email.recipients}</div>
      <div>Subject: ${email.subject}</div>
      <div>Timestamp: ${email.timestamp}</div>
      <br> 
      <div id="wrapper">
        <div class="email-buttons">
          <button class="btn-email" id="reply">Reply</button>
          <button class="btn-email" id="replyAll">Reply All</button>
          <button class="btn-email" id="read">${email["read"] ? "Mark as Unread" : "Mark as Read"}</button>
        </div>
        <div class="archived">
          <button class="btn-email" id="archive">${email["archived"] ? "Unarchive" : "Archive"}</button>
        </div>
      </div>

      <hr>
      <div>
        ${email.body}
      </div>
      `;
      //for archived emails the only option/button available is UNARCHIVE.
      console.log(sent)
        if (sent) {
          document.querySelector('.email-buttons').style.display = 'block';
          document.querySelector('.archived').style.display = 'none';
        }

        document.querySelector('#archive').addEventListener('click', () => {
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: !email.archived
            })
          })
          // .then(responde => response.json())
          .then(email => {
            load_mailbox('archive')
          });
      })

      document.querySelector('#read').addEventListener('click', () => {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: !email.read
          })
        })
        // .then(responde => response.json())
        .then(email => {
          load_mailbox('inbox')
        });
    })

      document.querySelector('#reply').addEventListener('click', () => {

        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
        document.querySelector('#email-view').style.display = 'none';

        document.querySelector('#compose-recipients').value = email.sender;

        console.log(email.subject.slice(0,3))
        console.log(email.subject.slice(0,3) != "Re:")

        if (email.subject.slice(0,3) == "Re:") {
          document.querySelector('#compose-subject').value = email.subject;
        }
        else {
          document.querySelector('#compose-subject').value = "Re: " + email.subject;
        }

        document.querySelector('#compose-body').value = `\n\n--------------------------------------\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}\n\n`;

      })

      document.querySelector('#replyAll').addEventListener('click', () => {

        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
        document.querySelector('#email-view').style.display = 'none';

        document.querySelector('#compose-recipients').value = email.sender + "," + email.recipients;

        console.log(email.subject.slice(0,3))
        console.log(email.subject.slice(0,3) != "Re:")

        if (email.subject.slice(0,3) == "Re:") {
          document.querySelector('#compose-subject').value = email.subject;
        }
        else {
          document.querySelector('#compose-subject').value = "Re: " + email.subject;
        }

        document.querySelector('#compose-body').value = `\n\n--------------------------------------\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}\n\n`;

      })

      
  })
}