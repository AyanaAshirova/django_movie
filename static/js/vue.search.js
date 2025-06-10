let debounceTimer = null;

const searchApp = Vue.createApp({
  components: { MovieList, MovieItem },
  data() {
    return {
      movies: [],
      query: '',
    }
  },
  template: `
  <div style="display: flex; flex-direction: column; height:100%">  
    <form class="search-model-form mb-4" @submit.prevent>
      <input type="text" v-model="query" @input="debouncedFetch" id="search-input" placeholder="Что ищем?">
    </form>
    <div style="grid: 1;height: 80vh; overflow-y: auto; padding: 10px;">
      <movie-list
        :movies="movies"
      />
  </div>
  </div>
  `,
  methods: {
    debouncedFetch() {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        this.fetchMovies();
      }, 300); // задержка в 300 мс
    },
    async fetchMovies() {
      if (!this.query.trim()){
        this.movies = []
        return;
      } 
      try {
        const response = await fetch(`/api/v1/movies/search/${encodeURIComponent(this.query)}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data)
          this.movies = data
        } else {
          this.movies = []
        }

      } catch (error) {
        console.error("Ошибка при поиске:", error);
      }
    }
  }
});

searchApp.mount('#v-search');













