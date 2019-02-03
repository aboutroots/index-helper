// set date in footer
const date = document.querySelector("#date");
let year = new Date().getFullYear();
date.innerHTML = year;

// update label text
const fileInput = document.querySelector("#file-input");
const uploadLabel = document.querySelector("#upload-label");

if (fileInput) {
  fileInput.onchange = () => {
    let filePath = fileInput.value.split("\\");
    let fileName = filePath[filePath.length - 1];
    uploadLabel.textContent = fileName;
  };
}

// submit form
const runBtn = document.querySelector(".run-btn");
const fileForm = document.querySelector("#file-form");
const downloadWrapper = document.querySelector("#download-wrapper");
const downloadLink = document.querySelector("#download-wrapper a");
const infoBox = document.querySelector("#info-box");
downloadWrapper.style.transition = "all 0.5s";
infoBox.style.transition = "all 0.5s";

runBtn.addEventListener("click", () => {
  if (fileInput.files.length) {
    const formData = new FormData(fileForm);
    const options = {
      method: "POST",
      body: formData
    };
    fetch("", options)
      .then(resp => resp.json())
      .then(json => {
        if (json.success) {
          downloadWrapper.classList.add("expanded");
          downloadLink.href = json.uploaded_file_url;
          infoBox.innerHTML = "";
          infoBox.classList.remove("expanded");
        } else {
          infoBox.innerHTML = json.error;
          infoBox.classList.add("expanded");
          downloadWrapper.classList.remove("expanded");
          console.log(json.error);
        }
      })
      .catch(reason => {
        console.log(`Promise rejected with reason: ${reason}`);
        infoBox.textContent =
          "Some strange error occurred. Please contact let me (aboutroots) know about it!";
        infoBox.classList.add("expanded");
        downloadWrapper.classList.remove("expanded");
      });
  }
});

// hide warning message on click
infoBox.addEventListener("click", () => infoBox.classList.remove("expanded"));
