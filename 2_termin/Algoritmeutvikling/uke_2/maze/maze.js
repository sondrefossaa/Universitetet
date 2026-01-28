let data = ''
process.stdin.on('data', chunk => {
  data += chunk
})
process.stdin.on('end', () => {
  const lines = data.trim().split('\n');
  getSoulution(lines)
})

const directions = {
  down: [1, 0],
  left: [0, -1],
  up: [-1, 0],
  right: [0, 1],
}

const leftOf = {
  down: 'right',
  right: 'up',
  up: 'left',
  left: 'down',
};

const rightOf = {
  down: 'left',
  left: 'up',
  up: 'right',
  right: 'down',
};

class robot {
  constructor(startPos, goalPos, grid, gridSize) {
    this.currPos = startPos;
    this.goalPos = goalPos;
    this.grid = grid;
    this.gridSize = gridSize;
    this.directionName = 'right';
    this.visited = []
    for (let i = 0; i < this.gridSize[0]; i++) {
      this.visited[i] = [];
      for (let j = 0; j < this.gridSize[1]; j++) {
        this.visited[i][j] = new Set();
      }
    }
    this.visited[this.currPos[0]][this.currPos[1]].add(this.directionName);
  }

  move() {
    const inBounds = (pos) => {
      return pos[0] >= 0 && pos[0] < this.gridSize[0] &&
        pos[1] >= 0 && pos[1] < this.gridSize[1];
    };

    const currentDir = directions[this.directionName];
    const leftDirName = leftOf[this.directionName];
    const leftDir = directions[leftDirName];

    const left_square = [
      this.currPos[0] + leftDir[0],
      this.currPos[1] + leftDir[1]
    ];

    if (inBounds(left_square) && this.grid[left_square[0]][left_square[1]] === '0') {
      this.directionName = leftDirName;
      this.currPos = left_square;
    } else {
      const forwardPos = [
        this.currPos[0] + currentDir[0],
        this.currPos[1] + currentDir[1]
      ];

      if (inBounds(forwardPos) && this.grid[forwardPos[0]][forwardPos[1]] === '0') {
        this.currPos = forwardPos;
      } else {
        this.directionName = rightOf[this.directionName];
      }
    }

    if (this.currPos[0] === this.goalPos[0] && this.currPos[1] === this.goalPos[1]) {
      console.log(1)
      process.exit()
    }

    if (this.visited[this.currPos[0]][this.currPos[1]].has(this.directionName)) {
      console.log(0)
      process.exit()
    }

    this.visited[this.currPos[0]][this.currPos[1]].add(this.directionName);
  }
}

function getSoulution(input) {
  const lines = input;
  const gridSize = lines[0].split(" ").map(Number);
  const startpos = lines[1].split(" ").map(Number);
  const endpos = lines[2].split(" ").map(Number);

  // Decrement because the 0,0 of the grid is 1,1
  startpos[0]--;
  startpos[1]--;
  endpos[0]--;
  endpos[1]--;

  const grid = [];

  for (let i = 3; i < 3 + gridSize[0]; i++) {
    grid.push(lines[i]);
  }

  const ant = new robot(startpos, endpos, grid, gridSize);
  while (true) {
    ant.move();
  }
}
