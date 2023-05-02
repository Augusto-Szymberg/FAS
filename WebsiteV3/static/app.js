const chatForm = document.getElementById("chat-form");
const chatbox = document.getElementById("chatbox");
const input = document.getElementById("input");
const menuHeader = document.getElementById("menu-header");
const menuContainer = document.getElementById("menu-container");

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    addMessageToChatbox(`Vos: ${message}`);
    input.value = "";
    input.focus();

    const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: message })
    });

    const responseText = await response.text();
    addMessageToChatbox(`Mesero: ${responseText}`);
});

function addMessageToChatbox(message) {
    const messageElement = document.createElement("div");
    messageElement.className = "message";

    // Split the message on the newline character and wrap each line in a <p> element
    const lines = message.split("\n");
    lines.forEach((line) => {
        const p = document.createElement("p");
        p.innerText = line;
        messageElement.appendChild(p);
    });

    chatbox.appendChild(messageElement);
    chatbox.scrollTop = chatbox.scrollHeight;
}


menuBtn.addEventListener("click", () => {
    menuContainer.classList.remove("hidden");
});

closeMenuBtn.addEventListener("click", () => {
    menuContainer.classList.add("hidden");
});

let isMouseDownOnMenuHeader = false;
let startY;
let menuTransformY = 0;

menuHeader.addEventListener("mousedown", (event) => {
    isMouseDownOnMenuHeader = true;
    startY = event.clientY;
});

window.addEventListener("mousemove", (event) => {
    if (isMouseDownOnMenuHeader) {
        const deltaY = startY - event.clientY;
        menuTransformY = Math.min(Math.max(menuTransformY + deltaY, -menuContainer.offsetHeight + 50), 0);
        menuContainer.style.transform = `translateX(-50%) translateY(${menuTransformY}px)`;
        startY = event.clientY;
    }
});

window.addEventListener("mouseup", () => {
    isMouseDownOnMenuHeader = false;
});

const loginBtn = document.getElementById("login-btn");

loginBtn.addEventListener("click", () => {
    window.location.href = "/login"; 
});

const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const password = document.getElementById("password").value.trim();
    if (!password) return;

    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ password: password })
    });

    if (response.ok) {
        window.location.href = "/admin";
    } else {
        alert("Incorrect password. Please try again.");
    }
});



