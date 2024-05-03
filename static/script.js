function checkInputLength() {
  const textInput = document.getElementById("textInput");
  const text = textInput.value.trim();
  const summaryLength = (
    parseInt(document.getElementById("wordLimitSlider").value) * 50
  ).toString();

  // Calculate the number of words in the input text
  const wordCount = text.split(/\s+/).length;

  // Compare the word count with the summary length
  if (wordCount < summaryLength) {
    // If input text exceeds the summary length, alert the user
    alert(
      "Input text exceeds the selected summary length. Please provide a shorter input text."
    );
    return false; // Return false to indicate that summarization should not proceed
  } else {
    return true; // Return true to indicate that summarization can proceed
  }
}

function summarizeTextIfValid() {
  if (checkInputLength()) {
    summarizeText();
  }
}

function summarizeText() {
  const textInput = document.getElementById("textInput");
  const text = textInput.value;
  let summaryLength = document.getElementById("wordLimitSlider").value; // Get the selected summary length
  summaryLength = parseInt(summaryLength) * 50; // Scale the summary length by 50
  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text, summary_length: summaryLength }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("summaryText").innerText = data.summarized_text;
    });
}

function toggleTheme() {
  const body = document.body;
  const toggleIcon = document.querySelector(".theme-toggle");
  // Toggle between 'dark-mode' and 'light-mode' classes
  body.classList.toggle("dark-mode");
  body.classList.toggle("light-mode");

  // Switch icon from moon to sun and vice versa
  if (body.classList.contains("light-mode")) {
    toggleIcon.classList.replace("fa-moon", "fa-sun");
  } else {
    toggleIcon.classList.replace("fa-sun", "fa-moon");
  }
}

const slider = document.getElementById("wordLimitSlider");
const output = document.getElementById("sliderValue");

slider.oninput = function () {
  let newVal = this.value;
  switch (parseInt(this.value)) {
    case 1:
      output.innerHTML = "Extra Small (50 words)";
      break;
    case 2:
      output.innerHTML = "Small (100 words)";
      break;
    case 3:
      output.innerHTML = "Medium (150 words)";
      break;
    case 4:
      output.innerHTML = "Large (200 words)";
      break;
    default:
      output.innerHTML = "Small (50 words)";
  }
};
