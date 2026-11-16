import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type, x-cb-key",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
const SLOT = /^[A-Za-z0-9_\-]{1,80}(#[0-9])?$/;

async function sha256(s: string) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
}
function j(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });
}
function cleanRec(v: any) {
  if (!v || typeof v !== "object" || Array.isArray(v)) return null;
  const s = JSON.stringify(v);
  return s.length > 4000 ? null : v;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return j({ error: "method" }, 405);
  let body: any = {};
  try { body = await req.json(); } catch { return j({ error: "bad json" }, 400); }

  // Passcode gate: exchange the passcode for a device key (stored hashed).
  if (body.action === "unlock") {
    const { data: c } = await db.from("cb_config").select("pass_hash, fails, last_fail").eq("bank_id", "dijae").single();
    if (!c) return j({ error: "not configured" }, 500);
    const recent = c.last_fail && Date.now() - new Date(c.last_fail).getTime() < 3600_000;
    if (recent && c.fails >= 10) return j({ error: "locked", retry_after_minutes: 60 }, 429);
    const pass = String(body.passcode || "").slice(0, 40);
    if ((await sha256("cb:" + pass)) !== c.pass_hash) {
      await db.from("cb_config").update({ fails: (recent ? c.fails : 0) + 1, last_fail: new Date().toISOString() }).eq("bank_id", "dijae");
      return j({ error: "wrong passcode" }, 401);
    }
    await db.from("cb_config").update({ fails: 0, last_fail: null }).eq("bank_id", "dijae");
    const raw = new Uint8Array(32); crypto.getRandomValues(raw);
    const key = Array.from(raw).map((x) => x.toString(16).padStart(2, "0")).join("");
    const { error } = await db.from("cb_keys").insert({ bank_id: "dijae", key_hash: await sha256(key) });
    if (error) return j({ error: error.message }, 500);
    return j({ key });
  }

  const key = req.headers.get("x-cb-key") || "";
  if (key.length < 20) return j({ error: "unauthorized" }, 401);
  const { data: k } = await db.from("cb_keys").select("bank_id").eq("key_hash", await sha256(key)).limit(1).maybeSingle();
  if (!k) return j({ error: "unauthorized" }, 401);
  const id = k.bank_id;
  const a = body.action;
  const get = async () => {
    const { data } = await db.from("cb_state").select("rec, me, updated_at").eq("id", id).single();
    return data;
  };
  if (a === "check") return j({ ok: true });
  if (a === "get") return j(await get());
  if (a === "set" || a === "del") {
    const slot = String(body.slot || "");
    if (!SLOT.test(slot)) return j({ error: "bad slot" }, 400);
    const val = a === "set" ? cleanRec(body.value) : null;
    if (a === "set" && !val) return j({ error: "bad value" }, 400);
    const { error } = await db.rpc("cb_apply", { p_id: id, p_slot: slot, p_value: val });
    if (error) return j({ error: error.message }, 500);
    return j(await get());
  }
  if (a === "merge") {
    const cur = (await get())?.rec || {};
    const inc = body.rec && typeof body.rec === "object" ? body.rec : {};
    let n = 0;
    for (const s of Object.keys(inc).slice(0, 500)) {
      if (!SLOT.test(s) || cur[s]) continue;
      const v = cleanRec(inc[s]);
      if (!v) continue;
      await db.rpc("cb_apply", { p_id: id, p_slot: s, p_value: v });
      n++;
    }
    return j({ merged: n, ...(await get()) });
  }
  if (a === "me") {
    const me = String(body.me ?? "").slice(0, 120);
    await db.from("cb_state").update({ me, updated_at: new Date().toISOString() }).eq("id", id);
    return j(await get());
  }
  return j({ error: "unknown action" }, 400);
});
