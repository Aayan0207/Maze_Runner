var startCellSelected = false;
var goalCellSelected = false;
var isMouseDown = false;

document.addEventListener("DOMContentLoaded", function () {
  const explore = document.getElementById("explored");
  const diagonal_movement = document.getElementById("diagonal_movement");
  const cells = document.querySelectorAll(".square");
  const message = document.getElementById("text_string");
  const reset = document.getElementById("reset");
  const form = document.querySelector("#MazeRunner-form");
  form.onsubmit = (event) => {
    event.preventDefault();
    let row = 0;
    let column = 0;
    startCellSelected = false;
    goalCellSelected = false;
    cells.forEach((cell) => {
      if (cell.style.backgroundColor === "green") {
        startCellSelected = true;
      }
      if (cell.style.backgroundColor === "red") {
        goalCellSelected = true;
      }
    });
    fetch("/", {
      method: "POST",
      body: new FormData(form),
    })
      .then((response) => response.json())
      .then((data) => {
        message.innerHTML = data.string;
        cells.forEach((cell) => {
          if (row == 20) {
            return;
          }
          if (data.string === "Start or Goal is undefined.") {
            cell.style.backgroundColor = "white";
            cell.value = "white";
            startCellSelected = false;
            goalCellSelected = false;
          } else {
            cell.style.backgroundColor = data.answer[row][column];
            cell.value = data.answer[row][column];
          }
          column += 1;
          if (column === 20) {
            row += 1;
            column = 0;
          }
        });
      })
      .catch((error) => {
        console.log(error);
      });
  };
  reset.onclick = () => {
    message.innerHTML =
      "Choose start cell (green). Choose goal cell (red). Drag/Click to put obstructions (black).";
    explore.value = "";
    explore.style.backgroundColor = "red";
    diagonal_movement.value = "";
    diagonal_movement.style.backgroundColor = "red";
    cells.forEach((cell) => {
      cell.style.backgroundColor = "white";
      cell.value = "white";
      startCellSelected = false;
      goalCellSelected = false;
    });
  };
  explore.onclick = () => {
    if (explore.value === "Show All Explored Cells") {
      explore.value = "";
      explore.style.backgroundColor = "red";
    } else {
      explore.value = "Show All Explored Cells";
      explore.style.backgroundColor = "green";
    }
  };
  diagonal_movement.onclick = () => {
    if (diagonal_movement.value === "Allow Diagonal Movement") {
      diagonal_movement.value = "";
      diagonal_movement.style.backgroundColor = "red";
    } else {
      diagonal_movement.value = "Allow Diagonal Movement";
      diagonal_movement.style.backgroundColor = "green";
    }
  };
  function cellLogic(cell) {
    if (
      !startCellSelected &&
      goalCellSelected &&
      cell.style.backgroundColor === "red"
    ) {
      cell.style.backgroundColor = "green";
      document.getElementById(cell.getAttribute("name")).value = "green";
      startCellSelected = true;
      goalCellSelected = false;
    } else if (
      startCellSelected &&
      !goalCellSelected &&
      cell.style.backgroundColor === "green"
    ) {
      cell.style.backgroundColor = "red";
      document.getElementById(cell.getAttribute("name")).value = "red";
      startCellSelected = false;
      goalCellSelected = true;
    } else if (!startCellSelected) {
      cell.style.backgroundColor = "green";
      document.getElementById(cell.getAttribute("name")).value = "green";
      startCellSelected = true;
    } else if (startCellSelected && !goalCellSelected) {
      cell.style.backgroundColor = "red";
      document.getElementById(cell.getAttribute("name")).value = "red";
      goalCellSelected = true;
    } else if (startCellSelected && goalCellSelected) {
      if (cell.style.backgroundColor === "green") {
        cell.style.backgroundColor = "white";
        document.getElementById(cell.getAttribute("name")).value = "white";
        startCellSelected = false;
      } else if (cell.style.backgroundColor === "red") {
        cell.style.backgroundColor = "white";
        document.getElementById(cell.getAttribute("name")).value = "white";
        goalCellSelected = false;
      } else if (cell.style.backgroundColor === "black") {
        cell.style.backgroundColor = "white";
        document.getElementById(cell.getAttribute("name")).value = "white";
      } else {
        cell.style.backgroundColor = "black";
        document.getElementById(cell.getAttribute("name")).value = "black";
      }
    }
  }
  cells.forEach((cell) => {
    cell.onmousedown = () => {
      isMouseDown = true;
      cellLogic(cell);
    };
    cell.onmouseenter= () => {
      if (isMouseDown) {
        cellLogic(cell);
      }
    };
    cell.onmouseup= () => {
      isMouseDown = false;
    };
  });
});
