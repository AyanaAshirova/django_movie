
const movieId = document.querySelector('input[name="movie"]').value
document.getElementById('comment-post-form').addEventListener('submit', async function(event) {
    event.preventDefault()

    const userId = this.querySelector('input[name="user"]').value
    const content = this.querySelector('textarea[name="content"]').value

    const formData = new FormData(this)
    
    const response = await fetch(`/api/v1/movies/${movieId}/comments/`, {
        method: 'post',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })

    console.log({
        user: userId,
        movie: movieId,
        content: content,
        parent: null,
    })
    console.log(response.body)

    if (response.ok) {
        const data = await response.json()

        // Пример добавления нового комментария
        const commentBlock = document.createElement('div')
        commentBlock.innerHTML = `<strong>${data.username}</strong>: ${data.content}`
        document.getElementById('commentsList').prepend(commentBlock)

        this.reset()
    } else {
        alert('Ошибка при отправке комментария')
    }
})

function getCookie(name) {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop().split(';').shift()
}



commentsBody = document.getElementById('comment-section')

// Загружаем и отображаем комментарии
// async function loadComments() {
//     const res = await fetch(`/api/v1/movies/${movieId}/comments/`);
//     const comments = await res.json();
//     commentsBody.innerHTML = '';
//     const commentTree = buildTree(comments);
//     console.log(commentTree)
//     tree.forEach(comment => renderComment(commentsBody, comment));
//   }

document.addEventListener('DOMContentLoaded', () => {
    fetch(`/api/v1/movies/${movieId}/comments/`,
        {
            method: 'get',
            headers: {
                'Content-Type': 'applications/json'
            }
        })
        .then(response =>  response.json())
        .then(data => {
            console.log(data)
            commentTree = buildTree(data)
            commentsBody.innerHTML = ''
            console.log(commentTree)
            
            commentTree.forEach(comment => renderComment(commentsBody, comment))
        })
        .catch(error => console.log("Error: ", error))
})    


function buildTree(comments, parent = null) {
    return comments
    .filter(c => c.parent === parent)
    .map(c => ({
        ...c,
        children: buildTree(comments, c.id)
    }));
}


function renderComment(container, comment){
    const wrapper = document.createElement('div');
    wrapper.className = comment.parent ? 'anime__replies' : 'anime__review__item';
    wrapper.innerHTML = `
        <div class="anime__review__item__pic">
            <img src="/static/media/avatars/default-3.jpg" bg-set="/static/media/avatars/default-3.jpg" alt="">
        </div>
        <div class="anime__review__item__text">
            <h6>${comment.username} - <span>${comment.created_at}</span>
            </h6>
            <p>${comment.content}</p>
        </div>
        <div class="anime__review__item__reply">
            <button class="reply-btn site-btn" data-id="${comment.id}" click="replyComment">Ответить</button>
            <div class="anime__details__form reply-comment-form">
                <form method="post" class="reply-form">
                    <textarea name="content" placeholder="Text your comment here.."></textarea>
                    <button type="submit"><i class="fa fa-location-arrow send-reply" data-parent="${comment.id}"></i></button>
                </form>
            </div>
        </div>
    `;
  
    container.appendChild(wrapper);
  
    const repliesContainer = document.createElement('div');
    repliesContainer.className = 'anime__replies';
    wrapper.appendChild(repliesContainer);
  
    comment.children.forEach(child => renderComment(repliesContainer, child));
  }
  
  // Обработка формы отправки нового комментария
  commentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(commentForm);
    const body = {
      content: formData.get('content'),
      parent: formData.get('parent') || null
    };
  
    const res = await fetch(`/api/v1/movies/${movieId}/comments/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(body)
    });
  
    if (res.ok) {
      commentForm.reset();
      await loadComments();
    }
  });

  
// Ответ по кнопке
function replyComment(this){
    
}


// commentsBody.addEventListener('click', (e) => {
//     if (e.target.classList.contains('reply-btn')) {
//       const replyBox = e.target.nextElementSibling;
//       replyBox.style.display = replyBox.style.display === 'none' ? 'block' : 'none';
//     }
//     if (e.target.classList.contains('send-reply')) {
//       const parentId = e.target.dataset.parent;
//       const content = e.target.previousElementSibling.value;
  
//       fetch(`/api/v1/movies/${movieId}/comments/`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//           content: content,
//           parent: parentId
//         })
//       }).then(() => loadComments());
//     }
//   });

//     wrapper = document.createElement('div').addClassList('anime__review__item')
//     wrapper.appendChild(
//         document.createElement(div)
//         .addClassList('anime__review__item__text')
//         .innerHTML=`
//             <h6>${comment.username} - <span>${comment.created_at}</span></h6>
//             <p>${comment.content}</p>
//         `)
//         wrapper.appendChild(
//         document.createElement(div)
//         .addClassList('anime__review__item__reply')
//         .innerHTML=`
//                 <button class="reply-btn site-btn" click="replyComment">Reply</button>
//             <div class="anime__details__form reply-comment-form">
//                 <form method="post">
//                     <textarea name="content" placeholder="Напишите комментарий.."></textarea>
//                     <button type="submit"><i class="fa fa-location-arrow"></i></button>
//                 </form>
//             </div>

//         `)


//         HTML += 
//         ```
//         <div class="anime__review__item" >
//             <div class="anime__review__item__pic">
//                 <img src="{{ comment.user.profile.avatar.url }}" alt="">
//             </div>
//             <div class="anime__review__item__text">
//                 <h6>${comment.username} - <span>${comment.created_at}</span>
//                 </h6>
//                 <p>${comment.content}</p>
//             </div>
//             <div class="anime__review__item__reply">
//                 <button class="reply-btn site-btn" click="replyComment">Reply</button>
//                 <div class="anime__details__form reply-comment-form">
//                     <form method="post">
//                         <textarea name="content" placeholder="Напишите комментарии.."></textarea>
//                         <button type="submit"><i class="fa fa-location-arrow"></i></button>
//                     </form>
//                 </div>

//             </div>

//             <div class="anime__replies">
//             {% if comment.replies.all %}
//                 {% for reply in comment.replies.all %}
//                     <div class="anime__review__item anime__reply__item">
//                         <div class="anime__review__item__pic">
//                             <img src="{{ reply.user.profile.avatar.url }}" alt="">
//                         </div>
//                         <div class="anime__review__item__text">
//                             <h6>{{ reply.user.username }} - <span>{{ reply.created_at }}</span>
//                             </h6>
//                             <p>{{ reply.content }}</p>
//                         </div>
//                     </div>
//                 {% endfor %}
//             {% endif %}
//             </div>
//         </div>
//         ```
//     });
// }


// Ответ по кнопке
commentSection.addEventListener('click', (e) => {
    if (e.target.classList.contains('reply-btn')) {
      const replyBox = e.target.nextElementSibling;
      replyBox.style.display = replyBox.style.display === 'none' ? 'block' : 'none';
    }
    if (e.target.classList.contains('send-reply')) {
      const parentId = e.target.dataset.parent;
      const content = e.target.previousElementSibling.value;
  
      fetch(`/api/v1/movies/${movieId}/comments/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          content: content,
          parent: parentId
        })
      }).then(() => loadComments());
    }
  });



    //   <strong>${comment.username}</strong> <small>${comment.created_at}</small>
    //   <p>${comment.content}</p>
    //   <button class="reply-btn" data-id="${comment.id}">Ответить</button>
    //   <div class="reply-form" style="display:none;">
    //     <textarea placeholder="Ваш ответ..."></textarea>
    //     <button class="send-reply" data-parent="${comment.id}">Отправить</button>
    //   </div>