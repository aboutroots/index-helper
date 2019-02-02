// set date in footer
const date = document.querySelector("#date");
let year = new Date().getFullYear();
date.innerHTML = year;

// update label text
const fileInput = document.querySelector("#file-input");
const uploadLabel = document.querySelector("#upload-label");

fileInput.onchange = () => {
  let filePath = fileInput.value.split("\\");
  let fileName = filePath[filePath.length - 1];
  uploadLabel.textContent = fileName;
};

// submit form
const runBtn = document.querySelector(".run-btn");
const fileForm = document.querySelector("#file-form");
const data = new URLSearchParams(new FormData(fileForm));
runBtn.addEventListener("click", () => {
  if (fileInput.files.length) {
    fetch('', {
        method: 'post',
        body: data,
    })
    .then();
  }
});
