const canvas = document.querySelector("#canva");
const ctx = canvas.getContext("2d");
let width_1 = window.innerWidth;
let height_2 = window.innerHeight;
const colors = ["#1D5B79", "#468B97", "#EF6262", "#F3AA60"];
const mousePos = {
  mouseX: undefined,
  mouseY: undefined,
};
let balls = [];

addEventListener("mousemove", (e) => {
  mousePos.mouseX = e.clientX;
  mousePos.mouseY = e.clientY;
});

canvas.width = width_1;
canvas.height = height_2;

window.addEventListener("resize", () => {
  width_1 = window.innerWidth;
  height_2 = window.innerHeight;
  canvas.width = width_1;
  canvas.height = height_2;
  init();
});

class Balls {
  constructor() {
    this.radius = 20;
    this.x = Math.random() * (width_1 - this.radius * 2) + this.radius;
    this.y = Math.random() * (height_2 - this.radius * 2) + this.radius;
    this.colors = colors[Math.round(Math.random() * (colors.length - 1))];
    this.velocity = {
      x: Math.random() * 5,
      y: Math.random() * 5,
    };
    this.mass = 1;
    this.opacity = 0.2;
  }
  draw() {
    ctx.beginPath();
    ctx.fillStyle = `${this.colors}`;
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.save();
    ctx.globalAlpha = this.opacity;
    ctx.fill();
    ctx.restore();
    ctx.stroke();
    ctx.closePath();
  }
  update(particle) {
    for (let j = 0; j < particle.length; j++) {
      if (this === particle[j]) continue;

      if (
        collesionDistance(particle[j].x, this.x, particle[j].y, this.y) -
          particle[j].radius -
          this.radius <
        0
      ) {
        resolveCollision(this, particle[j]);
      }
    }

    if (
      this.x + this.radius + this.velocity.x > canvas.width ||
      this.x - this.radius + this.velocity.y < 0
    ) {
      this.velocity.x = -this.velocity.x;
    }

    if (
      this.y + this.radius + this.velocity.y > canvas.height ||
      this.y - this.radius + this.velocity.y < 0
    ) {
      this.velocity.y = -this.velocity.y;
    }
    this.x += this.velocity.x;
    this.y += this.velocity.y;
    this.draw();
  }
}

function resolveCollision(particle, otherParticle) {
  const xVelocityDiff = particle.velocity.x - otherParticle.velocity.x;
  const yVelocityDiff = particle.velocity.y - otherParticle.velocity.y;

  const xDist = otherParticle.x - particle.x;
  const yDist = otherParticle.y - particle.y;

  // Prevent accidental overlap of particles
  if (xVelocityDiff * xDist + yVelocityDiff * yDist >= 0) {
    // Grab angle between the two colliding particles
    const angle = -Math.atan2(
      otherParticle.y - particle.y,
      otherParticle.x - particle.x
    );

    // Store mass in var for better readability in collision equation
    const m1 = particle.mass;
    const m2 = otherParticle.mass;

    // Velocity before equation
    const u1 = rotate(particle.velocity, angle);
    const u2 = rotate(otherParticle.velocity, angle);

    // Velocity after 1d collision equation
    const v1 = {
      x: (u1.x * (m1 - m2)) / (m1 + m2) + (u2.x * 2 * m2) / (m1 + m2),
      y: u1.y,
    };
    const v2 = {
      x: (u2.x * (m1 - m2)) / (m1 + m2) + (u1.x * 2 * m2) / (m1 + m2),
      y: u2.y,
    };

    // Final velocity after rotating axis back to original location
    const vFinal1 = rotate(v1, -angle);
    const vFinal2 = rotate(v2, -angle);

    // Swap particle velocities for realistic bounce effect
    particle.velocity.x = vFinal1.x;
    particle.velocity.y = vFinal1.y;

    otherParticle.velocity.x = vFinal2.x;
    otherParticle.velocity.y = vFinal2.y;
  }
}

function rotate(velocity, angle) {
  const rotatedVelocities = {
    x: velocity.x * Math.cos(angle) - velocity.y * Math.sin(angle),
    y: velocity.x * Math.sin(angle) + velocity.y * Math.cos(angle),
  };

  return rotatedVelocities;
}

/**
 * detecteCollesion - detect collesion between balls
 * @element: an instance of balls
 * @list: an array of balls
 * Return: true in case of collesion and false if not
 */
function detecteCollesion(element, list) {
  for (let i = 0; i < list.length; i++) {
    let zDistance = collesionDistance(
      list[i].x,
      element.x,
      list[i].y,
      element.y
    );
    if (zDistance - element.radius - list[i].radius < 0) {
      return true;
    }
  }
  return false;
}

function collesionDistance(x1, x2, y1, y2) {
  let xDistance = x1 - x2;
  let yDistance = y1 - y2;
  return Math.sqrt(Math.pow(xDistance, 2) + Math.pow(yDistance, 2));
}

function init() {
  balls = [];
  let i = 0;
  while (balls.length < 20 && i < 100) {
    let newBall = new Balls();
    if (!detecteCollesion(newBall, balls)) {
      balls.push(newBall);
    }
    i++;
  }
}

function Animate() {
  ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
  ctx.beginPath();
  for (let i = 0; i < balls.length; i++) {
    balls[i].update(balls);
    if (
      collesionDistance(
        balls[i].x,
        mousePos.mouseX,
        balls[i].y,
        mousePos.mouseY
      ) <
      balls[i].radius + 100
    ) {
      balls[i].opacity += 0.02;
    }
  }
  requestAnimationFrame(Animate);
}

Animate();
init();
