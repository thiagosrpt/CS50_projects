document.addEventListener('DOMContentLoaded', function () {



  document.querySelector('#create-event-form').onsubmit = create_event;

});

function delete_event(eventId) {

    fetch(`/delete/${eventId}`, {
        method: 'POST',
        body: JSON.stringify({
          eventId: parseInt(eventId), //converts text to integer
        })
      })
      .then(response => response.json())
}