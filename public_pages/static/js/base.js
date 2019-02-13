// set date in footer
const date = document.querySelector("#date");
let year = new Date().getFullYear();
date.innerHTML = year;

// set help items opacity to 1 after 1

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

async function loadSpinner() {
  respBox.innerHTML = `
    <div class="spinner">
      <div class="bounce1"></div>
      <div class="bounce2"></div>
      <div class="bounce3"></div>
    </div>
  `;
  respBox.classList.add("spinner-wrap");
  respBox.classList.add("expanded");
}

function handleForm() {
  if (fileInput.files.length) {
    // check if file is a txt file
    const extension = fileInput.files[0].name.split(".").pop();
    if (extension !== "txt") {
      respBox.textContent =
        'Please make sure to select a simple text file (with ".txt" extension)';
      respBox.classList.add("expanded");
      return;
    }

    loadSpinner();
    const formData = new FormData(fileForm);
    const options = {
      method: "POST",
      body: formData
    };
    fetch("", options)
      .then(resp => resp.json())
      .then(json => {
        respBox.classList.remove("spinner-wrap");
        if (json.success) {
          respBox.innerHTML = `<a href="${
            json.uploaded_file_url
          }" download="index_new.txt"><i class="fa fa-download"> <span>index_new.txt</span></i></a>`;
          respBox.classList.add("expanded");
        } else {
          console.log(json.error);
          respBox.innerHTML = json.error;
          respBox.classList.add("expanded");
        }
      })
      .catch(reason => {
        respBox.classList.remove("spinner-wrap");
        console.log(`Promise rejected with reason: ${reason}`);
        respBox.textContent =
          "Some strange error occurred. Please contact let me (aboutroots) know about it!";
        respBox.classList.add("expanded");
      });
  }
}
runBtn.addEventListener("click", handleForm);

//copy problematic line to clipboard on click
respBox.addEventListener("click", () => {
  let range = document.createRange();
  let badLine = document.getElementById("bad-line");
  if (!badLine) return;
  range.selectNode(badLine);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand("copy");
});

// hide warning message on click
respBox.addEventListener("click", () => respBox.classList.remove("expanded"));
