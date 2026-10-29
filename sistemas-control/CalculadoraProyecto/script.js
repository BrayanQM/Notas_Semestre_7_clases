/* ==========================================================================
   LaplaceCalc - Motor de calculo y controlador de interfaz
   ========================================================================== */

const state = {
  mode: 'laplace',
  view: 'calculator',
  theme: localStorage.getItem('lapcalc_theme') || 'dark',
  history: JSON.parse(localStorage.getItem('lapcalc_history') || '[]'),
  chart: null,
  tMin: 0,
  tMax: 10,
  result: null
};

/* ========== Utilidades de expresion ========== */

function normalize(expr) {
  if (!expr) return '';
  let s = expr.trim();
  s = s.replace(/−/g, '-').replace(/×/g, '*').replace(/÷/g, '/');
  s = s.replace(/π/g, 'pi').replace(/ω/g, 'w');
  s = s.replace(/\bsen\b/g, 'sin').replace(/\btg\b/g, 'tan');
  s = s.replace(/²/g, '^2').replace(/³/g, '^3');
  // e^  -> exp
  s = s.replace(/\be\s*\^\s*\(/gi, 'exp(');
  s = s.replace(/\be\s*\^\s*([a-zA-Z0-9_]+)/gi, 'exp($1)');
  // multiplicacion implicita
  s = s.replace(/(\d+)\s*([a-zA-Z(])/g, '$1*$2');
  s = s.replace(/\)\s*([a-zA-Z0-9_(])/g, ')*$1');
  return s;
}

function validate(expr) {
  if (!expr || expr.trim() === '') return { ok: false, error: 'Ingresa una expresion matematica.' };
  let bal = 0;
  for (const ch of expr) {
    if (ch === '(') bal++;
    else if (ch === ')') bal--;
    if (bal < 0) return { ok: false, error: 'Parentesis desbalanceados.' };
  }
  if (bal !== 0) return { ok: false, error: 'Faltan parentesis de cierre.' };
  if (/(\+\+|\/\/|\^\^)/.test(expr)) return { ok: false, error: 'Operadores consecutivos invalidos.' };
  return { ok: true };
}

function toLatex(expr) {
  if (!expr) return '';
  let s = String(expr);
  try {
    if (window.math && window.math.parse) {
      return window.math.parse(s).toTex({ parenthesis: 'auto' });
    }
  } catch (e) { /* fallback */ }
  s = s.replace(/\bexp\((.*?)\)/g, 'e^{$1}');
  s = s.replace(/\bsin\((.*?)\)/g, '\\sin($1)');
  s = s.replace(/\bcos\((.*?)\)/g, '\\cos($1)');
  s = s.replace(/\bsinh\((.*?)\)/g, '\\sinh($1)');
  s = s.replace(/\bcosh\((.*?)\)/g, '\\cosh($1)');
  s = s.replace(/\bsqrt\((.*?)\)/g, '\\sqrt{$1}');
  s = s.replace(/\bpi\b/g, '\\pi');
  s = s.replace(/\*/g, ' \\cdot ');
  s = s.replace(/\^([0-9a-zA-Z]+)/g, '^{$1}');
  return s;
}

function renderLatex(el, tex, display = true) {
  if (!el) return;
  if (window.katex) {
    try { window.katex.render(tex, el, { throwOnError: false, displayMode: display }); return; }
    catch (e) { el.textContent = tex; }
  }
  el.textContent = tex;
}

function isNum(v) { return !isNaN(parseFloat(v)) && isFinite(v); }
function factorial(n) { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; }

function splitTerms(expr) {
  const terms = [];
  let depth = 0, start = 0;
  for (let i = 0; i < expr.length; i++) {
    const c = expr[i];
    if (c === '(') depth++;
    else if (c === ')') depth--;
    else if ((c === '+' || c === '-') && depth === 0 && i > 0 &&
             expr[i-1] !== '*' && expr[i-1] !== '^' && expr[i-1] !== '/') {
      terms.push(expr.slice(start, i).trim());
      start = i;
    }
  }
  terms.push(expr.slice(start).trim());
  return terms.filter(t => t.length);
}

function splitFactors(term) {
  const factors = [];
  let depth = 0, start = 0;
  for (let i = 0; i < term.length; i++) {
    const c = term[i];
    if (c === '(') depth++;
    else if (c === ')') depth--;
    else if (c === '*' && depth === 0) { factors.push(term.slice(start, i).trim()); start = i + 1; }
  }
  factors.push(term.slice(start).trim());
  return factors;
}

function extractCoeffOfVar(x, v) {
  let s = x.trim();
  if (s === v) return '1';
  if (s === '-' + v) return '-1';
  s = s.replace(new RegExp('\\*?' + v + '$', ''), '');
  return s.trim() || '1';
}

function extractNumDen(expr) {
  let depth = 0;
  for (let i = 0; i < expr.length; i++) {
    const c = expr[i];
    if (c === '(') depth++;
    else if (c === ')') depth--;
    else if (c === '/' && depth === 0) {
      let num = expr.slice(0, i).trim(), den = expr.slice(i + 1).trim();
      if (num.startsWith('(') && num.endsWith(')')) num = num.slice(1, -1);
      if (den.startsWith('(') && den.endsWith(')')) den = den.slice(1, -1);
      return { num, den };
    }
  }
  return { num: expr, den: '1' };
}

function coeffAndCore(term) {
  let s = term.trim(), sign = 1;
  if (s.startsWith('+')) s = s.slice(1).trim();
  else if (s.startsWith('-')) { sign = -1; s = s.slice(1).trim(); }
  const m = s.match(/^([0-9.]+)\*(.*)$/);
  if (m) return { coeff: sign * parseFloat(m[1]), core: m[2].trim() };
  return { coeff: sign, core: s };
}

function estimateDegree(poly, v) {
  const facs = poly.match(new RegExp('\\([^)]*' + v + '[^)]*\\)', 'g'));
  if (facs && facs.length > 1) return facs.length;
  let d = 0;
  const re = new RegExp(v + '\\^([0-9]+)', 'g');
  let m;
  while ((m = re.exec(poly)) !== null) d = Math.max(d, parseInt(m[1], 10));
  if (poly.includes(v) && !poly.includes('^')) d = Math.max(d, 1);
  return d;
}

/* ========== Motor: Transformada directa ℒ{F(t)} ========== */

function transformSingleTerm(term) {
  let sign = 1, t = term.trim();
  if (t.startsWith('+')) t = t.slice(1).trim();
  else if (t.startsWith('-')) { sign = -1; t = t.slice(1).trim(); }
  const sgn = sign < 0 ? '-' : '';

  // Constante
  if (!t.includes('t')) {
    const c = t === '' ? '1' : t;
    return { type: 'constant', property: 'Constante', formula: '\\mathcal{L}\\{c\\} = \\frac{c}{s}',
      latex: sgn + '\\frac{' + toLatex(c) + '}{s}', expr: sign + '*(' + c + ')/s',
      desc: 'Para una constante $c$, $\\mathcal{L}\\{c\\} = \\frac{c}{s}$.' };
  }

  // t^n
  const pw = t.match(/^t(\^([0-9a-zA-Z_]+))?$/);
  if (pw) {
    const p = pw[2] ? pw[2] : '1';
    if (isNum(p) && parseInt(p, 10) >= 0) {
      const n = parseInt(p, 10), nf = factorial(n), e = n + 1;
      return { type: 'power', property: 'Potencias de t', formula: '\\mathcal{L}\\{t^n\\} = \\frac{n!}{s^{n+1}}',
        latex: sgn + '\\frac{' + nf + '}{s^{' + e + '}}', expr: sign + '*(' + nf + ')/(s^' + e + ')',
        desc: 'Para $t^' + n + '$: $n! = ' + nf + '$ y el denominador es $s^{' + e + '}$.' };
    }
    return { type: 'power', property: 'Potencia general (Gamma)', formula: '\\mathcal{L}\\{t^n\\} = \\frac{\\Gamma(n+1)}{s^{n+1}}',
      latex: sgn + '\\frac{\\Gamma(' + p + '+1)}{s^{' + p + '+1}}', expr: sign + '/s^(' + p + '+1)',
      desc: 'Para potencias simbolicas se usa la funcion Gamma.' };
  }

  // sqrt(t)
  if (t === 'sqrt(t)' || t === 't^(1/2)' || t === 't^0.5') {
    return { type: 'sqrt', property: 'Raiz cuadrada', formula: '\\mathcal{L}\\{\\sqrt{t}\\} = \\frac{\\sqrt{\\pi}}{2s^{3/2}}',
      latex: sgn + '\\frac{\\sqrt{\\pi}}{2s^{3/2}}', expr: sign + '*sqrt(pi)/(2*s^(1.5))',
      desc: 'Como $\\sqrt{t} = t^{1/2}$ se usa $\\Gamma(3/2) = \\frac{\\sqrt{\\pi}}{2}$.' };
  }

  // exp(a*t)
  const ex = t.match(/^exp\(([^()]*)\)$/);
  if (ex) {
    const a = extractCoeffOfVar(ex[1], 't');
    const den = a.startsWith('-') ? 's + ' + a.slice(1) : 's - ' + a;
    return { type: 'exp', property: 'Exponencial', formula: '\\mathcal{L}\\{e^{at}\\} = \\frac{1}{s-a}',
      latex: sgn + '\\frac{1}{' + den + '}', expr: sign + '/(' + den.replace(/ /g, '') + ')',
      desc: 'Exponencial con $a = ' + a + '$.' };
  }

  // trig: sin, cos, sinh, cosh
  const tg = t.match(/^(sin|cos|sinh|cosh)\((.*?)\)$/);
  if (tg) {
    const fn = tg[1], ins = tg[2].trim(), w = extractCoeffOfVar(ins, 't');
    const isH = fn.startsWith('sinh') || fn.startsWith('cosh');
    const signOp = isH ? '-' : '+';
    const ws = isNum(w) ? Math.pow(parseFloat(w), 2) : w + '^2';
    let num, form;
    if (fn === 'sin') { num = w; form = '\\frac{\\omega}{s^2+\\omega^2}'; }
    else if (fn === 'cos') { num = 's'; form = '\\frac{s}{s^2+\\omega^2}'; }
    else if (fn === 'sinh') { num = w; form = '\\frac{a}{s^2-a^2}'; }
    else { num = 's'; form = '\\frac{s}{s^2-a^2}'; }
    return { type: 'trig', property: 'Funcion ' + fn.toUpperCase(), formula: form,
      latex: sgn + '\\frac{' + num + '}{s^2' + signOp + ws + '}',
      expr: sign + '*(' + num + ')/(s^2' + signOp + ws + ')',
      desc: 'Aplicamos la formula trigonometrica con frecuencia $\\omega = ' + w + '$.' };
  }

  // e^{at} * f(t) traslacion
  if (t.includes('exp(')) {
    const parts = splitFactors(t);
    const expPart = parts.find(p => p.startsWith('exp('));
    const others = parts.filter(p => p !== expPart);
    if (expPart && others.length) {
      const a = extractCoeffOfVar(expPart.slice(4, -1), 't');
      const baseTree = transformSingleTerm(others.join('*'));
      const shiftDesc = a.startsWith('-') ? 's + ' + a.slice(1) : 's - ' + a;
      return { type: 'shift', property: 'Primer Teorema de Traslacion', formula: '\\mathcal{L}\\{e^{at} f(t)\\} = F(s-a)',
        latex: sgn + substitute(baseTree.latex.replace(/^[-+]?\\frac/, '\\frac'), 's', '(' + shiftDesc + ')'),
        expr: sign + '*(' + substitute(baseTree.expr, 's', '(' + shiftDesc.replace(/ /g, '') + ')') + ')',
        desc: 'Base $F(s) = ' + baseTree.latex + '$ con traslacion $s \\mapsto (' + shiftDesc + ')$.' };
    }
  }

  // t^n * f(t)
  const tm = t.match(/^t\^([0-9]+)\*(.*)$/) || t.match(/^t\*1\*(.*)$/);
  if (tm || t.startsWith('t*')) {
    let n = 1, base;
    if (t.startsWith('t*')) { n = 1; base = t.slice(2); }
    else { n = parseInt(tm[1], 10); base = tm[2]; }
    let baseTree = null;
    try { baseTree = transformSingleTerm(base); } catch (e) {}
    return { type: 'mult_t', property: 'Multiplicacion por t^' + n, formula: '\\mathcal{L}\\{t^n f(t)\\} = (-1)^n \\frac{d^n}{ds^n}[F(s)]',
      latex: sgn + '(-1)^{' + n + '} \\frac{d^{' + n + '}}{ds^{' + n + '}}\\left[' + (baseTree ? baseTree.latex : toLatex(base)) + '\\right]',
      expr: sign + '*(' + (baseTree ? baseTree.expr : base) + ')',
      desc: 'Se deriva la transformada base $n=' + n + '$ veces respecto a $s$.' };
  }

  return { type: 'general', property: 'Definicion integral', formula: '\\mathcal{L}\\{f(t)\\} = \\int_0^\\infty e^{-st} f(t) dt',
    latex: sgn + '\\mathcal{L}\\{' + toLatex(t) + '\\}', expr: sign + '*laplace(' + t + ', t, s)',
    desc: 'Se evalua por definicion o tabla.' };
}

function calculateLaplace(input) {
  const norm = normalize(input);
  const steps = [];
  const terms = splitTerms(norm);

  if (terms.length > 1) {
    steps.push({ title: 'Propiedad de linealidad', prop: 'Linealidad',
      formula: '\\mathcal{L}\\{a f(t) + b g(t)\\} = a \\mathcal{L}\\{f(t)\\} + b \\mathcal{L}\\{g(t)\\}',
      desc: 'Separamos la transformada de la suma en la suma de transformadas.' });
  }

  const parts = terms.map((term, i) => {
    const { coeff, core } = coeffAndCore(term);
    const tree = transformSingleTerm(core);
    let latex;
    if (coeff === 1) latex = tree.latex;
    else if (coeff === -1) latex = '-' + tree.latex;
    else latex = coeff + ' \\cdot \\left(' + tree.latex + '\\right)';
    steps.push({ title: 'Termino ' + (i + 1) + ': $' + toLatex(term) + '$', prop: tree.property,
      formula: tree.formula, desc: tree.desc, latex: latex });
    return { latex, expr: coeff === 1 ? tree.expr : coeff + '*(' + tree.expr + ')' };
  });

  const finalLatex = parts.map((p, i) => i > 0 && !p.latex.trim().startsWith('-') ? '+ ' + p.latex : p.latex).join(' ');
  const finalExpr = parts.map(p => p.expr).join(' + ');
  const method = terms.length > 1 ? 'Linealidad y transformadas fundamentales' : (steps.length ? steps[steps.length - 1].prop : 'Transformada directa');
  return { input: norm, steps, finalLatex, finalExpr, method };
}

function substitute(str, v, r) { return str.replace(new RegExp('\\b' + v + '\\b', 'g'), r); }

/* ========== Motor: Antitransformada ℒ⁻¹{F(s)} ========== */

/* ---- utilidades de polinomios (coeficientes de menor grado primero) ---- */
function pTrim(p){while(p.length>1&&Math.abs(p[p.length-1])<1e-11)p.pop();return p;}
function pAdd(a,b){const n=Math.max(a.length,b.length),r=new Array(n).fill(0);for(let i=0;i<n;i++)r[i]=(a[i]||0)+(b[i]||0);return pTrim(r);}
function pSub(a,b){return pAdd(a,pScale(b,-1));}
function pScale(a,k){return a.map(x=>x*k);}
function pMul(a,b){const r=new Array(a.length+b.length-1).fill(0);for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)r[i+j]+=a[i]*b[j];return pTrim(r);}
function pMonom(k){const r=new Array(k+1).fill(0);r[k]=1;return r;}
function pLin(r){return[-r,1];}
function pQuad(b,c){return[c,b,1];}
function pPow_(p,n){let r=[1];for(let i=0;i<n;i++)r=pMul(r,p);return r;}

function solveSystem(A,b){const n=b.length,M=A.map((row,i)=>row.slice().concat([b[i]]));
  for(let c=0;c<n;c++){let pv=c;for(let r=c+1;r<n;r++)if(Math.abs(M[r][c])>Math.abs(M[pv][c]))pv=r;[M[c],M[pv]]=[M[pv],M[c]];
    if(Math.abs(M[c][c])<1e-12)throw new Error('singular');for(let r=0;r<n;r++){if(r===c)continue;const f=M[r][c]/M[c][c];for(let cc=c;cc<=n;cc++)M[r][cc]-=f*M[c][cc];}}
  const x=new Array(n);for(let i=0;i<n;i++)x[i]=M[i][n]/M[i][i];return x;}

function parsePoly(str){str=str.replace(/\s+/g,'').replace(/\*\*/g,'^');const coeff={};const re=/([+-]?)([0-9.]*)\*?s(?:\^(\d+))?|([+-]?)([0-9.]+)(?![\d.])/g;let m;
  while((m=re.exec(str))!==null){if(m[1]!==undefined){const g=m[3]?+m[3]:1,sp=m[1]==='-'?-1:1,co=m[2]===''?1:+m[2];coeff[g]=(coeff[g]||0)+sp*co;}else{const sp=m[4]==='-'?-1:1;coeff[0]=(coeff[0]||0)+sp*(+m[5]);}}
  const md=Math.max(0,...Object.keys(coeff).map(Number)),ar=new Array(md+1).fill(0);for(const k in coeff)ar[+k]=coeff[k];return pTrim(ar);}

/* Raices numericas (Durand-Kerner) de un polinomio monico */
function rootsOfPoly(poly){const n=poly.length-1;if(n===0)return[];const lead=poly[n];const p=poly.map(c=>c/lead);
  let z=p.slice(),zero=0;while(z.length>1&&Math.abs(z[0])<1e-12){zero++;z=z.slice(1);}
  const roots=[];for(let i=0;i<zero;i++)roots.push({re:0,im:0});
  const deg=z.length-1;if(deg===0)return roots;
  if(deg===1){roots.push({re:-z[0],im:0});return roots;}
  if(deg===2){const d=z[1]*z[1]-4*z[2]*z[0],sr=Math.sqrt(Math.abs(d)),real=-z[1]/2;
    if(d>=0){roots.push({re:real+sr/2,im:0});roots.push({re:real-sr/2,im:0});}else{roots.push({re:real,im:sr/2});roots.push({re:real,im:-sr/2});}
    return roots;}
  let R=[];const rad=1+Math.sqrt(Math.max(1,...z.map(Math.abs)));
  for(let i=0;i<deg;i++)R.push({re:rad*Math.cos(2*Math.PI*i/deg+0.2),im:rad*Math.sin(2*Math.PI*i/deg+0.2)});
  const mag=c=>c.re*c.re+c.im*c.im;
  for(let it=0;it<3000;it++){let mm=0;
    for(let i=0;i<deg;i++){let re=z[deg],im=0;
      for(let k=deg-1;k>=0;k--){const nre=re*R[i].re-im*R[i].im+z[k];im=re*R[i].im+im*R[i].re;re=nre;}
      let dre=1,dim=0;
      for(let j=0;j<deg;j++){if(j===i)continue;const nre=dre*(R[i].re-R[j].re)-dim*(R[i].im-R[j].im);dim=dre*(R[i].im-R[j].im)+dim*(R[i].re-R[j].re);dre=nre;}
      let ds=mag({re:dre,im:dim});if(ds<1e-30)ds=1e-30;
      const nr={re:(re*dre+im*dim)/ds,im:(im*dre-re*dim)/ds};
      R[i].re-=nr.re;R[i].im-=nr.im;mm=Math.max(mm,Math.abs(nr.re)+Math.abs(nr.im));
    }
    if(mm<1e-12)break;}
  for(let i=0;i<deg;i++)roots.push(R[i]);return roots;}

function roundRoot(r){const re=Math.abs(r.re-Math.round(r.re))<1e-6?Math.round(r.re):r.re;return {re,im:Math.abs(r.im)<1e-3?0:r.im};}

/* Factorizar un polinomio (via raices) -> {linear:[{root,mult}], quad:[{b,c,mult}]} */
function factorPoly(Q){const roots=rootsOfPoly(Q).map(roundRoot);
  const lin=[],quad=[],used=new Array(roots.length).fill(false);
  for(let i=0;i<roots.length;i++){if(used[i])continue;
    if(roots[i].im===0){used[i]=true;lin.push({root:roots[i].re});continue;}
    let pair=null;for(let j=i+1;j<roots.length;j++)if(!used[j]&&Math.abs(roots[i].re-roots[j].re)<1e-4&&Math.abs(roots[i].im+roots[j].im)<1e-4){pair=j;break;}
    if(pair!==null){used[i]=used[pair]=true;const b=-2*roots[i].re,c=roots[i].re*roots[i].re+roots[i].im*roots[i].im;quad.push({b,c});}
  }
  const lm={};lin.forEach(f=>lm[f.root]=(lm[f.root]||0)+1);const la=Object.entries(lm).map(([r,m])=>({root:+r,mult:m}));
  const qm={};quad.forEach(q=>qm[q.b+','+q.c]=(qm[q.b+','+q.c]||0)+1);const qa=Object.entries(qm).map(([k,m])=>{const[b,c]=k.split(',').map(Number);return{b,c,mult:m};});
  return {linear:la,quad:qa};}

/* Expandir denominador -> {Q, scalar, linear, quad} */
function expandDenominator(str){str=str.trim();
  const parts=[];let depth=0,start=0;
  for(let i=0;i<str.length;i++){const c=str[i];if(c==='(')depth++;else if(c===')')depth--;else if(c==='*'&&depth===0&&str[i+1]==='('){parts.push(str.slice(start,i));start=i+1;}}
  parts.push(str.slice(start));
  let Q=[1],scalar=1;const linear=[],quad=[];
  for(let raw of parts){raw=raw.trim();if(!raw)continue;
    if(/^s\^\d+$/.test(raw)){const k=+raw.match(/\d+/)[0];Q=pMul(Q,pMonom(k));linear.push({root:0,mult:k});continue;}
    let mult=1,base=raw;const pm=raw.match(/^(.*?)\^(\d+)$/);
    if(pm){mult=+pm[2];base=pm[1].trim();}
    if(base.startsWith('(')&&base.endsWith(')'))base=base.slice(1,-1).trim();
    const ml=base.match(/^([+-]?[0-9.]*)\*?s\s*([+-])\s*([0-9.]+)$/);
    if(ml){const a=ml[1]===''||ml[1]==='+'||ml[1]==='1'?1:(ml[1]==='-'?-1:+ml[1]);const b=(ml[2]==='-'?-1:1)*(+ml[3]);scalar*=Math.pow(a,mult);linear.push({root:-b/a,mult});Q=pMul(Q,pPow_(pLin(-b/a),mult));continue;}
    const mq=base.match(/^([+-]?[0-9.]*)\*?s\^2(.*)$/);
    if(mq){const a=mq[1]===''||mq[1]==='+'||mq[1]==='1'?1:(mq[1]==='-'?-1:+mq[1]);scalar*=Math.pow(a,mult);
      let rest=mq[2].trim(),b=0,c=0;const mb=rest.match(/^([+-])\s*([0-9.]*)\*?s/);if(mb){b=(mb[1]==='-'?-1:1)*(+mb[2]);rest=rest.slice(mb[0].length).trim();}
      const mc=rest.match(/^([+-])\s*([0-9.]+)$/);if(mc)c=(mc[1]==='-'?-1:1)*(+mc[2]);
      b/=a;c/=a;
      if(b*b-4*c>0){const sr=Math.sqrt(b*b-4*c);linear.push({root:(-b+sr)/2,mult});linear.push({root:(-b-sr)/2,mult});}
      else{quad.push({b,c,mult});}
      Q=pMul(Q,pPow_(pQuad(b,c),mult));continue;}
    const sub=parsePoly(base),subSt=factorPoly(sub);
    for(const f of subSt.linear)linear.push({root:f.root,mult:f.mult});
    for(const q of subSt.quad)quad.push({b:q.b,c:q.c,mult:q.mult});
    Q=pMul(Q,pPow_(sub,mult));
  }
  const lm={};linear.forEach(f=>lm[f.root]=(lm[f.root]||0)+(f.mult||1));const linA=Object.entries(lm).map(([r,m])=>({root:+r,mult:m}));
  const qm={};quad.forEach(q=>qm[q.b+','+q.c]=(qm[q.b+','+q.c]||0)+(q.mult||1));const quA=Object.entries(qm).map(([k,m])=>{const[b,c]=k.split(',').map(Number);return{b,c,mult:m};});
  return {Q,scalar,linear:linA,quad:quA};}

function buildFactors(struct){const factors=[];
  for(const f of struct.linear)for(let k=0;k<f.mult;k++)factors.push({type:'lin',root:f.root,sp:pLin(f.root)});
  for(const q of struct.quad)for(let k=0;k<q.mult;k++)factors.push({type:'quad',b:q.b,c:q.c,sp:pQuad(q.b,q.c)});
  return factors;}
function buildOt(struct,t,allFactors){let O=[1],skipped=0,needSkip=t.j;
  for(const f of allFactors){
    if(t.type==='lin'&&f.type==='lin'&&Math.abs(f.root-t.root)<1e-9){if(skipped<needSkip){skipped++;continue;}}
    else if(t.type==='quad'&&f.type==='quad'&&Math.abs(f.b-t.b)<1e-9&&Math.abs(f.c-t.c)<1e-9){if(skipped<needSkip){skipped++;continue;}}
    O=pMul(O,f.sp);
  }
  return O;}
function partialFrac(P,Q,struct){const terms=[];
  for(const f of struct.linear)for(let j=1;j<=f.mult;j++)terms.push({type:'lin',root:f.root,j});
  for(const q of struct.quad)for(let j=1;j<=q.mult;j++)terms.push({type:'quad',b:q.b,c:q.c,j});
  const unk=[];terms.forEach(t=>{if(t.type==='lin'){t.ck=unk.length;unk.push(null);}else{t.ck=unk.length;unk.push(null);t.dk=unk.length;unk.push(null);}});
  const allFactors=buildFactors(struct),degQ=Q.length-1,nUnk=unk.length;
  const A=new Array(degQ).fill(0).map(()=>new Array(nUnk).fill(0));
  const B=new Array(degQ).fill(0);for(let k=0;k<P.length;k++)B[k]=P[k];
  function add(un,poly){for(let k=0;k<poly.length;k++)if(k<degQ)A[k][un]+=poly[k];}
  terms.forEach(t=>{const O=buildOt(struct,t,allFactors);
    if(t.type==='lin'){add(t.ck,O);}
    else{const sO=pMul(O,pMonom(1));add(t.ck,sO);add(t.dk,O);}
  });
  const sol=solveSystem(A,B);
  terms.forEach(t=>{if(t.type==='lin')t.coeff=sol[t.ck];else{t.ce=sol[t.ck];t.de=sol[t.dk];}});
  return terms;}

/* ---- formato numerico ---- */
function nfmt(x){const q=Math.round(x*1e8)/1e8;return Math.abs(q)<1e-9?0:q;}

/* ---- formatear un exponente ---- */
function bExpLatex(beta){ // e^{beta t}
  if(Math.abs(beta)<1e-9)return '';
  const s=beta<0?'-':'';
  const v=Math.abs(beta);
  const str=(Math.abs(v-1)<1e-9)?'':(Number.isInteger(v)?String(v):String(nfmt(v)));
  return 'e^{'+s+str+'t}';
}

/* --- inversion de termino lineal A/(s-r)^k --- */
function invLin(A,r,k){
  if(Math.abs(A)<1e-9)return {latex:'',expr:'',zero:true};
  const Aq=nfmt(A);let fact=1;for(let i=2;i<=k-1;i++)fact*=i;
  const eT=bExpLatex(r);
  const hasE=!!eT, eS=eT&&eT[2]==='-'; // for spacing
  let pre='',Astr='';
  if(A===1)Astr='';else if(A===-1)pre='-';else Astr=String(Aq);
  let res;
  if(k===1){
    res=(pre+Astr)+ (eT?(' '+eT):'');
    if(pre+Astr==='')res=eT||'1';
  } else {
    const tpow=(k-1===1)?'t':'t^{'+(k-1)+'}';
    const tb=(fact===1?'':String(fact));
    if(A===1||A===-1) res=pre+'\\frac{'+tpow+(eT?' '+eT:'')+'}{'+(tb||'1')+'}';
    else res= (Astr.startsWith('-')?'-':'')+'\\frac{'+Astr.replace('-','')+tpow+(eT?' '+eT:'')+'}{'+(tb||'1')+'}';
  }
  res=res.trim();
  let expr;
  if(k===1) expr=String(Aq)+'*exp('+nfmt(r)+'*t)';
  else expr=String(Aq)+'*t^'+(k-1)+(fact!==1?('/'+fact):'')+'*exp('+nfmt(r)+'*t)';
  return {latex:res,expr,zero:false};
}

/* --- inversion de termino cuadratico (Cs+D)/(s^2+bs+c) --- */
function invQuad(C,D,b,c){
  const beta=-b/2,w2=c-beta*beta,w=Math.sqrt(w2);
  const Dp=D+C*beta;
  const eT=bExpLatex(beta);
  const wSqrt=Number.isInteger(w)?String(Math.round(w)):('\\sqrt{'+String(nfmt(w2))+'}');
  const wArg=(Math.abs(w-1)<1e-9)?'t':(wSqrt+' t');
  const parts=[],exprs=[];
  if(Math.abs(C)>1e-9){
    const cpre=(C===1?'':(C===-1?'-':String(nfmt(C))));
    parts.push([cpre,eT,'\\cos('+wArg+')'].filter(Boolean).join(' '));
    exprs.push((Math.abs(C-1)<1e-9?'':(Math.abs(C+1)<1e-9?'-':String(nfmt(C))+'*'))+'cos('+w+'*t)');
  }
  if(Math.abs(Dp)>1e-9){
    let spr;
    if(Number.isInteger(w)){ spr=(Math.abs(Dp/w-1)<1e-9?'':(Math.abs(Dp/w+1)<1e-9?'-':String(nfmt(Dp/w))+' ')); }
    else { const dv=nfmt(Dp); spr=((dv<0)?('-\\frac{'+Math.abs(dv)+'}{'+wSqrt+'}'):('\\frac{'+dv+'}{'+wSqrt+'}')); }
    parts.push([spr,eT,'\\sin('+wArg+')'].filter(Boolean).join(' '));
    const sc=nfmt(Dp/w);
    exprs.push((Math.abs(sc-1)<1e-9?'':(Math.abs(sc+1)<1e-9?'-':String(sc)+'*'))+'sin('+w+'*t)');
  }
  return {latex:parts.join(' + ').replace(/\+ -/g,'- '),expr:exprs.join(' + '),zero:(parts.length===0)};
}

/* ======================== Antitransformada principal ======================== */
function calculateInverse(input){
  const norm=normalize(input);
  const steps=[];
  const terms=splitTerms(norm);
  const allTerms=[];let lastMethod='';

  // Linealidad: resolver cada termino de la suma
  if(terms.length>1){
    steps.push({title:'Propiedad de linealidad',prop:'Linealidad',
      formula:'\\mathcal{L}^{-1}\\{af(s)+bg(s)\\} = a\\mathcal{L}^{-1}\\{f(s)\\} + b\\mathcal{L}^{-1}\\{g(s)\\}',
      desc:'Separamos la antitransformada de la suma en la suma de antitransformadas.'});
  }

  for(const term of terms){
    const core=term.trim().replace(/^[+-]\s*/,'');
    const res=inverseSingle(core,norm);
    if(res.error){
      steps.push(res.step);
      allTerms.push({latex:res.error,expr:'',method:res.method});
      lastMethod=res.method;
      continue;
    }
    res.steps.forEach(s=>steps.push(s));
    allTerms.push({latex:res.latex,expr:res.expr,method:res.method});
    lastMethod=res.method;
    // signo
  }

  const pieces=terms.map((t,i)=>{
    const sign=t.trim().startsWith('-')?'-':'';
    let lx=allTerms[i].latex;let ex=allTerms[i].expr;
    if(sign==='-'&&!lx.trim().startsWith('-')){lx=sign+' '+lx;ex='-'+ex;}
    return {lx,ex};
  });
  let finalLatex=pieces.map((p,i)=>i>0&&!p.lx.trim().startsWith('-')?'+ '+p.lx:p.lx).join(' ').replace(/^ /,'').replace(/\+ -/g,'- ');
  if(!finalLatex.trim()||finalLatex==='0')finalLatex='0';
  const finalExpr=pieces.map(p=>p.ex).filter(Boolean).join(' + ');
  const method=terms.length>1?('Linealidad: '+lastMethod):lastMethod;
  return {input:norm,steps,finalLatex,finalExpr,method};
}

/* Antitransformada de una sola fraccion N(s)/D(s) */
function inverseSingle(frac,norm){
  const steps=[];
  let num,den;
  if(!frac.includes('/')){
    // puede ser un termino constante o una expresion no fraccionaria
    return {error:'\\text{Ingresa una fraccion N(s)/D(s)}',step:{title:'Entrada',prop:'Entrada invalida',formula:'\\text{Se espera F(s) = N(s)/D(s)}',desc:'El termino "$'+toLatex(frac)+'"$ no es una fraccion.'},method:'Entrada invalida'};
  }
  const nd=extractNumDen(frac);
  num=nd.num;den=nd.den;
  const P=parsePoly(num);
  const D=expandDenominator(den);
  const Q=D.Q,scalar=D.scalar;
  const degQ=Q.length-1,degP=P.length-1;

  steps.push({title:'Analisis del tipo de fraccion',prop:'Clasificacion de grado',
    formula:degP>=degQ?'\\text{Fraccion impropia}':'\\text{Fraccion propia}',
    desc:'Numerador de grado $'+degP+'$ y denominador de grado $'+degQ+'$. Si el numerador tiene grado mayor o igual sube la exponencial primero.'});

  if(Q.length===1&&Q[0]===1){
    return {error:'\\text{Ingresa una fraccion N(s)/D(s)}',step:{title:'Entrada',prop:'Entrada invalida',formula:'',desc:'El denominador es $1$.'},method:'Entrada invalida'};
  }

  // Escalar el numerador por 1/scalar (factores no monicos como (2s-1))
  const PP=pScale(P,1/scalar);

  const struct={linear:D.linear,quad:D.quad};

  // ---- Casos especiales / directos ----
  // 1) 1/s^n  (raiz 0, mult n, numerador constante)
  if(struct.linear.length===1&&struct.linear[0].root===0&&struct.quad.length===0){
    const n=struct.linear[0].mult;
    if(degP===0){
      const K=PP[0];
      const fact=(n>1)?(()=>{let f=1;for(let i=2;i<=n-1;i++)f*=i;return f;})():1;
      let res;
      if(n===1){res=(K===1?'1':String(nfmt(K)));}
      else if(fact===1){ // n=2 -> t^(n-1)/(n-1)! = t
        res=(K===1?'':(K===-1?'-':String(nfmt(K))+' '))+'t';
        res=res.trim();
      }
      else{
        const tpow=(n-1===1)?'t':'t^{'+(n-1)+'}';
        res=(K===1?'':(K===-1?'-':String(nfmt(K))+' '))+'\\frac{'+tpow+'}{'+fact+'}';
        res=res.trim();
      }
      const expr=(n===1)?String(nfmt(K)):('('+String(nfmt(K))+'*t^'+(n-1)+')/'+fact);
      steps.push({title:'Potencia en s',prop:'K/s^{n}',formula:'\\mathcal{L}^{-1}\\{\\frac{K}{s^n}\\} = K\\frac{t^{n-1}}{(n-1)!}',
        desc:'Con $K='+nfmt(K)+'$ y $n='+n+'$.',latex:res});
      return {steps,latex:res,expr,method:'Potencia t^{n-1}'};
    }
  }

  // 2) denominador lineal simple (a s + b) -> 1/(s-r)
  if(struct.linear.length===1&&struct.linear[0].mult===1&&struct.quad.length===0){
    const r=struct.linear[0].root;
    const K=PP.length?PP[0]:0;
    const res=bExpLatex(r);
    const out=(Math.abs(K-1)<1e-9?(res||'1'):(String(nfmt(K))+' '+(res||'1'))).trim();
    const expr=String(nfmt(K))+'*exp('+r+'*t)';
    steps.push({title:'Antitransformada exponencial',prop:'Exponencial',
      formula:'\\mathcal{L}^{-1}\\{\\frac{1}{s-r}\\} = e^{rt}',desc:'Polo en $s='+nfmt(r)+'$.',latex:out});
    return {steps,latex:out,expr,method:'Exponencial'};
  }

  // 3) fracciones parciales generales
  try{
    const terms=partialFrac(PP,Q,struct);
    const pieces=[];
    const sTemplate=struct.linear.map((f,i)=>(f.mult===1?'\\frac{A_{'+(i+1)+'}}{s-'+nfmt(f.root)+'}':'\\frac{A_{'+(i+1)+'}}{(s-'+nfmt(f.root)+')^{'+f.mult+'}}')).join(' + ')
      + (struct.quad.length?(' + '+struct.quad.map((q)=>(q.mult===1?'\\frac{B_{}s+C_{}}{s^2+'+nfmt(q.b)+'s+'+nfmt(q.c)+'}':'')).join(' + ')):'');
    steps.push({title:'Descomposicion en fracciones parciales',prop:'Fracciones parciales',
      formula:'\\frac{P(s)}{Q(s)} = '+sTemplate,desc:'Factorizamos el denominador y planteamos el sistema de coeficientes.'});

    for(const t of terms){
      if(t.type==='lin'){
        const lx=invLin(t.coeff,t.root,t.j);
        const fact=(()=>{let f=1;for(let i=2;i<=t.j-1;i++)f*=i;return f;})();
        if(!lx.zero){
          pieces.push(lx);
          steps.push({title:'Termino $\\frac{A}{s-'+nfmt(t.root)+'}$',prop:'Exponencial / potencia',
            formula:'\\mathcal{L}^{-1}\\{\\frac{A}{(s-r)^k}\\} = A\\frac{t^{k-1}}{(k-1)!}e^{rt}',
            desc:'Con $A='+nfmt(t.coeff)+'$, $r='+nfmt(t.root)+'$ y $k='+t.j+'$.',latex:lx.latex});
        }
      } else {
        const lx=invQuad(t.ce,t.de,t.b,t.c);
        if(!lx.zero){
          pieces.push(lx);
          steps.push({title:'Termino cuadratico',prop:'Completacion de cuadrados',
            formula:'\\frac{Cs+D}{s^2+bs+c} = e^{\\beta t}\\left[C\\cos(\\omega t)+\\frac{D+C\\beta}{\\omega}\\sin(\\omega t)\\right]',
            desc:'Con $\\beta='+nfmt(-t.b/2)+'$ y $\\omega=\\sqrt{'+nfmt(t.c-Math.pow(t.b/2,2))+'}$.',latex:lx.latex});
        }
      }
    }
    const fin=pieces.map(p=>p.latex).filter(x=>x&&x!=='0').join(' + ').replace(/\+ -/g,'- ').replace(/^ /,'');
    const exprTerm=pieces.map(p=>p.expr).filter(Boolean).join(' + ');
    return {steps,latex:(fin||'0'),expr:exprTerm,method:'Fracciones parciales'};
  }catch(e){
    return {error:'\\text{Metodo adicional requerido}',step:{title:'Analisis simbolico',prop:'Fuera de alcance',formula:'\\text{Consultar Bromwich o residuos}',desc:'No se pudo descomponer esta fraccion.'},method:'No estandar'};
  }
}
/* ========== Graficas ========== */

function plot(expr, tMin, tMax) {
  const canvas = document.getElementById('plotCanvas');
  if (!canvas) return;
  let fn = null;
  try {
    const clean = expr.replace(/\\cdot/g, '*').replace(/e\^\{([^}]+)\}/g, 'exp($1)').replace(/\\sin/g, 'sin').replace(/\\cos/g, 'cos').replace(/\\pi/g, 'pi');
    fn = window.math.compile(clean);
  } catch (e) { /* no grafica */ }
  const labels = [], data = [];
  const pts = 300;
  for (let i = 0; i <= pts; i++) {
    const t = tMin + i * (tMax - tMin) / pts;
    labels.push(t.toFixed(2));
    let y = null;
    if (fn) {
      try {
        const v = fn.evaluate({ t });
        if (typeof v === 'number' && isFinite(v)) y = Math.max(-60, Math.min(60, v));
      } catch (e) { y = null; }
    }
    data.push(y);
  }
  if (state.chart) state.chart.destroy();
  const isDark = state.theme === 'dark';
  const ctx = canvas.getContext('2d');
  state.chart = new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: 'f(t)', data, borderColor: '#7dcfff', backgroundColor: 'rgba(125,207,255,0.10)', borderWidth: 2.5, tension: 0.3, pointRadius: 0, pointHoverRadius: 5, fill: true }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: isDark ? '#c0caf5' : '#565f89', font: { family: 'Space Grotesk', weight: 600 } } } },
      scales: {
        x: { title: { display: true, text: 't (seg)', color: isDark ? '#565f89' : '#565f89' }, grid: { color: isDark ? 'rgba(65,72,104,0.4)' : 'rgba(65,72,104,0.25)' }, ticks: { color: isDark ? '#a9b1d6' : '#565f89', maxTicksLimit: 10 } },
        y: { grid: { color: isDark ? 'rgba(65,72,104,0.4)' : 'rgba(65,72,104,0.25)' }, ticks: { color: isDark ? '#a9b1d6' : '#565f89' } }
      }
    }
  });
}

