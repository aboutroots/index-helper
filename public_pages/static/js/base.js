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
const downloadWrapper = document.querySelector("#download-wrapper");
const downloadLink = document.querySelector("#download-wrapper a");
runBtn.addEventListener("click", () => {
  if (fileInput.files.length) {
    const formData = new FormData(fileForm);
    const options = {
      method: 'POST',
      body: formData,
    };
    fetch('', options)
      .then(resp => resp.json())
      .then( json => {
        downloadWrapper.classList.toggle("hidden");
        downloadLink['href'] = json['uploaded_file_url']
      });
  }
});

// TODO: parser
// todo: heroku