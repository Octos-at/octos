<?php
if($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $message = htmlspecialchars($_POST['message']);

    $to = "info@octos.at";
    $subject = "New message from website contact form";
    $body = "Name: $name
Email: $email
Message:
$message";
    $headers = "From: noreply@octos.at
";
    $headers .= "Reply-To: $email
";

    if(mail($to, $subject, $body, $headers)) {
        echo "success";
    } else {
        echo "error";
    }
}
?>