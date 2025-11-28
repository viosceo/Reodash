<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMS Gönderme Arayüzü</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <!-- SMS Formu Çerçevesi -->
        <div class="sms-form">
            <img src="../../assets/main/img/sms.png" alt="SMS Icon" class="sms-icon">
            <h2>SMS BLOOMS V2</h2>
            <form id="smsForm">
                <input type="text" id="phoneNumber" placeholder="544909xx" required>
                <button type="submit">Gönder</button>
            </form>
            <div id="responseMessage"></div>
        </div>

        <!-- Site Durumu Çerçevesi -->
        <div class="site-status">
            <p id="siteStatusMessage">API Durumu: <span id="statusText">Aktif</span></p>
            <p id="successMessage"></p>
            <p id="doc"></p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>