/* ========== UI ========== */

const Formulas = [
  { cat: 'basicas', f: '1', F: '\\frac{1}{s}', prop: 'Constante', ex: '1' },
  { cat: 'basicas', f: 't', F: '\\frac{1}{s^2}', prop: 'Potencia lineal', ex: 't' },
  { cat: 'basicas', f: 't^n', F: '\\frac{n!}{s^{n+1}}', prop: 'Potencias', ex: 't^3' },
  { cat: 'basicas', f: 'e^{at}', F: '\\frac{1}{s-a}', prop: 'Exponencial', ex: 'e^(-2*t)' },
  { cat: 'trig', f: '\\sin(\\omega t)', F: '\\frac{\\omega}{s^2+\\omega^2}', prop: 'Seno', ex: 'sin(3*t)' },
  { cat: 'trig', f: '\\cos(\\omega t)', F: '\\frac{s}{s^2+\\omega^2}', prop: 'Coseno', ex: 'cos(4*t)' },
  { cat: 'hiper', f: '\\sinh(at)', F: '\\frac{a}{s^2-a^2}', prop: 'Seno hiperbolico', ex: 'sinh(2*t)' },
  { cat: 'hiper', f: '\\cosh(at)', F: '\\frac{s}{s^2-a^2}', prop: 'Coseno hiperbolico', ex: 'cosh(2*t)' },
  { cat: 'propiedades', f: 'e^{at} f(t)', F: 'F(s-a)', prop: 'Traslacion en s', ex: 'e^(2*t)*sin(3*t)' },
  { cat: 'propiedades', f: 't f(t)', F: '-\\frac{d}{ds}[F(s)]', prop: 'Multiplicacion por t', ex: 't*sin(2*t)' },
  { cat: 'propiedades', f: 'f\'(t)', F: 'sF(s)-f(0)', prop: 'Primera derivada', ex: "f'(t)" },
  { cat: 'propiedades', f: 'f\'\'(t)', F: 's^2F(s)-sf(0)-f\'(0)', prop: 'Segunda derivada', ex: "f''(t)" },
  { cat: 'propiedades', f: '\\int_0^t f(u)du', F: '\\frac{F(s)}{s}', prop: 'Integral', ex: 'sin(2*t)' }
];

