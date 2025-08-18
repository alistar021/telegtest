addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request))
})

const TOKEN = "8476998300:AAEk3pHApz2Ex1GbZjX7fFc6qL883opak2A";
const CHANNEL = "@alialisend123";
const PHOTO_URL = "https://example.com/image.jpg"; // لینک عکس

async function handleRequest(request) {
  try {
    // دانلود عکس
    const res = await fetch(PHOTO_URL);
    const blob = await res.blob();
    const formData = new FormData();
    formData.append("chat_id", CHANNEL);
    formData.append("photo", blob, "image.jpg");

    // ارسال عکس به تلگرام
    const telegramRes = await fetch(`https://api.telegram.org/bot${TOKEN}/sendPhoto`, {
      method: "POST",
      body: formData
    });

    const result = await telegramRes.json();
    return new Response("عکس ارسال شد: " + JSON.stringify(result));
  } catch (err) {
    return new Response("خطا: " + err, { status: 500 });
  }
}
