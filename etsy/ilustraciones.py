"""Ilustraciones vectoriales propias (SVG) para los packs. Cada función recibe la paleta del tema."""


def _svg(cuerpo, t):
    return (f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><g stroke="{t["ink"]}" stroke-width="3" '
            f'stroke-linejoin="round" stroke-linecap="round">{cuerpo}</g></svg>')


def tree(t):
    return _svg(
        f'<rect x="43" y="82" width="14" height="12" fill="#9a6a45"/>'
        f'<path d="M50 14 70 40H60L78 62H64L84 84H16L36 62H22L40 40H30Z" fill="{t["c2"]}"/>'
        f'<path d="M50 3l3.2 6.6 7.3 1-5.3 5.1 1.3 7.2L50 19.5l-6.5 3.4 1.3-7.2-5.3-5.1 7.3-1Z" fill="{t["c3"]}" stroke-width="2.2"/>'
        f'<g stroke-width="1.8"><circle cx="43" cy="50" r="4" fill="{t["c1"]}"/><circle cx="59" cy="70" r="4" fill="{t["c3"]}"/>'
        f'<circle cx="35" cy="74" r="4" fill="#fff"/><circle cx="57" cy="40" r="3.5" fill="#fff"/><circle cx="68" cy="76" r="3.5" fill="{t["c1"]}"/></g>', t)


def gift(t):
    return _svg(
        f'<rect x="18" y="44" width="64" height="46" rx="4" fill="{t["c1"]}"/><rect x="13" y="32" width="74" height="16" rx="4" fill="{t["c1"]}"/>'
        f'<rect x="43" y="32" width="14" height="58" fill="{t["c3"]}"/>'
        f'<path d="M50 32C40 8 18 14 28 32ZM50 32C60 8 82 14 72 32Z" fill="{t["c3"]}"/>', t)


def santa(t):
    return _svg(
        f'<path d="M20 72Q28 24 60 16Q84 12 86 42L74 36Q78 54 80 72Z" fill="{t["c1"]}"/>'
        f'<rect x="10" y="68" width="80" height="19" rx="9.5" fill="#fff"/><circle cx="86" cy="45" r="9.5" fill="#fff"/>', t)


def ginger(t):
    return _svg(
        f'<path d="M50 38C41 38 39 45 39 45L22 43a7 7 0 0 0-2 14L38 61 31 83a7 7 0 0 0 13 5L50 74l6 14a7 7 0 0 0 13-5L62 61l18-4a7 7 0 0 0-2-14L61 45S59 38 50 38Z" fill="#cf9254"/>'
        f'<circle cx="50" cy="25" r="17" fill="#cf9254"/>'
        f'<g stroke-width="2"><circle cx="44" cy="22" r="1.6" fill="{t["ink"]}"/><circle cx="56" cy="22" r="1.6" fill="{t["ink"]}"/>'
        f'<path d="M43 29q7 6 14 0" fill="none"/><circle cx="50" cy="50" r="3" fill="{t["c1"]}"/><circle cx="50" cy="61" r="3" fill="{t["c2"]}"/>'
        f'<path d="M24 47l4 6M72 53l4-6M35 80l7 3M58 83l7-3" stroke="#fff" stroke-width="3"/></g>', t)


def ornament(t):
    return _svg(
        f'<circle cx="50" cy="13" r="6" fill="none"/><rect x="42" y="18" width="16" height="11" rx="2" fill="{t["c3"]}"/>'
        f'<circle cx="50" cy="60" r="32" fill="{t["c1"]}"/>'
        f'<path d="M21 56l8-8 7 8 7-8 7 8 7-8 7 8 7-8 8 8" stroke="#fff" stroke-width="4" fill="none"/>'
        f'<g stroke="none" fill="{t["c3"]}"><circle cx="34" cy="72" r="3.5"/><circle cx="50" cy="76" r="3.5"/><circle cx="66" cy="72" r="3.5"/></g>', t)


def cane(t):
    d = "M36 90V38a17 17 0 0 1 34 0v8"
    return (f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke-linecap="round">'
            f'<path d="{d}" stroke="{t["ink"]}" stroke-width="19"/><path d="{d}" stroke="#fff" stroke-width="13"/>'
            f'<path d="{d}" stroke="{t["c1"]}" stroke-width="13" stroke-dasharray="9 11" stroke-linecap="butt"/></g></svg>')


def snowman(t):
    return _svg(
        f'<circle cx="50" cy="68" r="25" fill="#fff"/><circle cx="50" cy="36" r="17" fill="#fff"/>'
        f'<path d="M35 46q15 9 30 0l2 7q-17 9-34 0Z" fill="{t["c1"]}"/>'
        f'<rect x="38" y="6" width="24" height="16" rx="2" fill="{t["ink"]}"/><path d="M30 22H70" stroke-width="5"/>'
        f'<g stroke-width="2"><circle cx="44" cy="32" r="1.6" fill="{t["ink"]}"/><circle cx="56" cy="32" r="1.6" fill="{t["ink"]}"/>'
        f'<path d="M50 36l13 3-13 3Z" fill="{t["c3"]}"/><circle cx="50" cy="62" r="2.4" fill="{t["ink"]}"/><circle cx="50" cy="74" r="2.4" fill="{t["ink"]}"/></g>', t)


