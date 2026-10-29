/**
 * ==========================================================================
 * LAPLACE MASTER — Motor Simbólico y Controlador de Interfaz
 * ==========================================================================
 * Calculadora simbólica avanzada para:
 * 1. Transformada de Laplace ℒ{F(t)} → F(s)
 * 2. Transformada Inversa de Laplace ℒ⁻¹{F(s)} → F(t)
 *
 * Implementa resolución simbólica con KaTeX, Math.js, Algebrite y Chart.js.
 */

// Estado global de la aplicación
const AppState = {
  currentMode: 'laplace', // 'laplace' | 'inverse'
  currentView: 'calculator', // 'calculator' | 'formulas' | 'examples' | 'history' | 'settings'
  theme: localStorage.getItem('laplace_theme') || 'dark',
  history: JSON.parse(localStorage.getItem('laplace_history') || '[]'),
  chartInstance: null,
  tMin: 0,
  tMax: 10,
  tStep: 0.05,
  lastResult: null
};

// ==========================================================================
// 1. UTILIDADES Y NORMALIZACIÓN DE ENTRADAS
// ==========================================================================

/**
 * Sanitiza y normaliza expresiones algebraicas para estandarizar sintaxis.
 * Soporta notaciones en español (sen, tg), exponentes con 'e^', potencias implícitas, etc.
 */
