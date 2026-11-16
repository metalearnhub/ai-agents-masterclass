import { createClient } from "npm:@supabase/supabase-js@2.45.4";
import nodemailer from "npm:nodemailer@6.9.16";

// Private CRM API for Dijae: contacts (nl_subscribers), custom fields, tags, activity, dashboard stats.
// Sign-in: 6-digit code emailed through Zoho to the owner address, then a 30-day session token.
const OWNER = "dijaedadula@gmail.com";
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type, authorization",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const EMAIL = /^[^\s@<>"']{1,64}@[^\s@<>"']{1,190}\.[A-Za-z]{2,24}$/;
const STATUSES = ["subscribed", "unsubscribed", "bounced", "lead"];
const COLS = "id,email,first_name,last_name,phone,company,source,tags,status,fields,notes,consent_text,consent_at,welcome_sent_at,created_at,updated_at";

async function sha256(s: string) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
function j(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });
}
const str = (v: unknown, n: number) => (v == null ? "" : String(v)).trim().slice(0, n);
const nul = (v: unknown, n: number) => { const s = str(v, n); return s ? s : null; };
function cleanTags(v: unknown): string[] {
  const a = Array.isArray(v) ? v : String(v || "").split(/[,;|]/);
  return [...new Set(a.map((t) => String(t).trim().toLowerCase().replace(/[^a-z0-9 _\-]/g, "").slice(0, 40)).filter(Boolean))].slice(0, 40);
}
function cleanFields(v: unknown) {
  const out: Record<string, string> = {};
  if (v && typeof v === "object" && !Array.isArray(v)) for (const [k, x] of Object.entries(v as any).slice(0, 60)) if (/^[a-z][a-z0-9_]{0,39}$/.test(k)) out[k] = str(x, 2000);
  return out;
}
async function log(contact_id: number, kind: string, detail: string) {
  await db.from("crm_activity").insert({ contact_id, kind, detail: detail.slice(0, 1000) });
}

async function sendCode(code: string) {
  const user = Deno.env.get("ZOHO_SMTP_USER"), pass = Deno.env.get("ZOHO_SMTP_PASS");
  if (!user || !pass) throw new Error("no smtp");
  const t = nodemailer.createTransport({ host: Deno.env.get("ZOHO_SMTP_HOST") || "smtp.zoho.com", port: 465, secure: true, auth: { user, pass } });
  await t.sendMail({
    from: `Dijae CRM <${Deno.env.get("NL_FROM") || user}>`, to: OWNER,
    subject: `Your CRM sign-in code: ${code}`,
    text: `Your sign-in code is ${code}. It expires in 10 minutes. If you did not ask for it, ignore this email.`,
    html: `<div style="font-family:Inter,Arial,sans-serif;font-size:16px;color:#1a1a1a"><p>Your CRM sign-in code:</p><p style="font-size:32px;font-weight:800;letter-spacing:6px">${code}</p><p style="color:#666;font-size:13px">It expires in 10 minutes. If you did not ask for it, ignore this email.</p></div>`,
  });
  t.close();
}

