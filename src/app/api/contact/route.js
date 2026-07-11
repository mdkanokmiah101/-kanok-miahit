"use server";

import nodemailer from "nodemailer";

// SMTP config for sending email notifications
const EMAIL_FROM = "mdkanokmiah232@gmail.com";
const EMAIL_TO = "mdkanokmiah101@gmail.com";
const SMTP_USER = "mdkanokmiah232@gmail.com";
const SMTP_PASS = "akll wbko qtqh sgjc";

// Create transporter
const transporter = nodemailer.createTransport({
  host: "smtp.gmail.com",
  port: 587,
  secure: false,
  auth: { user: SMTP_USER, pass: SMTP_PASS },
});

async function sendEmail({ name, email, phone, website, message }) {
  try {
    const html = `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9;">
        <div style="background: #124D1C; color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
          <h1 style="margin: 0; font-size: 22px;">🔴 NEW SEO LEAD</h1>
          <p style="margin: 5px 0 0; opacity: 0.9;">kanokmiah.com.bd</p>
        </div>
        <div style="background: white; padding: 25px; border-radius: 0 0 10px 10px; border: 1px solid #e0e0e0;">
          <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; font-weight: bold; color: #333; width: 100px;">👤 Name</td><td style="padding: 8px;">${name}</td></tr>
            <tr style="background: #f5f5f5;"><td style="padding: 8px; font-weight: bold; color: #333;">📧 Email</td><td style="padding: 8px;">${email}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold; color: #333;">📞 Phone</td><td style="padding: 8px;">${phone}</td></tr>
            <tr style="background: #f5f5f5;"><td style="padding: 8px; font-weight: bold; color: #333;">🌐 Website</td><td style="padding: 8px;">${website}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold; color: #333;">💬 Message</td><td style="padding: 8px;">${message || "—"}</td></tr>
          </table>
          <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 8px;">
            <a href="https://wa.me/8801604809110?text=Hi!%20Regarding%20your%20lead%20${name}%20(${phone})" 
               style="display: inline-block; background: #25D366; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-weight: bold;">
              💬 Reply on WhatsApp
            </a>
            <a href="mailto:${email}" 
               style="display: inline-block; background: #124D1C; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; margin-left: 10px;">
              📧 Reply via Email
            </a>
          </div>
        </div>
      </div>
    `;

    await transporter.sendMail({
      from: `"Md Kanok Miah - Lead" <${EMAIL_FROM}>`,
      to: EMAIL_TO,
      subject: `🔴 New SEO Lead: ${name} - ${phone}`,
      html,
    });

    console.log(`📧 Email sent to ${EMAIL_TO} for lead: ${name}`);
    return true;
  } catch (err) {
    console.error("📧 Email error:", err.message);
    return false;
  }
}

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

    // Log to leads file
    try {
      const fs = require("fs");
      const leadRecord = `[${new Date().toISOString()}] ${name} | ${email} | ${phone} | ${website} | ${subject}\n`;
      fs.appendFileSync("/root/.hermes/leads.log", leadRecord);
    } catch(e) {}

    // Send Email notification
    sendEmail({ name, email, phone, website, message }).catch(() => {});

    // Try WhatsApp lead notification bot (port 3099)
    try {
      fetch("http://127.0.0.1:3099/send-lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, phone, website, subject }),
        signal: AbortSignal.timeout(3000),
      }).catch(() => {});
    } catch(e) {}

    // Telegram notification
    const token = process.env.TELEGRAM_BOT_TOKEN;
    if (token) {
      const text = `🔔 **🔴 NEW SEO LEAD — kanokmiah.com.bd**
👤 Name: ${name}
📧 Email: ${email}
📞 Phone: ${phone}
🌐 Website: ${website}
💬 Message: ${message}
📧 Email sent to: mdkanokmiah101@gmail.com
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
