/* Motor v2 de Atajos IA: construye una línea de tiempo GSAP determinista a partir de window.GUION.
 * El grabador llama a window.__seek(t) cuadro por cuadro y captura la pantalla.
 * window.__sfx expone los efectos de sonido (nombre, tiempo, duración) para la mezcla de audio. */
(function () {
  gsap.registerPlugin(TextPlugin);
  gsap.ticker.lagSmoothing(0);
  const G = window.GUION;
  const SFX = [];
  const ACENTO = (G.marca && G.marca.acento) || "#ffd400";
  document.documentElement.style.setProperty("--acento", ACENTO);

  // ---------- utilidades ----------
  function el(tag, cls, html, padre) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    if (padre) padre.appendChild(e);
    return e;
  }
  const icono = (n) => (G.iconos && G.iconos[n]) || "";
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const marcar = (s) => esc(s).replace(/\*([^*]+)\*/g, '<span class="resaltado">$1</span>');
  function sonido(n, t, dur) { if (t >= 0) SFX.push({ n, t: +t.toFixed(3), dur: dur ? +dur.toFixed(3) : undefined }); }
  const fmtNum = (v, dec) => Number(v).toLocaleString("es-ES", { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 });
  function reloj(seg) {
    seg = Math.round(seg);
    const h = Math.floor(seg / 3600), m = Math.floor((seg % 3600) / 60), s = seg % 60;
    return h ? `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}` : `${m}:${String(s).padStart(2, "0")}`;
  }
  const PUNTERO = '<svg viewBox="0 0 24 24"><path d="M4 2 L4 19 L8.5 15 L11.5 22 L14.5 20.7 L11.6 14 L18 14 Z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
  const LOGO = `<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="48" fill="${ACENTO}"/><path d="M28 30 L50 50 L28 70 Z M50 30 L72 50 L50 70 Z" fill="#0b0d12"/></svg>`;

  // contexto de una escena: tiempos de beats relativos al inicio de la escena
  function contexto(es) {
    const beats = es.beats;
    return {
      B: (i, off = 0) => beats[Math.max(0, Math.min(i, beats.length - 1))].t + (off || 0),
      D: (i) => beats[Math.max(0, Math.min(i, beats.length - 1))].d,
      fin: es.dur,
      abs: (t) => es.inicio + t,
      sonido: (n, t, dur) => sonido(n, es.inicio + t, dur),
    };
  }

  // ---------- plantillas ----------
  const P = {};

  P.titular = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    const caja = el("div", "centrado", null, cam);
    let kicker;
    if (d.etiqueta) kicker = el("div", "kicker", (d.icono ? `<span class="icono" style="width:30px;height:30px">${icono(d.icono)}</span>` : "") + esc(d.etiqueta), caja);
    const tit = el("div", "titular", null, caja);
    if (d.tamano) tit.style.fontSize = d.tamano + "px";
    const lineas = (d.lineas || []).map((l) => (typeof l === "string" ? { texto: l } : l));
    lineas.forEach((l, i) => {
      const ln = el("span", "linea", null, tit);
      ln.innerHTML = marcar(l.texto).split(/(<span class="resaltado">[^<]*<\/span>| )/).filter((x) => x && x !== " ")
        .map((w) => (w.startsWith("<span") ? w.replace('class="resaltado"', 'class="palabra resaltado"') : `<span class="palabra">${w}</span>`)).join(" ");
      const t = c.B(l.beat || 0, 0.25 + (l.beat ? 0 : i * 0.18));
      tl.from(ln.querySelectorAll(".palabra"), { yPercent: 115, rotate: 3, duration: 0.8, ease: "power4.out", stagger: 0.06 }, t);
      ln.querySelectorAll(".resaltado").forEach((r) => {
        tl.fromTo(r, { "--trazo": 0 }, { "--trazo": 1, duration: 0.5, ease: "power2.inOut" }, t + 0.45);
        c.sonido("pop", t + 0.5);
      });
    });
    if (kicker) tl.from(kicker, { y: 30, opacity: 0, duration: 0.6 }, c.B(0, 0.1));
    if (d.sub) {
      const sub = el("div", "sub", marcar(d.sub), caja);
      tl.from(sub, { y: 40, opacity: 0, duration: 0.7 }, c.B(d.sub_beat != null ? d.sub_beat : Math.min(1, es.beats.length - 1), 0.2));
    }
    return tl;
  };

  P.cifra = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    const caja = el("div", "centrado", null, cam);
    const num = el("div", "cifra-num", (d.prefijo || "") + fmtNum(0, d.decimales) + (d.sufijo || ""), caja);
    const etq = el("div", "cifra-etq", marcar(d.etiqueta || ""), caja);
    const t0 = c.B(0, 0.2);
    const proxy = { v: 0 };
    tl.from(num, { scale: 0.6, opacity: 0, duration: 0.6, ease: "back.out(1.6)" }, t0);
    tl.to(proxy, { v: d.valor, duration: 1.4, ease: "power2.out",
      onUpdate: () => { num.textContent = (d.prefijo || "") + fmtNum(proxy.v, d.decimales) + (d.sufijo || ""); } }, t0);
    c.sonido("subida", t0, 1.4);
    c.sonido("ding", t0 + 1.4);
    tl.from(etq, { y: 40, opacity: 0, duration: 0.7 }, t0 + 0.6);
    if (d.fuente) tl.from(el("div", "fuente", "Fuente: " + esc(d.fuente), caja), { opacity: 0, duration: 0.6 }, t0 + 1.2);
    return tl;
  };

  P.antes_despues = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    const lado = (k, x) => {
      const o = d[k], caja = el("div", "ad tarjeta " + k, null, cam);
      el("div", "etq", k === "antes" ? "Antes" : "Después", caja);
      const r = el("div", "reloj", reloj(0), caja);
      el("div", "det", marcar(o.texto || ""), caja);
      const t = c.B(o.beat != null ? o.beat : (k === "antes" ? 0 : 1), 0.2);
      tl.from(caja, { x, opacity: 0, duration: 0.7, ease: "power3.out" }, t);
      const p = { v: 0 };
      tl.to(p, { v: o.segundos, duration: 1.2, ease: "power2.out", onUpdate: () => { r.textContent = reloj(p.v); } }, t + 0.3);
      c.sonido(k === "antes" ? "tic" : "ding", t + (k === "antes" ? 0.3 : 1.5), k === "antes" ? 1.2 : undefined);
      return t;
    };
    lado("antes", -120);
    const t2 = lado("despues", 120);
    const vs = el("div", "vs", "VS", cam);
    tl.from(vs, { scale: 0, duration: 0.5, ease: "back.out(2)" }, t2);
    return tl;
  };

  P.lista = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    if (d.titulo) tl.from(el("div", "lista-titulo", marcar(d.titulo), cam), { y: 30, opacity: 0, duration: 0.6 }, c.B(0, 0.15));
    const lista = el("div", "lista", null, cam);
    if (d.titulo) lista.style.top = "57%";
    d.items.forEach((it, i) => {
      it = typeof it === "string" ? { texto: it } : it;
      const fila = el("div", "item tarjeta", null, lista);
      el("div", "num", it.icono ? icono(it.icono) : String(i + 1), fila);
      el("div", "txt", marcar(it.texto) + (it.detalle ? `<small>${esc(it.detalle)}</small>` : ""), fila);
      const t = c.B(it.beat != null ? it.beat : i, 0.15);
      tl.from(fila, { x: 90, opacity: 0, duration: 0.6, ease: "power3.out" }, t);
      tl.from(fila.querySelector(".num"), { scale: 0, rotate: -20, duration: 0.5, ease: "back.out(2)" }, t + 0.1);
      c.sonido("pop", t + 0.1);
    });
    return tl;
  };

  P.capitulo = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    const caja = el("div", "centrado", null, cam);
    caja.style.gap = "34px";
    const n = el("div", "cap-num", String(d.numero).padStart(2, "0"), caja);
    const tit = el("div", "cap-tit", marcar(d.titulo), caja);
    const seg = el("div", "cap-seg", null, caja);
    for (let i = 1; i <= (d.total || 4); i++) el("div", "", "<i></i>", seg);
    tl.from(n, { scale: 1.6, opacity: 0, duration: 0.8, ease: "expo.out" }, 0.15);
    tl.from(tit, { y: 50, opacity: 0, duration: 0.7 }, 0.35);
    tl.to(seg.querySelectorAll("i"), { scaleX: (i) => (i < d.numero ? 1 : 0), duration: 0.6, stagger: 0.08, ease: "power2.inOut" }, 0.6);
    return tl;
  };

  P.aviso = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    const caja = el("div", "centrado", null, cam);
    const card = el("div", "aviso tarjeta" + (d.nivel === "rojo" ? " rojo" : ""), null, caja);
    const ic = el("div", "icono", icono(d.icono || "triangle-alert"), card);
    el("div", "", `<h2>${marcar(d.titulo)}</h2>` + (d.texto ? `<p>${marcar(d.texto)}</p>` : ""), card);
    tl.from(card, { scale: 0.85, opacity: 0, duration: 0.6, ease: "back.out(1.5)" }, c.B(0, 0.15));
    tl.fromTo(ic, { rotate: 0 }, { keyframes: { rotate: [0, -12, 10, -6, 4, 0] }, duration: 0.7 }, c.B(0, 0.5));
    c.sonido("alerta", c.B(0, 0.45));
    return tl;
  };

  P.comparar = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    if (d.titulo) tl.from(el("div", "lista-titulo", marcar(d.titulo), cam), { y: 30, opacity: 0, duration: 0.6 }, c.B(0, 0.15));
    const card = el("div", "tabla-cmp tarjeta", null, cam);
    const tb = el("table", "", `<tr>${d.columnas.map((x) => `<th>${esc(x)}</th>`).join("")}</tr>`, card);
    d.filas.forEach((f, i) => {
      const tr = el("tr", "", f.map((x) => `<td>${marcar(x)}</td>`).join(""), tb);
      tl.from(tr, { opacity: 0, x: 40, duration: 0.5 }, c.B(d.beats_filas ? d.beats_filas[i] : i, 0.15));
      c.sonido("pop", c.B(d.beats_filas ? d.beats_filas[i] : i, 0.15));
      if (d.ganador === i) {
        tl.set(tr, { className: "gana" }, c.B(d.ganador_beat != null ? d.ganador_beat : es.beats.length - 1, 0.2));
        c.sonido("ding", c.B(d.ganador_beat != null ? d.ganador_beat : es.beats.length - 1, 0.2));
      }
    });
    return tl;
  };

  P.final = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    const tit = el("div", "titular", marcar(d.titulo || "Sigue con este atajo"), cam);
    Object.assign(tit.style, { position: "absolute", left: "160px", top: "150px", fontSize: "84px" });
    const v = el("div", "final-hueco", null, cam);
    Object.assign(v.style, { left: "160px", top: "330px", width: "1000px", height: "563px" });
    const s = el("div", "final-hueco", null, cam);
    Object.assign(s.style, { left: "1300px", top: "430px", width: "360px", height: "360px", borderRadius: "50%" });
    tl.from(tit, { y: 40, opacity: 0, duration: 0.7 }, 0.2);
    tl.from([v, s], { scale: 0.9, opacity: 0, duration: 0.6, stagger: 0.15 }, 0.4);
    return tl;
  };

  // ---------- réplica de Excel ----------
  const FILA = 48, CAB_H = 36, CAB_W = 64, HOJA_Y = 210, XL_X = 160, XL_Y = 120;
  const colNum = (s) => s.split("").reduce((n, ch) => n * 26 + ch.charCodeAt(0) - 64, 0) - 1;
  const colLetra = (n) => { let s = ""; n++; while (n) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; };
  function parseRef(ref) {
    const [a, b] = ref.split(":");
    const p = (x) => { const m = x.match(/^([A-Z]+)(\d+)$/); return { c: colNum(m[1]), r: +m[2] }; };
    const A = p(a), Bb = b ? p(b) : A;
    return { c1: Math.min(A.c, Bb.c), r1: Math.min(A.r, Bb.r), c2: Math.max(A.c, Bb.c), r2: Math.max(A.r, Bb.r) };
  }

  P.excel = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline({ defaults: { ease: "power3.inOut" } });
    const datos = d.celdas || [];
    const ncol = Math.max(8, (datos[0] || []).length + 3);
    const anchos = Array.from({ length: ncol }, (_, i) => (d.anchos && d.anchos[i]) || 210);
    const colX = [CAB_W];
    anchos.forEach((w, i) => colX.push(colX[i] + w));
    const nfil = 12;

    const xl = el("div", "xl", null, cam);
    el("div", "xl-titulo", `<span class="app">${icono("sheet")}</span>${esc(d.archivo || "Libro1.xlsx")}<span style="opacity:.75;font-weight:400">  ·  Guardado</span>` +
      `<div class="der"><span class="xl-boton-ia">${icono("sparkles")}${esc(d.asistente || "Copilot")}</span></div>`, xl);
    el("div", "xl-pestanas", ["Archivo", "Inicio", "Insertar", "Disposición", "Fórmulas", "Datos", "Revisar", "Vista"]
      .map((t) => `<span class="${t === (d.pestana || "Inicio") ? "on" : ""}">${t}</span>`).join(""), xl);
    el("div", "xl-cinta", ["clipboard-paste", "|", "bold", "italic", "underline", "|", "align-left", "align-center", "|", "percent", "dollar-sign", "|", "sigma", "funnel", "chart-column", "table", "|", "paint-bucket"]
      .map((n) => (n === "|" ? '<span class="sep"></span>' : `<span class="icono">${icono(n)}</span>`)).join(""), xl);
    const fbar = el("div", "xl-formula", null, xl);
    const nombre = el("div", "xl-nombre", "A1", fbar);
    el("div", "xl-fx", "fx", fbar);
    const ftexto = el("div", "xl-ftexto", "", fbar);
    const hoja = el("div", "xl-hoja", null, xl);
    el("div", "xl-pie", `<span class="on">${esc(d.hoja || "Hoja1")}</span><span>+</span>`, xl);
    hoja.style.top = HOJA_Y + "px";

    // grilla
    const celdas = {}, cabCol = [], cabFil = [];
    el("div", "xl-celda cab", "", hoja).style.cssText = `left:0;top:0;width:${CAB_W}px;height:${CAB_H}px`;
    for (let ci = 0; ci < ncol; ci++) {
      const h = el("div", "xl-celda cab", colLetra(ci), hoja);
      h.style.cssText = `left:${colX[ci]}px;top:0;width:${anchos[ci]}px;height:${CAB_H}px`;
      cabCol.push(h);
    }
    for (let r = 1; r <= nfil; r++) {
      const h = el("div", "xl-celda cab", String(r), hoja);
      h.style.cssText = `left:0;top:${CAB_H + (r - 1) * FILA}px;width:${CAB_W}px;height:${FILA}px`;
      cabFil.push(h);
      for (let ci = 0; ci < ncol; ci++) {
        const v = datos[r - 1] && datos[r - 1][ci] != null ? String(datos[r - 1][ci]) : "";
        const esNum = /^[-+]?[$€]?\s?[\d.,]+\s?%?$/.test(v.trim()) && v.trim() !== "";
        const cel = el("div", "xl-celda" + (esNum ? " num" : "") + (r === 1 && d.encabezado !== false ? " enc" : ""), null, hoja);
        cel.style.cssText = `left:${colX[ci]}px;top:${CAB_H + (r - 1) * FILA}px;width:${anchos[ci]}px;height:${FILA}px`;
        const span = el("span", "", esc(v), cel);
        celdas[colLetra(ci) + r] = { cel, span };
      }
    }
    const rect = (ref) => {
      const R = parseRef(ref);
      return { x: colX[R.c1], y: HOJA_Y + CAB_H + (R.r1 - 1) * FILA, w: colX[R.c2 + 1] - colX[R.c1], h: (R.r2 - R.r1 + 1) * FILA, R };
    };
    const sel = el("div", "xl-sel", null, xl);
    const s0 = rect(d.seleccion_inicial || "A1");
    gsap.set(sel, { left: s0.x, top: s0.y, width: s0.w, height: s0.h });
    const puntero = el("div", "puntero", PUNTERO, xl);
    const onda = el("div", "onda", null, xl);
    let px = 1250, py = 760;
    gsap.set(puntero, { x: px, y: py });
    let notaActual = null, refs = [], panel = null, panelMsgs = null, panelInput = null, colsOn = [];
    let zs = 1, zx = 0, zy = 0; // estado de la cámara (escala y desplazamiento de la ventana)
    const enPantalla = (x, y) => ({ x: XL_X + zx + x * zs, y: XL_Y + zy + y * zs });

    // entrada de la ventana
    tl.from(xl, { y: 80, rotateX: 8, opacity: 0, duration: 0.9, ease: "power3.out", transformPerspective: 1800 }, 0.1);

    const mover = (x, y, t, dur = 0.55) => { tl.to(puntero, { x, y, duration: dur, ease: "power2.inOut" }, t); px = x; py = y; return t + dur; };
    const clic = (t) => {
      tl.set(onda, { x: px + 4, y: py + 4 }, t);
      tl.fromTo(onda, { scale: 0.3, opacity: 1 }, { scale: 1.5, opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false }, t);
      tl.to(puntero, { scale: 0.85, duration: 0.08, yoyo: true, repeat: 1, ease: "none" }, t);
      tl.to(puntero, { x: px + 70, y: py + 60, duration: 0.6, ease: "power2.out" }, t + 0.35); // se aparta para no tapar el resultado
      px += 70; py += 60;
      c.sonido("clic", t);
    };
    const encabezados = (ref, t) => {
      const R = parseRef(ref);
      colsOn.forEach((h) => tl.set(h, { className: "xl-celda cab" }, t));
      colsOn = [];
      for (let ci = R.c1; ci <= R.c2; ci++) { tl.set(cabCol[ci], { className: "xl-celda cab on" }, t); colsOn.push(cabCol[ci]); }
      for (let r = R.r1; r <= R.r2 && r <= nfil; r++) { tl.set(cabFil[r - 1], { className: "xl-celda cab on" }, t); colsOn.push(cabFil[r - 1]); }
    };
    const seleccionar = (ref, t, conClic = true) => {
      const r = rect(ref), primera = ref.split(":")[0], r1 = rect(primera);
      let tt = mover(r1.x + r1.w / 2, r1.y + r1.h / 2, t);
      if (conClic) clic(tt);
      tl.to(sel, { left: r1.x, top: r1.y, width: r1.w, height: r1.h, duration: 0.18, ease: "power2.out" }, tt);
      tl.set(nombre, { text: primera }, tt);
      encabezados(primera, tt);
      if (ref.includes(":")) {
        mover(r.x + r.w - 20, r.y + r.h - 14, tt + 0.1, 0.6);
        tl.to(sel, { width: r.w, height: r.h, duration: 0.6, ease: "power2.inOut" }, tt + 0.1);
        encabezados(ref, tt + 0.7);
        tt += 0.7;
      }
      return tt + 0.15;
    };
    const quitarRefs = (t) => { refs.forEach((x) => tl.to(x, { opacity: 0, duration: 0.3 }, t)); refs = []; };
    const mostrarRefs = (formula, t) => {
      const colores = ["#3b6fd8", "#d24726", "#8e44ad", "#16a085"];
      [...new Set((formula.match(/\$?[A-Z]{1,2}\$?\d+(:\$?[A-Z]{1,2}\$?\d+)?/g) || []).map((x) => x.replace(/\$/g, "")))].forEach((ref, i) => {
        const r = rect(ref.replace(/\$/g, ""));
        const b = el("div", "xl-ref", null, xl);
        Object.assign(b.style, { left: r.x + "px", top: r.y + "px", width: r.w + "px", height: r.h + "px", borderColor: colores[i % 4], background: colores[i % 4] + "14" });
        tl.fromTo(b, { opacity: 0 }, { opacity: 1, duration: 0.25, immediateRender: true }, t + i * 0.08);
        refs.push(b);
      });
    };
    const quitarNota = (t) => { if (notaActual) { tl.to(notaActual, { opacity: 0, scale: 0.9, duration: 0.25 }, t); notaActual = null; } };

    const A = {
      seleccionar: (a, t) => { quitarRefs(t); seleccionar(a.rango, t); },
      escribir: (a, t) => {
        quitarRefs(t);
        let tt = seleccionar(a.celda, t);
        const { span, cel } = celdas[a.celda];
        const dur = a.duracion || Math.min(3.2, Math.max(0.9, a.texto.length / 13));
        tl.set(cel, { justifyContent: "flex-start", overflow: "visible", zIndex: 2 }, tt);
        tl.set(span, { text: "" }, tt);
        tl.set(ftexto, { text: "" }, tt);
        tl.to(span, { text: { value: a.texto }, duration: dur, ease: "none" }, tt);
        tl.to(ftexto, { text: { value: a.texto }, duration: dur, ease: "none" }, tt);
        c.sonido("tecleo", tt, dur);
        mostrarRefs(a.texto, tt + dur * 0.6);
        tl.to(sel, { borderColor: "#3b6fd8", duration: 0.1 }, tt);
        tl.to(sel, { borderColor: "#107c41", duration: 0.1 }, tt + dur + 0.2);
      },
      calcular: (a, t) => {
        const { span, cel } = celdas[a.celda];
        quitarRefs(t);
        tl.set(span, { text: a.valor }, t);
        tl.set(cel, { overflow: "hidden", zIndex: 0 }, t);
        if (a.derecha !== false) tl.set(cel, { justifyContent: "flex-end" }, t);
        tl.fromTo(cel, { backgroundColor: "#fff3a6" }, { backgroundColor: "rgba(255,255,255,0)", duration: 1.2, ease: "power2.out", immediateRender: false }, t);
        tl.fromTo(span, { scale: 1.25 }, { scale: 1, duration: 0.5, ease: "back.out(2)", immediateRender: false }, t);
        c.sonido("pop", t);
      },
      rellenar: (a, t) => {
        const r = rect(a.rango), R = r.R;
        const r1 = rect(colLetra(R.c1) + R.r1);
        mover(r1.x + r1.w - 4, r1.y + r1.h - 4, t, 0.45);
        clic(t + 0.45);
        const dur = a.duracion || 0.9;
        mover(r1.x + r1.w - 4, r.y + r.h - 4, t + 0.55, dur);
        tl.to(sel, { left: r.x, top: r.y, width: r.w, height: r.h, duration: dur, ease: "power2.inOut" }, t + 0.55);
        (a.valores || []).forEach((v, i) => {
          const ref = colLetra(R.c1) + (R.r1 + i);
          if (!celdas[ref]) return;
          const tc = t + 0.55 + (dur * (i + 1)) / a.valores.length;
          tl.set(celdas[ref].span, { text: String(v) }, tc);
          tl.set(celdas[ref].cel, { justifyContent: /^[-+$€\d]/.test(String(v)) ? "flex-end" : "flex-start" }, tc);
          tl.fromTo(celdas[ref].cel, { backgroundColor: "#fff3a6" }, { backgroundColor: "rgba(255,255,255,0)", duration: 0.8, immediateRender: false }, tc);
        });
        c.sonido("arrastre", t + 0.55, dur);
        encabezados(a.rango, t + 0.55 + dur);
      },
      resaltar: (a, t) => {
        const r = rect(a.rango), col = a.color || ACENTO;
        const b = el("div", "xl-marca", null, xl);
        Object.assign(b.style, { left: r.x + "px", top: r.y + "px", width: r.w + "px", height: r.h + "px", background: col + "2e", border: `3px solid ${col}` });
        tl.fromTo(b, { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)", immediateRender: true }, t);
        if (a.etiqueta) {
          const e = el("div", "xl-etiqueta", esc(a.etiqueta), xl);
          const derecha = enPantalla(r.x + r.w + 240, 0).x < 1890;
          Object.assign(e.style, derecha ? { left: r.x + r.w + 14 + "px", top: r.y + 6 + "px" } : { left: r.x + "px", top: r.y + r.h + 10 + "px" });
          Object.assign(e.style, { background: col, color: col === ACENTO ? "#111" : "#fff" });
          tl.fromTo(e, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.35, immediateRender: true }, t + 0.15);
          if (a.hasta != null) tl.to(e, { opacity: 0, duration: 0.3 }, t + a.hasta);
        }
        if (a.hasta != null) tl.to(b, { opacity: 0, duration: 0.3 }, t + a.hasta);
        c.sonido("pop", t);
      },
      formato: (a, t) => {
        const lista = a.celdas ? Object.entries(a.celdas) : [];
        if (a.rango) {
          const R = parseRef(a.rango);
          for (let ci = R.c1; ci <= R.c2; ci++) for (let rr = R.r1; rr <= R.r2; rr++) lista.push([colLetra(ci) + rr, a.fondo]);
        }
        lista.forEach(([ref, col], i) => {
          if (!celdas[ref]) return;
          tl.to(celdas[ref].cel, { backgroundColor: col, color: a.texto || "#1f1f1f", duration: 0.35, ease: "power1.out" }, t + i * 0.05);
        });
        c.sonido("brillo", t, 0.4 + lista.length * 0.05);
      },
      zoom: (a, t) => {
        const r = rect(a.rango), s = a.escala || 1.6;
        const cx = r.x + r.w / 2, cy = r.y + r.h / 2;
        zs = s; zx = 960 - XL_X - cx * s; zy = 560 - XL_Y - cy * s;
        tl.to(xl, { scale: s, x: zx, y: zy, duration: a.duracion || 1.1, ease: "power3.inOut" }, t);
        c.sonido("zoom", t);
      },
      zoom_fuera: (a, t) => { zs = 1; zx = 0; zy = 0; tl.to(xl, { scale: 1, x: 0, y: 0, duration: a.duracion || 1, ease: "power3.inOut" }, t); c.sonido("zoom", t); },
      nota: (a, t) => {
        quitarNota(t);
        const r = rect(a.celda || a.rango);
        const n = el("div", "xl-nota", marcar(a.texto), xl);
        let lado = a.lado || "derecha";
        if (!a.lado && enPantalla(r.x + r.w + 26 + 560, 0).x > 1890) lado = enPantalla(r.x, r.y + r.h + 140).y < 1040 ? "abajo" : "arriba";
        const pos = lado === "derecha" ? { left: r.x + r.w + 26, top: r.y + r.h / 2 - 40 }
          : lado === "abajo" ? { left: r.x, top: r.y + r.h + 22 } : lado === "arriba" ? { left: r.x, top: r.y - 130 } : { left: r.x - 650, top: r.y };
        Object.assign(n.style, { left: pos.left + "px", top: pos.top + "px" });
        tl.fromTo(n, { opacity: 0, scale: 0.85, x: -20 }, { opacity: 1, scale: 1, x: 0, duration: 0.45, ease: "back.out(1.8)", transformOrigin: "0% 50%", immediateRender: true }, t);
        notaActual = n;
        c.sonido("pop", t);
      },
      quitar_nota: (a, t) => quitarNota(t),
      grafico: (a, t) => {
        const g = el("div", "xl-grafico", `<h4>${esc(a.titulo || "")}</h4>`, xl);
        Object.assign(g.style, { left: (a.x || 860) + "px", top: (a.y || 290) + "px", width: (a.ancho || 640) + "px" });
        const bars = el("div", "xl-barras", null, g), ejes = el("div", "xl-ejes", null, g);
        const max = Math.max(...a.valores);
        a.valores.forEach((v, i) => {
          const b = el("div", "b", `<span>${esc(a.textos ? a.textos[i] : v)}</span>`, bars);
          b.style.height = (v / max) * 100 + "%";
          if (a.destacar === i) b.style.background = "#f2b100";
          el("span", "", esc(a.etiquetas[i]), ejes);
          tl.fromTo(b, { scaleY: 0 }, { scaleY: 1, duration: 0.7, ease: "power3.out", immediateRender: true }, t + 0.3 + i * 0.08);
        });
        tl.fromTo(g, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, immediateRender: true }, t);
        c.sonido("subida", t + 0.3, 0.8);
      },
      panel_ia: (a, t) => {
        if (!panel) {
          panel = el("div", "xl-ia", null, xl);
          el("div", "xl-ia-cab", icono("sparkles") + esc(d.asistente || "Copilot"), panel);
          panelMsgs = el("div", "xl-ia-msgs", null, panel);
          panelInput = el("div", "xl-ia-input", "", panel);
          tl.fromTo(panel, { x: 600 }, { x: 0, duration: 0.6, ease: "power3.out", immediateRender: true }, t);
          c.sonido("whoosh_suave", t);
          t += 0.5;
        }
        const ib = { x: 1040 + 280, y: 880 - 44 - 60 };
        let tt = mover(ib.x, ib.y, t, 0.5);
        clic(tt);
        const dp = a.duracion_prompt || Math.min(3, Math.max(1, a.prompt.length / 24));
        tl.set(panelInput, { text: "" }, tt);
        tl.to(panelInput, { text: { value: a.prompt }, duration: dp, ease: "none" }, tt + 0.1);
        c.sonido("tecleo", tt + 0.1, dp);
        tt += dp + 0.35;
        const bu = el("div", "burbuja-u", esc(a.prompt), panelMsgs);
        tl.fromTo(bu, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, immediateRender: true }, tt);
        tl.set(panelInput, { text: "" }, tt);
        c.sonido("enviar", tt);
        tt += 0.5;
        const bi = el("div", "burbuja-ia", "", panelMsgs);
        tl.fromTo(bi, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: true }, tt);
        const dr = a.duracion_respuesta || Math.min(5, Math.max(1.2, a.respuesta.split(" ").length / 9));
        tl.to(bi, { text: { value: a.respuesta, delimiter: " " }, duration: dr, ease: "none" }, tt + 0.1);
        tt += dr + 0.2;
        if (a.formula) {
          const f = el("div", "", `<code></code>`, bi);
          tl.fromTo(f, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: true }, tt);
          tl.to(f.firstChild, { text: { value: a.formula }, duration: Math.min(1.5, a.formula.length / 25), ease: "none" }, tt);
          tt += 0.8;
          if (a.boton !== false) {
            const btn = el("span", "boton-insertar", "Insertar", bi);
            tl.fromTo(btn, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, immediateRender: true }, tt);
          }
        }
        c.sonido("respuesta", tt - dr - 0.2, 0.6);
      },
      insertar: (a, t) => {
        // clic en "Insertar" del panel y la fórmula aparece en la celda
        mover(1040 + 120, 640, t, 0.5);
        clic(t + 0.5);
        const { span, cel } = celdas[a.celda];
        const r = rect(a.celda);
        tl.to(sel, { left: r.x, top: r.y, width: r.w, height: r.h, duration: 0.25 }, t + 0.6);
        tl.set(nombre, { text: a.celda }, t + 0.6);
        tl.set(ftexto, { text: a.formula }, t + 0.6);
        tl.set(cel, { justifyContent: a.derecha === false ? "flex-start" : "flex-end" }, t + 0.6);
        tl.set(span, { text: a.valor || a.formula }, t + 0.6);
        tl.fromTo(cel, { backgroundColor: "#fff3a6" }, { backgroundColor: "rgba(255,255,255,0)", duration: 1.2, immediateRender: false }, t + 0.6);
        mostrarRefs(a.formula, t + 0.7);
        c.sonido("pop", t + 0.6);
      },
      cerrar_panel: (a, t) => { if (panel) { tl.to(panel, { x: 600, duration: 0.5, ease: "power3.in" }, t); c.sonido("whoosh_suave", t); } },
      quitar_refs: (a, t) => quitarRefs(t),
      mover: (a, t) => { const r = rect(a.celda); mover(r.x + r.w / 2, r.y + r.h / 2, t); },
    };

    // acciones ordenadas por tiempo absoluto dentro de la escena
    const acciones = [];
    es.beats.forEach((b, i) => {
      [].concat(b.accion || [], b.acciones || []).forEach((a) => acciones.push({ a, t: b.t + (a.retraso || 0) }));
    });
    acciones.sort((x, y) => x.t - y.t).forEach(({ a, t }) => {
      if (!A[a.tipo]) throw new Error("acción de Excel desconocida: " + a.tipo);
      A[a.tipo](a, Math.max(0.9, t));
    });
    return tl;
  };

  // ---------- chat a pantalla completa ----------
  P.chat = function (cam, es, c) {
    const d = es.datos, tl = gsap.timeline();
    const w = el("div", "chat", null, cam);
    el("div", "chat-cab", `<span class="punto"></span>${esc(d.app || "Asistente de IA")}<span style="margin-left:auto;font-size:20px;color:#8a8f9e;font-weight:500">${esc(d.modelo || "")}</span>`, w);
    const msgs = el("div", "chat-msgs", null, w);
    const input = el("div", "chat-input", "", w);
    tl.from(w, { y: 70, opacity: 0, scale: 0.97, duration: 0.8, ease: "power3.out" }, 0.1);
    const acciones = [];
    es.beats.forEach((b) => [].concat(b.accion || [], b.acciones || []).forEach((a) => acciones.push({ a, t: b.t + (a.retraso || 0) })));
    acciones.sort((x, y) => x.t - y.t).forEach(({ a, t }) => {
      t = Math.max(0.8, t);
      if (a.tipo === "prompt") {
        const dp = a.duracion || Math.min(3.5, Math.max(1, a.texto.length / 22));
        tl.set(input, { text: "" }, t);
        tl.to(input, { text: { value: a.texto }, duration: dp, ease: "none" }, t);
        c.sonido("tecleo", t, dp);
        const bu = el("div", "chat-u", esc(a.texto), msgs);
        tl.fromTo(bu, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, immediateRender: true }, t + dp + 0.3);
        tl.set(input, { text: "" }, t + dp + 0.3);
        c.sonido("enviar", t + dp + 0.3);
      } else if (a.tipo === "respuesta") {
        const bi = el("div", "chat-ia", "", msgs);
        const dr = a.duracion || Math.min(6, Math.max(1.5, a.texto.split(" ").length / 8));
        tl.fromTo(bi, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: true }, t);
        tl.to(bi, { text: { value: a.texto, delimiter: " " }, duration: dr, ease: "none" }, t + 0.1);
        c.sonido("respuesta", t, 0.6);
        if (a.formula) {
          const f = el("div", "chat-ia", "<code></code>", msgs);
          tl.fromTo(f, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: true }, t + dr + 0.2);
          tl.to(f.firstChild, { text: { value: a.formula }, duration: Math.min(1.6, a.formula.length / 22), ease: "none" }, t + dr + 0.2);
        }
      }
    });
    return tl;
  };

  // ---------- montaje ----------
  const raiz = document.getElementById("escenas");
  const master = gsap.timeline({ paused: true });
  const TR = 0.65; // duración de las transiciones
  const capas = [];
  G.escenas.forEach((es, i) => {
    const capa = el("div", "escena", null, raiz);
    const deriva = el("div", "camara", null, capa);
    const cam = el("div", "camara", null, deriva);
    capa.style.zIndex = 10 + i;
    if (!P[es.plantilla]) throw new Error("plantilla desconocida: " + es.plantilla);
    master.add(P[es.plantilla](cam, es, contexto(es)), es.inicio);
    master.fromTo(deriva, { scale: 1 }, { scale: es.plantilla === "excel" || es.plantilla === "chat" ? 1.015 : 1.035, duration: es.dur + TR, ease: "none", immediateRender: false }, es.inicio);
    capas.push(capa);
  });
  G.escenas.forEach((es, i) => {
    const capa = capas[i], prev = capas[i - 1], t = es.inicio;
    const tipo = i === 0 ? "ninguna" : es.transicion || (es.plantilla === "capitulo" ? "barrido" : es.plantilla === "excel" || es.plantilla === "chat" ? "zoom" : "empuje");
    master.set(capa, { visibility: "visible" }, t);
    if (G.escenas[i + 1]) master.set(capa, { visibility: "hidden" }, G.escenas[i + 1].inicio + TR + 0.05);
    if (!prev) return;
    if (tipo === "empuje") {
      master.fromTo(capa, { xPercent: 100 }, { xPercent: 0, duration: TR, ease: "power3.inOut", immediateRender: false }, t);
      master.to(prev, { xPercent: -35, opacity: 0, duration: TR, ease: "power3.inOut" }, t);
      sonido("whoosh", t - 0.05);
    } else if (tipo === "zoom") {
      master.fromTo(capa, { scale: 1.25, opacity: 0 }, { scale: 1, opacity: 1, duration: TR, ease: "power3.out", immediateRender: false }, t);
      master.to(prev, { scale: 0.85, opacity: 0, duration: TR * 0.8, ease: "power2.in" }, t);
      sonido("whoosh", t - 0.05);
    } else if (tipo === "barrido") {
      const panel = el("div", "", `<div style="width:140px;height:140px">${LOGO}</div>`, document.getElementById("barridos"));
      Object.assign(panel.style, { position: "absolute", inset: 0, background: ACENTO, display: "flex", alignItems: "center", justifyContent: "center", zIndex: 60 });
      gsap.set(panel, { xPercent: -101 });
      master.to(panel, { xPercent: 0, duration: 0.35, ease: "power3.in" }, t - 0.35);
      master.to(panel, { xPercent: 101, duration: 0.45, ease: "power3.out" }, t + 0.05);
      master.set(prev, { opacity: 0 }, t);
      sonido("whoosh", t - 0.4);
    } else if (tipo === "fundido") {
      master.fromTo(capa, { opacity: 0 }, { opacity: 1, duration: TR, ease: "none", immediateRender: false }, t);
    }
  });

  // fondo vivo, barra de progreso, marca y subtítulos
  const dur = G.duracion;
  master.to(".m1", { x: 420, y: 260, duration: dur, ease: "none" }, 0);
  master.to(".m2", { x: -380, y: 300, duration: dur, ease: "none" }, 0);
  master.to(".m3", { x: 260, y: -360, duration: dur, ease: "none" }, 0);
  master.to("#reticula", { x: 64, y: 64, duration: dur, ease: "none" }, 0);
  master.to("#grano", { backgroundPosition: `${Math.round(dur * 37)}px ${Math.round(dur * 23)}px`, duration: dur, ease: `steps(${Math.max(1, Math.round(dur * 12))})` }, 0);
  if (G.progreso !== false) {
    master.fromTo("#progreso .barra", { scaleX: 0 }, { scaleX: 1, duration: dur, ease: "none" }, 0);
    G.escenas.forEach((es) => { if (es.capitulo) el("div", "marca-cap", null, document.getElementById("progreso")).style.left = (es.inicio / dur) * 100 + "%"; });
  } else document.getElementById("progreso").style.display = "none";
  document.getElementById("marca").innerHTML = LOGO + esc((G.marca && G.marca.nombre) || "Atajos IA");
  if (G.subtitulos) {
    const span = el("span", "", "", document.getElementById("subtitulos"));
    gsap.set(span, { opacity: 0 });
    G.escenas.forEach((es) => es.beats.forEach((b) => (b.trozos || []).forEach((tr) => {
      master.set(span, { text: tr.texto, opacity: 1 }, es.inicio + tr.t);
    })));
  }

  // grano: textura de ruido generada una vez
  const cv = document.createElement("canvas");
  cv.width = cv.height = 256;
  const cx = cv.getContext("2d"), img = cx.createImageData(256, 256);
  let semilla = 7;
  const azar = () => ((semilla = (semilla * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < img.data.length; i += 4) { const v = azar() * 255; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
  cx.putImageData(img, 0, 0);
  document.getElementById("grano").style.backgroundImage = `url(${cv.toDataURL()})`;

  window.__duracion = dur;
  window.__sfx = SFX.sort((a, b) => a.t - b.t);
  window.__seek = (t) => { master.seek(t, false); };
  master.seek(0);
  window.__listo = true;
})();
