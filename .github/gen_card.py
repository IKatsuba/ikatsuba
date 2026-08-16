#!/usr/bin/env python3
"""Generate the katsuba.dev-style SVG card (desktop + mobile) for the GitHub profile README."""
import os
import textwrap

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0a0a0a", fg="#fafafa", muted="#a1a1a1", faint="#737373",
                 border="#ffffff1a", chip="#262626"),
    "light": dict(bg="#ffffff", fg="#0a0a0a", muted="#737373", faint="#a1a1a1",
                  border="#e5e5e5", chip="#f5f5f5"),
}
FONT = "ui-monospace,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
CW13 = 8.7
CW17 = 11.5
CW18 = 12.2
LH = 21

VARIANTS = {
    "": dict(W=840, PAD=32, mobile=False),
    "mobile-": dict(W=480, PAD=24, mobile=True),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(s, px, cw=CW13):
    return textwrap.wrap(s, width=int(px / cw))


def text(x, y, s, fill, size=13, weight=None, anchor=None, preserve=False):
    a = f' font-weight="{weight}"' if weight else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    a += ' xml:space="preserve"' if preserve else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{a}>{s}</text>'


MANIFEST = ("I build software whose users are increasingly not people. "
            "Agents call it, other systems depend on it, and it has to keep "
            "working when nobody's watching.")

ABOUT_PARAGRAPHS = [
    "I'm a platform engineer working out of Valencia. For the last while I've been "
    "living at the seam between AI agents and backend infrastructure — the "
    "unglamorous layer that decides whether the clever stuff on top actually holds.",
    "The framing on this page isn't a gimmick. It's genuinely how I think about "
    "building: define a capability once, expose it through whatever transport the "
    "caller speaks — HTTP, MCP, a CLI. Same idea applies to a person. This is me, "
    "exposed over the transports below.",
    "Nearly everything I've built has been for other engineers rather than for end "
    "users: platform foundations, release paths, test corpora, the internal tools "
    "nobody demos. That comes with the other half of the job — hiring for the team, "
    "reviewing its code, and starting the weekly meeting where designs get argued "
    "out loud.",
]

FNS = [
    ("fn building()", "Durable execution, agent orchestration, developer tooling, the glue "
     "between systems. I'm happiest one layer below the product, where reliability "
     "is the whole job."),
    ("fn leading()", "Platform teams, hiring tracks, and the weekly meeting where designs get "
     "argued in public instead of in DMs. Building for other engineers is most of "
     "what I do, and the people half comes with it."),
    ("fn writing()", "I run a Telegram channel on Angular and frontend, and a blog with 20+ "
     "articles. Explaining things is how I understand them, and it turns out other "
     "people find it useful too."),
    ("fn speaking()", "Conference talks on monorepos, build tooling, and pipeline acceleration — "
     "Frontend Conf, CodeFest, Podlodka. The recordings age; the problems they "
     "solve mostly don't."),
]

TOOLS = [
    ("01", "NGGUIDE", "An Angular course an agent takes itself. Delivered over MCP, "
     "built for the world where the student isn't always human."),
    ("02", "roost", "A native macOS workspace for Claude Code sessions — projects, tabs, a tree "
     "of terminal panes, and an attention queue that tells you which agent is stuck."),
    ("03", "nx-cache-server", "Self-hosted remote cache for Nx. S3, Docker, Helm — bring your "
     "own infra, keep your build times."),
    ("04", "mutates", "AST mutation toolkit — mutate the AST, not your brain. Hands for an agent "
     "that needs to rewrite code and be sure it did."),
    ("05", "ng-http", "Experimental declarative HTTP server written with Angular. What if your "
     "backend spoke the framework your frontend already does?"),
    ("06", "deno-mastra", "AI agents built with Deno and the Mastra framework — the runtime and "
     "the orchestration, end to end."),
    ("07", "serverless-redis", "HTTP → Redis server, Upstash-compatible. Hono + Deno, one click "
     "to deploy on Railway."),
]

TALKS = [
    ("Repository evolution: from simple to complex", "Frontend Conf 2021"),
    ("Extreme Pipeline Acceleration", "CodeFest Russia 2022"),
    ("It's all about Nx", "Podlodka 2022"),
]

ROLES = [
    ("ManifestLabs", "Platform Team", "2025 —",
     "Legal-tech SaaS. The platform, the release path, the incident root cause, and "
     "the company's internal AI agent platform."),
    ("Plata Card", "Principal Engineer · Frontend Platform Lead", "2022–2025",
     "Consumer fintech. Led the frontend platform team and built the foundation every "
     "frontend product shipped on, from the internal CRM to the public site."),
    ("Tinkoff", "Staff Engineer · Frontend Platform", "2020–2022",
     "Built the company's frontend platform. Parts were released as open source, which "
     "is the visible tenth of it."),
    ("Fix Group", "Senior Frontend Developer", "2018–2020",
     "Product frontend, and the first tooling I owned rather than used."),
    ("RTLabs", "Frontend Developer", "2014–2018",
     "Where I started — large government-scale web applications."),
]

RESUME_LINK = ("GET /resume", "katsuba.dev/resume.md")

CONTACT_TEXT = ("This server accepts connections. If you want to talk infrastructure, "
                "agents, or the tooling underneath both — or just argue about durable "
                "execution — open a connection.")

TRANSPORTS = [
    ("github", "github.com/IKatsuba"),
    ("x", "x.com/katsuba_igor"),
    ("instagram", "instagram.com/igor.katsuba"),
    ("telegram", "t.me/Katsuba"),
    ("email", "igor@katsuba.dev"),
]


def build(t, v):
    W, PAD, mobile = v["W"], v["PAD"], v["mobile"]
    CONTENT = W - 2 * PAD
    el = []
    y = 0

    def divider(full=True):
        x1 = 1 if full else PAD
        el.append(f'<line x1="{x1}" y1="{y}" x2="{W - x1}" y2="{y}" stroke="{t["border"]}"/>')

    def section(method, path, meta, meta_short):
        nonlocal y
        divider()
        y += 26
        chip_w = int(len(method) * 7.5) + 18
        el.append(f'<rect x="{PAD}" y="{y - 16}" width="{chip_w}" height="24" rx="6" fill="{t["chip"]}"/>')
        el.append(text(PAD + chip_w / 2, y, method, t["fg"], 12, weight=600, anchor="middle"))
        el.append(text(PAD + chip_w + 12, y + 0.5, esc(path), t["fg"], 14, weight=600))
        el.append(text(W - PAD, y, esc(meta_short if mobile else meta), t["muted"], 12, anchor="end"))
        y += 40

    def paragraph(s, px=None, color=None, size=13, lh=LH, x=None, cw=CW13):
        nonlocal y
        for ln in wrap(s, px or CONTENT, cw):
            el.append(text(x or PAD, y, esc(ln), color or t["muted"], size))
            y += lh

    # ---- terminal top bar
    for cx in (PAD - 6, PAD + 10, PAD + 26):
        el.append(f'<circle cx="{cx}" cy="21" r="4.5" fill="{t["chip"]}"/>')
    el.append(text(PAD + 48, 25.5, "katsuba.dev", t["muted"], 13))
    el.append(text(W - PAD + 6, 25.5, ":8080", t["faint"], 13, anchor="end"))
    y = 41
    divider()

    # ---- hero
    y += 37
    el.append(text(PAD, y, f'$ <tspan fill="{t["fg"]}">./katsuba --serve</tspan>', t["faint"], 14, preserve=True))
    el.append(f'<rect x="{PAD + 170}" y="{y - 13}" width="8" height="16" fill="{t["fg"]}">'
              f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" '
              f'dur="1.1s" repeatCount="indefinite"/></rect>')
    y += 40
    title = "Igor Katsuba — a system exposed over a few transports."
    if mobile:
        for ln in wrap(title, CONTENT, CW18):
            el.append(text(PAD, y, esc(ln), t["fg"], 18, weight=600))
            y += 28
        y += 10
    else:
        el.append(text(PAD, y, title, t["fg"], 19, weight=600))
        y += 38
    kv_size = 13 if mobile else 14
    kv_cw = CW13 if mobile else 9.4
    for key, val in [("capabilities:  ", "[ building, leading, writing, speaking ]"),
                     ("transports:    ", "[ github · telegram · email ]"),
                     ("status:        ", "200 OK — up and serving traffic")]:
        if (len(key) + len(val)) * kv_cw > CONTENT:
            # Narrow card: the value gets its own indented line rather than
            # running off the edge.
            el.append(text(PAD, y, key.strip(), t["faint"], kv_size))
            y += 22
            el.append(text(PAD + 14, y, val, t["fg"], kv_size))
        else:
            el.append(text(PAD, y, f'{key}<tspan fill="{t["fg"]}">{val}</tspan>',
                           t["faint"], kv_size, preserve=True))
        y += 26
    y += 14

    # ---- manifest
    divider()
    y += 34
    el.append(text(PAD, y, "// manifest", t["faint"], 13))
    y += 32
    m_size, m_cw, m_lh = (16, 10.9, 26) if mobile else (17, CW17, 28)
    for ln in wrap(MANIFEST, CONTENT, m_cw):
        el.append(text(PAD, y, esc(ln), t["fg"], m_size, weight=600))
        y += m_lh
    y += 12

    # ---- GET /about
    section("GET", "/about", "200 OK · text/plain", "200 OK")
    for p in ABOUT_PARAGRAPHS:
        paragraph(p)
        y += 12
    y += 4
    divider(full=False)
    y += 30
    for name, desc in FNS:
        el.append(text(PAD, y, esc(name), t["fg"], 14, weight=600))
        y += 24
        paragraph(desc)
        y += 14
    y += 4

    # ---- GET /tools
    section("GET", "/tools", "200 OK · 7 items · application/json", "200 OK · 7")
    for num, name, desc in TOOLS:
        el.append(text(PAD, y, num, t["faint"], 13))
        el.append(text(PAD + 40, y, esc(name), t["fg"], 15, weight=600))
        y += 24
        if mobile:
            paragraph(desc)
        else:
            paragraph(desc, px=CONTENT - 40, x=PAD + 40)
        y += 16
    y += 2

    # ---- GET /speaking
    section("GET", "/speaking", "200 OK · 3 talks · video", "200 OK · 3")
    for title_, venue in TALKS:
        el.append(f'<polygon points="{PAD},{y - 11} {PAD},{y + 1} {PAD + 11},{y - 5}" fill="{t["faint"]}"/>')
        if mobile:
            for ln in wrap(title_, CONTENT - 26, 9.4):
                el.append(text(PAD + 26, y, esc(ln), t["fg"], 14, weight=600))
                y += 22
            el.append(text(PAD + 26, y, esc(venue), t["muted"], 13))
            y += 34
        else:
            el.append(text(PAD + 26, y, esc(title_), t["fg"], 14, weight=600))
            el.append(text(W - PAD, y, esc(venue), t["muted"], 13, anchor="end"))
            y += 34
    y += 4

    # ---- GET /experience
    section("GET", "/experience", f"200 OK · {len(ROLES)} roles · résumé", f"200 OK · {len(ROLES)}")
    for i, (company, role, period, summary) in enumerate(ROLES):
        el.append(text(PAD, y, esc(company), t["fg"], 14, weight=600))
        el.append(text(W - PAD, y, period, t["faint"], 13, anchor="end"))
        if mobile:
            y += 22
            el.append(text(PAD, y, esc(role), t["muted"], 13))
        else:
            # Role sits right after the company name, as on the site — the roles
            # are long enough now that a fixed column would run into the period.
            el.append(text(PAD + len(company) * CW18 * 14 / 18 + 14, y, esc(role), t["muted"], 13))
        y += 22
        paragraph(summary)
        y += 8
        if i < len(ROLES) - 1:
            divider(full=False)
            y += 22
    y += 6
    el.append(text(PAD, y, f'→ <tspan fill="{t["fg"]}" font-weight="600">{RESUME_LINK[0]}</tspan>'
                          f'  <tspan fill="{t["muted"]}">{RESUME_LINK[1]}</tspan>',
                   t["faint"], 13, preserve=True))
    y += 16

    # ---- POST /contact
    section("POST", "/contact", "accepting connections", "accepting")
    paragraph(CONTACT_TEXT)
    y += 16
    for label, url in TRANSPORTS:
        el.append(text(PAD, y, f'→ <tspan fill="{t["fg"]}" font-weight="600">{esc(label.ljust(11))}</tspan>'
                              f'<tspan fill="{t["muted"]}">{esc(url)}</tspan>', t["faint"], 13, preserve=True))
        y += 24
    y += 14

    # ---- footer
    divider()
    y += 26
    el.append(text(W / 2, y, f'<tspan fill="{t["muted"]}">katsuba.dev</tspan> · connection closed · '
                             f'<tspan fill="{t["muted"]}">200</tspan>', t["faint"], 12, anchor="middle"))
    y += 22

    h = y
    body = "\n  ".join(el)
    return (
        f'<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">\n'
        f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="10" '
        f'fill="{t["bg"]}" stroke="{t["border"]}"/>\n'
        f'  {body}\n</svg>\n'
    )


for prefix, v in VARIANTS.items():
    for theme, t in THEMES.items():
        with open(os.path.join(OUT, f"card-{prefix}{theme}.svg"), "w") as f:
            f.write(build(t, v))

print("done:", sorted(os.listdir(OUT)))
