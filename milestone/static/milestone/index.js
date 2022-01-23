document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#new_event').addEventListener('click', new_event);
    document.querySelector('#close_window').addEventListener('click', close_window);
    
    
    document.querySelector('#dislike').addEventListener('click', function() {
        like(false);
    }); // listen to #dislike
    document.querySelector('#like').addEventListener('click', function() {
        like(true);
    });

    document.querySelector('#create-event-form').onsubmit = create_event;

    //document.querySelector('#delete_event').addEventListener('click', delete_event);

    document.querySelectorAll('#delete_event').forEach(event => {
      event.onclick = function() {            
          delete_event(this.dataset.eventId);
          window.location.reload()
      }
    })

    document.querySelectorAll('#edit_event').forEach(event => {
      event.onclick = function() {            
          edit_event(this.dataset.eventId);
      }
    })

    
});

function delete_event(eventId) {
  var result = confirm("Are you sure you want to delete this event?");
  if (result) {
    fetch(`/delete/${eventId}`, {
      method: 'POST',
      body: JSON.stringify({
        eventId: parseInt(eventId), //converts text to integer
      })
    })
    .then(response => response.json())
  }
}

function edit_event(eventId) {
  organizer = document.querySelector(`.organizer-${eventId}`).innerHTML.replace(/\s/g, '');
  participants = document.querySelector(`.participants-${eventId}`).innerHTML.replace(/\s/g, '');
  considering = document.querySelector(`.considering-${eventId}`).innerHTML
  event_name = document.querySelector(`.event_name-${eventId}`).innerHTML
  event_date = document.querySelector(`.date-${eventId}`).innerHTML

  text = document.querySelector(`.create-view`)
  content = text.innerHTML

  text.innerHTML = `
    <div class="create-view">
    <h3>Edit Event</h3>
        <form id="create-event-form">
                <div class="form-group">
                    <input disabled="" class="form-control" id="organizer" value="${organizer}">
                </div>

                <div class="form-group">
                    <input class="form-control" id="event_name" value="${event_name}">
                </div>

                <div class="form-group">
                    <input disabled="" id="participants" class="form-control" value="${participants}">
                </div>
                <br>
                <div class="checkbox-list">
                        <div class="checkbox">
                            <input id="delivery" name="considering" value="True" class="form-control" type="radio" checked="checked">
                            <label for="delivery">Delivery</label>
                        </div>
                        <div class="checkbox">
                            <input id="pickup" name="considering" value="True" class="form-control" type="radio" checked="checked">
                            <label for="pickup">Pick-up</label>
                        </div>
                        <div class="checkbox">
                            <input id="dinein" name="considering" value="True" class="form-control" type="radio" checked="checked">
                            <label for="dinein">Dine-in</label>
                        </div>
                </div>
                <br>
                <div class="form-group">
                    <div class="date">
                        <br>
                        <input type="datetime-local" class="form-control" id="event_date" name="date">
                    </div>
                </div>

                <input type="submit" class="btn btn-warning" id="submit_edit">
                <button class="btn btn-warning" id="close_window">Close</button>
        </form>
    </div>`

  window.scrollTo(1, 1);
  document.querySelector(".create-view-container").style.display = 'block';
  document.querySelector("#create-event-form").onsubmit = () => {
    submit_edit_event(eventId);
}


}


function submit_edit_event(eventId){

  const event_Id = eventId;
  const event_name = document.querySelector('#event_name').value;
  const event_delivery = document.querySelector('#delivery');
  const event_pickup = document.querySelector('#pickup');
  const event_dinein = document.querySelector('#dinein');
  const event_date = document.querySelector('#event_date').value;

  fetch('/event', {
    method: 'POST',
    body: JSON.stringify({
      eventId: event_Id,
      event_name: event_name,
      delivery: event_delivery.checked,
      pickup: event_pickup.checked,
      dinein: event_dinein.checked,
      date: event_date
    })
  })
  .then(response => response.json())
  .then(
      close_window()
  )
  .then(
      window.location.reload()
  )
  return false;
}

function update_event(eventId) {
  fetch(`/edit/${eventId}`, {
    method: 'GET'
  })
  .then(response => response.json())
}

function like(like) {
    const eventId = document.getElementById('event_in_view').className;
    const foodId = document.getElementById('food_in_view').className;

    fetch(`/like/${eventId}`, {
        method: 'POST',
        body: JSON.stringify({
          eventId: parseInt(eventId), //converts text to integer
          foodId: parseInt(foodId), //converts text to integer
          like: like
        })
      })
      .then(response => response.json())
}


//this can be removed
function event_view(eventId) {

    fetch(`event/${eventId}`, {
        method: 'GET'
      })
      .then(response => response.json());
}


function new_event() {
    // Show create event window
    document.querySelector('.create-view-container').style.display = 'block';
  }

function close_window() {
    // hides create event window
    text = document.querySelector(`.create-view`)
    document.querySelector('.create-view-container').style.display = 'none';
    text.innerHTML = content
}

function create_event(){

    const event_organizer = document.querySelector('#organizer').value;
    const event_name = document.querySelector('#event_name').value;
    const event_participants = document.querySelector('#participants').value;
    const event_delivery = document.querySelector('#delivery');
    const event_pickup = document.querySelector('#pickup');
    const event_dinein = document.querySelector('#dinein');
    const event_date = document.querySelector('#event_date').value;
  
    fetch('/event', {
      method: 'POST',
      body: JSON.stringify({
        organizer: event_organizer,
        event_name: event_name,
        participants: event_participants,
        delivery: event_delivery.checked,
        pickup: event_pickup.checked,
        dinein: event_dinein.checked,
        date: event_date
      })
    })
    .then(response => response.json())
    .then(
        close_window()
    )
    .then(
        window.location.reload()
    )
    return false;
}



