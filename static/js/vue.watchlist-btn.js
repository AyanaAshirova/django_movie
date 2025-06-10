const WatchListButtonApp = Vue.createApp({
  data() {
    return {
      watchlists: [],
      movieId: null,
      userId: null,
      current: null
    }
  },
  mounted() {
    const watchlistAppbtn = document.getElementById('v-watchlist-btn')
    this.movieId = parseInt(watchlistAppbtn.getAttribute('data-movie-id'))
    this.userId = parseInt(watchlistAppbtn.getAttribute('data-user-id'))
    this.fetchUserWatchLists()
  },
  template: `
<div v-if="userId">
    <select  class="follow-btn" v-model="current" @change="catchCurrent" >
      <option disabled :value="null" hidden>Добавить в список</option>
      <option 
        v-for="list in watchlists" 
        :value="list.id" :key="list.id" 
        v-text="list.name"
      ></option>
      <option :value="0" class="text-warning">Удалить из списка</option>
    </select>
</div>
<div v-else><a href="/accounts/login/">Войдите</a>, чтобы добавить фильм в список</div>
  `,
  methods: {
    catchCurrent() {
      if (!this.movieId || !this.userId) return;
      if (this.current === 0){
        this.delMovieFromWatchList()
        return
      } else {
        this.postMovieToWatchList()
      }
    },
    async delMovieFromWatchList() {
      try {
        const response = await fetch(`/api/v1/watchlists/movies/${this.movieId}/remove_from_watchlist/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          },
        }) 
        const data = await response.json()
        console.log(data)
        this.current = null
        console.log(this.current)
        alertInstance.addAlert('фильм удалён из списка!', 'success');

      } catch (error) {
        console.error("Error:", error);
        alertInstance.addAlert('Ошибка при удалении', 'error');
      }
    },
    async postMovieToWatchList() {
      // const currentList = this.watchlists.filter(wl => wl.id === this.current)[0]
      try {
        const response = await fetch(`/api/v1/watchlists/movies/${this.movieId}/add_to_watchlist/${this.current}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          },
        });
        let data = await response.json();
        console.log(data)
        alertInstance.addAlert('Фильм добавлен в список!', 'success');

      } catch (error) {
        console.error("Error:", error);
        alertInstance.addAlert('не получилось добавить фильм список!', 'erro');
      }
    },
    async fetchUserWatchLists() {
    if (!this.userId) return;
    try {
      const response = await fetch(`/api/v1/watchlists/users/${this.userId}/movies/${this.movieId}/`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      let data = await response.json();
      this.watchlists = data;
      this.currentListId = this.watchlists.find(wl => wl.movie_is_watchlist === true)?.id || null
    } catch (error) {
      console.error("Error:", error);
    }
    },
  }
})


WatchListButtonApp.mount('#v-watchlist-btn');


