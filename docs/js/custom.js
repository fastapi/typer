document.querySelectorAll(".use-termynal").forEach(node => {
    node.style.display = "block";
    new Termynal(node, {
        lineDelay: 500
    });
});
const progressLiteralStart = "---> 100%";
const promptLiteralStart = "$ ";
const termynalActivateClass = "termy";
let termynals = [];

function createTermynals() {
    document
        .querySelectorAll(`.${termynalActivateClass} .codehilite`)
        .forEach(node => {
            const text = node.textContent;
            const lines = text.split("\n");
            const useLines = [];
            let buffer = [];
            function saveBuffer() {
                if (buffer.length) {
                    let isBlankSpace = true;
                    buffer.forEach(line => {
                        if (line) {
                            isBlankSpace = false;
                        }
                    });
                    dataValue = {};
                    if (isBlankSpace) {
                        dataValue["delay"] = 0;
                    }
                    if (buffer.length > 1 && buffer[buffer.length - 1] === "") {
                        // The last single <br> won't have effect
                        // so put an additional one
                        buffer.push("");
                    }
                    const bufferValue = buffer.join("<br>");
                    dataValue["value"] = bufferValue;
                    useLines.push(dataValue);
                    buffer = [];
                }
            }
            for (let line of lines) {
                if (line === progressLiteralStart) {
                    saveBuffer();
                    useLines.push({
                        type: "progress"
                    });
                } else if (line.startsWith(promptLiteralStart)) {
                    saveBuffer();
                    const value = line.replace(promptLiteralStart, "").trimEnd();
                    useLines.push({
                        type: "input",
                        value: value
                    });
                } else if (line.startsWith("// ")) {
                    saveBuffer();
                    const value = line.replace("// ", "").trimEnd();
                    useLines.push({
                        value: value,
                        class: "termynal-comment",
                        delay: 0
                    });
                } else {
                    buffer.push(line);
                }
            }
            saveBuffer();
            const div = document.createElement("div");
            node.replaceWith(div);
            const termynal = new Termynal(div, {
                lineData: useLines,
                noInit: true,
                lineDelay: 500
            });
            termynals.push(termynal);
        });
}

function loadVisibleTermynals() {
    termynals = termynals.filter(termynal => {
        if (termynal.container.getBoundingClientRect().top - innerHeight <= 0) {
            termynal.init();
            return false;
        }
        return true;
    });
}
window.addEventListener("scroll", loadVisibleTermynals);
createTermynals();
loadVisibleTermynals();