function normalizeExpression(expr, variable = 't') {
  if (!expr || typeof expr !== 'string') return '';
  let str = expr.trim();

  // Reemplazar signos tipográficos especiales
  str = str.replace(/−/g, '-').replace(/×/g, '*').replace(/÷/g, '/');
  str = str.replace(/ω/g, 'w').replace(/Ω/g, 'w').replace(/π/g, 'pi');

  // Funciones trigonométricas en español
  str = str.replace(/\bsen\b/gi, 'sin');
  str = str.replace(/\btg\b/gi, 'tan');
  str = str.replace(/\barctg\b/gi, 'atan');
  str = str.replace(/\barcsen\b/gi, 'asin');
  str = str.replace(/\barccos\b/gi, 'acos');

  // Notaciones de exponencial: e^(...) o exp(...)
  str = str.replace(/\be\s*\^\s*\(/gi, 'exp(');
  // Casos como e^(-2t) o e^(2*t)
  str = str.replace(/\be\s*\^\s*([a-zA-Z0-9_]+)/gi, 'exp($1)');

  // Potencias con superíndices comunes
  str = str.replace(/²/g, '^2').replace(/³/g, '^3').replace(/⁴/g, '^4');

  // Insertar multiplicación implícita: número seguido de letra (ej: 2t -> 2*t, 3s -> 3*s)
  str = str.replace(/(\d+)\s*([a-zA-Z(])/g, '$1*$2');
  
  // Paréntesis cerrado seguido de letra o paréntesis abierto: )t -> )*t, )( -> )*(
  str = str.replace(/\)\s*([a-zA-Z0-9_(])/g, ')*$1');

  // Letra seguida de paréntesis si no es una función conocida: ej t(s+1) -> t*(s+1)
  const knownFuncs = ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'exp', 'sqrt', 'log', 'ln', 'asin', 'acos', 'atan', 'abs'];
  const funcPattern = new RegExp(`\\b(${knownFuncs.join('|')})\\s*\\*\\(`, 'g');
  // Revertir falso positivo de funciones conocidas
  str = str.replace(funcPattern, '$1(');

  return str;
}

/**
 * Valida la sintaxis básica y balance de paréntesis de la expresión.
 */
function validateInput(expr) {
  if (!expr || expr.trim() === '') {
    return { valid: false, error: 'Por favor, ingresa una expresión matemática.' };
  }

  let balance = 0;
  for (let i = 0; i < expr.length; i++) {
    if (expr[i] === '(') balance++;
    if (expr[i] === ')') balance--;
    if (balance < 0) {
      return { valid: false, error: 'Paréntesis desbalanceados: hay un paréntesis de cierre ")" sin apertura previa.' };
    }
  }
  if (balance !== 0) {
    return { valid: false, error: 'Paréntesis desbalanceados: faltan paréntesis de cierre ")".' };
  }

  // Comprobar operadores duplicados inválidos como ++, **, //
  if (/(\+\+|\/\/|\^\^)/.test(expr)) {
    return { valid: false, error: 'Operadores matemáticos consecutivos inválidos en la expresión.' };
  }

  return { valid: true };
}

/**
 * Convierte expresiones de texto a formato LaTeX para renderizar con KaTeX.
 */
function exprToLatex(expr) {
  if (!expr) return '';
  let s = expr.toString();

  try {
    // Si math.js puede parsear, usamos su generador de LaTeX nativo
    if (window.math && window.math.parse) {
      const parsed = window.math.parse(s);
      return parsed.toTex({ parenthesis: 'auto' });
    }
  } catch (e) {
    // Fallback a reemplazos regulares si math.js falla
  }

  // Reemplazos de LaTeX estándar
  s = s.replace(/\bexp\((.*?)\)/g, 'e^{$1}');
  s = s.replace(/\bsin\((.*?)\)/g, '\\sin($1)');
  s = s.replace(/\bcos\((.*?)\)/g, '\\cos($1)');
  s = s.replace(/\bsinh\((.*?)\)/g, '\\sinh($1)');
  s = s.replace(/\bcosh\((.*?)\)/g, '\\cosh($1)');
  s = s.replace(/\bsqrt\((.*?)\)/g, '\\sqrt{$1}');
  s = s.replace(/\bpi\b/g, '\\pi');
  s = s.replace(/\*/g, ' \\cdot ');
  s = s.replace(/\^([0-9a-zA-Z]+)/g, '^{$1}');
  s = s.replace(/\^\{(.*?)\}/g, '^{$1}');

  return s;
}

/**
 * Renderiza una cadena LaTeX dentro de un elemento DOM usando KaTeX.
 */
function renderLatex(elementId, latexStr, displayMode = true) {
  const el = typeof elementId === 'string' ? document.getElementById(elementId) : elementId;
  if (!el) return;

  if (window.katex) {
    try {
      window.katex.render(latexStr, el, {
        throwOnError: false,
        displayMode: displayMode
      });
    } catch (err) {
      el.textContent = latexStr;
    }
  } else {
    el.textContent = latexStr;
  }
}

// ==========================================================================
// 2. MOTOR DE TRANSFORMADA DE LAPLACE DIRECTA ℒ{F(t)}
// ==========================================================================

/**
 * Analiza un término individual f(t) y calcula su Transformada de Laplace con pasos.
 */
function transformSingleTerm(termStr) {
  const t = 't';
  let term = termStr.trim();
  
  // Extraer signo inicial
  let sign = 1;
  if (term.startsWith('+')) {
    term = term.slice(1).trim();
  } else if (term.startsWith('-')) {
    sign = -1;
    term = term.slice(1).trim();
  }

  // 1. Constante pura
  if (!term.includes('t')) {
    const constVal = term === '' ? 1 : term;
    return {
      type: 'constant',
      original: (sign < 0 ? '-' : '') + term,
      coeff: sign,
      baseFunc: constVal,
      property: 'Constante',
      formula: '\\mathcal{L}\\{c\\} = \\frac{c}{s}',
      explanation: `Transformada de una función constante. Para cualquier constante real $c$, $\\mathcal{L}\\{c\\} = \\frac{c}{s}$.`,
      resultLatex: sign < 0 ? `-\\frac{${exprToLatex(constVal)}}{s}` : `\\frac{${exprToLatex(constVal)}}{s}`,
      resultExpr: `${sign * (parseFloat(constVal) || 1)}/s`
    };
  }

  // 2. Potencia de t: t o t^n
  const powerMatch = term.match(/^t(\^([0-9a-zA-Z_]+))?$/);
  if (powerMatch) {
    const power = powerMatch[2] ? powerMatch[2] : '1';
    const numPower = parseInt(power, 10);
    
    if (!isNaN(numPower) && numPower >= 0) {
      const nFact = factorial(numPower);
      const sExp = numPower + 1;
      return {
        type: 'power',
        original: (sign < 0 ? '-' : '') + term,
        property: 'Potencias de t',
        formula: '\\mathcal{L}\\{t^n\\} = \\frac{n!}{s^{n+1}} \\quad (n \\in \\mathbb{N})',
        explanation: `Para $t^n$ con $n = ${numPower}$, calculamos $n! = ${numPower}! = ${nFact}$ y el denominador es $s^{${numPower}+1} = s^{${sExp}}$.`,
        resultLatex: sign < 0 ? `-\\frac{${nFact}}{s^{${sExp}}}` : `\\frac{${nFact}}{s^{${sExp}}}`,
        resultExpr: `${sign * nFact}/(s^${sExp})`
      };
    } else {
      // Potencia simbólica n
      return {
        type: 'symbolic_power',
        original: (sign < 0 ? '-' : '') + term,
        property: 'Potencia general (Función Gamma)',
        formula: '\\mathcal{L}\\{t^n\\} = \\frac{\\Gamma(n+1)}{s^{n+1}}',
        explanation: `Para potencias simbólicas o no enteras $t^n$, la transformada utiliza la función Gamma $\\Gamma(n+1)$.`,
        resultLatex: sign < 0 ? `-\\frac{\\Gamma(${power}+1)}{s^{${power}+1}}` : `\\frac{\\Gamma(${power}+1)}{s^{${power}+1}}`,
        resultExpr: `gamma(${power}+1)/(s^(${power}+1))`
      };
    }
  }

  // Raíz cuadrada: sqrt(t) = t^(1/2)
  if (term === 'sqrt(t)' || term === 't^(1/2)' || term === 't^0.5') {
    return {
      type: 'sqrt',
      original: (sign < 0 ? '-' : '') + term,
      property: 'Raíz cuadrada / Potencia fraccionaria',
      formula: '\\mathcal{L}\\{\\sqrt{t}\\} = \\frac{\\sqrt{\\pi}}{2 s^{3/2}}',
      explanation: `Como $\\sqrt{t} = t^{1/2}$, evaluamos $\\Gamma(3/2) = \\frac{\\sqrt{\\pi}}{2}$.`,
      resultLatex: sign < 0 ? `-\\frac{\\sqrt{\\pi}}{2 s^{3/2}}` : `\\frac{\\sqrt{\\pi}}{2 s^{3/2}}`,
      resultExpr: `sqrt(pi)/(2 * s^(1.5))`
    };
  }

  // 3. Exponencial: exp(a*t) o e^(a*t)
  const expMatch = term.match(/^exp\((.*?)\)$/);
  if (expMatch) {
    const inside = expMatch[1].trim();
    let aVal = extractCoefficientOfT(inside);
    let denomLatex = '';
    let denomExpr = '';

    if (aVal === '1') {
      denomLatex = 's - 1';
      denomExpr = '(s - 1)';
    } else if (aVal === '-1') {
      denomLatex = 's + 1';
      denomExpr = '(s + 1)';
    } else if (aVal.startsWith('-')) {
      const posA = aVal.slice(1);
      denomLatex = `s + ${posA}`;
      denomExpr = `(s + ${posA})`;
    } else {
      denomLatex = `s - ${aVal}`;
      denomExpr = `(s - ${aVal})`;
    }

    return {
      type: 'exponential',
      original: (sign < 0 ? '-' : '') + term,
      property: 'Función Exponencial',
      formula: '\\mathcal{L}\\{e^{at}\\} = \\frac{1}{s - a}',
      explanation: `Identificamos una exponencial $e^{at}$ con parámetro $a = ${aVal}$. Sustituyendo en la fórmula básica: $\\frac{1}{s - (${aVal})} = \\frac{1}{${denomLatex}}$.`,
      resultLatex: sign < 0 ? `-\\frac{1}{${denomLatex}}` : `\\frac{1}{${denomLatex}}`,
      resultExpr: `${sign}/(${denomExpr})`
    };
  }

  // 4. Funciones trigonométricas básicas: sin(w*t), cos(w*t), sinh(a*t), cosh(a*t)
  const trigMatch = term.match(/^(sin|cos|sinh|cosh)\((.*?)\)$/);
  if (trigMatch) {
    const funcName = trigMatch[1];
    const inside = trigMatch[2].trim();
    const wVal = extractCoefficientOfT(inside);

    let formulaLatex = '';
    let numerLatex = '';
    let denomLatex = '';
    let isHyperbolic = funcName.startsWith('sinh') || funcName.startsWith('cosh');
    let signOp = isHyperbolic ? '-' : '+';

    let wSqLatex = isNumeric(wVal) ? Math.pow(parseFloat(wVal), 2).toString() : `${wVal}^2`;

    if (funcName === 'sin') {
      formulaLatex = '\\mathcal{L}\\{\\sin(\\omega t)\\} = \\frac{\\omega}{s^2 + \\omega^2}';
      numerLatex = wVal;
      denomLatex = `s^2 + ${wSqLatex}`;
    } else if (funcName === 'cos') {
      formulaLatex = '\\mathcal{L}\\{\\cos(\\omega t)\\} = \\frac{s}{s^2 + \\omega^2}';
      numerLatex = 's';
      denomLatex = `s^2 + ${wSqLatex}`;
    } else if (funcName === 'sinh') {
      formulaLatex = '\\mathcal{L}\\{\\sinh(at)\\} = \\frac{a}{s^2 - a^2}';
      numerLatex = wVal;
      denomLatex = `s^2 - ${wSqLatex}`;
    } else if (funcName === 'cosh') {
      formulaLatex = '\\mathcal{L}\\{\\cosh(at)\\} = \\frac{s}{s^2 - a^2}';
      numerLatex = 's';
      denomLatex = `s^2 - ${wSqLatex}`;
    }

    return {
      type: 'trig',
      original: (sign < 0 ? '-' : '') + term,
      property: `Función ${funcName.toUpperCase()}`,
      formula: formulaLatex,
      explanation: `Aplicamos la transformada trigonométrica con frecuencia angular/parámetro $\\omega = ${wVal}$. Obtenemos el término cuadrático $\\omega^2 = ${wSqLatex}$.`,
      resultLatex: sign < 0 ? `-\\frac{${numerLatex}}{${denomLatex}}` : `\\frac{${numerLatex}}{${denomLatex}}`,
      resultExpr: `${sign} * (${numerLatex}) / (${denomLatex})`
    };
  }

  // 5. Producto exp(a*t) * g(t) — Primer Teorema de Traslación
  if (term.includes('exp(')) {
    const parts = splitProductFactors(term);
    const expPart = parts.find(p => p.startsWith('exp('));
    const otherParts = parts.filter(p => p !== expPart);

    if (expPart && otherParts.length > 0) {
      const expInside = expPart.slice(4, -1);
      const aVal = extractCoefficientOfT(expInside);
      const baseFunc = otherParts.join('*');
      const baseTransform = transformSingleTerm(baseFunc);

      const shiftDesc = aVal.startsWith('-') ? `s + ${aVal.slice(1)}` : `s - ${aVal}`;

      return {
        type: 'shift_s',
        original: (sign < 0 ? '-' : '') + term,
        property: 'Primer Teorema de Traslación (Traslación en s)',
        formula: '\\mathcal{L}\\{e^{at} f(t)\\} = F(s - a) \\quad \\text{donde } F(s) = \\mathcal{L}\\{f(t)\\}',
        explanation: `1. Calculamos la transformada base de $f(t) = ${exprToLatex(baseFunc)}$: $F(s) = ${baseTransform.resultLatex}$.<br>
                      2. Aplicamos traslación con $a = ${aVal}$, sustituyendo $s \\to ${shiftDesc}$.`,
        intermediate: {
          base: baseTransform.resultLatex,
          shift: shiftDesc
        },
        resultLatex: substituteVariable(baseTransform.resultLatex, 's', `(${shiftDesc})`),
        resultExpr: substituteVariable(baseTransform.resultExpr, 's', `(${shiftDesc})`)
      };
    }
  }

  // 6. Multiplicación por t o t^n: t*f(t) o t^n * f(t) — Derivada de la Transformada
  if (term.startsWith('t*') || term.match(/^t\^[0-9]+\*/)) {
    let n = 1;
    let baseFunc = '';
    
    if (term.startsWith('t*')) {
      n = 1;
      baseFunc = term.slice(2);
    } else {
      const m = term.match(/^t\^([0-9]+)\*(.*)$/);
      if (m) {
        n = parseInt(m[1], 10);
        baseFunc = m[2];
      }
    }

    const baseTransform = transformSingleTerm(baseFunc);
    
    // Si la base es trigonométrica conocida
    if (baseFunc.startsWith('sin(') || baseFunc.startsWith('cos(')) {
      const isSin = baseFunc.startsWith('sin(');
      const wVal = extractCoefficientOfT(baseFunc.slice(4, -1));
      const wSq = isNumeric(wVal) ? Math.pow(parseFloat(wVal), 2) : `${wVal}^2`;

      if (n === 1 && isSin) {
        // L{t*sin(wt)} = 2*w*s / (s^2 + w^2)^2
        const factor2w = isNumeric(wVal) ? 2 * parseFloat(wVal) : `2${wVal}`;
        return {
          type: 'mult_t',
          original: (sign < 0 ? '-' : '') + term,
          property: 'Multiplicación por t (Derivada en s)',
          formula: '\\mathcal{L}\\{t F(t)\\} = -\\frac{d}{ds}[F(s)]',
          explanation: `1. Transformada base: $\\mathcal{L}\\{\\sin(${wVal}t)\\} = \\frac{${wVal}}{s^2 + ${wSq}}$.<br>
                        2. Aplicamos la propiedad: $-\\frac{d}{ds}\\left[\\frac{${wVal}}{s^2 + ${wSq}}\\right] = -\\left[ -\\frac{2s \\cdot ${wVal}}{(s^2 + ${wSq})^2} \\right] = \\frac{${factor2w}s}{(s^2 + ${wSq})^2}$.`,
          resultLatex: `\\frac{${factor2w}s}{(s^2 + ${wSq})^2}`,
          resultExpr: `(${factor2w}*s)/((s^2 + ${wSq})^2)`
        };
      }

      if (n === 1 && !isSin) {
        // L{t*cos(wt)} = (s^2 - w^2) / (s^2 + w^2)^2
        return {
          type: 'mult_t',
          original: (sign < 0 ? '-' : '') + term,
          property: 'Multiplicación por t (Derivada en s)',
          formula: '\\mathcal{L}\\{t F(t)\\} = -\\frac{d}{ds}[F(s)]',
          explanation: `1. Transformada base: $\\mathcal{L}\\{\\cos(${wVal}t)\\} = \\frac{s}{s^2 + ${wSq}}$.<br>
                        2. Derivamos con respecto a $s$: $-\\frac{d}{ds}\\left[\\frac{s}{s^2 + ${wSq}}\\right] = -\\left[\\frac{-(s^2 - ${wSq})}{(s^2 + ${wSq})^2}\\right] = \\frac{s^2 - ${wSq}}{(s^2 + ${wSq})^2}$.`,
          resultLatex: `\\frac{s^2 - ${wSq}}{(s^2 + ${wSq})^2}`,
          resultExpr: `(s^2 - ${wSq})/((s^2 + ${wSq})^2)`
        };
      }
    }

    return {
      type: 'mult_t_general',
      original: (sign < 0 ? '-' : '') + term,
      property: `Multiplicación por t^${n}`,
      formula: `\\mathcal{L}\\{t^n f(t)\\} = (-1)^n \\frac{d^n}{ds^n}[F(s)]`,
      explanation: `Se deriva la transformada base $F(s) = ${baseTransform.resultLatex}$ $n=${n}$ veces con respecto a $s$ y se multiplica por $(-1)^n$.`,
      resultLatex: `(-1)^{${n}} \\frac{d^{${n}}}{ds^{${n}}}\\left[ ${baseTransform.resultLatex} \\right]`,
      resultExpr: `derivative(${baseTransform.resultExpr}, s, ${n})`
    };
  }

  // Si no encaja en las anteriores, intentar resolución general
  return {
    type: 'general',
    original: (sign < 0 ? '-' : '') + term,
    property: 'Transformada directa',
    formula: '\\mathcal{L}\\{f(t)\\} = \\int_0^\\infty e^{-st} f(t) dt',
    explanation: 'Se evalúa la definición integral o tabla de transformadas.',
    resultLatex: `\\mathcal{L}\\{${exprToLatex(term)}\\}`,
    resultExpr: `laplace(${term}, t, s)`
  };
}

/**
 * Calcula la Transformada de Laplace de una función F(t).
 * Maneja linealidad a F(t) + b G(t), traslaciones, multiplicaciones y derivadas.
 */
function calculateLaplace(inputStr) {
  const norm = normalizeExpression(inputStr, 't');
  const validation = validateInput(norm);
  if (!validation.valid) {
    throw new Error(validation.error);
  }

  // 1. Manejo especial de Derivadas: f'(t), f''(t)
  if (/^[a-zA-Z][']+(\(t\))?$/.test(norm.replace(/\s+/g, ''))) {
    const apostrophes = (norm.match(/'/g) || []).length;
    const funcLetter = norm.charAt(0).toUpperCase();
    if (apostrophes === 1) {
      return {
        input: norm,
        type: 'derivative',
        steps: [
          {
            title: 'Propiedad de la Primera Derivada',
            property: 'Derivada en el tiempo',
            description: 'La transformada de la primera derivada de una función transforma la diferenciación temporal en multiplicación algebraica por $s$.',
            formula: '\\mathcal{L}\\{f\'(t)\\} = s F(s) - f(0)'
          }
        ],
        finalLatex: `s ${funcLetter}(s) - ${norm.charAt(0).toLowerCase()}(0)`,
        finalExpr: `s*${funcLetter}(s) - ${norm.charAt(0).toLowerCase()}(0)`,
        method: 'Propiedad de la Derivada'
      };
    } else if (apostrophes === 2) {
      return {
        input: norm,
        type: 'derivative',
        steps: [
          {
            title: 'Propiedad de la Segunda Derivada',
            property: 'Segunda Derivada',
            description: 'Para la segunda derivada se involucran las condiciones iniciales en $t=0$ de la función y de su primera derivada.',
            formula: '\\mathcal{L}\\{f\'\'(t)\\} = s^2 F(s) - s f(0) - f\'(0)'
          }
        ],
        finalLatex: `s^2 ${funcLetter}(s) - s ${norm.charAt(0).toLowerCase()}(0) - ${norm.charAt(0).toLowerCase()}\'(0)`,
        finalExpr: `s^2*${funcLetter}(s) - s*${norm.charAt(0).toLowerCase()}(0) - ${norm.charAt(0).toLowerCase()}\'(0)`,
        method: 'Propiedad de la Segunda Derivada'
      };
    }
  }

  // 2. Manejo de Integrales: int(f(t))
  if (norm.startsWith('int(') || norm.startsWith('integral(')) {
    return {
      input: norm,
      type: 'integral',
      steps: [
        {
          title: 'Propiedad de la Integral en el Tiempo',
          property: 'Integración',
          description: 'La integración en el dominio del tiempo corresponde a la división por $s$ en el dominio de Laplace.',
          formula: '\\mathcal{L}\\left\\{ \\int_0^t f(u) du \\right\\} = \\frac{F(s)}{s}'
        }
      ],
      finalLatex: `\\frac{F(s)}{s}`,
      finalExpr: `F(s)/s`,
      method: 'Propiedad de Integración'
    };
  }

  // 3. Separar términos por adición/sustracción respetando paréntesis
  const rawTerms = splitIntoTerms(norm);
  const steps = [];
  const termResults = [];

  // Paso 1: Identificación y Linealidad
  if (rawTerms.length > 1) {
    steps.push({
      title: 'Propiedad de Linealidad',
      property: 'Linealidad',
      description: 'Separamos la transformada de la suma en la suma de las transformadas de cada término individual, factorizando las constantes fuera del operador:',
      formula: '\\mathcal{L}\\{a f(t) + b g(t)\\} = a \\mathcal{L}\\{f(t)\\} + b \\mathcal{L}\\{g(t)\\}'
    });
  }

  // Procesar cada término
  rawTerms.forEach((tStr, index) => {
    // Extraer coeficiente numérico si existe: ej 3*t^3 -> coeff 3, core t^3
    const { coeff, core } = parseCoefficientAndCore(tStr);
    const transformed = transformSingleTerm(core);

    let termLatex = '';
    if (coeff === 1) {
      termLatex = transformed.resultLatex;
    } else if (coeff === -1) {
      termLatex = `-${transformed.resultLatex}`;
    } else {
      termLatex = `${coeff} \\cdot \\left(${transformed.resultLatex}\\right)`;
    }

    steps.push({
      title: `Término ${index + 1}: $${exprToLatex(tStr)}$`,
      property: transformed.property,
      description: transformed.explanation,
      formula: transformed.formula,
      latex: termLatex
    });

    termResults.push({
      latex: termLatex,
      expr: coeff === 1 ? transformed.resultExpr : `${coeff}*(${transformed.resultExpr})`
    });
  });

  // Ensamblar resultado final
  let finalLatex = termResults.map((r, i) => {
    let lx = r.latex.trim();
    if (i > 0 && !lx.startsWith('-')) return `+ ${lx}`;
    return lx;
  }).join(' ');

  // Intentar simplificación simbólica con Algebrite o Math.js si es posible
  let finalExpr = termResults.map(r => r.expr).join(' + ');

  return {
    input: norm,
    steps: steps,
    finalLatex: finalLatex,
    finalExpr: finalExpr,
    method: rawTerms.length > 1 ? 'Linealidad y Transformadas Fundamentales' : (steps[0] ? steps[0].property : 'Transformada Directa')
  };
}

// ==========================================================================
// 3. MOTOR DE ANTITRANSFORMADA DE LAPLACE ℒ⁻¹{F(s)}
// ==========================================================================

/**
 * Algoritmo completo de Transformada Inversa según especificación:
 * 1. Análisis de fracción propia / impropia
 * 2. Factorización del denominador (Casos A, B, C, D)
 * 3. Fracciones parciales (Heaviside) y Completación de cuadrados
 * 4. Inversión término a término
 */
function calculateInverseLaplace(inputStr) {
  const norm = normalizeExpression(inputStr, 's');
  const validation = validateInput(norm);
  if (!validation.valid) {
    throw new Error(validation.error);
  }

  const steps = [];

  // Separar en numerador y denominador si es una fracción general
  const frac = extractNumeratorAndDenominator(norm);
  let P = frac.num; // Numerador
  let Q = frac.den; // Denominador

  // Paso 1: Analizar grado de fracción
  const degP = estimateDegree(P, 's');
  const degQ = estimateDegree(Q, 's');

  steps.push({
    title: 'Paso 1: Análisis del Tipo de Fracción',
    property: 'Clasificación de Grado',
    description: `Determinamos el grado del numerador $P(s) = ${exprToLatex(P)}$ (grado ${degP}) y del denominador $Q(s) = ${exprToLatex(Q)}$ (grado ${degQ}).`,
    formula: degP >= degQ ? '\\text{Fracción Impropia: } \\operatorname{deg}(P) \\ge \\operatorname{deg}(Q)' : '\\text{Fracción Propia: } \\operatorname{deg}(P) < \\operatorname{deg}(Q)'
  });

  if (degP >= degQ && degQ > 0) {
    steps.push({
      title: 'Paso 1.1: División Polinomial',
      property: 'División de Polinomios',
      description: 'Como la fracción es impropia, realizamos la división algebraica $F(s) = C(s) + \\frac{R(s)}{Q(s)}$. El cociente $C(s)$ genera impulsos de Dirac $\\delta(t)$ y sus derivadas, mientras que el residuo $R(s)/Q(s)$ es una fracción propia.',
      formula: 'F(s) = C(s) + \\frac{R(s)}{Q(s)} \\implies \\mathcal{L}^{-1}\\{F(s)\\} = c_0 \\delta(t) + c_1 \\delta\'(t) + \\dots + \\mathcal{L}^{-1}\\left\\{\\frac{R(s)}{Q(s)}\\right\\}'
    });
  }

  // Paso 2: Casos Canónicos de Transformadas Inversas

  // Caso 0: Formas simples 1/(s-a), 1/s^n
  // 0.1: 1/(s-a) o 1/(s+a)
  const linearMatch = Q.match(/^(s\s*([+-])\s*([0-9a-zA-Z_]+))$/);
  if (P === '1' && linearMatch) {
    const sign = linearMatch[2];
    const aVal = linearMatch[3];
    const expSign = sign === '+' ? '-' : '';
    const resultLatex = `e^{${expSign}${aVal}t}`;

    steps.push({
      title: 'Identificación de Factor Lineal Simple',
      property: 'Antitransformada Exponencial',
      description: `Reconocemos la forma estándar de la función exponencial $\\frac{1}{s - a}$ con polo en $s = ${sign === '+' ? '-' + aVal : aVal}$.`,
      formula: '\\mathcal{L}^{-1}\\left\\{ \\frac{1}{s - a} \\right\\} = e^{at}',
      latex: resultLatex
    });

    return {
      input: norm,
      steps: steps,
      finalLatex: resultLatex,
      finalExpr: `exp(${expSign}${aVal}*t)`,
      method: 'Antitransformada Directa (Exponencial)'
    };
  }

  // 0.2: Potencias 1/s^(n+1)
  const sPowerMatch = Q.match(/^s(\^([0-9]+))?$/);
  if (P === '1' && sPowerMatch) {
    const nPlusOne = sPowerMatch[2] ? parseInt(sPowerMatch[2], 10) : 1;
    if (nPlusOne === 1) {
      return {
        input: norm,
        steps: steps,
        finalLatex: '1',
        finalExpr: '1',
        method: 'Antitransformada de Constante (1/s)'
      };
    } else if (nPlusOne === 2) {
      return {
        input: norm,
        steps: steps,
        finalLatex: 't',
        finalExpr: 't',
        method: 'Antitransformada de Potencia t (1/s²)'
      };
    } else {
      const n = nPlusOne - 1;
      const nFact = factorial(n);
      return {
        input: norm,
        steps: steps,
        finalLatex: `\\frac{t^{${n}}}{${nFact}}`,
        finalExpr: `(t^${n})/${nFact}`,
        method: 'Antitransformada de Potencia t^n'
      };
    }
  }

  // Caso C: Trinomio Cuadrático o Cuadrático Puro: s^2 + w^2 o s^2 + bs + c
  const quadMatch = parseQuadraticDenominator(Q);
  if (quadMatch) {
    const { a, b, c, discr } = quadMatch;

    // Subcaso: s^2 + w^2 (puro, b = 0)
    if (b === 0 && c > 0) {
      const wSq = c;
      const w = Math.sqrt(wSq);
      const isPerfectSquare = Number.isInteger(w);
      const wLatex = isPerfectSquare ? w.toString() : `\\sqrt{${wSq}}`;
      const { M, N } = parseLinearNumerator(P);

      // Si P es constante N/(s^2 + w^2)
      if (M === 0) {
        const pNum = N;
        const coeff = pNum / (isPerfectSquare ? w : 1);
        const coeffLatex = isPerfectSquare 
          ? (coeff === 1 ? '' : (pNum === 1 ? `\\frac{1}{${w}}` : `\\frac{${pNum}}{${w}}`))
          : `\\frac{${pNum}}{\\sqrt{${wSq}}}`;
        
        steps.push({
          title: 'Paso 2: Reconocimiento de Forma Senoidal',
          property: 'Seno Trigonométrico',
          description: `El denominador corresponde a $s^2 + \\omega^2$ con $\\omega^2 = ${wSq} \\implies \\omega = ${wLatex}$. Multiplicamos y dividimos por $\\omega$ para completar la forma estándar:`,
          formula: '\\mathcal{L}^{-1}\\left\\{ \\frac{\\omega}{s^2 + \\omega^2} \\right\\} = \\sin(\\omega t)',
          latex: `${coeffLatex} \\sin(${wLatex} t)`.trim()
        });

        return {
          input: norm,
          steps: steps,
          finalLatex: `${coeffLatex} \\sin(${wLatex} t)`.trim(),
          finalExpr: `(${pNum}/${w}) * sin(${w}*t)`,
          method: 'Antitransformada Seno'
        };
      }

      // Si P es puro M*s/(s^2 + w^2)
      if (N === 0) {
        const coeffLatex = M === 1 ? '' : (M === -1 ? '-' : `${M} `);
        steps.push({
          title: 'Paso 2: Reconocimiento de Forma Cosenoidal',
          property: 'Coseno Trigonométrico',
          description: `El numerador $s$ y el denominador $s^2 + \\omega^2$ corresponden exactamente a la transformada del coseno con $\\omega = ${wLatex}$.`,
          formula: '\\mathcal{L}^{-1}\\left\\{ \\frac{s}{s^2 + \\omega^2} \\right\\} = \\cos(\\omega t)',
          latex: `${coeffLatex}\\cos(${wLatex} t)`.trim()
        });

        return {
          input: norm,
          steps: steps,
          finalLatex: `${coeffLatex}\\cos(${wLatex} t)`.trim(),
          finalExpr: `${M} * cos(${w}*t)`,
          method: 'Antitransformada Coseno'
        };
      }

      // Si P es M*s + N general
      const cosTermLatex = M === 1 ? `\\cos(${wLatex} t)` : (M === -1 ? `-\\cos(${wLatex} t)` : `${M} \\cos(${wLatex} t)`);
      const sinCoeff = isPerfectSquare ? (N / w) : N;
      const sinTermLatex = isPerfectSquare 
        ? (sinCoeff === 1 ? `\\sin(${wLatex} t)` : (sinCoeff === -1 ? `-\\sin(${wLatex} t)` : `${sinCoeff} \\sin(${wLatex} t)`))
        : `\\frac{${N}}{${wLatex}} \\sin(${wLatex} t)`;

      const combinedResult = sinTermLatex.startsWith('-') ? `${cosTermLatex} ${sinTermLatex}` : `${cosTermLatex} + ${sinTermLatex}`;

      steps.push({
        title: 'Paso 2: Descomposición en Componentes Coseno y Seno',
        property: 'Linealidad Trigonométrica',
        description: `Separamos el numerador lineal $P(s) = ${exprToLatex(P)}$ en términos de $\\cos(\\omega t)$ y $\\sin(\\omega t)$ con $\\omega = ${wLatex}$:<br>
                      $$\\frac{${exprToLatex(P)}}{s^2 + ${wSq}} = ${M !== 0 ? `${M} \\frac{s}{s^2 + ${wSq}}` : ''} + \\frac{${N}}{${wLatex}} \\frac{${wLatex}}{s^2 + ${wSq}}$$`,
        formula: '\\mathcal{L}^{-1}\\left\\{ M\\frac{s}{s^2+\\omega^2} + \\frac{N}{\\omega}\\frac{\\omega}{s^2+\\omega^2} \\right\\} = M\\cos(\\omega t) + \\frac{N}{\\omega}\\sin(\\omega t)',
        latex: combinedResult
      });

      return {
        input: norm,
        steps: steps,
        finalLatex: combinedResult,
        finalExpr: `${M} * cos(${w}*t) + (${N}/${w}) * sin(${w}*t)`,
        method: 'Linealidad Trigonométrica (Seno y Coseno)'
      };
    }

    // Subcaso: s^2 + bs + c con b != 0 y discriminante negativo (Completación de Cuadrados)
    if (discr < 0) {
      // s^2 + bs + c = (s + b/2)^2 + (c - b^2/4) = (s - alpha)^2 + w^2
      const alpha = -b / 2;
      const wSq = c - Math.pow(b / 2, 2);
      const w = Math.sqrt(wSq);
      const isPerfectSquare = Number.isInteger(w);
      const wLatex = isPerfectSquare ? w.toString() : `\\sqrt{${wSq}}`;

      const alphaLatex = alpha < 0 ? `+ ${Math.abs(alpha)}` : `- ${alpha}`;
      const signExp = alpha > 0 ? `${alpha}` : `${alpha}`;

      steps.push({
        title: 'Paso 2: Completación de Cuadrados del Denominador',
        property: 'Completación de Cuadrados',
        description: `El trinomio cuadrático $s^2 + ${b}s + ${c}$ no tiene raíces reales ($b^2 - 4c = ${discr} < 0$). Realizamos la completación de cuadrados:`,
        formula: `s^2 + ${b}s + ${c} = \\left(s + \\frac{${b}}{2}\\right)^2 + \\left(${c} - \\frac{${b}^2}{4}\\right) = (s ${alphaLatex})^2 + ${wSq} = (s ${alphaLatex})^2 + ${wLatex}^2`
      });

      // Numerador lineal P(s) = M*s + N
      const { M, N } = parseLinearNumerator(P);

      // Descomposición en términos de (s - alpha) y w
      // M*s + N = M*(s - alpha) + (N + M*alpha)
      const remainder = N + M * alpha;

      steps.push({
        title: 'Paso 3: Ajuste del Numerador al Término Desplazado',
        property: 'Descomposición del Numerador',
        description: `Expresamos el numerador en términos de $(s ${alphaLatex})$ para separar los componentes del coseno amortiguado y seno amortiguado:`,
        formula: `${exprToLatex(P)} = ${M !== 0 ? `${M}(s ${alphaLatex})` : ''} ${remainder !== 0 ? (remainder > 0 ? `+ ${remainder}` : `- ${Math.abs(remainder)}`) : ''}`
      });

      let cosTermLatex = '';
      let sinTermLatex = '';
      const expFactor = alpha !== 0 ? (alpha === 1 ? 'e^{t}' : (alpha === -1 ? 'e^{-t}' : `e^{${signExp}t}`)) : '';

      if (M !== 0) {
        cosTermLatex = `${M !== 1 ? M : ''}${expFactor} \\cos(${wLatex} t)`;
      }

      if (remainder !== 0) {
        const sinCoeff = isPerfectSquare ? (remainder / w) : remainder;
        const sinCoeffLatex = isPerfectSquare 
          ? (sinCoeff === 1 ? '' : (sinCoeff === -1 ? '-' : `${sinCoeff}`))
          : `\\frac{${remainder}}{${wLatex}}`;
        sinTermLatex = `${sinCoeffLatex}${expFactor} \\sin(${wLatex} t)`;
      }

      let combinedResultLatex = '';
      if (cosTermLatex && sinTermLatex) {
        combinedResultLatex = sinTermLatex.startsWith('-') 
          ? `${cosTermLatex} ${sinTermLatex}` 
          : `${cosTermLatex} + ${sinTermLatex}`;
      } else {
        combinedResultLatex = cosTermLatex || sinTermLatex;
      }

      steps.push({
        title: 'Paso 4: Aplicación del Teorema de Traslación Inverso',
        property: 'Inversión por Traslación',
        description: 'Aplicamos las transformadas inversas elementales con desplazamiento exponencial $e^{\\alpha t}$:',
        formula: '\\mathcal{L}^{-1}\\left\\{ \\frac{s - \\alpha}{(s-\\alpha)^2 + \\omega^2} \\right\\} = e^{\\alpha t}\\cos(\\omega t), \\quad \\mathcal{L}^{-1}\\left\\{ \\frac{\\omega}{(s-\\alpha)^2 + \\omega^2} \\right\\} = e^{\\alpha t}\\sin(\\omega t)',
        latex: combinedResultLatex
      });

      return {
        input: norm,
        steps: steps,
        finalLatex: combinedResultLatex,
        finalExpr: `${expFactor} * (${M} * cos(${w}*t) + (${remainder}/${w}) * sin(${w}*t))`,
        method: 'Completación de Cuadrados y Traslación en s'
      };
    }
  }

  // Caso A: Fracciones Parciales para Factores Lineales Reales Distintos: (s - r1)(s - r2)...
  const factoredDenom = parseFactoredDenominator(Q);
  if (factoredDenom && factoredDenom.length > 1) {
    steps.push({
      title: 'Paso 2: Factorización y Estructura de Fracciones Parciales',
      property: 'Descomposición en Fracciones Parciales',
      description: `El denominador se compone de los factores lineales reales distintos: $${factoredDenom.map(f => `(s - ${f.root})`).join('')}$. Planteamos la descomposición:`,
      formula: `\\frac{${exprToLatex(P)}}{${exprToLatex(Q)}} = ` + factoredDenom.map((f, i) => `\\frac{A_{${i+1}}}{s - (${f.root})}`).join(' + ')
    });

    // Método de Heaviside (Cover-up method)
    const coefficients = [];
    factoredDenom.forEach((factor, idx) => {
      const r = factor.root;
      // Evaluar P(r)
      const pVal = evaluatePolynomial(P, r);
      // Evaluar producto de los otros factores en r
      let otherProd = 1;
      factoredDenom.forEach((other, oIdx) => {
        if (oIdx !== idx) {
          otherProd *= (r - other.root);
        }
      });

      const A = pVal / otherProd;
      coefficients.push({ root: r, coeff: A, index: idx + 1 });

      steps.push({
        title: `Paso 3.${idx + 1}: Coeficiente $A_{${idx+1}}$ por Método de Heaviside`,
        property: 'Método de Heaviside (Encubrimiento)',
        description: `Multiplicamos por $(s - (${r}))$ y evaluamos en el polo $s = ${r}$:<br>
                      $$A_{${idx+1}} = \\lim_{s \\to ${r}} (s - (${r})) F(s) = \\frac{P(${r})}{\\prod_{j \\neq ${idx+1}} (${r} - r_j)} = \\frac{${pVal}}{${otherProd}} = ${A}$$`,
        formula: `A_{${idx+1}} = ${A}`
      });
    });

    // Inversión término a término
    const termsLatex = coefficients.map(c => {
      const expSign = c.root > 0 ? `${c.root}` : (c.root === 0 ? '' : `${c.root}`);
      const expLatex = c.root === 0 ? '' : (c.root === 1 ? 'e^{t}' : (c.root === -1 ? 'e^{-t}' : `e^{${expSign}t}`));
      
      if (c.coeff === 1) return expLatex || '1';
      if (c.coeff === -1) return `-${expLatex || '1'}`;
      return `${c.coeff}${expLatex ? ' ' + expLatex : ''}`;
    });

    const finalResultLatex = termsLatex.map((tl, i) => {
      if (i > 0 && !tl.startsWith('-')) return `+ ${tl}`;
      return tl;
    }).join(' ');

    steps.push({
      title: 'Paso 4: Transformada Inversa Término a Término',
      property: 'Inversión de Fracciones Simples',
      description: 'Aplicamos la transformada inversa a cada fracción simple obtenida:',
      formula: '\\mathcal{L}^{-1}\\left\\{ \\sum \\frac{A_k}{s - r_k} \\right\\} = \\sum A_k e^{r_k t}',
      latex: finalResultLatex
    });

    return {
      input: norm,
      steps: steps,
      finalLatex: finalResultLatex,
      finalExpr: coefficients.map(c => `${c.coeff}*exp(${c.root}*t)`).join(' + '),
      method: 'Fracciones Parciales (Método de Heaviside)'
    };
  }

  // Caso B: Factores Lineales Repetidos: 1/(s-a)^n
  const repMatch = Q.match(/^\(?(s\s*([+-])\s*([0-9a-zA-Z_]+))\)?\^([0-9]+)$/);
  if (repMatch) {
    const sign = repMatch[2];
    const aVal = repMatch[3];
    const n = parseInt(repMatch[4], 10);
    const root = sign === '+' ? `-${aVal}` : aVal;
    const power = n - 1;
    const nFact = factorial(power);

    const expTerm = root === '0' ? '' : (root === '1' ? 'e^{t}' : (root === '-1' ? 'e^{-t}' : `e^{${root}t}`));
    const tTerm = power === 0 ? '' : (power === 1 ? 't' : `t^{${power}}`);

    let finalLatex = '';
    if (power === 0) {
      finalLatex = expTerm || '1';
    } else {
      finalLatex = nFact === 1 
        ? `${tTerm} ${expTerm}`.trim() 
        : `\\frac{${tTerm} ${expTerm}}{${nFact}}`.trim();
    }

    steps.push({
      title: 'Paso 2: Identificación de Factor Repetido',
      property: 'Polo Múltiple / Potencia de s',
      description: `El denominador contiene el factor lineal repetido $(s - (${root}))^${n}$. Aplicamos el teorema de traslación inversa para potencias:`,
      formula: '\\mathcal{L}^{-1}\\left\\{ \\frac{1}{(s - a)^n} \\right\\} = \\frac{t^{n-1}}{(n-1)!} e^{at}',
      latex: finalLatex
    });

    return {
      input: norm,
      steps: steps,
      finalLatex: finalLatex,
      finalExpr: `(t^${power} * exp(${root}*t)) / ${nFact}`,
      method: 'Antitransformada de Factor Repetido'
    };
  }

  // Fallback a Algebrite o Math.js si está disponible
  try {
    if (window.Algebrite) {
      // Intentar descomposición o análisis simbólico
      const algRes = window.Algebrite.run(`roots(${Q})`);
      // Si Algebrite arroja raíces pero no hay regla específica
    }
  } catch (err) {
    // Silencioso
  }

  // Explicación clara si el motor no tiene regla directa implementada
  steps.push({
    title: 'Análisis Simbólico Complejo',
    property: 'Límite de Algoritmo Simbólico',
    description: 'Esta expresión requiere un método simbólico adicional que no está implementado actualmente.',
    formula: '\\text{Consulte métodos de inversión por integración en el plano complejo (Bromwich) o expansión por residuos.}'
  });

  return {
    input: norm,
    steps: steps,
    finalLatex: '\\text{Método simbólico adicional requerido}',
    finalExpr: '',
    method: 'Resolución no estándar'
  };
}

// ==========================================================================
// 4. PARSERS ALGEBRAICOS AUXILIARES
// ==========================================================================

/**
 * Divide una expresión en sus términos de suma/resta sin romper paréntesis.
 */
function splitIntoTerms(expr) {
  const terms = [];
  let depth = 0;
  let start = 0;

  for (let i = 0; i < expr.length; i++) {
    const c = expr[i];
    if (c === '(') depth++;
    else if (c === ')') depth--;
    else if ((c === '+' || c === '-') && depth === 0 && i > 0 && expr[i - 1] !== '*' && expr[i - 1] !== '^' && expr[i - 1] !== '/') {
      terms.push(expr.slice(start, i).trim());
      start = i;
    }
  }
  terms.push(expr.slice(start).trim());
  return terms.filter(t => t.length > 0);
}

/**
 * Separa un término en coeficiente y función base: ej '3*t^2' -> { coeff: 3, core: 't^2' }
 */
function parseCoefficientAndCore(term) {
  let str = term.trim();
  let sign = 1;

  if (str.startsWith('+')) {
    str = str.slice(1).trim();
  } else if (str.startsWith('-')) {
    sign = -1;
    str = str.slice(1).trim();
  }

  // Comprobar si empieza por número seguido de '*'
  const numMatch = str.match(/^([0-9.]+)\*(.*)$/);
  if (numMatch) {
    const coeff = sign * parseFloat(numMatch[1]);
    return { coeff, core: numMatch[2].trim() };
  }

  return { coeff: sign, core: str };
}

/**
 * Separa factores de un producto (respetando paréntesis).
 */
function splitProductFactors(term) {
  const factors = [];
  let depth = 0;
  let start = 0;

  for (let i = 0; i < term.length; i++) {
    const c = term[i];
    if (c === '(') depth++;
    else if (c === ')') depth--;
    else if (c === '*' && depth === 0) {
      factors.push(term.slice(start, i).trim());
      start = i + 1;
    }
  }
  factors.push(term.slice(start).trim());
  return factors;
}

/**
 * Extrae el coeficiente numérico de la variable 't' dentro de un argumento: ej '2*t' -> '2', '-3*t' -> '-3', 'w*t' -> 'w'
 */
function extractCoefficientOfT(expr) {
  let s = expr.trim();
  if (s === 't') return '1';
  if (s === '-t') return '-1';
  
  // Casos como '2*t', 'a*t', '-2*t'
  s = s.replace(/\*t$/, '').replace(/t$/, '');
  return s.trim() || '1';
}

/**
 * Separa una fracción en numerador P y denominador Q.
 */
function extractNumeratorAndDenominator(expr) {
  let s = expr.trim();
  
  // Buscar barra de división '/' en nivel 0 de profundidad
  let depth = 0;
  for (let i = 0; i < s.length; i++) {
    if (s[i] === '(') depth++;
    else if (s[i] === ')') depth--;
    else if (s[i] === '/' && depth === 0) {
      let num = s.slice(0, i).trim();
      let den = s.slice(i + 1).trim();
      
      // Quitar paréntesis exteriores redundantes
      if (num.startsWith('(') && num.endsWith(')') && validateInput(num.slice(1, -1)).valid) {
        num = num.slice(1, -1);
      }
      if (den.startsWith('(') && den.endsWith(')') && validateInput(den.slice(1, -1)).valid) {
        den = den.slice(1, -1);
      }
      return { num, den };
    }
  }

  return { num: s, den: '1' };
}

/**
 * Estima el grado algebraico de un polinomio respecto a una variable.
 */
function estimateDegree(polyStr, variable = 's') {
  if (!polyStr || !polyStr.includes(variable)) return 0;
  
  // Si contiene productos factorizados como (s+1)*(s+2)
  const factorMatches = polyStr.match(new RegExp(`\\(${variable}\\s*[+-]\\s*[0-9a-zA-Z_]+\\)`, 'g'));
  if (factorMatches && factorMatches.length > 1) {
    return factorMatches.length;
  }

  // Buscar potencias explícitas s^n
  const powRegex = new RegExp(`${variable}\\^([0-9]+)`, 'g');
  let maxDegree = 1;
  let match;
  while ((match = powRegex.exec(polyStr)) !== null) {
    const d = parseInt(match[1], 10);
    if (d > maxDegree) maxDegree = d;
  }

  return maxDegree;
}

/**
 * Parsea trinomios cuadráticos en 's': s^2 + bs + c
 */
function parseQuadraticDenominator(denom) {
  let s = denom.trim();
  if (s.startsWith('(') && s.endsWith(')')) s = s.slice(1, -1).trim();

  // Caso: s^2 + c
  let m = s.match(/^s\^2\s*\+\s*([0-9.]+)$/);
  if (m) {
    return { a: 1, b: 0, c: parseFloat(m[1]), discr: -4 * parseFloat(m[1]) };
  }

  // Caso: s^2 - c
  m = s.match(/^s\^2\s*-\s*([0-9.]+)$/);
  if (m) {
    return { a: 1, b: 0, c: -parseFloat(m[1]), discr: 4 * parseFloat(m[1]) };
  }

  // Caso: s^2 + b*s + c o s^2 + bs + c
  m = s.match(/^s\^2\s*([+-])\s*([0-9.]*)\*?s\s*([+-])\s*([0-9.]+)$/);
  if (m) {
    const signB = m[1] === '-' ? -1 : 1;
    const bVal = m[2] === '' ? 1 : parseFloat(m[2]);
    const b = signB * bVal;

    const signC = m[3] === '-' ? -1 : 1;
    const c = signC * parseFloat(m[4]);

    const discr = b * b - 4 * c;
    return { a: 1, b, c, discr };
  }

  return null;
}

/**
 * Parsea un numerador lineal de la forma M*s + N
 */
function parseLinearNumerator(numStr) {
  let s = numStr.trim();
  if (s.startsWith('(') && s.endsWith(')')) s = s.slice(1, -1).trim();

  if (s === 's') return { M: 1, N: 0 };
  if (s === '-s') return { M: -1, N: 0 };
  if (isNumeric(s)) return { M: 0, N: parseFloat(s) };

  // Caso: M*s + N
  const m = s.match(/^([+-]?[0-9.]*)\*?s\s*([+-])\s*([0-9.]+)$/);
  if (m) {
    let mStr = m[1];
    let M = 1;
    if (mStr === '-' || mStr === '-1') M = -1;
    else if (mStr !== '' && mStr !== '+') M = parseFloat(mStr);

    const signN = m[2] === '-' ? -1 : 1;
    const N = signN * parseFloat(m[3]);
    return { M, N };
  }

  // Caso: solo M*s
  const mOnly = s.match(/^([+-]?[0-9.]*)\*?s$/);
  if (mOnly) {
    let mStr = mOnly[1];
    let M = 1;
    if (mStr === '-') M = -1;
    else if (mStr !== '') M = parseFloat(mStr);
    return { M, N: 0 };
  }

  return { M: 1, N: 0 };
}

/**
 * Parsea un denominador factorizado en factores lineales: ej (s+1)*(s+2), s*(s+2) o trinomios con raíces reales
 */
function parseFactoredDenominator(denom) {
  let s = denom.trim();
  if (s.startsWith('(') && s.endsWith(')') && validateInput(s.slice(1, -1)).valid) {
    s = s.slice(1, -1).trim();
  }

  const factors = [];
  
  // 1. Detectar factor 's' aislado: ej s*(s+1) o (s+1)*s
  if (/^s\s*\*|\*\s*s$|\(s\)\s*\*|\*\s*\(s\)/.test(s) || s === 's') {
    factors.push({ root: 0, raw: 's' });
    s = s.replace(/^s\s*\*|\*\s*s$/, '');
  }

  // 2. Factores lineales explícitos: (s + a) o (s - a)
  const regex = /\(s\s*([+-])\s*([0-9.]+)\)/g;
  let match;
  while ((match = regex.exec(s)) !== null) {
    const sign = match[1];
    const val = parseFloat(match[2]);
    const root = sign === '+' ? -val : val;
    factors.push({ root, raw: match[0] });
  }

  if (factors.length >= 2) return factors;

  // 3. Si no venía factorizado, comprobar si es un trinomio cuadrático s^2 + bs + c factorizable (discr > 0)
  const quad = parseQuadraticDenominator(denom);
  if (quad && quad.discr > 0) {
    const sqrtD = Math.sqrt(quad.discr);
    const r1 = (-quad.b + sqrtD) / 2;
    const r2 = (-quad.b - sqrtD) / 2;
    return [
      { root: r1, raw: `(s ${r1 < 0 ? '+ ' + Math.abs(r1) : '- ' + r1})` },
      { root: r2, raw: `(s ${r2 < 0 ? '+ ' + Math.abs(r2) : '- ' + r2})` }
    ];
  }

  return null;
}

/**
 * Evalúa un polinomio simple P(s) = M*s + N en s = r
 */
function evaluatePolynomial(polyStr, r) {
  const { M, N } = parseLinearNumerator(polyStr);
  return M * r + N;
}

function factorial(n) {
  if (n <= 1) return 1;
  let res = 1;
  for (let i = 2; i <= n; i++) res *= i;
  return res;
}

function isNumeric(val) {
  return !isNaN(parseFloat(val)) && isFinite(val);
}

function substituteVariable(expr, varName, replacement) {
  const regex = new RegExp(`\\b${varName}\\b`, 'g');
  return expr.replace(regex, replacement);
}

// ==========================================================================
// 5. GRÁFICAS INTERACTIVAS CON CHART.JS
// ==========================================================================

/**
 * Grafica la función temporal F(t) en el rango configurado.
 */
function plotFunction(funcExpr, tMin = 0, tMax = 10, step = 0.05) {
  const canvas = document.getElementById('laplaceChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  // Preparar evaluador de math.js
  let compiledFunc = null;
  try {
    if (window.math) {
      // Normalizar para evaluación
      const evalExpr = funcExpr
        .replace(/\\cdot/g, '*')
        .replace(/e\^\{([^}]+)\}/g, 'exp($1)')
        .replace(/\\sin/g, 'sin')
        .replace(/\\cos/g, 'cos')
        .replace(/\\pi/g, 'pi');
      compiledFunc = window.math.compile(evalExpr);
    }
  } catch (e) {
    console.warn('No se pudo compilar la función para graficar:', e);
  }

  const labels = [];
  const dataPoints = [];

  const pointsCount = Math.min(400, Math.max(50, Math.floor((tMax - tMin) / step)));
  const actualStep = (tMax - tMin) / pointsCount;

  for (let i = 0; i <= pointsCount; i++) {
    const tVal = tMin + i * actualStep;
    labels.push(tVal.toFixed(2));

    let yVal = null;
    if (compiledFunc) {
      try {
        const val = compiledFunc.evaluate({ t: tVal });
        if (typeof val === 'number' && isFinite(val) && !isNaN(val)) {
          yVal = Math.max(-100, Math.min(100, val)); // Clamping para asíntotas
        }
      } catch (err) {
        yVal = null;
      }
    }
    dataPoints.push(yVal);
  }

  // Destruir instancia previa
  if (AppState.chartInstance) {
    AppState.chartInstance.destroy();
  }

  const isDark = AppState.theme === 'dark';
  const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';
  const textColor = isDark ? '#94a3b8' : '#64748b';
  const lineColor = '#6366f1';

  AppState.chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'F(t)',
        data: dataPoints,
        borderColor: lineColor,
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: '#6366f1',
        pointHoverBorderColor: '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          display: true,
          labels: {
            color: textColor,
            font: { family: 'Inter', weight: 600 }
          }
        },
        tooltip: {
          backgroundColor: isDark ? '#1e293b' : '#ffffff',
          titleColor: isDark ? '#f8fafc' : '#0f172a',
          bodyColor: isDark ? '#94a3b8' : '#475569',
          borderColor: isDark ? '#334155' : '#e2e8f0',
          borderWidth: 1,
          padding: 10,
          displayColors: false,
          callbacks: {
            label: (context) => `F(t) = ${context.parsed.y !== null ? context.parsed.y.toFixed(4) : 'Indefinido'}`
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Tiempo t (segundos)',
            color: textColor,
            font: { weight: 600 }
          },
          grid: { color: gridColor },
          ticks: { color: textColor, maxTicksLimit: 12 }
        },
        y: {
          title: {
            display: true,
            text: 'Amplitud F(t)',
            color: textColor,
            font: { weight: 600 }
          },
          grid: { color: gridColor },
          ticks: { color: textColor }
        }
      }
    }
  });
}

