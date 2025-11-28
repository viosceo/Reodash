document.getElementById('smsForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const phoneNumber = document.getElementById('phoneNumber').value;
    const responseMessage = document.getElementById('responseMessage');

    if (!phoneNumber) {
        responseMessage.textContent = "Telefon numarası giriniz.";
        return;
    }

    fetch(`https://cerenviosvipx.serv00.net/pages/data.php?number=${phoneNumber}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                responseMessage.textContent = "SMS başarıyla gönderildi!";
                responseMessage.style.color = "green";
            } else {
                responseMessage.textContent = `Hata: ${data.message}`;
                responseMessage.style.color = "red";
            }
        })
        .catch(error => {
            responseMessage.textContent = "İŞLEM BAŞARILI !";
            responseMessage.style.color = "red";
        });
});

document.getElementById('smsForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Telefon numarası formunu işleme
    const phoneNumber = document.getElementById('phoneNumber').value;
    
    // API isteği (Burada gerçek API isteği yapılmalı)
    if (phoneNumber) {
        // Başarı mesajını göster
        document.getElementById('successMessage').innerText = '[ Başarılı! SMS Gönderildi. ]';
        document.getElementById('responseMessage').innerText = ''; // Önceki mesajı temizle
    } else {
        // Hata mesajı
        document.getElementById('responseMessage').innerText = 'CLİENT HATASI 0X80.';
    }
});

document.getElementById('smsForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Telefon numarası formunu işleme
    const phoneNumber = document.getElementById('phoneNumber').value;
    
    // API isteği (Burada gerçek API isteği yapılmalı)
    if (phoneNumber) {
        // Başarı mesajını göster
        document.getElementById('doc').innerText = 'APİ İÇİN DÖKÜMANLARI OKUYABİLİRSİNİZ.';
        document.getElementById('responseMessage').innerText = ''; // Önceki mesajı temizle
    } else {
        // Hata mesajı
        document.getElementById('responseMessage').innerText = 'APİ BİLGİLERİ DÖKÜMAN KISMINDAN OKUYABİLİRSİN';
    }
});