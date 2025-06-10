function buildTree(comments, parent = null) {

return comments
.filter(c => c.parent === parent)
.map(c => ({
    ...c,
    children: buildTree(comments, c.id)
  }));
}

// *******************
let CommentItem = {}
let CommentTree = {}

CommentItem = {
  components: { CommentItem },
  name: 'CommentItem',
  props: ['comment', 'userId'],
  data() {
    return {
      replyText: '',
      showForm: false,
    };
  },
  mounted() {
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
          return newReply
        }else {
          console.error('Error while send reply:', response.statusText, response.json)
        }
      }catch (error) { console.error('Error post reply:', error) }
      
    }
  },
  template: `
    <div class="anime__review__item">
        <div class="anime__review__item__pic">
            <img :src="comment.user.avatar">
        </div>
        <div class="anime__review__item__text">
            <h6>{{ comment.user.username }}<span> - {{ comment.created_at }}</span> </h6>
            <p>{{ comment.content }}</p>
        </div>
        <div v-if="false && userId" class="anime__review__item__reply">
            <button class="reply-btn site-btn" @click="showForm = !showForm" >Ответить</button>
            <div v-if="showForm"  class="reply-form">
                <textarea  v-model="replyText" @input="replyText = $event.target.value" name="content" placeholder="Ваш ответ..."></textarea>
                <button @click="addReply" type="submit"><i class="fa fa-location-arrow send-reply"></i></button>
            </div>
        </div>

      <div v-if="comment.children.length > 0" class="anime__review__item__reply">
        <comment-item
          v-for="child in comment.children"
          :key="child.id"
          :comment="child"
          :userId="userId"
        />
        
      </div>
    </div>
  `
};

CommentTree = {
  name: 'CommentTree',
  props: ['comments', 'userId'],
  components: { CommentItem },
  template: `
      <comment-item
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :userId="userId"
      />
  `,

}


const CommentForm = {
  name: 'CommentForm',
  props: ['movieId'],
  data() {
    return {
      contentText: '',
    }
},
  template: `
  <div class="anime__details__form">
    <form id="comment-post-form" @submit.prevent="postComment">
      <textarea  @input="contentText = $event.target.value" placeholder="Оставьте свой комментарий..."></textarea>
      <button type="submit" ><i class="fa fa-location-arrow"></i> Отправить</button>
    </form>
  </div>
  `,
  methods: {
    async postComment() {
      if (!this.contentText.trim()) return;
      const comment = {
        movie: this.movieId,
        content: this.contentText,
        parent: null
      }
      let newComment = {}
      try {
        const response = await fetch(`/api/v1/comments/`, {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
          },  
          body: JSON.stringify(comment)            
        })
        
        if (response.ok) {
          newComment = await response.json()
          this.$emit('new-comment', newComment)
          this.contentText = ''
        }else {
          console.error('Error while send comment:', response.statusText, response.json)
        }
      }catch (error) { console.error('Error post comment:', error) }
    },
    }
}

const commentApp = Vue.createApp({
  components: { CommentItem, CommentTree, CommentForm, },
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
      userId: null
    }
  },
  template: `
  <div>
    <comment-form v-if="userId" :movieId="movieId" @new-comment="addComment"> </comment-form>
    <div v-else>
      <p>Чтобы оставить комментарий, <a href="/accounts/login/">войдите</a> или <a href="/accounts/signup/">зарегистрируйтесь</a>.</p>
    </div>

    <comment-tree
        v-if="comments"
        :comments="comments"
        :userId="userId"
      />
      <div v-else>
        <p>Комментариев пока нет. Будьте первым!</p>  
      </div>
  </div>
  `,
  methods: {
    addComment(comment) {
      this.fetchComments()
    },
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
      
        let data = await response.json();
        this.comments = buildTree(data);
        

      } catch (error) {
        console.error("Error:", error);
      }
    },
    
  }
});

commentApp.mount('#v-comment');

