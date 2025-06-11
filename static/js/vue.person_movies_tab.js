// v-person-movies-tab
const personMoviesApp = Vue.createApp({
  components: { movieCardList },
  data() {
    return {
      personId: null,
      roles: [],
      usedTabs: [],
      activeTabIndex: 0, // текущая активная вкладка 0
      pageSize: 12,
      currentPage: 1, 
    };
  },
  mounted() {
    const personMoviesApp = document.getElementById('v-person-movies-tab');
    this.personId = parseInt(personMoviesApp.getAttribute('data-person-id'));
    this.init()
  },
  methods: {
    async init() {
      await this.fetchPersonRoles()
      this.fetchPersonMovies()
    },
    async fetchPersonRoles() {
      if (!this.personId) return;
      try {
        const response = await fetch(`/api/v1/persons/${this.personId}/roles/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        for (let [index, item] of data.entries()) {
           this.roles[index] = {
              role: item,
              movies: [],
              pagination: {
                count: 0
              }
            }
        }
      } catch (error) {
        console.error('Ошибка при получении ролей:', error);
      }
    },
    async fetchPersonMovies(url=null, page=1) {
      const currentTab = this.activeTabIndex;
      const roleId = this.roles[currentTab]?.role?.id;
      if (!this.personId || !roleId) return;
      const endpoint = url ?? `/api/v1/persons/${this.personId}/roles/${roleId}/movies/?page=${page}`;
      try {
        const response = await fetch(endpoint, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
        });
        const data = await response.json();
        this.roles[currentTab].pagination = {
          next: data.next,
          previous: data.previous,
          count: data.count
        }
        this.roles[currentTab].movies = data.results
        this.currentPage = page;
        this.usedTabs.push(currentTab)
      } catch (error) {
        console.error('Ошибка при получении списков:', error);
      }
    },
    setActiveTab(index) {
      this.activeTabIndex = index;
      this.fetchPersonMovies()
    },
    loadNextPage() {
      const tab = this.roles[this.activeTabIndex]
      if (tab.pagination?.next) {
        this.fetchPersonMovies(tab.pagination.next)
      }
    },
    loadPrevPage() {
      const tab = this.roles[this.activeTabIndex]
      if (tab.pagination?.prev) {
        this.fetchPersonMovies(tab.pagination.previous)
      }
    },
    goToPage(page) {
      this.fetchPersonMovies(null, page);
    },
  },
  template: `
  <div>
    <div class="custom-tabs-wrapper">
      <ul class="custom-tabs">
        <li 
          v-for="(list, index) in roles"
          :key="list.role && list.role.id"
          :class="{ active: index === activeTabIndex }"
          @click="setActiveTab(index)"
        >
          {{ list.role.name }} 
        </li>
      </ul>
    </div>
    

      <div class="tab-content pt-4">
        <div
          v-for="(list, index) in roles"
          :key="list.role && list.role.id"
          v-show="index === activeTabIndex"
          class="tab-panel"
        >
            <movie-card-list
              :movies="list.movies"
            />

            <div v-if="list.movies.length <= 0">Пусто</div>
        </div>

<!-- Пагинация Vue -->
<div 
  v-if="roles.length > 0 
         && roles[activeTabIndex] 
         && totalPages > 1" 
  class="product__pagination"
>
  <span v-for="page in totalPages" :key="page">
    <span 
      v-if="page === currentPage"
      class="current-page"
    >
      {{ page }}
    </span>

    <a 
      v-else-if="Math.abs(currentPage - page) <= 1"
      href="#"
      @click.prevent="goToPage(page)"
    >
      {{ page }}
    </a>

    <a 
      v-else-if="Math.abs(currentPage - page) === 2"
      href="#"
      @click.prevent="goToPage(page)"
      :aria-label="page > currentPage ? 'Next' : 'Previous'"
      :class="page > currentPage ? 'next' : 'prev'"
    >
      <i :class="page > currentPage ? 'fa fa-angle-double-right' : 'fa fa-angle-double-left'"></i>
    </a>
  </span>
</div>


      </div>
    </div>
  </div>

  `,
  computed: {
    totalPages() {
      const tab = this.roles[this.activeTabIndex];
      if (!tab || !tab.pagination) return 1;
      return Math.ceil(tab.pagination.count / this.pageSize);
    },
  }
});

personMoviesApp.mount('#v-person-movies-tab');

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}



    