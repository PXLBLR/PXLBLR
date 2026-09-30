"""Beat-based reel template: describe a reel as a list of beats and get a full timeline spec.

Beat keys (all optional except "d"):
  d        seconds on screen
  rh       monitor rhythm: (name, kw, readout[, color]) · "off" hides it · omitted keeps the previous one
  pill     (text, bg) small label above the top text
  top      headline text (supports *accent*) · hook=True makes it the big opening hook
  big      large reveal text · big_color · sub (line under big)
  bottom   body text in the lower zone · bullets=[...] left-aligned list
  quiz     seconds of countdown before big/sub are revealed
  shock    True adds charge → shock + flash at the reveal
  sfx      extra [(offset, name, gain)]
"""
from engine.brand import CYAN, NAVY, RED, WHITE, YELLOW

from .reels import SHOCK, M, P, T, endcard, logo

END = 4.5


def story(rid, beats, ask="Save this for your next *megacode*.", cover_t=1.6, **meta):
    els, fx = [], []
    t = 0.0
    cur_rh, rh_start = None, 0.0

    def close_monitor(at):
        if cur_rh and cur_rh != "off":
            name, kw, ro, *rest = cur_rh
            extra = {}
            if rest and rest[0]:
                extra["color"] = rest[0]
            if len(rest) > 1:
                extra["label"] = rest[1]
            if name in ("vfib", "asystole", "fine_vs_asystole", "cpr"):
                extra["beeps"] = False
            els.append(M(name, (rh_start, at), readout=ro, kw=kw, **extra))

    for i, b in enumerate(beats):
        d = b["d"]
        s, e = t, t + d
        if "rh" in b and b["rh"] != cur_rh:
            close_monitor(s)
            cur_rh, rh_start = b["rh"], s
        mon = cur_rh not in (None, "off")
        hook = b.get("hook")
        if i == 0:
            fx.append((0, b.get("open_sfx", "alarm"), 0.65))
        elif b.get("whoosh", True):
            fx.append((s, "whoosh", 0.6))
        y_top = 330
        if b.get("pill"):
            txt, bg = b["pill"]
            els.append(P(txt, (s, e), 300, bg=bg, fg=NAVY if bg in (CYAN, YELLOW) else WHITE, anim="pop"))
            y_top = 385
        if b.get("top"):
            if hook:
                els.append(T(b["top"], (s, e), 310, b.get("top_size", 100), anim="pop", max_w=960))
            else:
                els.append(T(b["top"], (s + 0.05, e), y_top if mon else y_top + 40, b.get("top_size", 62),
                             max_w=920))
        if b.get("sub_top"):
            els.append(T(b["sub_top"], (s + 0.5, e), 600, 44, weight="semibold", family="body", color=CYAN,
                         max_w=900))
        base = 1085 if mon else 820
        reveal = s + 0.45
        if b.get("quiz"):
            els.append({"type": "countdown", "t": (s + 0.4, s + 0.4 + b["quiz"]), "n": round(b["quiz"]),
                        "cy": base + 170})
            reveal = s + 0.4 + b["quiz"]
        y = base
        if b.get("big"):
            els.append(T(b["big"], (reveal, e), y, b.get("big_size", 112), color=b.get("big_color", RED),
                         anim="pop", weight="black", max_w=960, accent=b.get("big_accent", CYAN)))
            y += int(b.get("big_size", 112) * (1.1 * (b["big"].count("\n") + 1))) + 28
            if not b.get("quiz") and not b.get("shock"):
                fx.append((reveal, "pop", 0.7))
            if b.get("quiz"):
                fx.append((reveal, b.get("reveal_sfx", "ding"), 0.9))
        if b.get("sub"):
            els.append(T(b["sub"], (reveal + 0.15, e), y, b.get("sub_size", 48), weight="semibold",
                         family="body", color=b.get("sub_color", WHITE), accent=b.get("sub_accent", YELLOW),
                         max_w=900))
            y += 150
        if b.get("bottom"):
            els.append(T(b["bottom"], (reveal + (0.4 if b.get("big") else 0), e), y, b.get("bottom_size", 54),
                         max_w=900, accent=b.get("bottom_accent", RED)))
        if b.get("bullets"):
            txt = "\n".join("•  " + x for x in b["bullets"])
            els.append(T(txt, (reveal, e), y, b.get("bullet_size", 46), align="left", x=110, max_w=860,
                         weight="semibold", family="body", accent=CYAN, line_gap=1.38))
            fx.append((reveal, "pop", 0.6))
        if b.get("shock"):
            e2, f2, _ = SHOCK(reveal)
            els += e2
            fx += f2
        for off, name, gain in b.get("sfx", []):
            fx.append((s + off, name, gain))
        t = e
    close_monitor(t)
    els += endcard(t, t + END, ask=ask)
    D = t + END
    spec = {"id": rid, "duration": D, "elements": [logo(D)] + els, "sfx": fx, "cover_t": cover_t}
    spec.update(meta)
    return spec
