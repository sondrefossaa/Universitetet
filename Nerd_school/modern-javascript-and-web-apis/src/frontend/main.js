import {getMoviesFromApi, postMovieToApi} from './api.js'
import { createMovieList, createMovieCards } from './dom.js';

const movieData = await getMoviesFromApi();

const { movies } = movieData;


const movieCardsContainer = document.getElementById('movie-cards');
const movieCards = createMovieCards(movies);
for(const movieCard of movieCards) {
  movieCardsContainer.appendChild(movieCard);
}


// We get a reference to the form DOM element
const createMovieForm = document.getElementById('create-movie-form');

// Add an event listener to the submit action, so that we can
// capture its data as it is submitted
createMovieForm.addEventListener('submit', async (e) => {

  // We prevent the default submit action to be executed, since
  // we want to handle the data submitting ourselves.
  e.preventDefault();

  const formData = new FormData(e.target)
  const title = formData.get('movie-title');
  const overview = formData.get('movie-overview');

  // Create a new movie object from the form inputs and submit 
  // it to our web api using fetch
    postMovieToApi({ title, overview });
  e.target.reset();
})