// ==========================================================================
// 6. CONTROLADOR DE HISTORIAL EN LOCALSTORAGE
// ==========================================================================

function saveHistoryItem(item) {
  const entry = {
    id: Date.now(),
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    type: item.type, // 'laplace' | 'inverse'
    input: item.input,
    resultLatex: item.resultLatex,
    method: item.method
  };

  AppState.history.unshift(entry);
  if (AppState.history.length > 50) AppState.history.pop();
  localStorage.setItem('laplace_history', JSON.stringify(AppState.history));
  renderHistoryView();
  updateHistoryBadge();
}

function renderHistoryView() {
  const container = document.getElementById('historyList');
  if (!container) return;

  if (AppState.history.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">🕘</div>
        <p>No hay operaciones en el historial todavía.</p>
        <span style="font-size: 0.85rem; color: var(--text-dim);">Tus cálculos recientes aparecerán aquí automáticamente.</span>
      </div>
    `;
    return;
  }

  container.innerHTML = '';
  AppState.history.forEach(item => {
    const div = document.createElement('div');
    div.className = 'history-item';
    const isLaplace = item.type === 'laplace';

    div.innerHTML = `
      <div style="flex: 1; min-width: 260px;">
        <div class="history-meta">
          <span class="history-badge ${isLaplace ? 'laplace' : 'inverse'}">
            ${isLaplace ? 'Transformada' : 'Antitransformada'}
          </span>
          <span class="history-timestamp">${item.timestamp}</span>
          <span style="font-size: 0.78rem; color: var(--text-dim);">${item.method || ''}</span>
        </div>
        <div class="history-equation">
          <strong>${isLaplace ? 'F(t)' : 'F(s)'} = </strong> <code>${item.input}</code>
          <span style="margin: 0 8px; color: var(--text-dim);">→</span>
          <span id="hist_res_${item.id}"></span>
        </div>
      </div>
      <div class="history-actions">
        <button class="history-action-btn" onclick="reuseHistoryItem(${item.id})">Reutilizar</button>
        <button class="history-action-btn history-delete-btn" onclick="deleteHistoryItem(${item.id})">Eliminar</button>
      </div>
    `;
    container.appendChild(div);

    renderLatex(`hist_res_${item.id}`, item.resultLatex, false);
  });
}

function reuseHistoryItem(id) {
  const item = AppState.history.find(h => h.id === id);
  if (!item) return;

  switchMode(item.type);
  switchView('calculator');

  const inputEl = document.getElementById('mathExpressionInput');
  if (inputEl) {
    inputEl.value = item.input;
    updateLivePreview(item.input);
    executeCalculation();
  }
}

function deleteHistoryItem(id) {
  AppState.history = AppState.history.filter(h => h.id !== id);
  localStorage.setItem('laplace_history', JSON.stringify(AppState.history));
  renderHistoryView();
  updateHistoryBadge();
}

function clearAllHistory() {
  if (confirm('¿Estás seguro de que deseas vaciar todo el historial?')) {
    AppState.history = [];
    localStorage.removeItem('laplace_history');
    renderHistoryView();
    updateHistoryBadge();
  }
}

function updateHistoryBadge() {
  const badge = document.getElementById('historyCountBadge');
  if (badge) {
    badge.textContent = AppState.history.length.toString();
  }
}

// ==========================================================================
// 7. TABLA INTERACTIVA DE FÓRMULAS
// ==========================================================================

const FormulasDatabase = [
  { cat: 'basicas', f_t: '1', F_s: '\\frac{1}{s}', prop: 'Constante', ex: 'ℒ{1} = 1/s' },
  { cat: 'basicas', f_t: 't', F_s: '\\frac{1}{s^2}', prop: 'Potencia lineal', ex: 'ℒ{t} = 1/s²' },
  { cat: 'polinomios', f_t: 't^n', F_s: '\\frac{n!}{s^{n+1}}', prop: 'Potencias de t', ex: 'ℒ{t³} = 6/s⁴' },
  { cat: 'basicas', f_t: 'e^{at}', F_s: '\\frac{1}{s - a}', prop: 'Exponencial', ex: 'ℒ{e^{-2t}} = 1/(s+2)' },
  { cat: 'trig', f_t: '\\sin(\\omega t)', F_s: '\\frac{\\omega}{s^2 + \\omega^2}', prop: 'Seno', ex: 'ℒ{sin(3t)} = 3/(s²+9)' },
  { cat: 'trig', f_t: '\\cos(\\omega t)', F_s: '\\frac{s}{s^2 + \\omega^2}', prop: 'Coseno', ex: 'ℒ{cos(4t)} = s/(s²+16)' },
  { cat: 'hiper', f_t: '\\sinh(at)', F_s: '\\frac{a}{s^2 - a^2}', prop: 'Seno hiperbólico', ex: 'ℒ{sinh(2t)} = 2/(s²-4)' },
  { cat: 'hiper', f_t: '\\cosh(at)', F_s: '\\frac{s}{s^2 - a^2}', prop: 'Coseno hiperbólico', ex: 'ℒ{cosh(2t)} = s/(s²-4)' },
  { cat: 'propiedades', f_t: 'e^{at} f(t)', F_s: 'F(s - a)', prop: 'Primer Teorema de Traslación', ex: 'ℒ{e^{2t}sin(3t)} = 3/((s-2)²+9)' },
  { cat: 'propiedades', f_t: 't f(t)', F_s: '-\\frac{d}{ds}[F(s)]', prop: 'Multiplicación por t', ex: 'ℒ{t sin(2t)} = 4s/(s²+4)²' },
  { cat: 'propiedades', f_t: 'f\'(t)', F_s: 's F(s) - f(0)', prop: 'Primera Derivada', ex: 'Condiciones iniciales' },
  { cat: 'propiedades', f_t: 'f\'\'(t)', F_s: 's^2 F(s) - s f(0) - f\'(0)', prop: 'Segunda Derivada', ex: 'EDOs lineales' },
  { cat: 'propiedades', f_t: '\\int_0^t f(u) du', F_s: '\\frac{F(s)}{s}', prop: 'Integral en el tiempo', ex: 'ℒ{∫ sin(u)du} = 1/(s(s²+1))' }
];

function renderFormulasTable(filterText = '', category = 'todas') {
  const tbody = document.getElementById('formulasTableBody');
  if (!tbody) return;

  tbody.innerHTML = '';
  const search = filterText.toLowerCase().trim();

  const filtered = FormulasDatabase.filter(item => {
    const matchCat = category === 'todas' || item.cat === category;
    const matchSearch = !search || 
      item.f_t.toLowerCase().includes(search) || 
      item.prop.toLowerCase().includes(search) || 
      item.ex.toLowerCase().includes(search);
    return matchCat && matchSearch;
  });

  filtered.forEach((f, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="formula-render-cell" id="f_t_${idx}"></td>
      <td class="formula-render-cell" id="F_s_${idx}"></td>
      <td><strong>${f.prop}</strong></td>
      <td><code>${f.ex}</code></td>
      <td>
        <button class="formula-load-btn" onclick="loadFormulaToCalc('${f.ex.replace(/['"]/g, '')}')">Cargar</button>
      </td>
    `;
    tbody.appendChild(tr);

    renderLatex(`f_t_${idx}`, f.f_t, false);
    renderLatex(`F_s_${idx}`, f.F_s, false);
  });
}

