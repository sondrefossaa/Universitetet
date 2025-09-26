(function(){
    const myInfo = {
    name: "Alex Johnson",
    age: 28,
    favoriteFoods: ["Pizza", "Sushi", "Tacos"],
    favoriteMovies: [
        {
        name: "Inception",
        credits: {
            director: "Christopher Nolan",
            star: "Leonardo DiCaprio"
        }
        },
        {
        name: "The Shawshank Redemption",
        credits: {
            director: "Frank Darabont",
            star: "Tim Robbins"
        }
        },
        {
        name: "Pulp Fiction",
        credits: {
            director: "Quentin Tarantino",
            star: "John Travolta"
        }
        }
    ]
    };
    (function presentMyself(myInfo){
        const text = `Hello, my name is ${myInfo.name}. Im ${myInfo.age} years old and my favorite movies are: `+
        myInfo.favoriteMovies
        .reverse()
        .map(element => `${element.name} which is directed by ${element.credits.director} and stars ${element.credits.star}`)
        .reduce((acc, curr, index, array) =>{
            console.log(index)
            if (index == 0) {return curr}
            else if (index === array.length-1) {return acc + ` and ` + curr}
            else {return acc + `, ` + curr}
        },``);
        const newElement = document.createElement("p")
        newElement.innerHTML = text
        document.body.appendChild(newElement)
    })(myInfo)
})();   