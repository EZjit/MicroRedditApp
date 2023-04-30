const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;


// Reply button

document.addEventListener(
  "click",
  function(event) {
      var target = event.target;
      var replyForm;
      if (target.matches("[data-toggle='reply-form']")) {
          replyForm = document.getElementById(target.getAttribute("data-target"));
          replyForm.classList.toggle("d-none");
      }
  },
  false
);