async function auth(req: Request) {
  const h = req.headers.get("authorization") || "";
  const tok = h.startsWith("Bearer ") ? h.slice(7) : "";
  if (tok.length < 20) return null;
  const { data } = await db.from("crm_sessions").select("email,expires_at").eq("token_hash", await sha256(tok)).maybeSingle();
  if (!data || new Date(data.expires_at).getTime() < Date.now()) return null;
  return { email: data.email, tokHash: await sha256(tok) };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return j({ error: "method" }, 405);
  let b: any = {};
  try { b = await req.json(); } catch { return j({ error: "bad json" }, 400); }
  const a = String(b.action || "");

  // ---- sign-in ----
  if (a === "request_code") {
    const { count } = await db.from("crm_codes").select("id", { count: "exact", head: true }).gt("created_at", new Date(Date.now() - 3600_000).toISOString());
    if ((count || 0) >= 6) return j({ error: "Too many codes requested. Try again in an hour." }, 429);
    const code = String(crypto.getRandomValues(new Uint32Array(1))[0] % 1000000).padStart(6, "0");
    await db.from("crm_codes").update({ used: true }).eq("used", false);
    await db.from("crm_codes").insert({ email: OWNER, code_hash: await sha256("crm:" + code), expires_at: new Date(Date.now() + 600_000).toISOString() });
    try { await sendCode(code); } catch (e) { return j({ error: "Could not send the code: " + String(e).slice(0, 120) }, 500); }
    return j({ ok: true, to: OWNER.replace(/^(.).*(@.*)$/, "$1•••$2") });
  }
  if (a === "verify") {
    const code = str(b.code, 12).replace(/\D/g, "");
    const { data: c } = await db.from("crm_codes").select("*").eq("used", false).order("id", { ascending: false }).limit(1).maybeSingle();
    if (!c || new Date(c.expires_at).getTime() < Date.now()) return j({ error: "Code expired. Request a new one." }, 401);
    if (c.attempts >= 5) return j({ error: "Too many wrong tries. Request a new code." }, 429);
    if ((await sha256("crm:" + code)) !== c.code_hash) {
      await db.from("crm_codes").update({ attempts: c.attempts + 1 }).eq("id", c.id);
      return j({ error: "Wrong code." }, 401);
    }
    await db.from("crm_codes").update({ used: true }).eq("id", c.id);
    const raw = crypto.getRandomValues(new Uint8Array(32));
    const token = Array.from(raw).map((x) => x.toString(16).padStart(2, "0")).join("");
    const expires = new Date(Date.now() + 30 * 86400_000).toISOString();
    await db.from("crm_sessions").insert({ token_hash: await sha256(token), email: OWNER, expires_at: expires });
    return j({ token, expires_at: expires, email: OWNER });
  }

  const s = await auth(req);
  if (!s) return j({ error: "unauthorized" }, 401);

  try {
    switch (a) {
      case "me": return j({ email: s.email });
      case "signout": await db.from("crm_sessions").delete().eq("token_hash", s.tokHash); return j({ ok: true });

      case "stats": {
        const { data, error } = await db.rpc("crm_stats");
        if (error) throw error;
        return j(data);
      }

      case "contacts.list": {
        const page = Math.max(0, parseInt(b.page) || 0), size = Math.min(200, Math.max(10, parseInt(b.size) || 50));
        let q = db.from("nl_subscribers").select(COLS, { count: "exact" });
        const term = str(b.q, 100).replace(/[%,()]/g, " ").trim();
        if (term) q = q.or(`email.ilike.%${term}%,first_name.ilike.%${term}%,last_name.ilike.%${term}%,company.ilike.%${term}%,phone.ilike.%${term}%`);
        if (b.status && STATUSES.includes(b.status)) q = q.eq("status", b.status);
        if (b.tag) q = q.contains("tags", [str(b.tag, 40).toLowerCase()]);
        const sort = ["created_at", "email", "first_name", "updated_at"].includes(b.sort) ? b.sort : "created_at";
        q = q.order(sort, { ascending: sort === "email" || sort === "first_name" }).range(page * size, page * size + size - 1);
        const { data, count, error } = await q;
        if (error) throw error;
        return j({ rows: data, total: count, page, size });
      }

      case "contacts.get": {
        const id = parseInt(b.id);
        const { data: c, error } = await db.from("nl_subscribers").select(COLS).eq("id", id).single();
        if (error) throw error;
        const { data: act } = await db.from("crm_activity").select("kind,detail,at").eq("contact_id", id).order("at", { ascending: false }).limit(100);
        const { data: sends } = await db.from("nl_sends").select("kind,subject,status,error,created_at").eq("subscriber_id", id).order("created_at", { ascending: false }).limit(100);
        return j({ contact: c, activity: act || [], sends: sends || [] });
      }

      case "contacts.save": {
        const c = b.contact || {};
        const email = str(c.email, 254).toLowerCase();
        if (!EMAIL.test(email)) return j({ error: "Enter a valid email." }, 400);
        const status = STATUSES.includes(c.status) ? c.status : "lead";
        const row: any = {
          email, first_name: nul(c.first_name, 60), last_name: nul(c.last_name, 60), phone: nul(c.phone, 40), company: nul(c.company, 120),
          tags: cleanTags(c.tags), status, fields: cleanFields(c.fields), notes: nul(c.notes, 5000), updated_at: new Date().toISOString(),
        };
        if (c.id) {
          const { data: old } = await db.from("nl_subscribers").select("status,tags").eq("id", c.id).single();
          if (old && old.status !== "subscribed" && status === "subscribed" && !c.consent) return j({ error: "Only mark someone as subscribed if they opted in. Tick the consent box." }, 400);
          if (status === "subscribed" && c.consent && old?.status !== "subscribed") { row.consent_at = new Date().toISOString(); row.consent_text = "Marked as opted in by Dijae in the CRM"; }
          const { data, error } = await db.from("nl_subscribers").update(row).eq("id", c.id).select(COLS).single();
          if (error) throw error;
          const changes: string[] = [];
          if (old && old.status !== status) changes.push(`status ${old.status} → ${status}`);
          const added = row.tags.filter((t: string) => !(old?.tags || []).includes(t)), removed = (old?.tags || []).filter((t: string) => !row.tags.includes(t));
          if (added.length) changes.push("tags + " + added.join(", "));
          if (removed.length) changes.push("tags − " + removed.join(", "));
          await log(c.id, "edit", changes.length ? changes.join("; ") : "Details updated");
          return j({ contact: data });
        }
        if (status === "subscribed" && !c.consent) return j({ error: "Only add someone as subscribed if they opted in. Tick the consent box or save as a lead." }, 400);
        const { data: dup } = await db.from("nl_subscribers").select("id").eq("email", email).maybeSingle();
        if (dup) return j({ error: "A contact with this email already exists.", id: dup.id }, 409);
        row.source = nul(c.source, 60) || "crm";
        if (status === "subscribed") { row.consent_at = new Date().toISOString(); row.consent_text = "Marked as opted in by Dijae in the CRM"; }
        const { data, error } = await db.from("nl_subscribers").insert(row).select(COLS).single();
        if (error) throw error;
        await log(data.id, "created", "Added in the CRM as " + status);
        return j({ contact: data });
      }

      case "contacts.note": {
        const id = parseInt(b.id), text = str(b.text, 1000);
        if (!text) return j({ error: "Empty note" }, 400);
        await log(id, "note", text);
        return j({ ok: true });
      }

      case "contacts.delete": {
        const ids = (Array.isArray(b.ids) ? b.ids : [b.id]).map((x: any) => parseInt(x)).filter(Boolean).slice(0, 500);
        if (!ids.length) return j({ error: "Nothing to delete" }, 400);
        await db.from("nl_sends").delete().in("subscriber_id", ids);
        const { error } = await db.from("nl_subscribers").delete().in("id", ids);
        if (error) throw error;
        return j({ deleted: ids.length });
      }

      case "contacts.bulk": {
        const ids = (b.ids || []).map((x: any) => parseInt(x)).filter(Boolean).slice(0, 1000);
        const op = b.op, tag = cleanTags([b.tag])[0];
        const { data: rows } = await db.from("nl_subscribers").select("id,tags,status").in("id", ids);
        let n = 0;
        for (const r of rows || []) {
          let tags = r.tags || [], status = r.status;
          if (op === "tag_add" && tag && !tags.includes(tag)) tags = [...tags, tag];
          else if (op === "tag_remove" && tag) tags = tags.filter((t: string) => t !== tag);
          else if (op === "unsubscribe") status = "unsubscribed";
          else if (op === "lead") status = "lead";
          else continue;
          await db.from("nl_subscribers").update({ tags, status, updated_at: new Date().toISOString() }).eq("id", r.id);
          await log(r.id, "edit", op === "tag_add" ? "tags + " + tag : op === "tag_remove" ? "tags − " + tag : "status → " + status);
          n++;
        }
        return j({ updated: n });
      }

      case "contacts.import": {
        const rows = Array.isArray(b.rows) ? b.rows.slice(0, 5000) : [];
        const optedIn = b.opted_in === true;
        const status = optedIn ? "subscribed" : "lead";
        const extraTags = cleanTags(b.tags);
        const source = nul(b.source, 60) || "import";
        let created = 0, updated = 0, skipped = 0;
        const now = new Date().toISOString();
        const emails = rows.map((r: any) => str(r.email, 254).toLowerCase()).filter((e: string) => EMAIL.test(e));
        const existing = new Map<string, any>();
        for (let i = 0; i < emails.length; i += 500) {
          const { data } = await db.from("nl_subscribers").select("id,email,tags,status,fields").in("email", emails.slice(i, i + 500));
          (data || []).forEach((x: any) => existing.set(x.email, x));
        }
        const inserts: any[] = [];
        const seen = new Set<string>();
        for (const r of rows) {
          const email = str(r.email, 254).toLowerCase();
          if (!EMAIL.test(email) || seen.has(email)) { skipped++; continue; }
          seen.add(email);
          const tags = cleanTags([...(cleanTags(r.tags)), ...extraTags]);
          const fields = cleanFields(r.fields);
          const ex = existing.get(email);
          if (ex) {
            // never resubscribe someone who unsubscribed or bounced
            const upd: any = { tags: cleanTags([...(ex.tags || []), ...tags]), fields: { ...(ex.fields || {}), ...fields }, updated_at: now };
            for (const k of ["first_name", "last_name", "phone", "company"]) { const v = nul(r[k], 120); if (v) upd[k] = v; }
            await db.from("nl_subscribers").update(upd).eq("id", ex.id);
            updated++;
          } else {
            inserts.push({
              email, first_name: nul(r.first_name, 60), last_name: nul(r.last_name, 60), phone: nul(r.phone, 40), company: nul(r.company, 120),
              tags, fields, status, source,
              consent_text: optedIn ? "Imported as opted in by Dijae (CSV import)" : null, consent_at: optedIn ? now : null,
              welcome_sent_at: now, // imported contacts do not get the welcome email
            });
          }
        }
        for (let i = 0; i < inserts.length; i += 500) {
          const { data, error } = await db.from("nl_subscribers").insert(inserts.slice(i, i + 500)).select("id");
          if (error) throw error;
          created += (data || []).length;
          await db.from("crm_activity").insert((data || []).map((x: any) => ({ contact_id: x.id, kind: "created", detail: `Imported (${source}) as ${status}` })));
        }
        return j({ created, updated, skipped });
      }

      case "contacts.export": {
        const all: any[] = [];
        for (let p = 0; p < 50; p++) {
          const { data } = await db.from("nl_subscribers").select(COLS).order("id").range(p * 1000, p * 1000 + 999);
          if (!data || !data.length) break;
          all.push(...data);
          if (data.length < 1000) break;
        }
        return j({ rows: all });
      }

      case "fields.list": {
        const { data } = await db.from("crm_fields").select("*").order("position").order("created_at");
        return j({ fields: data || [] });
      }
      case "fields.save": {
        const f = b.field || {};
        const key = str(f.key, 40).toLowerCase().replace(/[^a-z0-9_]/g, "_").replace(/^[^a-z]+/, "");
        if (!key) return j({ error: "Field key must start with a letter." }, 400);
        const row = { key, label: str(f.label, 60) || key, type: ["text", "number", "date", "select", "url", "textarea"].includes(f.type) ? f.type : "text", options: Array.isArray(f.options) ? f.options.map((o: any) => str(o, 60)).filter(Boolean).slice(0, 50) : [], position: parseInt(f.position) || 0 };
        const { error } = await db.from("crm_fields").upsert(row);
        if (error) throw error;
        return j({ ok: true });
      }
      case "fields.delete": {
        await db.from("crm_fields").delete().eq("key", str(b.key, 40));
        return j({ ok: true });
      }

      // ---- pipelines & deals ----
      case "pipelines.list": {
        const { data } = await db.from("crm_pipelines").select("*").order("position").order("id");
        return j({ pipelines: data || [] });
      }
      case "pipelines.save": {
        const p = b.pipeline || {};
        const name = str(p.name, 80);
        if (!name) return j({ error: "Give the pipeline a name." }, 400);
        const stages = (Array.isArray(p.stages) ? p.stages : []).slice(0, 20).map((s: any, i: number) => ({
          id: str(s.id, 40).toLowerCase().replace(/[^a-z0-9_-]/g, "") || ("s" + Date.now().toString(36) + i),
          name: str(s.name, 60) || "Stage " + (i + 1),
          kind: ["open", "won", "lost"].includes(s.kind) ? s.kind : "open",
        }));
        if (!stages.length) return j({ error: "Add at least one stage." }, 400);
        if (p.id) {
          const { data: old } = await db.from("crm_pipelines").select("stages").eq("id", p.id).single();
          const gone = (old?.stages || []).map((s: any) => s.id).filter((id: string) => !stages.some((s: any) => s.id === id));
          if (gone.length) {
            const { count } = await db.from("crm_deals").select("id", { count: "exact", head: true }).eq("pipeline_id", p.id).in("stage", gone);
            if (count) return j({ error: `Move the ${count} deal(s) out of the stages you removed first.` }, 400);
          }
          const { error } = await db.from("crm_pipelines").update({ name, stages }).eq("id", p.id);
          if (error) throw error;
          return j({ ok: true, id: p.id });
        }
        const { data, error } = await db.from("crm_pipelines").insert({ name, stages, position: parseInt(p.position) || 0 }).select("id").single();
        if (error) throw error;
        return j({ ok: true, id: data.id });
      }
      case "pipelines.delete": {
        const id = parseInt(b.id);
        const { count } = await db.from("crm_deals").select("id", { count: "exact", head: true }).eq("pipeline_id", id);
        if (count) return j({ error: `This pipeline still has ${count} deal(s). Delete or move them first.` }, 400);
        await db.from("crm_pipelines").delete().eq("id", id);
        return j({ ok: true });
      }
      case "deals.list": {
        let q = db.from("crm_deals").select("*, contact:nl_subscribers(id,email,first_name,last_name,company)");
        if (b.pipeline_id) q = q.eq("pipeline_id", parseInt(b.pipeline_id));
        if (b.contact_id) q = q.eq("contact_id", parseInt(b.contact_id));
        const { data, error } = await q.order("position").order("id").limit(2000);
        if (error) throw error;
        return j({ deals: data || [] });
      }
      case "deals.save": {
        const d = b.deal || {};
        const title = str(d.title, 140);
        if (!title) return j({ error: "Give the deal a title." }, 400);
        const pid = parseInt(d.pipeline_id);
        const { data: p } = await db.from("crm_pipelines").select("stages").eq("id", pid).single();
        if (!p) return j({ error: "Pipeline not found." }, 400);
        const st = (p.stages || []).find((s: any) => s.id === d.stage) || p.stages[0];
        const row: any = {
          pipeline_id: pid, stage: st.id, title, value: Math.max(0, Number(d.value) || 0), currency: str(d.currency, 3).toUpperCase() || "PHP",
          contact_id: parseInt(d.contact_id) || null, next_date: /^\d{4}-\d{2}-\d{2}$/.test(d.next_date || "") ? d.next_date : null,
          next_step: nul(d.next_step, 200), notes: nul(d.notes, 5000), status: st.kind, updated_at: new Date().toISOString(),
        };
        if (st.kind !== "open") row.closed_at = new Date().toISOString(); else row.closed_at = null;
        if (d.id) {
          const { data: old } = await db.from("crm_deals").select("stage,status,contact_id").eq("id", d.id).single();
          if (old && old.status !== "open" && st.kind !== "open" && old.stage === st.id) delete row.closed_at;
          const { data, error } = await db.from("crm_deals").update(row).eq("id", d.id).select("*").single();
          if (error) throw error;
          if (row.contact_id && old?.stage !== st.id) await log(row.contact_id, "deal", `${title}: moved to ${st.name}`);
          return j({ deal: data });
        }
        row.position = Date.now() / 1000;
        const { data, error } = await db.from("crm_deals").insert(row).select("*").single();
        if (error) throw error;
        if (row.contact_id) await log(row.contact_id, "deal", `${title}: created in ${st.name}`);
        return j({ deal: data });
      }
      case "deals.move": {
        const id = parseInt(b.id);
        const { data: d } = await db.from("crm_deals").select("pipeline_id,stage,title,contact_id,status").eq("id", id).single();
        if (!d) return j({ error: "Deal not found." }, 404);
        const { data: p } = await db.from("crm_pipelines").select("stages").eq("id", d.pipeline_id).single();
        const st = (p?.stages || []).find((s: any) => s.id === b.stage);
        if (!st) return j({ error: "Stage not found." }, 400);
        const upd: any = { stage: st.id, status: st.kind, position: Number(b.position) || Date.now() / 1000, updated_at: new Date().toISOString() };
        if (d.stage !== st.id) upd.closed_at = st.kind === "open" ? null : new Date().toISOString();
        await db.from("crm_deals").update(upd).eq("id", id);
        if (d.contact_id && d.stage !== st.id) await log(d.contact_id, "deal", `${d.title}: moved to ${st.name}`);
        return j({ ok: true });
      }
      case "deals.delete": {
        await db.from("crm_deals").delete().eq("id", parseInt(b.id));
        return j({ ok: true });
      }
      case "contacts.pick": {
        const term = str(b.q, 100).replace(/[%,()]/g, " ").trim();
        let q = db.from("nl_subscribers").select("id,email,first_name,last_name,company");
        if (term) q = q.or(`email.ilike.%${term}%,first_name.ilike.%${term}%,last_name.ilike.%${term}%,company.ilike.%${term}%`);
        const { data } = await q.order("updated_at", { ascending: false }).limit(10);
        return j({ rows: data || [] });
      }

      case "tags.list": {
        const { data } = await db.rpc("crm_stats");
        return j({ tags: (data && data.tags) || [] });
      }
    }
    return j({ error: "unknown action" }, 400);
  } catch (e: any) {
    return j({ error: String(e?.message || e).slice(0, 300) }, 500);
  }
});
