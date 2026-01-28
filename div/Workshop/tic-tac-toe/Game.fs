module Game

open Errors
open Utilities

// The players
(*------------------------------------------------------*)
type Player =
    | X
    | O

let showPlayer (player: Player) : string =
    match player with
    | X -> "X"
    | O -> "O"

// TODO: this function should return the other player
let otherPlayer (player: Player) : Player = X

// State of board positions
(*------------------------------------------------------*)
type CellState =
    | Empty
    | Taken of Player

// TODO: this function should return "-" for empty cells and the result of `showPlayer` for taken cells
let showCellState (cellState: CellState) : string = ""

// TODO: this function should return true if the cell is taken and false if it is empty
let isTaken (cellState: CellState) : bool = false

// Board positions
(*------------------------------------------------------*)
type Position =
    | TL
    | TM
    | TR
    | ML
    | MM
    | MR
    | BL
    | BM
    | BR

let allPositions: List<Position> = [ TL; TM; TR; ML; MM; MR; BL; BM; BR ]

let tryReadPosition (pos: string) : Result<Position, PositionError> =
    match pos.ToLower() with
    | "tl" -> Ok TL
    | "tm" -> Ok TM
    | "tr" -> Ok TR
    | "ml" -> Ok ML
    | "mm" -> Ok MM
    | "mr" -> Ok MR
    | "bl" -> Ok BL
    | "bm" -> Ok BM
    | "br" -> Ok BR
    | pos -> Error(UnknownPosition pos)

// Game board
(*------------------------------------------------------*)
type Board =
    { TL: CellState
      TM: CellState
      TR: CellState
      ML: CellState
      MM: CellState
      MR: CellState
      BL: CellState
      BM: CellState
      BR: CellState }

let emptyBoard: Board =
    { TL = Empty
      TM = Empty
      TR = Empty
      ML = Empty
      MM = Empty
      MR = Empty
      BL = Empty
      BM = Empty
      BR = Empty }

let getCellState (board: Board) (pos: Position) : CellState =
    match pos with
    | TL -> board.TL
    | TM -> board.TM
    | TR -> board.TR
    | ML -> board.ML
    | MM -> board.MM
    | MR -> board.MR
    | BL -> board.BL
    | BM -> board.BM
    | BR -> board.BR

// TODO: this function should return true if all cells are taken, otherwise false
let boardIsFull (board: Board) : bool = true

// Winning streaks
(*------------------------------------------------------*)
let streaks: List<Position * Position * Position> =
    [ // rows
      (TL, TM, TR)
      (ML, MM, MR)
      (BL, BM, BR)

      // columns
      (TL, ML, BL)
      (TM, MM, BM)
      (TR, MR, BR)

      // diagonals
      (TL, MM, BR)
      (TR, MM, BL) ]

// Game state
(*------------------------------------------------------*)
type GameState =
    { CurrentPlayer: Player
      CurrentBoard: Board }

let initialState: GameState =
    { CurrentPlayer = X
      CurrentBoard = emptyBoard }

let showBoard (b: Board) : string =
    $" {showCellState b.TL} | {showCellState b.TM} | {showCellState b.TR} 
---+---+---
 {showCellState b.ML} | {showCellState b.MM} | {showCellState b.MR} 
---+---+---
 {showCellState b.BL} | {showCellState b.BM} | {showCellState b.BR}"

let showGameState (gameState: GameState) : string =
    $"\nCurrent board:
{showBoard gameState.CurrentBoard}

Current player: {gameState.CurrentPlayer}
"

// Game outcome
(*------------------------------------------------------*)
type Outcome =
    | Win of Player * Board
    | Draw of Board

// TODO: this function should return the player if all cells are taken by the same player, otherwise nothing
let allOnePlayer (cell1: CellState) (cell2: CellState) (cell3: CellState) : Option<Player> = None

let tryGetOutcome (board: Board) : Option<Outcome> =
    if boardIsFull board then
        Some(Draw board)
    else
        streaks
        |> List.map (mapTriple (getCellState board))
        |> List.choose ((<|||) allOnePlayer)
        |> List.map (fun player -> Win(player, board))
        |> List.tryHead

// Placing marks on the board
(*------------------------------------------------------*)
let placeMark (board: Board) (player: Player) (pos: Position) : Board =
    match pos with
    | TL -> { board with TL = Taken player }
    | TM -> { board with TM = Taken player }
    | TR -> { board with TR = Taken player }
    | ML -> { board with ML = Taken player }
    | MM -> { board with MM = Taken player }
    | MR -> { board with MR = Taken player }
    | BL -> { board with BL = Taken player }
    | BM -> { board with BM = Taken player }
    | BR -> { board with BR = Taken player }

// TODO: this function should set the cell at `pos` to taken by `player` if it is empty,
// otherwise it should return an error stating that the position is taken
let tryPlaceMark (board: Board) (player: Player) (pos: Position) : Result<Board, PositionError> = Ok board
