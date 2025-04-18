// Vue - render commentsTree
const CommentItem = {
  name: 'CommentItem',
  props: ['comment'],
  data() {
    return {
      replyText: '',
      showForm: false
    };
  },
  methods: {
    addReply() {
      if (!this.replyText.trim()) return;
      const newReply = {
        id: Date.now(),
        author: "Вы",
        content: this.replyText,
        children: []
      };
      this.comment.children.push(newReply);
      this.replyText = '';
      this.showForm = false;
    }
  },
  components: { CommentItem: null },
  template: `
    <div class="anime__review__item">
        <div class="anime__review__item__pic">
            <img src="{{ comment.user.avatar.url }}" alt="">
        </div>
        <div class="anime__review__item__text">
            <h6><span v-text="comment.username"></span> - <span v-text="comment.created_at"></span></h6>
            <p v-text="comment.content"></p>
        </div>
        <div class="anime__review__item__reply">
            <button class="reply-btn site-btn" @click="showForm = !showForm" >Ответить</button>
            <form v-if="showForm" method="post" class="reply-form">
                <textarea  v-model="replyText" name="content" placeholder="Ваш ответ..."></textarea>
                <button @click="addReply" type="submit"><i class="fa fa-location-arrow send-reply" data-parent=""></i></button>
            </form>
        </div>

      <div v-if="comment.children.length" class="anime__review__item__reply">
        <comment-item
          v-for="child in comment.children"
          :key="child.id"
          :comment="child"
        />
      </div>
    </div>
  `
};

const CommentTree = {
  props: ['movieId'],
  components: { CommentItem },
  data() {
    return {
      comments: []
    }
  },
  template: `
    <div>
      <comment-item
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
    </div>
  `,
  mounted() {
    this.fetchComments()
  },
  methods: {
    async fetchComments() {
      try {
        const response = await fetch(`/api/v1/movies/${this.movieId}/comments/`,
          {
              method: 'get',
              headers: {
                  'Content-Type': 'applications/json'
              }
          })
          .then(response =>  response = response.json())
          .then(data => {
              this.comments = buildTree(data)
              console.log(data)
          })

      } catch(error) {console.log("Error: ", error)}

    }
  }
};

const app = Vue.createApp({
  components: { CommentTree },
});


app.mount('#app');

// ***********
function buildTree(comments, parent = null) {
  return comments
  .filter(c => c.parent === parent)
  .map(c => ({
      ...c,
      children: buildTree(comments, c.id)
  }));
}


// children
// content
// created_at
// id
// movie
// parent
// user
// username

// ***************************


// const movieId = document.querySelector('input[name="movie"]').value
// document.getElementById('comment-post-form').addEventListener('submit', async function(event) {
//     event.preventDefault()
//     const userId = this.querySelector('input[name="user"]').value
//     const content = this.querySelector('textarea[name="content"]').value
//     const formData = new FormData(this)
//     const response = await fetch(`/api/v1/movies/${movieId}/comments/`, {
//         method: 'post',
//         body: formData,
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken')
//         }
//     })
//     console.log({
//         user: userId,
//         movie: movieId,
//         content: content,
//         parent: null,
//     })
//     console.log(response.body)

//     if (response.ok) {
//         const data = await response.json()

//         // Пример добавления нового комментария
//         const commentBlock = document.createElement('div')
//         commentBlock.innerHTML = `<strong>${data.username}</strong>: ${data.content}`
//         document.getElementById('commentsList').prepend(commentBlock)

//         this.reset()
//     } else {
//         alert('Ошибка при отправке комментария')
//     }
// })

// function getCookie(name) {
//     const value = `; ${document.cookie}`
//     const parts = value.split(`; ${name}=`)
//     if (parts.length === 2) return parts.pop().split(';').shift()
// }


  
//   // Обработка формы отправки нового комментария
//   commentForm.addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const formData = new FormData(commentForm);
//     const body = {
//       content: formData.get('content'),
//       parent: formData.get('parent') || null
//     };
  
//     const res = await fetch(`/api/v1/movies/${movieId}/comments/`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         'X-CSRFToken': getCookie('csrftoken')
//       },
//       body: JSON.stringify(body)
//     });
  
//     if (res.ok) {
//       commentForm.reset();
//       await loadComments();
//     }
//   });