function loadFormulaToCalc(exText) {
  // Extraer el argumento de ℒ{...}
  const match = exText.match(/ℒ\{([^}]+)\}/);
  const val = match ? match[1].trim() : 'sin(2*t)';
  
  switchMode('laplace');
  switchView('calculator');

  const inputEl = document.getElementById('mathExpressionInput');
  if (inputEl) {
    inputEl.value = val;
    updateLivePreview(val);
    executeCalculation();
  }
}

// ==========================================================================
// 8. CONTROLADOR DE INTERFAZ DE USUARIO Y EVENTOS
// ==========================================================================

function switchMode(mode) {
  AppState.currentMode = mode;
  const isLaplace = mode === 'laplace';

  document.getElementById('tabLaplace').classList.toggle('active', isLaplace);
  document.getElementById('tabInverse').classList.toggle('active', !isLaplace);

  const titleEl = document.getElementById('calcInputLabel');
  const placeholderEl = document.getElementById('mathExpressionInput');
  const calcBtnText = document.getElementById('calcButtonText');

  if (isLaplace) {
    titleEl.textContent = 'Función en el tiempo F(t)';
    placeholderEl.placeholder = 'Ejemplos: sin(2*t), e^(-2*t), t^2, exp(2*t)*sin(3*t)...';
    calcBtnText.textContent = 'CALCULAR TRANSFORMADA';
  } else {
    titleEl.textContent = 'Función en el dominio s F(s)';
    placeholderEl.placeholder = 'Ejemplos: 1/(s+2), 1/(s^2+4), (2*s+3)/(s^2+4*s+13), (3*s+5)/((s+1)*(s+2))...';
    calcBtnText.textContent = 'CALCULAR ANTITRANSFORMADA';
  }

  // Limpiar resultados anteriores
  document.getElementById('resultContainer').classList.remove('active');
  document.getElementById('errorCard').classList.remove('active');
  updateLivePreview(placeholderEl.value);
}

