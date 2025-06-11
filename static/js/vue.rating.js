const ratingApp = Vue.createApp({
  components: { },
  data() {
    return {
      movieId: null,
      userId: null,
      fetchRate: 0,
      count: 0,
      showPopup: false,
      selectedRating: 0,
      userRate: null,
    }
  },
  mounted(){
    const ratingApp = document.getElementById('v-rating');
    this.userId = parseInt(ratingApp.getAttribute('data-user-id'));
    this.movieId = parseInt(ratingApp.getAttribute('data-movie-id'));
    this.fetchMovieRating();
    this.fetchUserRate()

  },
  computed: {
    fullstars() {
      return this.fetchRate % 1 <= 0.9 ? Math.floor(this.fetchRate) : Math.ceil(this.fetchRate)
    },
    halfstar() {
      return this.fetchRate % 1 > 0.25 && this.fetchRate % 1 < 0.9
    },
    emptystars() {
      return 10 - this.fullstars - (this.halfstar ? 1 : 0)
    }
  },
  template: `
  <div class="anime__details__rating ml-5">
    <div class="row wrap">
      <div class="mr-3">
        <div class="rating">
          <a v-for="x in fullstars"><i class="fa fa-star"></i></a>
          <a v-if="halfstar"><i class="fa fa-star-half-empty"></i></a>
          <a v-for="x in emptystars"><i class="fa fa-star-o"></i></a>
        </div>
        <span>{{ count }} Голосов</span>
      </div>

      <div>
        <span v-if="userRate" class="px-2 py-1 bg-info rounded-pill d-inline text-white mr-2"><i class="fa fa-star"></i> {{ userRate }}</span>
        <button v-if="userId" @click="showPopup = !showPopup">Оценить </button>
      </div>
    </div>

    <!-- Popup -->
    <div v-if="showPopup" class="rating-popup" style="position:absolute; background:#3c3d55;padding:10px; border-radius:6px; z-index:999;">
      <p v-if="!userRate" style="margin-bottom: 5px;">Выберите рейтинг:</p>
      <p v-else style="margin-bottom: 5px;">Ваш рейтинг:</p>
      <div class="rating">
        <a 
          v-for="n in 10" 
          :key="'popup-' + n"
          @click.prevent="selectRating(n)"
        >
          <i class="fa" :class="getStarClass(n, 'popup')"></i>
        </a>
        <br>
        <button v-if="!userRate" @click="postUserRateForMovie"><li class="fa fa-location-arrow"></li></button>
        <button v-else @click="delRateForMovie">удалить</button>
      </div>
    </div>
</div> 
  `,
  methods: {
    async fetchUserRate() {
      if (!this.userId || !this.movieId) return
      try {
        const response = await fetch(`/api/v1/users/movies/${this.movieId}/rating/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        if (response.ok) {
          const data = await response.json()
          this.userRate = data.value
          this.selectedRating = data.value
        }

      } catch(error) {
        console.error('Error: ', error)
      }
    },
    async fetchMovieRating() {
      if (!this.movieId) return;
      try {
        const response = await fetch(`/api/v1/movies/${this.movieId}/rating/average/`, {
          method: 'GET',
          headers: { 
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          this.fetchRate = data['average_rating']
          this.count = data['count']
        } 
      } catch (error) {
        console.error("Error: ", error)
      }
    },
    async delRateForMovie() {
      if (!this.userId || !this.movieId) return;
      const ratingBody = {
        movie: this.movieId,
        value: this.selectedRating
      }
      try {
        const response = await fetch(`/api/v1/users/movies/${this.movieId}/rating/`, {
          method: 'DELETE',
          headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(ratingBody)
        });
        if (response.ok) {
          this.showPopup = false;
          this.userRate = null
          this.selectedRating = 0;
          await this.fetchMovieRating();
        } 
      } catch (error) {
        console.error("Ошибка при удалении рейтинга: ", error);
      }
    },
    async postUserRateForMovie() {
      if (!this.userId || !this.movieId || !this.selectedRating) return;
      const ratingBody = {
        movie: this.movieId,
        value: this.selectedRating
      }
      try {
        const response = await fetch(`/api/v1/users/movies/${this.movieId}/rating/`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify(ratingBody)
        });
        if (response.ok) {
          const data = await response.json();
          this.userRate = data.value
          this.showPopup = false;
          this.selectedRating = data.value;
          await this.fetchMovieRating();
        } 
      } catch (error) {
        console.error("Ошибка отправки рейтинга: ", error);
      }
    },

    getStarClass(n, context = 'display') {
      if (context === 'popup') {
        if (n <= this.selectedRating) return 'fa-star';
        return 'fa-star-o';
      } else {
        if (n <= this.fullstars) return 'fa-star';
        if (n === this.fullstars + 1 && this.halfstar) return 'fa-star-half-o';
        return 'fa-star-o';
      }
    },
    selectRating(n) {
      if (!this.userRate) {
        this.selectedRating = n;
      }
    }
  }
});

ratingApp.mount('#v-rating');

