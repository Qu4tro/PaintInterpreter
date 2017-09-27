module PrinterInterpreter where

import Data.Maybe
import Text.Read

type Board = [String]
type Coordinate = (Int, Int)

width :: Board -> Int
width = length . head
height :: Board -> Int
height = length

white = 'O'

data Command = I Int Int 
             | C
             | L Int Int Char
             | V Int Int Int Char
             | H Int Int Int Char
             | F Int Int Char
             deriving (Eq, Show, Read)


updateBoard :: [[a]] -> a -> Coordinate -> [[a]]
updateBoard board char (x, y) = top ++ [left ++ [char] ++ right] ++ bottom
    where top = take (y - 1) board
          left = take (x - 1) (board !! (y - 1))
          right = drop x (board !! (y - 1))
          bottom = drop y board


apply :: Board -> Command -> Board
apply board (I m n)           = replicate n (replicate m white)
apply board C                 = apply [] (I (width board) (height board))
apply board (L x y color)     = updateBoard board color (x, y)
apply board (V x y1 y2 color) = foldl apply board (map (\y -> L x y color) [y1..y2])
apply board (H x1 x2 y color) = foldl apply board (map (\x -> L x y color) [x1..x2])
apply board (F x y color)     = foldl apply board (map (\(x, y) -> L x y color) (region board [(x, y)]))

region = undefined

interpeter :: Board -> IO ()
interpeter board = do
    putStr "> "
    line <- getLine
    let command = readMaybe line :: Maybe Command
    let newBoard = apply board (fromJust command)

    if command == Nothing then
        interpeter board
    else
        do putStrLn $ unlines $ newBoard
           interpeter newBoard

main = interpeter []
