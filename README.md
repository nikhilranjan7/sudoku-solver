# Sudoku Solver

## Screenshot
![alt text](https://github.com/nikhilranjan7/sudoku-solver/blob/master/images/sample.png)

## Install
This project requires **Python 3**.
Clone this repository
```
git clone https://github.com/nikhilranjan7/sudoku-solver
```
## How to run
```python
python3 sudoku.py
```
### Input Format
81 characters long string **row wise 9x9** with each character implying the value filled in that particular box. If box is unfilled put '.' as its place.
For example:
![alt text](https://github.com/nikhilranjan7/sudoku-solver/blob/master/images/sudoku.png)
For this sudoku input:
```
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
```

## [Algorithms detail](http://norvig.com/sudoku.html)
### [Constraint propagation](http://www.lirmm.fr/~bessiere/stock/TR06020.pdf)
Used in functions **elimination** and **naked_twin** in ```utils.py``` to eliminate the possibility of presence of any digit if it is present in corresponding row, column or square.

### [Search](http://intelligence.worldofcomputing.net/ai-search/depth-first-search.html)
Implemented recursion techniques to create depth-first-search trees for solving hard sudokus that need guess work in any particular box to proceed.

## [Sudoku strategy](http://sudokudragon.com/sudokustrategy.htm)
* Only choice rule
* Single possibility rule
* Naked Twin exclusion rule

### MIT License

Copyright (c) 2017 [Nikhil Ranjan](http://nikhilranjan7.github.io)
