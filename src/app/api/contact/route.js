const RELAY_URL = process.env.EMAIL_RELAY_URL || "http://[2a02:4780:12:2d4a::1]:3098";

async function sendEmail({ name, email, phone, website, message }) {
  try {
    const res = await fetch(`${RELAY_URL}/send-lead`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, phone, website, message }),
      signal: AbortSignal.timeout(10000),
    });
    const data = await res.json();
    if (data.success) {
      console.log(`📧 Email relayed: ${name}`);
      return true;
    }
    console.error("📧 Relay error:", data.stderr || "unknown");
    return false;
  } catch (err) {
    console.error("📧 Relay request failed:", err.message);
    return false;
  }
}

export async function POST(request) {
  try {
    const ct = request.headers.get("content-type") || "";

    let name, email, phone, website, message, subject;

    if (ct.includes("application/json")) {
      const body = await request.text();
      try {
        const json = JSON.parse(body);
        name = json.name || "Not provided";
        email = json.email || "Not provided";
        phone = json.phone || "Not provided";
        website = json.website || "Not provided";
        message = json.message || "Not provided";
        subject = json._subject || "New SEO Lead";
      } catch {
        // If JSON parsing fails, try as formdata
        const params = new URLSearchParams(body);
        name = params.get("name") || "Not provided";
        email = params.get("email") || "Not provided";
        phone = params.get("phone") || "Not provided";
        website = params.get("website") || "Not provided";
        message = params.get("message") || "Not provided";
        subject = params.get("_subject") || "New SEO Lead";
      }
    } else {
      const formData = await request.formData();
      name = formData.get("name") || "Not provided";
      email = formData.get("email") || "Not provided";
      phone = formData.get("phone") || "Not provided";
      website = formData.get("website") || "Not provided";
      message = formData.get("message") || "Not provided";
      subject = formData.get("_subject") || "New SEO Lead";
    }

    console.log(`📬 ${subject}: ${name} / ${email} / ${phone}`);

    const emailSent = await sendEmail({ name, email, phone, website, message });
    console.log(`📧 Email result: ${emailSent ? "✅ SENT" : "❌ FAILED"}`);

    // Telegram notification (fire & forget)
    const token = process.env.TELEGRAM_BOT_TOKEN;
    if (token) {
      const text = [
        "🔔 **🔴 NEW SEO LEAD — kanokmiah.com.bd**",
        `👤 Name: ${name}`,
        `📧 Email: ${email}`,
        `📞 Phone: ${phone}`,
        `🌐 Website: ${website}`,
        `📧 Email: ${emailSent ? "✅ SENT" : "❌ FAILED"}`,
        `⏱ ${new Date().toLocaleString("en-BD", { timeZone: "Asia/Dhaka" })}`,
      ].join("\n");
      fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: "7203982414", text, parse_mode: "Markdown" }),
      }).catch(() => {});
    }

    return Response.json({
      success: true,
      email_sent: emailSent,
      message: "Thank you! Your message has been sent.",
    });
  } catch (err) {
    console.error("Form error:", err);
    return Response.json({ success: false, message: "Something went wrong." }, { status: 500 });
  }
}
