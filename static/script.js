const button = document.getElementById("roastButton");
const resumeBox = document.getElementById("resume");
const result = document.getElementById("result");

button.addEventListener("click", async () => {

    const resume = resumeBox.value.trim();

    if (!resume) {
        result.innerText = "Bro... give me a resume first. 😭";
        return;
    }

    button.disabled = true;
    button.innerText = "Roasting... 🔥";
    result.innerText = "AI is judging your resume...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resume: resume
            })
        });

        const data = await response.json();

        if (data.error) {
            result.innerText = data.error;
            return;
        }

        result.innerHTML = `
            <h2>Your Resume Roast 🔥</h2>
            <div class="feedback">
                ${data.feedback.replace(/\n/g, "<br>")}
            </div>
        `;

    } catch (error) {
        result.innerText =
            "Something went wrong. Check the terminal for details.";
        console.error(error);

    } finally {
        button.disabled = false;
        button.innerText = "Roast My Resume 🔥";
    }
});