function switchView(viewName) {
  AppState.currentView = viewName;

  document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));

  const targetView = document.getElementById(`view-${viewName}`);
  const targetNav = document.getElementById(`nav-${viewName}`);

  if (targetView) targetView.classList.add('active');
  if (targetNav) targetNav.classList.add('active');

  // Si cambiamos de vista en móvil, cerrar sidebar
  closeMobileSidebar();
}

function updateLivePreview(text) {
  const previewRender = document.getElementById('inputPreviewRender');
  if (!previewRender) return;

  if (!text || text.trim() === '') {
    previewRender.innerHTML = '<span style="color: var(--text-dim); font-size: 0.95rem;">Esperando entrada...</span>';
    return;
  }

  try {
    const norm = normalizeExpression(text, AppState.currentMode === 'laplace' ? 't' : 's');
    const lx = exprToLatex(norm);
    renderLatex(previewRender, lx, false);
  } catch (e) {
    previewRender.textContent = text;
  }
}

function insertSymbol(symbol) {
  const input = document.getElementById('mathExpressionInput');
  if (!input) return;

  const start = input.selectionStart;
  const end = input.selectionEnd;
  const oldVal = input.value;

  input.value = oldVal.substring(0, start) + symbol + oldVal.substring(end);
  input.focus();
  input.selectionStart = input.selectionEnd = start + symbol.length;

  updateLivePreview(input.value);
}

