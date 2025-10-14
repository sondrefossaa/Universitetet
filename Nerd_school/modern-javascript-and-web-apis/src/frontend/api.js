export const getMoviesFromApi = async () => {
  // Fetch code here
    const movieApiResponse = await fetch('/movie');
    const movieApiData = await movieApiResponse.json();

    return movieApiData
}
export const postMovieToApi = async (movie) => {
  const response = await fetch('/movie', {
    method: 'POST',
    body: JSON.stringify(movie),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  return await response.json();
}