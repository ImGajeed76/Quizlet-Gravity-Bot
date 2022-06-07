let lastWords = ""
setTimeout(() => {
    a(10)
}, $timeout$)

function a(delay) {
    setTimeout(() => {
        check()
        b(delay)
    }, delay)
}

function b(delay) {
    setTimeout(() => {
        check()
        a(delay)
    }, delay)
}

function check() {
    copyWords()
}

function copyWords() {
    let elements = document.getElementsByClassName('GravityTerm-text');
    let words = "";
    for (const element of elements) {
        let child = element.firstChild;
        words += child.innerHTML + ";;";
    }
    if (words !== "") {
        console.log(words.split(";;"))
        lastWords = words
        navigator.clipboard.writeText(words);
    }
}