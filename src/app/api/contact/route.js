"use server";

export async function POST(request) {
  try {
    const formData = await request.formData();
    
    const name = formData.get("name") || "Not provided";
    const email = formData.get("email") || "Not provided";
    const phone = formData.get("phone") || "Not provided";
    const website = formData.get("website") || "Not provided";
    const message = formData.get("message") || "Not provided";

    // Format the message for Telegram
    const text = `🔔 **New SEO Lead!**
👤 Name: ${name}
📧 Email: ${email}
📞 Phone: ${phone}
🌐 Website: ${website}
💬 Message: ${message}
⏱ Time: ${new Date().toLocaleString("en-BD", { timeZone: "Asia/Dhaka" })}`;

    // Try sending via Telegram bot
    const telegramToken = process.env.TELEGRAM_BOT_TOKEN;
    const telegramChatId = "7203982414";

    if (telegramToken) {
      await fetch(`https://api.telegram.org/bot${telegramToken}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: telegramChatId,
          text: text,
          parse_mode: "Markdown",
        }),
      });
    }

    // Try sending email via Nodemailer
    try {
      const nodemailer = await import("nodemailer");
      const transporter = nodemailer.default.createTransport({
        host: "smtp.gmail.com",
        port: 587,
        secure: false,
        auth: {
          user: "mdkanokmiah101@gmail.com",
          pass: process.env.GMAIL_APP_PASSWORD || "",
        },
      });

      await transporter.sendMail({
        from: '"Md Kanok Miah Website" <mdkanokmiah101@gmail.com>',
        to: "mdkanokmiah101@gmail.com",
        subject: "🔔 New SEO Lead from Website!",
        html: `
          <h2>New SEO Lead</h2>
          <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;font-family:Arial">
            <tr><td><b>Name</b></td><td>${name}</td></tr>
            <tr><td><b>Email</b></td><td>${email}</td></tr>
            <tr><td><b>Phone</b></td><td>${phone}</td></tr>
            <tr><td><b>Website</b></td><td>${website}</td></tr>
            <tr><td><b>Message</b></td><td>${message}</td></tr>
            <tr><td><b>Time</b></td><td>${new Date().toLocaleString("en-BD", { timeZone: "Asia/Dhaka" })}</td></tr>
          </table>
        `,
      });
    } catch (emailErr) {
      // Email may fail if SMTP not configured - that's ok
      console.log("Email sending skipped (SMTP not configured)");
    }

    return Response.redirect(new URL("/?success=true", request.url), 303);
  } catch (err) {
    console.error("Form error:", err);
    return Response.redirect(new URL("/?error=true", request.url), 303);
  }
}
