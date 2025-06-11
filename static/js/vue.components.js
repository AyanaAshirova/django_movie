const MovieItem = {
  props: ['movie'],
  template: `
    <div class="m-2 row">
        <div class="mr-2">
          <img :src="movie.poster" height="60px">
        </div>
        <div class="p-0 product__item__text ">
          <h5  class="mb-1"><a :href="'/movie_details/' + movie.id + '/'" v-text="movie.title"></a></h5>
          <ul>
            <li v-for="g in movie.genres" :key="g.id" v-text="g.name" class="mr-1"></li>
          </ul>
        </div>
        <div>
          <span v-if="movie.user_rating" class="px-2 py-1 bg-info rounded-pill d-inline text-white ml-2 mt-2"><i class="fa fa-star"></i> {{movie.user_rating}}</span>
        </div>

    </div>
  `,
}

const MovieList = {
  props: ['movies'],
  components: { MovieItem },
  template: `
  <div class="recent__product">
      <div class="d-flex flex-wrap">
          <movie-item
            v-for="movie in movies"
            :key="movie.id"
            :movie="movie"
          />
      </div>
  </div>  
  `,
}


const movieCardItem = { 
  props: ['movie'],
  template: `
<div class="col-xl-2 col-lg-3 col-md-4 col-sm-6">
    <div class="product__item">
        <div 
          class="product__item__pic set-bg" 
          :style="{ backgroundImage: 'url(' + movie.poster + ')' }"
          >
            <div  v-if="movie.average_rating" class="ep">{{ movie.average_rating }}</div>
            <div  v-if="movie.user_rating" class="ep bg-info" style="right: 10px; left: auto;">{{ movie.user_rating }}</div>
            <div class="comment"><i class="fa fa-comments"></i> {{ movie.comments }}</div>
            <div class="view"><i class="fa fa-eye"></i> {{ movie.views }}</div>
        </div>
        <div class="product__item__text">
            <ul>
                <li
                  v-for="genre in movie.genres"
                >{{ genre.name }}</li>
            </ul>
            <h5><a :href="'/movie_details/' + movie.id + '/'">{{ movie.title }}</a></h5>
        </div>
    </div>
</div>

  `,
}
const movieCardList = { 
  components: { movieCardItem },
  props: ['movies'],
  template: `
  <div class="recent__product">
    <div class="row">
          <movie-card-item
            v-for="movie in movies"
            :key="movie.id"
            :movie="movie"
          />
    </div>
  </div>
  `,
}