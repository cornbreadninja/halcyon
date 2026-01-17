const canvas = document.getElementById("wheel");
const ctx = canvas.getContext("2d");

const names = [
  "Alice",
  "Bob",
  "Charlie",
  "Diana",
  "Eve",
  "Frank"
];

const colors = [
  "#f94144",
  "#f3722c",
  "#f9c74f",
  "#90be6d",
  "#577590",
  "#277da1"
];

const center = canvas.width / 2;
const radius = center;
const sliceAngle = (2 * Math.PI) / names.length;

let rotation = 0;
let spinning = false;

// Draw the wheel
function drawWheel() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  names.forEach((name, i) => {
    const start = rotation + i * sliceAngle;
    const end = start + sliceAngle;

    // Slice
    ctx.beginPath();
    ctx.moveTo(center, center);
    ctx.arc(center, center, radius, start, end);
    ctx.fillStyle = colors[i % colors.length];
    ctx.fill();
    ctx.stroke();

    // Text
    ctx.save();
    ctx.translate(center, center);
    ctx.rotate(start + sliceAngle / 2);
    ctx.textAlign = "right";
    ctx.fillStyle = "#fff";
    ctx.font = "16px sans-serif";
    ctx.fillText(name, radius - 10, 5);
    ctx.restore();
  });

	// Pointer at the right (3 o’clock)
	ctx.fillStyle = "black";
	ctx.beginPath();
	ctx.moveTo(canvas.width + 5, center - 10);
	ctx.lineTo(canvas.width + 5, center + 10);
	ctx.lineTo(canvas.width - 30, center);
	ctx.closePath();
	ctx.fill();
}

// Spin logic
function spin() {
  if (spinning) return;

  spinning = true;
  let speed = Math.random() * 0.3 + 0.25;

  function animate() {
    rotation += speed;
    speed *= 0.98; // friction

    drawWheel();

    if (speed > 0.002) {
      requestAnimationFrame(animate);
    } else {
      spinning = false;
      announceWinner();
    }
  }

  animate();
}

function announceWinner() {
  const normalizedRotation =
    (2 * Math.PI - (rotation % (2 * Math.PI))) % (2 * Math.PI);

  const index =
    Math.floor(normalizedRotation / sliceAngle) % names.length;

  alert("Winner: " + names[index]);
}

drawWheel();
document.getElementById("spin").addEventListener("click", spin);
