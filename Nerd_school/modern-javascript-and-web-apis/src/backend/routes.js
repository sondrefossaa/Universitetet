import express, { Router } from 'express';
import { getMovies, insertMovie } from "./data/database.js";

const router = Router();
router.use(express.json());

router.get('/helloworld', async (req, res) => {
  const example = {
    message: 'Hello Nerdschool 🎉🎉🎉'
  };

  res.send(example);
});

router.get('/movie', async (req, res) => {
  const movies = await getMovies()

  res.send(movies);
});
export default router;

router.post('/movie', async (req, res) => {
  let new_movie = req.body
 insertMovie(new_movie)
  /* console.log('Request body is: ', req.body); */
});