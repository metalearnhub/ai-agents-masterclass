import { createClient } from "npm:@supabase/supabase-js@2.45.4";
import nodemailer from "npm:nodemailer@6.9.16";

// Newsletter: subscribe (POST), unsubscribe (GET ?u=token), broadcasts (POST action "run", called by pg_cron).
// Mail goes out through Zoho SMTP (secrets ZOHO_SMTP_USER / ZOHO_SMTP_PASS / NL_FROM).
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};
const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const EMAIL = /^[^\s@<>"']{1,64}@[^\s@<>"']{1,190}\.[A-Za-z]{2,24}$/;
const SELF = "https://qbubwemdvwflxvxwesrl.supabase.co/functions/v1/nl";
const BATCH = 40; // emails per run; cron runs every 5 minutes

function j(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });
}
function page(title: string, msg: string) {
  return new Response(`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><body style="font-family:Inter,Arial,sans-serif;max-width:520px;margin:80px auto;padding:0 20px;color:#1a1a1a"><h1 style="font-size:26px">${title}</h1><p style="font-size:17px;line-height:1.6">${msg}</p><p><a href="https://www.dijaedadula.com/blog" style="color:#007a66">Back to the blog</a></p></body>`, { headers: { "Content-Type": "text/html; charset=utf-8" } });
}
async function sha256(s: string) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
function transport() {
  const user = Deno.env.get("ZOHO_SMTP_USER");
  const pass = Deno.env.get("ZOHO_SMTP_PASS");
  if (!user || !pass) return null;
  return nodemailer.createTransport({ host: Deno.env.get("ZOHO_SMTP_HOST") || "smtp.zoho.com", port: 465, secure: true, pool: true, maxConnections: 1, auth: { user, pass } });
}
function fromAddr() {
  return `Dijae Dadula <${Deno.env.get("NL_FROM") || Deno.env.get("ZOHO_SMTP_USER")}>`;
}
function footer(unsub: string) {
  return `<p style="font-size:12px;color:#777;margin-top:28px">You are receiving this because you subscribed at dijaedadula.com. <a href="${unsub}" style="color:#777">Unsubscribe</a>.</p>`;
}
function personalize(s: string, first: string) {
  return s.replace(/\{\{\s*first_name\s*\}\}/g, first || "there");
}

async function sendWelcome(to: string, name: string, token: string) {
  const t = transport();
  if (!t) return "no-smtp";
  const unsub = `${SELF}?u=${token}`;
  const hi = name ? `Hi ${name},` : "Hi,";
  const html = `<div style="font-family:Inter,Arial,sans-serif;font-size:16px;line-height:1.6;color:#1a1a1a;max-width:560px"><p>${hi}</p><p>Welcome to the newsletter. Every week you get one practical idea on AI agents, automation and turning your skills into income, written for business owners and professionals.</p><p>Three good places to start:</p><ul><li><a href="https://www.dijaedadula.com/what-is-an-ai-agent">What Is an AI Agent? A Plain-English Guide</a></li><li><a href="https://www.dijaedadula.com/dont-automate-chaos">Don't Automate Chaos</a></li><li><a href="https://www.dijaedadula.com/turn-skills-into-ai-income">How to Turn Your Skills Into Repeatable Digital Income With AI</a></li></ul><p>Reply to this email any time. I read every reply.</p><p>Dijae Dadula<br><a href="https://www.dijaedadula.com">dijaedadula.com</a></p>${footer(unsub)}</div>`;
  await t.sendMail({
    from: fromAddr(), to,
    subject: "Welcome: your first practical idea is on its way",
    html,
    text: `${hi}\n\nWelcome to the newsletter. Every week you get one practical idea on AI agents, automation and turning your skills into income.\n\nUnsubscribe: ${unsub}`,
    headers: { "List-Unsubscribe": `<${unsub}>`, "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" },
  });
  t.close();
  return "sent";
}

async function welcomeJob(id: number, email: string, first: string, token: string) {
  let status = "queued", err: string | null = null;
  try { status = await sendWelcome(email, first, token); } catch (e) { status = "failed"; err = String(e).slice(0, 300); }
  await db.from("nl_sends").insert({ kind: "welcome", subscriber_id: id, status, error: err, subject: "Welcome" });
  if (status === "sent") await db.from("nl_subscribers").update({ welcome_sent_at: new Date().toISOString() }).eq("id", id);
}