function renderFormulas() {
  const body = document.getElementById('formulasBody');
  const q = (document.getElementById('formulaSearch').value || '').toLowerCase().trim();
  const cat = document.querySelector('.chip.active').dataset.cat;
  const list = Formulas.filter(f =>
    (cat === 'todas' || f.cat === cat) &&
    (!q || f.prop.toLowerCase().includes(q) || f.F.toLowerCase().includes(q) || f.f.toLowerCase().includes(q)));
  body.innerHTML = '';
  list.forEach((f, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td class="formula-cell" id="ff_' + i + '"></td><td class="formula-cell" id="fF_' + i + '"></td><td><strong>' + f.prop + '</strong></td><td><code>' + f.ex + '</code></td><td><button class="load-formula" data-expr="' + f.ex + '" data-type="' + (f.cat === 'propiedades' && f.ex.includes("'") ? 'inverse' : 'laplace') + '">Cargar</button></td>';
    body.appendChild(tr);
    renderLatex(document.getElementById('ff_' + i), f.f, false);
    renderLatex(document.getElementById('fF_' + i), f.F, false);
  });
}

const Examples = [
  /* ===== Transformadas directas L{F(t)} ===== */
  { type: 'laplace', section: 'Propiedades · Exponencial', expr: 'e^(-2*t)', title: 'Exponencial basica', desc: 'Transformada de una exponencial decayente, polo en s = -2.' },
  { type: 'laplace', section: 'Propiedades · Exponencial', expr: 'e^(a*t)', title: 'Parametro simbolico', desc: 'Transformada con constante simbolica a, genera 1/(s-a).' },
  { type: 'laplace', section: 'Propiedades · Potencia', expr: 't^2', title: 'Potencia', desc: 'Propiedad t^n con n = 2, genera 2!/s^3.' },
  { type: 'laplace', section: 'Propiedades · Linealidad', expr: '5 + 3*t - t^2', title: 'Linealidad', desc: 'Suma de terminos; cada uno se transforma por separado.' },
  { type: 'laplace', section: 'Propiedades · Traslacion', expr: 'e^(5*t)*cos(10*t)', title: 'Traslacion y coseno', desc: 'Ej del PDF: e^{5t}·cos(10t) desplaza s hacia s-5.' },
  { type: 'laplace', section: 'Propiedades · Multiplicacion por t', expr: 't*sin(2*t)', title: 'Multiplicacion por t', desc: 'Aplica (-1)^n d^n/ds^n a la transformada base.' },
  { type: 'laplace', section: 'Practica · Parte 1a', expr: '5 + 3*t - t^10', title: 'Linealidad (practica a)', desc: 'F(t) = 5 + 3t - t^10. Ejercicio a) de la practica.' },
  { type: 'laplace', section: 'Practica · Parte 1b', expr: '(e^t+e^(-t))^2', title: 'Binomio exponencial (practica b)', desc: 'F(t) = (e^t + e^-t)^2. Se simplifica antes de transformar.' },
  { type: 'laplace', section: 'Practica · Parte 1c', expr: 'e^(5*t)*cos(10*t)', title: 'Exponencial x coseno (practica c)', desc: 'F(t) = e^{5t}·cos(10t).' },
  { type: 'laplace', section: 'Practica · Parte 1d', expr: 't^2*sin(8*t)', title: 't^n x seno (practica d)', desc: 'F(t) = t^2·sin(8t). Derivada en s.' },
  { type: 'laplace', section: 'Practica · Parte 1e', expr: 't*e^t*cos(t)', title: 't x exponencial x coseno (practica e)', desc: 'F(t) = t·e^t·cos(t).' },

  /* ===== Antitransformadas L^-1{F(s)} ===== */
  { type: 'inverse', section: 'Seccion 4.1 · Linealidad', expr: '1/s^5 + 4/(s-8) - 2/(s^2+25)', title: 'Linealidad (ej 4.1)', desc: 'F(s) = 1/s^5 + 4/(s-8) - 2/(s^2+25). Se invierte termino a termino.' },
  { type: 'inverse', section: 'Seccion 4.2 · Traslacion', expr: '(s+2)/(s^2+4*s+7)', title: 'Traslacion (ej 4.2.1)', desc: 'Completa el cuadrado: polos complejos -2 ± j√3.' },
  { type: 'inverse', section: 'Seccion 4.2 · Traslacion', expr: '(s+2)/(s^2+5*s+7)', title: 'Traslacion (ej 4.2.2)', desc: 'Trinomio irreducible con b = 5.' },
  { type: 'inverse', section: 'Seccion 5.1 · Caso 1', expr: '(11*s^2-2*s+5)/((s-2)*(2*s-1)*(s+1))', title: 'Factores reales no repetidos', desc: 'Caso 1 del PDF. Se resuelve el sistema matricial M·X = N.' },
  { type: 'inverse', section: 'Seccion 5.2 · Caso 2', expr: '(s^2-2*s+2)/((s+3)*(s^2+2*s+2))', title: 'Factores complejos no repetidos', desc: 'Caso 2 del PDF. Mezcla factor real + cuadratico irreducible.' },
  { type: 'inverse', section: 'Practica · Parte 2a', expr: '(5*s-15)/(s^2+7)', title: 'Seno/coseno (practica a)', desc: 'F(s) = (5s-15)/(s^2+7). Polos complejos ±j√7.' },
  { type: 'inverse', section: 'Practica · Parte 2b', expr: '1/(4*s-3)', title: 'Denominador lineal (practica b)', desc: 'F(s) = 1/(4s-3). Ajusta el coeficiente del denominador.' },
  { type: 'inverse', section: 'Practica · Parte 2c', expr: '(3*s+8)/(s^2-2)', title: 'Raices reales (practica c)', desc: 'F(s) = (3s+8)/(s^2-2). Se factoriza en raices reales.' },
  { type: 'inverse', section: 'Practica · Parte 2d', expr: 's/(s+1)^5', title: 'Polo multiple (practica d)', desc: 'F(s) = s/(s+1)^5. Factor repetido de orden 5.' },
  { type: 'inverse', section: 'Practica · Parte 2e', expr: '(2*s-6)/(s^3-s)', title: 'Factor comun (practica e)', desc: 'F(s) = (2s-6)/(s^3-s) = (2s-6)/(s(s-1)(s+1)).' },
  { type: 'inverse', section: 'Practica · Parte 2f', expr: '(5*s+24)/(s^2+4)', title: 'Seno/coseno (practica f)', desc: 'F(s) = (5s+24)/(s^2+4). Polos complejos ±2j.' }
];