def star(t):
    return _svg(f'<path d="M50 8l12.5 26 28.5 4-20.7 20 5 28.5L50 73 24.7 86.500l5-28.500L9 38l28.500-4Z" fill="{t["c3"]}"/>'
                f'<g stroke-width="2"><circle cx="42" cy="46" r="1.8" fill="{t["ink"]}"/><circle cx="58" cy="46" r="1.8" fill="{t["ink"]}"/>'
                f'<path d="M43 55q7 6 14 0" fill="none"/></g>', t)


def partyhat(t):
    return _svg(
        f'<path d="M50 14 80 82H20Z" fill="{t["c1"]}"/>'
        f'<path d="M40 37 63 44M32 55 71 64M26 70 40 73" stroke="{t["c3"]}" stroke-width="6" fill="none"/>'
        f'<path d="M50 14 80 82H20Z" fill="none"/><ellipse cx="50" cy="83" rx="33" ry="7" fill="{t["c2"]}"/>'
        f'<circle cx="50" cy="12" r="8.500" fill="{t["c3"]}"/>', t)


def glass(t):
    return _svg(
        f'<path d="M34 10H66L62 48Q50 62 38 48Z" fill="#fff"/><path d="M36.500 28H63.500L62 48Q50 62 38 48Z" fill="{t["c3"]}"/>'
        f'<path d="M50 58V86M34 88H66" fill="none" stroke-width="4"/>'
        f'<g stroke-width="2" fill="#fff"><circle cx="46" cy="40" r="2.500"/><circle cx="55" cy="34" r="2"/><circle cx="52" cy="46" r="2"/></g>'
        f'<g stroke="{t["c1"]}" stroke-width="3" fill="none"><path d="M76 16l8-6M80 28h10M72 6l2-5"/></g>', t)


def clock(t):
    marcas = "".join(f'<path d="M50 24v6" transform="rotate({a} 50 54)"/>' for a in range(0, 360, 30))
    return _svg(
        f'<path d="M30 20l-8-8M70 20l8-8" stroke-width="5"/><circle cx="50" cy="54" r="36" fill="{t["c2"]}"/>'
        f'<circle cx="50" cy="54" r="28" fill="#fff"/><g stroke-width="2">{marcas}</g>'
        f'<path d="M50 54V32M50 54 43 36" stroke-width="4" fill="none"/><circle cx="50" cy="54" r="3" fill="{t["c1"]}"/>', t)


def firework(t):
    import math
    cols = [t["c1"], t["c3"], t["c2"]]
    rayos = ""
    for k in range(12):
        a = math.radians(k * 30)
        r1, r2 = 13, (40 if k % 2 == 0 else 30)
        x1, y1, x2, y2 = 50 + r1 * math.cos(a), 50 + r1 * math.sin(a), 50 + r2 * math.cos(a), 50 + r2 * math.sin(a)
        rayos += f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{cols[k % 3]}" stroke-width="6"/>'
        if k % 2:
            rayos += f'<circle cx="{50 + 42 * math.cos(a):.1f}" cy="{50 + 42 * math.sin(a):.1f}" r="3.500" fill="{cols[(k + 1) % 3]}" stroke="none"/>'
    return f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><g stroke-linecap="round">{rayos}<circle cx="50" cy="50" r="6" fill="{t["c3"]}" stroke="{t["ink"]}" stroke-width="2.500"/></g></svg>'


def balloon(t):
    return _svg(
        f'<path d="M50 74q-9 8 0 14t0 10" fill="none" stroke-width="2.500"/><ellipse cx="50" cy="40" rx="27" ry="33" fill="{t["c2"]}"/>'
        f'<path d="M45 72h10l-5 7Z" fill="{t["c2"]}"/><path d="M36 26q4-10 13-12" stroke="#fff" stroke-width="5" fill="none"/>', t)


def disco(t):
    return _svg(
        f'<path d="M50 4V22" stroke-width="3"/><circle cx="50" cy="56" r="34" fill="{t["c2"]}"/>'
        f'<g stroke="#fff" stroke-width="2.200" fill="none" opacity=".9"><path d="M17 50H83M19 66H81M26 36H74"/>'
        f'<path d="M50 22V90M36 25Q28 56 36 87M64 25Q72 56 64 87"/></g><circle cx="50" cy="56" r="34" fill="none"/>'
        f'<path d="M84 18l2 6 6 2-6 2-2 6-2-6-6-2 6-2Z" fill="{t["c3"]}" stroke-width="2"/>', t)