function clearCalculator() {
  const input = document.getElementById('mathExpressionInput');
  if (input) input.value = '';
  document.getElementById('resultContainer').classList.remove('active');
  document.getElementById('errorCard').classList.remove('active');
  updateLivePreview('');
}

function copyResultToClipboard() {
  if (!AppState.lastResult || !AppState.lastResult.finalLatex) return;

  const textToCopy = AppState.lastResult.finalExpr || AppState.lastResult.finalLatex;
  navigator.clipboard.writeText(textToCopy).then(() => {
    const toast = document.getElementById('copyToast');
    if (toast) {
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2500);
    }
  }).catch(err => {
    console.error('Error al copiar:', err);
  });
}

/**
 * Ejecuta el cálculo principal con animación de análisis y renderizado completo.
 */
function executeCalculation() {
  const inputEl = document.getElementById('mathExpressionInput');
  const val = inputEl ? inputEl.value.trim() : '';

  const progressCard = document.getElementById('analysisProgressCard');
  const resultContainer = document.getElementById('resultContainer');
  const errorCard = document.getElementById('errorCard');

  // Ocultar resultados previos
  resultContainer.classList.remove('active');
  errorCard.classList.remove('active');

  // Validar
  const check = validateInput(val);
  if (!check.valid) {
    showError(check.error);
    return;
  }

  // Mostrar animación de análisis progresivo (Requisito 27)
  progressCard.classList.add('active');
  const step1 = document.getElementById('progStep1');
  const step2 = document.getElementById('progStep2');
  const step3 = document.getElementById('progStep3');

  step1.className = 'progress-step-item';
  step2.className = 'progress-step-item';
  step3.className = 'progress-step-item';

  setTimeout(() => {
    step1.className = 'progress-step-item done';
  }, 120);

  setTimeout(() => {
    step2.className = 'progress-step-item done';
  }, 320);

  setTimeout(() => {
    step3.className = 'progress-step-item done';

    try {
      let result = null;
      if (AppState.currentMode === 'laplace') {
        result = calculateLaplace(val);
      } else {
        result = calculateInverseLaplace(val);
      }

      AppState.lastResult = result;
      progressCard.classList.remove('active');

      displayResult(result);
      saveHistoryItem({
        type: AppState.currentMode,
        input: val,
        resultLatex: result.finalLatex,
        method: result.method
      });
    } catch (err) {
      progressCard.classList.remove('active');
      showError(err.message || '⚠️ No se pudo interpretar la expresión. Verifica que hayas escrito correctamente los paréntesis y operadores.');
    }
  }, 500);
}

