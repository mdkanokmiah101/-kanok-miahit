import nodemailer from "nodemailer";

const RELAY_URL = process.env.EMAIL_RELAY_URL || "http://[2a02:4780:12:2d4a::1]:3098";
const FROM_EMAIL = "leads@kanokmiah.com.bd";
const TO_EMAIL = "mdkanokmiah101@gmail.com";

// Try 3 methods: direct MX → SMTP auth → relay
async function sendEmail({ name, email, phone, website, message }) {
  // Method 1: Direct MX delivery (no credentials, from Vercel IP)
  try {
    const transporter = nodemailer.createTransport({ direct: true });
    const html = buildHtml({ name, email, phone, website, message });
    const info = await transporter.sendMail({
      from: `"Kanok Miah - Lead" <${FROM_EMAIL}>`,
      to: TO_EMAIL,
      subject: `🔴 New SEO Lead: ${name} - ${phone}`,
      html,
    });
    console.log(`📧 Direct MX sent: ${info.messageId}`);
    return true;
  } catch (err) {
    console.log(`📧 Direct MX failed: ${err.message}`);
  }

  // Method 2: Gmail SMTP auth
  try {
    const transporter = nodemailer.createTransport({
      host: "smtp.gmail.com", port: 587, secure: false,
      auth: { user: "mdkanokmiah232@gmail.com", pass: process.env.GMAIL_APP_PASSWORD || "" },
    });
    const html = buildHtml({ name, email, phone, website, message });
    const info = await transporter.sendMail({
      from: `"Kanok Miah - Lead" <mdkanokmiah232@gmail.com>`,
      to: TO_EMAIL,
      subject: `🔴 New SEO Lead: ${name} - ${phone}`,
      html,
    });
    console.log(`📧 SMTP sent: ${info.messageId}`);
    return true;
  } catch (err) {
    console.log(`📧 SMTP failed: ${err.message}`);
  }

  // Method 3: Relay server
  try {
    const res = await fetch(`${RELAY_URL}/send-lead`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, phone, website, message }),
      signal: AbortSignal.timeout(10000),
    });
    const data = await res.json();
    if (data.success) {
      console.log(`📧 Relay sent: ${name}`);
      return true;
    }
    console.error("📧 Relay error:", data.stderr || "unknown");
  } catch (err) {
    console.error("📧 Relay failed:", err.message);
  }

  return false;
}

function buildHtml({ name, email, phone, website, message }) {
  return `<div style="font-family:Arial;max-width:600px;margin:auto;padding:20px;background:#f9f9f9">
    <div style="background:#124D1C;color:white;padding:20px;border-radius:10px 10px 0 0;text-align:center">
      <h1 style="margin:0">🔴 NEW SEO LEAD</h1>
      <p style="margin:5px 0 0;opacity:0.9">kanokmiah.com.bd</p></div>
    <div style="background:white;padding:25px;border:1px solid #e0e0e0">
      <table style="width:100%">
        <tr><td style="padding:8px;font-weight:bold">👤 Name</td><td style="padding:8px">${name||''}</td></tr>
        <tr style="background:#f5f5f5"><td style="padding:8px;font-weight:bold">📧 Email</td><td style="padding:8px">${email||''}</td></tr>
        <tr><td style="padding:8px;font-weight:bold">📞 Phone</td><td style="padding:8px">${phone||''}</td></tr>
        ${website ? `<tr style="background:#f5f5f5"><td style="padding:8px;font-weight:bold">🌐 Website</td><td style="padding:8px">${website}</td></tr>` : ''}
        ${message ? `<tr><td style="padding:8px;font-weight:bold">💬 Message</td><td style="padding:8px">${message}</td></tr>` : ''}
      </table>
      <div style="margin-top:20px;padding:15px;background:#e8f5e9;border-radius:8px;text-align:center">
        <a href="https://wa.me/8801604809110?text=Hi!%20Regarding%20your%20lead%20${encodeURIComponent(name||'')}%20(${encodeURIComponent(phone||'')})"
           style="display:inline-block;background:#25D366;color:white;text-decoration:none;padding:10px 20px;border-radius:5px">💬 WhatsApp</a>
      </div></div></div>`;
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

    // Telegram
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
