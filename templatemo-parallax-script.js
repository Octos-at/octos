// Contact form submission
var contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function () {
        alert('Thank you! Your message has been sent.');
    });
}
<script>
document.getElementById("contactForm").addEventListener("submit", function(event){
    event.preventDefault();

    emailjs.send("service_3kflnuh", "template_un57291)", {
        name: this.name.value,
        email: this.email.value,
        message: this.message.value,
        to_email: "info@octos.at"
    })
    .then(() => {
        alert("Thank you! Your message has been sent.");
        this.reset();
    }, (error) => {
        alert("Error sending message. Please try again.");
        console.log(error);
    });
});
</script>
``