def popper(t):
    return _svg(
        f'<path d="M12 90 38 36 66 64Z" fill="{t["c3"]}"/><path d="M27 59 43 75M20 74 28 82" stroke="{t["c1"]}" stroke-width="6" fill="none"/>'
        f'<path d="M12 90 38 36 66 64Z" fill="none"/>'
        f'<g fill="none" stroke-width="3.500"><path d="M52 36q-6-12 4-22" stroke="{t["c1"]}"/><path d="M66 48q12-10 24-2" stroke="{t["c2"]}"/></g>'
        f'<g stroke-width="2"><circle cx="70" cy="22" r="4.500" fill="{t["c2"]}"/><circle cx="84" cy="66" r="4" fill="{t["c1"]}"/>'
        f'<rect x="78" y="26" width="9" height="9" rx="2" fill="{t["c3"]}" transform="rotate(20 82 30)"/><circle cx="40" cy="14" r="3.500" fill="{t["c3"]}"/></g>', t)


def mug(t):
    return _svg(
        f'<path d="M68 46h8a11 11 0 0 1 0 22h-8" fill="none" stroke-width="6"/><rect x="20" y="36" width="50" height="50" rx="8" fill="{t["c1"]}"/>'
        f'<path d="M45 52l3.500 7 7.500 1-5.500 5.300 1.300 7.700L45 69.400 38.200 73l1.300-7.700L34 60l7.500-1Z" fill="#fff" stroke-width="2"/>'
        f'<g fill="none" stroke-width="3.500" stroke="{t["c2"]}"><path d="M34 26q-5-7 0-14M47 26q-5-7 0-14M60 26q-5-7 0-14"/></g>', t)


def trophy(t):
    return _svg(
        f'<path d="M30 22H18q0 22 16 24M70 22H82q0 22-16 24" fill="none" stroke-width="5"/>'
        f'<path d="M30 14H70V40a20 20 0 0 1-40 0Z" fill="{t["c3"]}"/><rect x="44" y="60" width="12" height="14" fill="{t["c3"]}"/>'
        f'<rect x="30" y="74" width="40" height="14" rx="3" fill="{t["c1"]}"/>'
        f'<path d="M50 24l3 6.200 6.800 1-5 4.800 1.200 6.800L50 39.600 44 42.800l1.200-6.800-5-4.800 6.800-1Z" fill="#fff" stroke-width="2"/>', t)


def laptop(t):
    return _svg(
        f'<rect x="20" y="20" width="60" height="44" rx="5" fill="{t["ink"]}"/><rect x="26" y="26" width="48" height="32" rx="2" fill="#fff" stroke-width="2"/>'
        f'<path d="M8 66H92l-7 14H15Z" fill="{t["c2"]}"/>'
        f'<path d="M50 30 60 44H55L62 54H38L45 44H40Z" fill="{t["c1"]}" stroke-width="2"/>', t)


ICONOS = dict(tree=tree, gift=gift, santa=santa, ginger=ginger, ornament=ornament, cane=cane, snowman=snowman, star=star,
              partyhat=partyhat, glass=glass, clock=clock, firework=firework, balloon=balloon, disco=disco, popper=popper,
              mug=mug, trophy=trophy, laptop=laptop)


def guirnalda(t):
    """Tira decorativa del borde superior: luces de colores (Navidad) o banderines."""
    cols = [t["c1"], t["c3"], t["c2"]]
    ink = t["ink"]
    if t["luces"]:
        d, luces = "M0 5", ""
        for k in range(10):
            x = k * 60
            d += f"Q{x + 30} 27 {x + 60} 5"
            for j, (dx, dy) in enumerate([(15, 13.500), (30, 16.500), (45, 13.500)]):
                c = cols[(k * 3 + j) % 3]
                luces += (f'<rect x="{x + dx - 2.500}" y="{dy - 2}" width="5" height="4" fill="{ink}"/>'
                          f'<ellipse cx="{x + dx}" cy="{dy + 8}" rx="5" ry="7" fill="{c}" stroke="{ink}" stroke-width="1.500"/>')
        return f'<svg viewBox="0 0 600 34" xmlns="http://www.w3.org/2000/svg"><path d="{d}" fill="none" stroke="{ink}" stroke-width="1.800"/>{luces}</svg>'
    flags = "".join(f'<path d="M{x} 4H{x + 34}L{x + 17} 30Z" fill="{cols[i % 3]}" stroke="{ink}" stroke-width="1.500" stroke-linejoin="round"/>'
                    for i, x in enumerate(range(3, 600, 40)))
    return f'<svg viewBox="0 0 600 34" xmlns="http://www.w3.org/2000/svg"><path d="M0 4H600" stroke="{ink}" stroke-width="2"/>{flags}</svg>'
