/*=====================
  Custom Sweet Alert Js
==========================*/
(function () {
  const alertButtons = document.querySelectorAll(".common-alert, .wishlist-alert");

  const alertMessages = {
    "common-alert": "Successfully added to your bag!",
    "wishlist-alert": "Added to your wishlist!",
  };

  alertButtons.forEach((button) => {
    button.addEventListener("click", () => {
      let alertMessage = "Default message";
      for (const [className, message] of Object.entries(alertMessages)) {
        if (button.classList.contains(className)) {
          alertMessage = message;
          break;
        }
      }

      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = Swal.stopTimer;
          toast.onmouseleave = Swal.resumeTimer;
        },
      });

      Toast.fire({
        icon: "success",
        title: alertMessage,
      });
    });
  });
})();