function showError(msg) {
  const errorCard = document.getElementById('errorCard');
  const errorMsg = document.getElementById('errorMessageText');
  if (errorCard && errorMsg) {
    errorMsg.textContent = msg;
    errorCard.classList.add('active');
  }
}

function displayResult(result) {
  const resultContainer = document.getElementById('resultContainer');
  resultContainer.classList.add('active');

  // 1. Tarjeta Grande de Resultado
  const isLaplace = AppState.currentMode === 'laplace';
  const labelPrefix = isLaplace ? 'F(s) =' : 'f(t) =';
  const finalFormulaEl = document.getElementById('finalFormulaRender');
  
  const fullLatex = `${labelPrefix} ${result.finalLatex}`;
  renderLatex(finalFormulaEl, fullLatex, true);

  // 2. Sección Desarrollo Paso a Paso
  const stepsContainer = document.getElementById('stepsContainer');
  stepsContainer.innerHTML = '';

  result.steps.forEach((step, idx) => {
    const card = document.createElement('div');
    card.className = 'step-card';
    card.innerHTML = `
      <div class="step-header">
        <div class="step-number">${idx + 1}</div>
        <div class="step-title">${step.title}</div>
        <div class="step-property-tag">${step.property || 'Propiedad'}</div>
      </div>
      <div class="step-description">${step.description}</div>
      ${step.formula ? `<div class="step-formula-box" id="step_formula_${idx}"></div>` : ''}
    `;
    stepsContainer.appendChild(card);

    if (step.formula) {
      renderLatex(`step_formula_${idx}`, step.formula, true);
    }
  });

  // 3. Gráfica en Chart.js
  // Si estamos en antitransformada, graficamos el resultado f(t).
  // Si estamos en directa, graficamos la entrada f(t).
  const graphExpr = isLaplace ? result.input : result.finalExpr;
  plotFunction(graphExpr, AppState.tMin, AppState.tMax, AppState.tStep);
}

