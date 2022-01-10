document.addEventListener('DOMContentLoaded', function () {

    document.querySelector('#compose-post').onsubmit = NewPost;
    document.querySelector('#follow_btn').onsubmit= Follow;

    document.querySelectorAll('.heart').forEach(post => {
        post.onclick = function() {
            likes(this.dataset.postId);
        }
    })

    document.querySelectorAll('.edit_post').forEach(post => {
        post.onclick = function() {            
            edit(this.dataset.postId);
        }
    })
});

function Follow(){
    const profile_name = document.querySelector('#profile_name').innerHTML
    const follow_request = document.querySelector('#follow_request').value
    fetch(`follow/${profile_name}` , {
        method: 'POST',
        body: JSON.stringify({
            profile_name: profile_name,
            follow_request: follow_request
        })
    })

}

function edit(postid)
{
    text = document.querySelector(`.text-${postid}`)
    content = text.innerHTML
    edit_btn = document.querySelector(`.edit_post-${postid}`)
    text.innerHTML = '';
    edit_btn.style.display = 'none';

    text.innerHTML = `
        <div class="my-buttons">
            <form>
                <div class="like">
                    <textarea class='form-control-3' id='edited_content' name='edit-input' placeholder="Write something">${content}</textarea>
                </div>
                <div class="" data-post-id="">
                    <button type='button' class='btn btn-primary' id='edit-post-form-${postid}'>Save</button>
                    <button type='button' class='btn btn-danger' id='cancel-edit-${postid}'>Cancel</button>
                </div>
            </form>
        </div>
    `
    document.querySelector(`#cancel-edit-${postid}`).onclick = () => {
        text.innerHTML = content;
        edit_btn.style.display = 'block'
    }

    document.querySelector(`#edit-post-form-${postid}`).onclick = () => {
        let edited_content = document.querySelector('#edited_content').value
        fetch(`editpost/${postid}`, {
            method: 'POST',
            body: JSON.stringify({
                new_content: edited_content
            })
        })
        .then(
            text.innerHTML = edited_content
        )
        .then(
            edit_btn.style.display = 'block'
        )            

    }
}

function NewPost() {
    const post_content = document.querySelector('#post-text').value;

    fetch('/createpost', {
        method: 'POST',
        body: JSON.stringify({
            post: post_content           
        })
    })
    //load_posts();
    document.querySelector('#post-text') = ''
    return false;
}

function likes(postid) 
{
    let heart = document.querySelector(`#heart-${postid}`);
    let likesNumber = document.querySelector(`#num-${postid}`);

    if (heart.classList.contains('added'))
    {
        fetch(`likes/${postid}`, {
            method: 'POST',                            
            body: JSON.stringify({
                like: false
            })
        })
        .then(() => {
            console.log("Removes Like")
            likesNumber.textContent--;
            heart.classList.replace('btn-danger', 'btn-success');
            heart.innerHTML = heart.innerHTML.replace('♥', '♡');
        })
    }
    else 
    {
        fetch(`likes/${postid}`, {
            method: 'POST',                            
            body: JSON.stringify({
                like: true
            })
        })
        .then(() => {
            console.log("Adds Like")
            likesNumber.textContent++;
            heart.classList.replace('btn-success', 'btn-danger');
            heart.innerHTML = heart.innerHTML.replace('♡', '♥');
        })
    }
    heart.classList.toggle('added');
}