function renderExamples() {
  const grid = document.getElementById('examplesGrid');
  grid.innerHTML = '';
  Examples.forEach((e, i) => {
    const card = document.createElement('div');
    card.className = 'example-card';
    card.innerHTML = '<span class="example-tag ' + e.type + '">' + (e.type === 'laplace' ? 'Transformada F(t)' : 'Antitransformada F(s)') + '</span>' + (e.section ? '<span class="example-section">' + e.section + '</span>' : '') + '<h4>' + e.title + '</h4><div class="example-code">' + e.expr + '</div><p class="example-desc">' + e.desc + '</p><button class="example-resolve" data-type="' + e.type + '" data-expr="' + e.expr + '">Cargar y resolver</button>';
    grid.appendChild(card);
  });
}

function renderHistory() {
  const list = document.getElementById('historyList');
  if (state.history.length === 0) {
    list.innerHTML = '<div class="empty-state">Aun no hay calculos en el historial.</div>';
    return;
  }
  list.innerHTML = '';
  state.history.forEach(h => {
    const item = document.createElement('div');
    item.className = 'history-item';
    item.innerHTML = '<div style="flex:1;min-width:220px"><div class="history-meta"><span class="hist-badge ' + h.type + '">' + (h.type === 'laplace' ? 'Transformada' : 'Antitransformada') + '</span><span class="hist-time">' + h.time + '</span></div><div class="hist-eq"><code>' + h.input + '</code><span class="hist-arrow">&rarr;</span><span id="hr_' + h.id + '"></span></div></div><div class="hist-actions"><button class="hist-btn" data-reuse="' + h.id + '">Reutilizar</button><button class="hist-btn del" data-del="' + h.id + '">Eliminar</button></div>';
    list.appendChild(item);
    renderLatex(document.getElementById('hr_' + h.id), h.resultLatex, false);
  });
}

