module Utilities

type ResultBuilder() =
    member __.Return(x: 'a) : Result<'a, 'e> = Ok x

    member __.Bind(m: Result<'a, 'e>, f: 'a -> Result<'b, 'e>) : Result<'b, 'e> = Result.bind f m

let result = ResultBuilder()

let mapTriple (f: 'a -> 'b) (triple: 'a * 'a * 'a) : 'b * 'b * 'b =
    match triple with
    | x, y, z -> (f x, f y, f z)
