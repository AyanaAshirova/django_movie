
const CommentItem = {
  name: 'CommentItem',
  props: ['comment'],
  data() {
    return {
      replyText: '',
      showForm: false,
      defaultAvatar: '/media/avatars/default-1.jpg',
      userId: null
    };
  },
  mounted() {
    const commentApp = document.getElementById('v-comment')
    this.userId = parseInt(commentApp.getAttribute('data-user-id'))
  },
  methods: {
    async addReply() {
      if (!this.replyText.trim()) return;
      let newReply = await this.sendReply()
      newReply['children'] = []
      if (newReply.id) this.comment.children.push(newReply);
      this.replyText = '';
      this.showForm = false;
    },
    async sendReply() {
      let newReply = {}
      const url = `/api/v1/comments/${this.comment.id}/reply/`
      const commentChildData = {
        user: this.userId,
        movie: parseInt(this.comment.movie),
        content: this.replyText,
        parent: parseInt(this.comment.id)
      }
      try {
        const response = await fetch(url, {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
          },  
          body: JSON.stringify(commentChildData)            
        })
        
        if (response.ok) {
          newReply = await response.json()
        }else {
          console.error('Error while send reply:', response.statusText, response.json)
        }
      }catch (error) { console.error('Error post reply:', error) }
      return newReply
    }
  },
  components: { CommentItem: null },
  template: `
    <div class="anime__review__item">
        <div class="anime__review__item__pic">
            <img :src="defaultAvatar" alt="user avatar">
        </div>
        <div class="anime__review__item__text">
            <h6><span v-text="comment.username"></span> <span>-</span> <span v-text="comment.created_at"></span></h6>
            <p v-text="comment.content"></p>
        </div>
        <div class="anime__review__item__reply">
            <button class="reply-btn site-btn" @click="showForm = !showForm" >Ответить</button>
            <div v-if="showForm"  class="reply-form">
                <textarea  v-model="replyText" name="content" placeholder="Ваш ответ..."></textarea>
                <button @click="addReply()" type="submit"><i class="fa fa-location-arrow send-reply"></i></button>
            </div>
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
  props: ['comments'],
  components: { CommentItem },
  template: `
    <div>
      <comment-item
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
    </div>
  `,

}

const app = Vue.createApp({
  components: { CommentTree},
  mounted() {
    const commentApp = document.getElementById('v-comment')
    this.movieId = parseInt(commentApp.getAttribute('data-movie-id'))
    this.userId = parseInt(commentApp.getAttribute('data-user-id'))
    this.fetchComments()
  },
  data() {
    return {
      comments: [],
      movieId: null,
    }
  },
  template: `
    <comment-tree :comments="comments"></comment-tree>
  `,
  methods: {
    async fetchComments() {
      if (!this.movieId) {
        console.error("Error: movieId is missing");
        return;
      }
      try {
        const response = await fetch(`/api/v1/movies/${this.movieId}/comments/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        this.comments = buildTree(data);
      } catch (error) {
        console.error("Error:", error);
      }
    }
  }
});

app.mount('#v-comment');

// *******************

function buildTree(comments, parent = null) {
return comments
.filter(c => c.parent === parent)
.map(c => ({
    ...c,
    children: buildTree(comments, c.id)
}));
}

function getCookie(name) {
const value = `; ${document.cookie}`
const parts = value.split(`; ${name}=`)
if (parts.length === 2) return parts.pop().split(';').shift()
}