function addHistory(item) {
  const entry = { id: Date.now(), time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), type: state.mode, input: item.input, resultLatex: item.finalLatex, method: item.method };
  state.history.unshift(entry);
  if (state.history.length > 40) state.history.pop();
  localStorage.setItem('lapcalc_history', JSON.stringify(state.history));
  renderHistory();
}

function switchMode(mode) {
  state.mode = mode;
  const lap = mode === 'laplace';
  document.getElementById('modeLaplace').classList.toggle('active', lap);
  document.getElementById('modeInverse').classList.toggle('active', !lap);
  document.getElementById('fieldLabel').textContent = lap ? 'Funcion en el tiempo F(t)' : 'Funcion en el dominio s F(s)';
  const inp = document.getElementById('exprInput');
  inp.placeholder = lap ? 'Ej: sin(2*t), e^(-2*t), t^2...' : 'Ej: 1/(s+2), 1/(s^2+4), (2*s+3)/(s^2+4*s+13)...';
  document.getElementById('calcBtn').textContent = lap ? 'Resolver' : 'Resolver';
  hideResults();
  updatePreview(inp.value);
}

function switchView(view) {
  state.view = view;
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', b.dataset.view === view));
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const t = document.getElementById('view-' + view);
  if (t) t.classList.add('active');
  if (view === 'formulas') renderFormulas();
  if (view === 'examples') renderExamples();
  if (view === 'history') renderHistory();
}

