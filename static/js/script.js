/* ==========================================
   DOM READY - Upload Preview Logic
========================================== */
document.addEventListener("DOMContentLoaded", function () {

    const uploadBox = document.getElementById("uploadBox");
    const fileInput = document.getElementById("fileInput");
    const previewImage = document.getElementById("previewImage");
    const uploadContent = document.getElementById("uploadContent");

    if (uploadBox && fileInput) {

        uploadBox.addEventListener("click", function () {
            fileInput.click();
        });

        fileInput.addEventListener("change", function () {
            const file = this.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewImage.style.display = "block";
                uploadContent.style.display = "none";
            };
            reader.readAsDataURL(file);
        });
    }

});


/* ==========================================
   GLOBAL VARIABLES
========================================== */
let originalText = "";
let audioPlayer = null;
let isPlaying = false;


/* ==========================================
   CLEAN TEXT
========================================== */
function cleanText(text) {
    if (!text) return "";
    return text
        .replace(/\*\*/g, "")
        .replace(/\*/g, "")
        .trim();
}


/* ==========================================
   FORMAT RESULT (Structured Output UI)
========================================== */
function formatResult(text){

    text = cleanText(text);

    const container = document.getElementById("result");
    container.innerHTML = "";

    const lines = text.split("\n").filter(line => line.trim() !== "");

    let ul = null;
    let isFirstLine = true;

    lines.forEach(line => {

        const cleanLine = cleanText(line);

        // Medicine Name
        if (isFirstLine) {
            const title = document.createElement("h2");
            title.className = "medicine-title";
            title.textContent = cleanLine.replace(":", "").trim();
            container.appendChild(title);
            isFirstLine = false;
            return;
        }

        // Section Titles
        if (cleanLine.endsWith(":") && cleanLine.length < 50) {

            if (ul) {
                container.appendChild(ul);
                ul = null;
            }

            const section = document.createElement("h3");
            section.className = "section-title";
            section.textContent = cleanLine.replace(":", "");
            container.appendChild(section);

            ul = document.createElement("ul");
            return;
        }

        // Bullet Points
        if (!ul) {
            ul = document.createElement("ul");
        }

        const li = document.createElement("li");
        li.textContent = cleanLine.replace(/^-/, "").trim();
        ul.appendChild(li);
    });

    if (ul) {
        container.appendChild(ul);
    }
}


/* ==========================================
   ANALYZE FUNCTION
========================================== */
function analyze() {

    const file = document.getElementById("fileInput").files[0];

    if(!file){
        alert("Please upload an image first.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    document.getElementById("result").innerHTML =
        "<p style='color:#2563eb;'>Analyzing image... Please wait.</p>";

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log("ANALYZE RESPONSE:", data); // 👈 ADD THIS

        if(data.error){
            document.getElementById("result").innerHTML =
                "<p style='color:red;'>Error: " + data.error + "</p>";
            return;
        }

        originalText = data.result;
        formatResult(originalText);
    })
    .catch(() => {
        document.getElementById("result").innerHTML =
            "<p style='color:red;'>Something went wrong.</p>";
    });
}


/* ==========================================
   TRANSLATE FUNCTION
========================================== */
function confirmTranslate(){

    if(!originalText){
        alert("Analyze medicine first.");
        return;
    }

    const lang = document.getElementById("modalLanguage").value;

    document.getElementById("result").innerHTML =
        "<p style='color:#2563eb;'>Translating...</p>";

    fetch("/translate", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            text: originalText,
            lang: lang
        })
    })
    .then(res => res.json())
    .then(data => {

        if(data.error){
            document.getElementById("result").innerHTML =
                "<p style='color:red;'>"+data.error+"</p>";
            return;
        }

        originalText = data.translated;
        formatResult(originalText);
    })
    .catch(() => {
        document.getElementById("result").innerHTML =
            "<p style='color:red;'>Server connection failed.</p>";
    });
}


/* ==========================================
   TEXT TO SPEECH (With Toggle + Loading)
========================================== */
function speakText() {

    if(!originalText){
        alert("Analyze medicine first.");
        return;
    }

    const lang = document.getElementById("modalLanguage").value;
    const ttsButton = document.getElementById("ttsButton");

    // Stop if playing
    if(isPlaying && audioPlayer){
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        isPlaying = false;
        ttsButton.innerHTML = "🔊 Listen";
        return;
    }

    ttsButton.innerHTML = "⏳ Preparing audio...";
    ttsButton.disabled = true;

    fetch("/tts", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            text: originalText,
            lang: lang
        })
    })
    .then(res => res.json())
    .then(data => {

        if(data.error){
            alert("Speech failed.");
            ttsButton.innerHTML = "🔊 Listen";
            ttsButton.disabled = false;
            return;
        }

        audioPlayer = new Audio(data.audio_url);

        audioPlayer.play();
        isPlaying = true;

        ttsButton.innerHTML = "⏹ Stop";
        ttsButton.disabled = false;

        audioPlayer.onended = function(){
            isPlaying = false;
            ttsButton.innerHTML = "🔊 Listen";
        };
    })
    .catch(() => {
        alert("Speech failed.");
        ttsButton.innerHTML = "🔊 Listen";
        ttsButton.disabled = false;
    });
}

/* ==========================================
   NAVBAR ACTIVE LINK ON SCROLL
========================================== */

const sections = [
    { id: "home", nav: null }, 
    { id: "features", nav: "nav-features" },
    { id: "how-it-works", nav: "nav-how" },
    { id: "analyzer", nav: "nav-analyzer" }
];

const navButtons = document.querySelectorAll(".nav-btn");

function setActiveNav() {
    let scrollPos = window.scrollY + window.innerHeight / 3;

    sections.forEach(section => {
        const el = document.getElementById(section.id);
        const nav = document.getElementById(section.nav);

        if (!el || !nav) return;

        const top = el.offsetTop;
        const height = el.offsetHeight;

        if (scrollPos >= top && scrollPos < top + height) {
            navButtons.forEach(btn => btn.classList.remove("active"));
            nav.classList.add("active");
        }
    });
}

window.addEventListener("scroll", setActiveNav);
window.addEventListener("load", setActiveNav);

// ================= MAKE FUNCTIONS GLOBAL =================
window.analyze = analyze;
window.confirmTranslate = confirmTranslate;
window.speakText = speakText;