// ==========================================================================
// 9. MODO OSCURO Y TEMA
// ==========================================================================

function toggleTheme() {
  const newTheme = AppState.theme === 'dark' ? 'light' : 'dark';
  applyTheme(newTheme);
}

function applyTheme(theme) {
  AppState.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('laplace_theme', theme);

  const btnText = document.getElementById('themeToggleText');
  const btnIcon = document.getElementById('themeToggleIcon');
  if (btnText && btnIcon) {
    if (theme === 'dark') {
      btnText.textContent = 'Modo claro';
      btnIcon.textContent = '☀️';
    } else {
      btnText.textContent = 'Modo oscuro';
      btnIcon.textContent = '🌙';
    }
  }

  // Re-renderizar gráfica con nuevos colores de cuadrícula
  if (AppState.lastResult) {
    const isLaplace = AppState.currentMode === 'laplace';
    const graphExpr = isLaplace ? AppState.lastResult.input : AppState.lastResult.finalExpr;
    plotFunction(graphExpr, AppState.tMin, AppState.tMax, AppState.tStep);
  }
}

// ==========================================================================
// 10. GESTIÓN MÓVIL Y RESPONSIVE
// ==========================================================================

function toggleMobileSidebar() {
  const sidebar = document.getElementById('appSidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

function closeMobileSidebar() {
  const sidebar = document.getElementById('appSidebar');
  if (sidebar) sidebar.classList.remove('open');
}

// ==========================================================================
// 11. INICIALIZACIÓN DE LA APLICACIÓN
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // Aplicar tema guardado
  applyTheme(AppState.theme);

  // Cargar historial inicial
  renderHistoryView();
  updateHistoryBadge();

  // Renderizar tabla de fórmulas
  renderFormulasTable();

  // Escuchar entrada en tiempo real
  const mathInput = document.getElementById('mathExpressionInput');
  if (mathInput) {
    updateLivePreview(mathInput.value);

    mathInput.addEventListener('input', (e) => {
      updateLivePreview(e.target.value);
    });

    mathInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        executeCalculation();
      }
    });
  }

  // Controles de gráfica
  const tMinInput = document.getElementById('graphTMin');
  const tMaxInput = document.getElementById('graphTMax');
  if (tMinInput && tMaxInput) {
    const updateGraphRange = () => {
      AppState.tMin = parseFloat(tMinInput.value) || 0;
      AppState.tMax = parseFloat(tMaxInput.value) || 10;
      if (AppState.lastResult) {
        const isLaplace = AppState.currentMode === 'laplace';
        const graphExpr = isLaplace ? AppState.lastResult.input : AppState.lastResult.finalExpr;
        plotFunction(graphExpr, AppState.tMin, AppState.tMax, AppState.tStep);
      }
    };
    tMinInput.addEventListener('change', updateGraphRange);
    tMaxInput.addEventListener('change', updateGraphRange);
  }

  // Búsqueda en tabla de fórmulas
  const formulaSearch = document.getElementById('formulaSearchInput');
  if (formulaSearch) {
    formulaSearch.addEventListener('input', (e) => {
      renderFormulasTable(e.target.value);
    });
  }

  // Filtros de categoría de fórmulas
  document.querySelectorAll('.filter-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const cat = chip.getAttribute('data-cat') || 'todas';
      renderFormulasTable(formulaSearch ? formulaSearch.value : '', cat);
    });
  });

  // Renderizar ejemplos de la galería
  renderExamplesGallery();
});

// Función para cargar ejemplos predefinidos (Requisitos 17 y 30)
function loadPredefinedExample(type, expr) {
  switchMode(type);
  switchView('calculator');

  const inputEl = document.getElementById('mathExpressionInput');
  if (inputEl) {
    inputEl.value = expr;
    updateLivePreview(expr);
    executeCalculation();
  }
}

function renderExamplesGallery() {
  const container = document.getElementById('examplesGalleryContainer');
  if (!container) return;

  const examples = [
    { type: 'laplace', expr: 'e^(-2*t)', title: 'Prueba 1: Exponencial básica', desc: 'Transformada directa de una exponencial decayente. Verifica cálculo de polo en s = -2.' },
    { type: 'inverse', expr: '1/(s^2+4)', title: 'Prueba 2: Función Senoidal', desc: 'Antitransformada inmediata con polo complejo conjugado ±2j. Reconoce forma seno.' },
    { type: 'laplace', expr: 'e^(a*t)', title: 'Prueba 3: Parámetro Simbólico', desc: 'Transformada con constante simbólica a. Genera 1/(s - a) de forma general.' },
    { type: 'laplace', expr: 't^2', title: 'Prueba 4: Potencia cuadrática', desc: 'Propiedad t^n con n = 2. Calcula factorial 2! / s³.' },
    { type: 'inverse', expr: '(2*s+3)/((s+1)*(s+2))', title: 'Prueba 5: Fracciones Parciales Heaviside', desc: 'Factores lineales distintos. Descompone por método de encubrimiento en e^(-t) + e^(-2t).' },
    { type: 'inverse', expr: '(2*s+3)/(s^2+4*s+13)', title: 'Prueba Avanzada: Completación de Cuadrados', desc: 'Trinomio irreducible. Completa (s+2)² + 3² y separa en coseno y seno amortiguados.' },
    { type: 'laplace', expr: 't*sin(2*t)', title: 'Prueba Avanzada: Multiplicación por t', desc: 'Aplica teorema de derivada en s: -d/ds[2/(s²+4)].' },
    { type: 'laplace', expr: '3*t^3 + 2*t', title: 'Linealidad polinomial', desc: 'Suma de dos potencias evaluadas independientemente.' }
  ];

  container.innerHTML = '';
  examples.forEach(ex => {
    const card = document.createElement('div');
    card.className = 'example-card';
    card.innerHTML = `
      <div class="example-card-header">
        <span class="example-tag">${ex.type === 'laplace' ? 'Transformada F(t)' : 'Antitransformada F(s)'}</span>
      </div>
      <h4 style="font-size: 1rem; font-weight: 700; margin-bottom: 6px;">${ex.title}</h4>
      <div class="example-input-render"><code>${ex.expr}</code></div>
      <p class="example-desc">${ex.desc}</p>
      <button class="example-try-btn" onclick="loadPredefinedExample('${ex.type}', '${ex.expr}')">Cargar y Resolver</button>
    `;
    container.appendChild(card);
  });
}

// Hacer funciones globales accesibles para onclick en HTML
window.switchMode = switchMode;
window.switchView = switchView;
window.insertSymbol = insertSymbol;
window.clearCalculator = clearCalculator;
window.copyResultToClipboard = copyResultToClipboard;
window.executeCalculation = executeCalculation;
window.toggleTheme = toggleTheme;
window.toggleMobileSidebar = toggleMobileSidebar;
window.reuseHistoryItem = reuseHistoryItem;
window.deleteHistoryItem = deleteHistoryItem;
window.clearAllHistory = clearAllHistory;
window.loadFormulaToCalc = loadFormulaToCalc;
window.loadPredefinedExample = loadPredefinedExample;