function updatePreview(val) {
  const box = document.getElementById('previewBox');
  if (!val || !val.trim()) { box.className = 'preview-box placeholder'; box.innerHTML = 'Esperando entrada...'; return; }
  box.className = 'preview-box';
  try { renderLatex(box, toLatex(normalize(val)), false); }
  catch (e) { box.textContent = val; }
}

function solve() {
  const val = document.getElementById('exprInput').value.trim();
  const check = validate(val);
  const err = document.getElementById('errorBanner');
  const errText = document.getElementById('errorText');
  hideResults();
  if (!check.ok) { errText.textContent = check.error; err.classList.add('show'); return; }
  err.classList.remove('show');

  const loader = document.getElementById('loader');
  loader.classList.add('show');
  setTimeout(() => {
    let result;
    try {
      result = state.mode === 'laplace' ? calculateLaplace(val) : calculateInverse(val);
    } catch (e) {
      loader.classList.remove('show');
      errText.textContent = 'Error al resolver la expresion. Verifica tu sintaxis.';
      err.classList.add('show');
      return;
    }
    loader.classList.remove('show');
    state.result = result;
    displayResult(result);
    addHistory(result);
  }, 400);
}

function displayResult(result) {
  document.getElementById('resultsArea').classList.add('show');
  const hero = document.getElementById('finalFormula');
  const label = state.mode === 'laplace' ? 'F(s) = ' : 'f(t) = ';
  renderLatex(hero, label + ' ' + result.finalLatex, true);

  const list = document.getElementById('stepsList');
  list.innerHTML = '';
  (result.steps || []).forEach((s, i) => {
    const item = document.createElement('div');
    item.className = 'step-item';
    item.innerHTML = '<div class="step-head"><div class="step-num">' + (i + 1) + '</div><div class="step-title">' + s.title + '</div><span class="step-tag">' + (s.prop || 'Propiedad') + '</span></div><div class="step-desc">' + (s.desc || '') + '</div>' + (s.formula ? '<div class="step-formula" id="sf_' + i + '"></div>' : '') + (s.latex ? '<div class="step-formula" id="sl_' + i + '"></div>' : '');
    list.appendChild(item);
    if (s.formula) renderLatex(document.getElementById('sf_' + i), s.formula, true);
    if (s.latex) renderLatex(document.getElementById('sl_' + i), s.latex, true);
  });

  const isInv = state.mode === 'inverse';
  const gExpr = isInv ? result.finalExpr : result.input;
  plot(gExpr, state.tMin, state.tMax);
}

