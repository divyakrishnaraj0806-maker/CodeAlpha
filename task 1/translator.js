const translateBtn = document.getElementById("translateBtn");
const textInput = document.getElementById("textInput");
const sourceLang = document.getElementById("sourceLang");
const targetLang = document.getElementById("targetLang");
const resultDiv = document.getElementById("result");

// Free Google Translate API endpoint
// No API key required for this demo (uses unofficial endpoint)
async function translateText(text, from, to) {
    resultDiv.innerText = "Translating...";

    try {
        const response = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${from}|${to}`);
        const data = await response.json();

        if (data.responseData && data.responseData.translatedText) {
            resultDiv.innerText = data.responseData.translatedText;
        } else {
            resultDiv.innerText = "Translation failed!";
        }
    } catch (error) {
        resultDiv.innerText = "Error: " + error.message;
    }
}

translateBtn.addEventListener("click", () => {
    const text = textInput.value.trim();
    if (!text) {
        alert("Please enter text to translate.");
        return;
    }
    translateText(text, sourceLang.value, targetLang.value);
});