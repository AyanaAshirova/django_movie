const watchListApp = Vue.createApp({
  components: { MovieItem },
  data() {
    return {
      userId: null,
      watchlists: [],
      activeTabIndex: 0, // текущая активная вкладка
    };
  },
  mounted() {
    const watchListApp = document.getElementById('v-watchlists');
    this.userId = parseInt(watchListApp.getAttribute('data-user-id'));
    this.fetchUserWatchlists();
  },
  methods: {
    async fetchUserWatchlists() {
      if (!this.userId) return;
      try {
        const response = await fetch(`/api/v1/users/${this.userId}/watchlists/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
        });
        this.watchlists = await response.json();
      } catch (error) {
        console.error('Ошибка при получении списков:', error);
      }
    },
    setActiveTab(index) {
      this.activeTabIndex = index;
    },
  },
  template: `
    <div>
      <ul class="custom-tabs">
        <li 
          v-for="(list, index) in watchlists"
          :key="list.id"
          :class="{ active: index === activeTabIndex }"
          @click="setActiveTab(index)"
        >
          {{ list.name }} 
        </li>
      </ul>

      <div class="tab-content pt-4">
        <div
          v-for="(list, index) in watchlists"
          :key="list.id"
          v-show="index === activeTabIndex"
          class="tab-panel"
        >
          <div class="d-flex flex-wrap">
            <movie-item
              v-for="item in list.items"
              :key="item.movie.id"
              :movie="item.movie"
            />
            <div v-if="list.items.length <= 0">Пусто</div>
          </div>
        </div>
      </div>
    </div>
  `,
});

watchListApp.mount('#v-watchlists');

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


            // <div 
            //   v-for="(item, i) in list.items"
            //   class="col-md-12 col-lg-6">
            //   <a class="btn btn-link" :href="'/movie_details/'+item.movie.id+'/'">
            //     {{ item.movie.title }}
            //   </a>
            // </div>