// Send due broadcasts in batches. Each subscriber gets each broadcast at most once (unique index).
async function runBroadcasts() {
  const { data: due } = await db.from("nl_broadcasts").select("*").in("status", ["scheduled", "sending"]).lte("send_at", new Date().toISOString()).order("send_at").limit(1);
  if (!due || !due.length) return { idle: true };
  const b = due[0];
  const t = transport();
  if (!t) return { error: "no-smtp" };
  if (b.status === "scheduled") await db.from("nl_broadcasts").update({ status: "sending" }).eq("id", b.id);

  // Test send: one email to test_to, then done.
  if (b.test_to) {
    let st = "sent", err: string | null = null;
    try {
      await t.sendMail({ from: fromAddr(), to: b.test_to, subject: "[TEST] " + b.subject, html: personalize(b.html, "Dijae") + footer(SELF), text: b.text ? personalize(b.text, "Dijae") : undefined });
    } catch (e) { st = "failed"; err = String(e).slice(0, 300); }
    await db.from("nl_broadcasts").update({ status: st, sent: st === "sent" ? 1 : 0, failed: st === "sent" ? 0 : 1, sent_at: new Date().toISOString() }).eq("id", b.id);
    t.close();
    return { test: st, err };
  }

  const { data: done } = await db.from("nl_sends").select("subscriber_id").eq("broadcast_id", b.id);
  const skip = new Set((done || []).map((r: any) => r.subscriber_id));
  const { data: subs } = await db.from("nl_subscribers").select("id,email,first_name,unsub_token").eq("status", "subscribed").contains("tags", ["newsletter"]).order("id").limit(5000);
  const todo = (subs || []).filter((s: any) => !skip.has(s.id));
  const batch = todo.slice(0, BATCH);
  let ok = 0, bad = 0;
  for (const s of batch) {
    const unsub = `${SELF}?u=${s.unsub_token}`;
    const first = (s.first_name || "").trim();
    let st = "sent", err: string | null = null;
    try {
      await t.sendMail({
        from: fromAddr(), to: s.email, subject: b.subject,
        html: `<div style="display:none;max-height:0;overflow:hidden">${b.preheader || ""}</div>` + personalize(b.html, first) + footer(unsub),
        text: b.text ? personalize(b.text, first) + `\n\nUnsubscribe: ${unsub}` : undefined,
        headers: { "List-Unsubscribe": `<${unsub}>`, "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" },
      });
      ok++;
    } catch (e) { st = "failed"; err = String(e).slice(0, 300); bad++; }
    await db.from("nl_sends").insert({ kind: b.kind, subject: b.subject, subscriber_id: s.id, broadcast_id: b.id, status: st, error: err });
  }
  t.close();
  const remaining = todo.length - batch.length;
  const upd: any = { sent: b.sent + ok, failed: b.failed + bad };
  if (remaining <= 0) { upd.status = "sent"; upd.sent_at = new Date().toISOString(); }
  await db.from("nl_broadcasts").update(upd).eq("id", b.id);
  return { broadcast: b.id, sent: ok, failed: bad, remaining };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const url = new URL(req.url);
  const u = url.searchParams.get("u");
  if (u) {
    if (!/^[0-9a-f-]{36}$/.test(u)) return page("Link not valid", "This unsubscribe link is not valid.");
    const { data } = await db.from("nl_subscribers").update({ status: "unsubscribed", updated_at: new Date().toISOString() }).eq("unsub_token", u).select("id");
    if (!data || !data.length) return page("Link not valid", "We could not find this subscription.");
    return page("You are unsubscribed", "You will not receive the newsletter any more. You can subscribe again at any time.");
  }
  if (req.method !== "POST") return j({ ok: true, service: "nl" });

  const runKey = req.headers.get("x-nl-run");
  if (runKey) {
    const { data: c } = await db.from("nl_config").select("v").eq("k", "run_key_hash").single();
    if (!c || (await sha256(runKey)) !== c.v) return j({ error: "unauthorized" }, 401);
    try { return j(await runBroadcasts()); } catch (e) { return j({ error: String(e).slice(0, 300) }, 500); }
  }

  let b: any = {};
  const ct = req.headers.get("content-type") || "";
  try {
    if (ct.includes("application/json")) b = await req.json();
    else { const f = await req.formData(); b = Object.fromEntries(f.entries()); }
  } catch { return j({ error: "bad request" }, 400); }
  if (b.website) return j({ ok: true }); // honeypot
  const email = String(b.email || "").trim().toLowerCase();
  const first = String(b.first_name || "").trim().slice(0, 60).replace(/[<>]/g, "");
  if (!EMAIL.test(email)) return j({ error: "Please enter a valid email." }, 400);
  const source = String(b.source || "web").slice(0, 60);
  const { data: ex } = await db.from("nl_subscribers").select("id,status,unsub_token,welcome_sent_at,first_name").eq("email", email).maybeSingle();
  let row = ex;
  if (!ex) {
    const { data, error } = await db.from("nl_subscribers").insert({
      email, first_name: first || null, source,
      consent_text: "Subscribed to the free weekly newsletter at dijaedadula.com",
      ip: req.headers.get("x-forwarded-for")?.split(",")[0] || null,
      user_agent: (req.headers.get("user-agent") || "").slice(0, 300),
    }).select("id,status,unsub_token,welcome_sent_at,first_name").single();
    if (error) return j({ error: "Could not subscribe right now." }, 500);
    row = data;
  } else if (ex.status !== "subscribed") {
    await db.from("nl_subscribers").update({ status: "subscribed", consent_at: new Date().toISOString(), updated_at: new Date().toISOString() }).eq("id", ex.id);
  }
  if (row && !row.welcome_sent_at) {
    const job = welcomeJob(row.id, email, first || row.first_name || "", row.unsub_token);
    // @ts-ignore EdgeRuntime is provided by Supabase
    if (typeof EdgeRuntime !== "undefined") EdgeRuntime.waitUntil(job); else await job;
  }
  return j({ ok: true });
});
