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
    uploadLabel.innerHTML = `<i class="fa fa-cloud-upload-alt"></i>
      <span id="upload-text">${fileName || "Select a file"}</span>`;
  };
}

// submit form
const runBtn = document.querySelector("#run-icon");
const fileForm = document.querySelector("#file-form");
const respBox = document.querySelector("#resp-box");
// const downloadLink = document.querySelector("#download-wrapper a");
// const infoBox = document.querySelector("#info-box");
// downloadWrapper.style.transition = "all 0.5s";
// infoBox.style.transition = "all 0.5s";

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
          respBox.classList.add("expanded");
          respBox.innerHTML = `<a href="${json.uploaded_file_url}" download="index_new.txt"><i class="fa fa-download"> <span>index_new.txt</span></i></a>`;
        } else {
          console.log(json.error);
          respBox.innerHTML = json.error;
          respBox.classList.add("expanded");
          // downloadWrapper.classList.remove("expanded");
        }
      })
      .catch(reason => {
        console.log(`Promise rejected with reason: ${reason}`);
        respBox.textContent =
          "Some strange error occurred. Please contact let me (aboutroots) know about it!";
        respBox.classList.add("expanded");
        // downloadWrapper.classList.remove("expanded");
      });
  }
});

//copy problematic line to clipboard on click
respBox.addEventListener("click", () => {
  let range = document.createRange();
  let badLine = document.getElementById("bad-line");
  if (!badLine) return
  range.selectNode(badLine);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand("copy");
});
// hide warning message on click
respBox.addEventListener("click", () => respBox.classList.remove("expanded"));
