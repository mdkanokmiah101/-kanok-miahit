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

    // Try Telegram notification (optional)
    const token = process.env.TELEGRAM_BOT_TOKEN;
    if (token) {
      const text = `🔔 **New SEO Lead**
👤 Name: ${name}
📧 Email: ${email}
📞 Phone: ${phone}
🌐 Website: ${website}
💬 ${message}
⏱ ${new Date().toLocaleString("en-BD", { timeZone: "Asia/Dhaka" })}`;
      fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: "7203982414", text, parse_mode: "Markdown" }),
      }).catch(() => {});
    }

    return Response.json({ success: true, message: "Thank you! Your message has been sent." });
  } catch (err) {
    console.error("Form error:", err);
    return Response.json({ success: false, message: "Something went wrong. Please try again." }, { status: 500 });
  }
}