function hideResults() { document.getElementById('resultsArea').classList.remove('show'); }

function copyResult() {
  if (!state.result) return;
  const text = state.result.finalExpr || state.result.finalLatex;
  navigator.clipboard.writeText(text).then(() => {
    const t = document.getElementById('copyToast');
    t.style.display = 'inline';
    setTimeout(() => t.style.display = 'none', 2000);
  }).catch(() => {});
}

function toggleTheme() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', state.theme);
  localStorage.setItem('lapcalc_theme', state.theme);
  if (state.result) {
    const isInv = state.mode === 'inverse';
    plot(isInv ? state.result.finalExpr : state.result.input, state.tMin, state.tMax);
  }
}

/* ========== Eventos e init ========== */

document.addEventListener('DOMContentLoaded', () => {
  document.documentElement.setAttribute('data-theme', state.theme);

  document.querySelectorAll('.nav-btn').forEach(b => b.addEventListener('click', () => switchView(b.dataset.view)));
  document.getElementById('modeLaplace').addEventListener('click', () => switchMode('laplace'));
  document.getElementById('modeInverse').addEventListener('click', () => switchMode('inverse'));
  document.getElementById('themeBtn').addEventListener('click', toggleTheme);
  document.getElementById('calcBtn').addEventListener('click', solve);
  document.getElementById('copyBtn').addEventListener('click', copyResult);

  const inp = document.getElementById('exprInput');
  inp.addEventListener('input', e => updatePreview(e.target.value));
  inp.addEventListener('keydown', e => { if (e.key === 'Enter') solve(); });

  document.querySelectorAll('.symbol-bar button').forEach(b =>
    b.addEventListener('click', () => {
      const sym = b.dataset.sym;
      const start = inp.selectionStart || inp.value.length;
      const before = inp.value.slice(0, start), after = inp.value.slice(inp.selectionEnd || inp.value.length);
      inp.value = before + sym + after;
      const pos = start + sym.length;
      inp.focus(); inp.selectionStart = inp.selectionEnd = pos;
      updatePreview(inp.value);
    }));

  document.querySelectorAll('.qp').forEach(b =>
    b.addEventListener('click', () => {
      switchMode(b.dataset.type);
      inp.value = b.dataset.expr;
      updatePreview(inp.value);
      solve();
    }));

  document.querySelectorAll('.chip').forEach(c =>
    c.addEventListener('click', () => {
      document.querySelectorAll('.chip').forEach(x => x.classList.remove('active'));
      c.classList.add('active');
      renderFormulas();
    }));
  const fs = document.getElementById('formulaSearch');
  fs.addEventListener('input', renderFormulas);

  document.getElementById('formulasBody').addEventListener('click', e => {
    const btn = e.target.closest('.load-formula');
    if (!btn) return;
    switchMode(btn.dataset.type);
    inp.value = btn.dataset.expr;
    updatePreview(inp.value);
    switchView('calculator');
    solve();
  });

  document.getElementById('examplesGrid').addEventListener('click', e => {
    const btn = e.target.closest('.example-resolve');
    if (!btn) return;
    switchMode(btn.dataset.type);
    inp.value = btn.dataset.expr;
    updatePreview(inp.value);
    switchView('calculator');
    solve();
  });

  document.getElementById('clearHistBtn').addEventListener('click', () => {
    if (confirm('Seguro que deseas vaciar el historial?')) {
      state.history = []; localStorage.removeItem('lapcalc_history'); renderHistory();
    }
  });

  document.getElementById('historyList').addEventListener('click', e => {
    const reuse = e.target.closest('[data-reuse]');
    const del = e.target.closest('[data-del]');
    if (reuse) {
      const h = state.history.find(x => x.id == reuse.dataset.reuse);
      if (!h) return;
      switchMode(h.type);
      inp.value = h.input;
      updatePreview(h.input);
      switchView('calculator');
      solve();
    }
    if (del) {
      state.history = state.history.filter(x => x.id != del.dataset.del);
      localStorage.setItem('lapcalc_history', JSON.stringify(state.history));
      renderHistory();
    }
  });

  document.getElementById('tMinVal').addEventListener('change', e => {
    state.tMin = parseFloat(e.target.value) || 0;
    if (state.result) { const isInv = state.mode === 'inverse'; plot(isInv ? state.result.finalExpr : state.result.input, state.tMin, state.tMax); }
  });
  document.getElementById('tMaxVal').addEventListener('change', e => {
    state.tMax = parseFloat(e.target.value) || 10;
    if (state.result) { const isInv = state.mode === 'inverse'; plot(isInv ? state.result.finalExpr : state.result.input, state.tMin, state.tMax); }
  });

  updatePreview(inp.value);
  renderHistory();
  renderFormulas();
  renderExamples();
});
