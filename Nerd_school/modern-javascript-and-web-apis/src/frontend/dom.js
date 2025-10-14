export const createMovieList = (movies) => {
  const moviesList = document.createElement('ul');

  for (const movie of movies) {
    const movieListEntry = document.createElement('li');
    const { title } = movie;
    movieListEntry.innerText = title;
    moviesList.appendChild(movieListEntry);
  }

  return moviesList;
}
const createMovieCard = (movie) => {
  const movieCard = document.createElement('div');
  movieCard.id = movie.id;
  movieCard.className = 'movie-card';

  // Create a div container containing a header and a 
  // paragraph for the title and overview of a movie. 

    const movieImage = document.createElement('img');
    movieImage.src = movie.posterUrl;

    const imageContainer = document.createElement('div');
    imageContainer.className = 'image-container';

    imageContainer.appendChild(movieImage);
  const contentContainer = document.createElement('div');
  contentContainer.className = 'content';

  const movieHeader = document.createElement('h2');
  movieHeader.innerText = movie.title;

  const movieOverview = document.createElement('p');
  movieOverview.innerText = movie.overview;

  contentContainer.appendChild(movieHeader);
  contentContainer.appendChild(movieOverview);

movieCard.appendChild(imageContainer);
  movieCard.appendChild(contentContainer);

  return movieCard;
}


export const createMovieCards = (movies) => {
  const movieCards = [];
  for (const movie of movies) {
    const movieCard = createMovieCard(movie);
    movieCards.push(movieCard);
  }

  return movieCards;
}