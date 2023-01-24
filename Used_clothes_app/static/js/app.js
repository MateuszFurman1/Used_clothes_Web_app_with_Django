document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
  /**
   * Function showing summary in js form
   */
  const submitAgree = document.getElementById("submit-agree");
  submitAgree.addEventListener("click", showSummary);

  function showSummary() {
    const categories = document.querySelectorAll("#categories");
    let category = []
    for (let i = 0; i < categories.length; i++) {
      if (categories[i].checked) {
        category.push(categories[i].dataset.name);
      }}
    const quantity = document.getElementById("quantity").value;
    const institution = document.querySelectorAll("#institution")
    let institut = []
    for (let i = 0; i < institution.length; i++) {
      if (institution[i].checked) {
        institut.push(institution[i].dataset.name);
      }}
    const address = document.getElementById("address").value;
    const city = document.getElementById("city").value;
    const zip_code = document.getElementById("zip_code").value;
    const phone_number = document.getElementById("phone_number").value;
    const pick_up_date = document.getElementById("pick_up_date").value;
    const pick_up_time = document.getElementById("pick_up_time").value;
    const pick_up_comment = document.getElementById("pick_up_comment").value;

    document.getElementById("summary-1").innerHTML = quantity + " worki/ów, w kategorii: "+ category[0];
    document.getElementById("summary-2").innerHTML = "Dla: " + institut;
    document.getElementById("summary-3").innerHTML += "<li>" + address + "</li>";
    document.getElementById("summary-3").innerHTML += "<li>" + city + "</li>";
    document.getElementById("summary-3").innerHTML += "<li>" + zip_code + "</li>";
    document.getElementById("summary-3").innerHTML += "<li>" + phone_number + "</li>";
    document.getElementById("summary-4").innerHTML += "<li>" + pick_up_date + "</li>";
    document.getElementById("summary-4").innerHTML += "<li>" + pick_up_time + "</li>";
    document.getElementById("summary-4").innerHTML += "<li>" + pick_up_comment + "</li>";
  }

  /**
   * From- submiting using fetch
   */

  const formSubmit = document.querySelector("form");

formSubmit.addEventListener("submit", event => {

  const formData = new FormData(formSubmit);

  // Send the formData to the server
  fetch('/add-donation/', {
    method: "POST",
    body: formData
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("HTTP error, status = " + response.status);
      }
      return response.json();
    })
    .then(data => {
      console.log("Success:", data);
      // window.location.href = '/success';
    })
    .catch(error => {
      console.error("Error:", error);
    });
});



  // const submitForm = document.getElementById("submit-form");
  // submitForm.addEventListener("click", submitDate);
  //
  // function submitDate() {

    /**
   * Recznie, można tak robić ale za dużo pracy i nieprofesjonalnie. Trzeba każką zmienną wyciągnąć
     * z DOMa i ręcznie przypisać. Trzeba też zadbać o crsf_token.Wywołać funkcjię cookieValue i przypisać ją
     * do zmiennej.
     * Najlepiej stworzyć FormData. Sama ogarnie crsf/0token i przeszuka DOM w celu wyciągnięcia potrzebnych info.
   */
//     const categories = document.querySelectorAll("#categories");
//     let category = []
//     for (let i = 0; i < categories.length; i++) {
//       if (categories[i].checked) {
//         category.push(categories[i].value);
//       }}
//     const bags = document.getElementById("bags").value;
//     const institution = document.querySelectorAll("#institution")
//     let institut = []
//     for (let i = 0; i < institution.length; i++) {
//       if (institution[i].checked) {
//         institut.push(institution[i].value);
//       }}
//     const street = document.getElementById("street").value;
//     const city = document.getElementById("city").value;
//     const postcode = document.getElementById("postcode").value;
//     const phone = document.getElementById("phone").value;
//     const date = document.getElementById("date").value;
//     const time = document.getElementById("time").value;
//     const more_info = document.getElementById("more_info").value;
//     function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//     const csrf_token = getCookie('csrftoken');

    // fetch('/add-donation/', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'X-CSRFToken': csrf_token // csrf token is used for security to prevent cross-site request forgery
    //   },
    //   body: JSON.stringify({'categories': categories, 'bags': bags, 'institution': institution,
    //     'street': street, 'city': city, 'postcode': postcode, 'phone': phone, 'date': date, 'time': time, 'more_info': more_info})
    // })
    //   .then(response => response.json())
    //   .then(data => {
    //     console.log('Success:', data);
    //   })
    //   .catch((error) => {
    //     console.error('Error:', error);
    //   });

});
