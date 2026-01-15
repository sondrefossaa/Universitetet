module Errors

type PositionError =
    | UnknownPosition of string
    | PositionTaken

let showPositionError (err: PositionError) : string =
    match err with
    | UnknownPosition pos -> $"Unknown position: {pos}"
    | PositionTaken -> "Position already taken!"
