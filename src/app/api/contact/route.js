"use server";

export async function POST(request) {
  try {
    const formData = await request.formData();

    const name = formData.get("name") || "Not provided";
    const email = formData.get("email") || "Not provided";
    const phone = formData.get("phone") || "Not provided";
    const website = formData.get("website") || "Not provided";
    const message = formData.get("message") || "Not provided";
    const subject = formData.get("_subject") || "New SEO Lead";

    // Log the submission
    console.log(`📬 ${subject}: ${name} / ${email} / ${phone}`);

    // Log to leads file for cron job processing
    try {
      const fs = require("fs");
      const leadRecord = `[${new Date().toISOString()}] ${name} | ${email} | ${phone} | ${website} | ${subject}\n`;
      fs.appendFileSync("/root/.hermes/leads.log", leadRecord);
    } catch(e) {}

    // Try WhatsApp lead notification bot
    try {
      fetch("http://127.0.0.1:3099/send-lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, phone, website, subject }),
        signal: AbortSignal.timeout(3000),
      }).catch(() => {});
    } catch(e) {}

    // Try Telegram notification
    const token = process.env.TELEGRAM_BOT_TOKEN;
    if (token) {
      const text = `🔔 **🔴 NEW SEO LEAD — kanokmiah.com.bd**
👤 Name: ${name}
📧 Email: ${email}
📞 Phone: ${phone}
🌐 Website: ${website}
💬 Message: ${message}
📱 WhatsApp: https://wa.me/8801604809110?text=${encodeURIComponent(`New lead: ${name} - ${phone}`)}
⏱ ${new Date().toLocaleString("en-BD", { timeZone: "Asia/Dhaka" })}`;
      fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: "7203982414", text, parse_mode: "Markdown" }),
      }).catch(() => {});
    }

    return Response.json({ 
      success: true, 
      message: "Thank you! Your message has been sent.",
      whatsapp: "https://wa.me/8801604809110?text=Hi%20Md%20Kanok%20Miah!%20I%20just%20submitted%20the%20contact%20form%20on%20your%20website.%20Please%20get%20back%20to%20me."
    });
  } catch (err) {
    console.error("Form error:", err);
    return Response.json({ success: false, message: "Something went wrong. Please try again." }, { status: 500 });
  }
}
