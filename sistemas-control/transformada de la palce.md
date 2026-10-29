%% ========================================================================
%  PROGRAMA: TRANSFORMADA DE LAPLACE - EJERCICIOS DEL PDF
%  MATERIA: Fundamentos Matemáticos de Sistemas de Control
% =========================================================================

clear; clc; close all;
syms t s a real  % Definimos variables simbólicas incluyendo 'a'

%% =========================================================================
%  SECCIÓN 2: TABLA DE TRANSFORMADA DE LAPLACE
% =========================================================================

fprintf('============================================================\n');
fprintf('  SECCIÓN 2: TRANSFORMADA DE LAPLACE - EJEMPLOS DIRECTOS\n');
fprintf('============================================================\n\n');

%% EJEMPLO a) F(t) = 8
fprintf('--- Ejemplo a) F(t) = 8 ---\n');
F_a = 8;
L_a = laplace(F_a, t, s);
fprintf('F(t) = %s\n', char(F_a));
fprintf('L{F(t)} = %s\n\n', char(L_a));

%% EJEMPLO b) F(t) = t^5
fprintf('--- Ejemplo b) F(t) = t^5 ---\n');
F_b = t^5;
L_b = laplace(F_b, t, s);
fprintf('F(t) = %s\n', char(F_b));
fprintf('L{F(t)} = %s\n\n', char(L_b));

%% EJEMPLO c) F(t) = t^13
fprintf('--- Ejemplo c) F(t) = t^13 ---\n');
F_c = t^13;
L_c = laplace(F_c, t, s);
fprintf('F(t) = %s\n', char(F_c));
fprintf('L{F(t)} = %s\n\n', char(L_c));

%% EJEMPLO d) F(t) = e^(4t)
fprintf('--- Ejemplo d) F(t) = e^(4t) ---\n');
F_d = exp(4*t);
L_d = laplace(F_d, t, s);
fprintf('F(t) = %s\n', char(F_d));
fprintf('L{F(t)} = %s\n\n', char(L_d));

%% EJEMPLO e) F(t) = e^(-8t)
fprintf('--- Ejemplo e) F(t) = e^(-8t) ---\n');
F_e = exp(-8*t);
L_e = laplace(F_e, t, s);
fprintf('F(t) = %s\n', char(F_e));
fprintf('L{F(t)} = %s\n\n', char(L_e));

%% EJEMPLO f) F(t) = sin(10t)
fprintf('--- Ejemplo f) F(t) = sin(10t) ---\n');
F_f = sin(10*t);
L_f = laplace(F_f, t, s);
fprintf('F(t) = %s\n', char(F_f));
fprintf('L{F(t)} = %s\n\n', char(L_f));

%% EJEMPLO g) F(t) = cos(7t)
fprintf('--- Ejemplo g) F(t) = cos(7t) ---\n');
F_g = cos(7*t);
L_g = laplace(F_g, t, s);
fprintf('F(t) = %s\n', char(F_g));
fprintf('L{F(t)} = %s\n\n', char(L_g));

%% EJEMPLO h) F(t) = sinh(10t)
fprintf('--- Ejemplo h) F(t) = sinh(10t) ---\n');
F_h = sinh(10*t);
L_h = laplace(F_h, t, s);
fprintf('F(t) = %s\n', char(F_h));
fprintf('L{F(t)} = %s\n\n', char(L_h));

%% =========================================================================
%  SECCIÓN 3.1: PROPIEDAD DE LINEALIDAD
% =========================================================================

fprintf('============================================================\n');
fprintf('  SECCIÓN 3.1: PROPIEDAD DE LINEALIDAD\n');
fprintf('============================================================\n\n');

%% Ejemplo: F(t) = 8e^(-7t) - 5cos(t) + 4
fprintf('--- Ejemplo de linealidad ---\n');
fprintf('F(t) = 8e^(-7t) - 5cos(t) + 4\n');
F_lineal = 8*exp(-7*t) - 5*cos(t) + 4;
L_lineal = laplace(F_lineal, t, s);
fprintf('L{F(t)} = %s\n\n', char(L_lineal));

%% =========================================================================
%  SECCIÓN 3.2: PRIMERA PROPIEDAD DE TRASLACIÓN
% =========================================================================

fprintf('============================================================\n');
fprintf('  SECCIÓN 3.2: PRIMERA PROPIEDAD DE TRASLACIÓN\n');
fprintf('  L{e^(at)F(t)} = f(s-a)\n');
fprintf('============================================================\n\n');

%% Ejemplo 1: G(t) = e^(8t) * t^5
fprintf('--- Ejemplo 1: G(t) = e^(8t) * t^5 ---\n');
G1 = exp(8*t) * t^5;
L_G1 = laplace(G1, t, s);
fprintf('G(t) = %s\n', char(G1));
fprintf('L{G(t)} = %s\n\n', char(L_G1));

%% Ejemplo 2: G(t) = 8e^(-2t) * sin(3t)
fprintf('--- Ejemplo 2: G(t) = 8e^(-2t) * sin(3t) ---\n');
G2 = 8*exp(-2*t)*sin(3*t);
L_G2 = laplace(G2, t, s);
fprintf('G(t) = %s\n', char(G2));
fprintf('L{G(t)} = %s\n\n', char(L_G2));

%% Ejemplo 3: G(t) = (8e^(-7t) - 5cos(t) + 4) * e^(-2t)
fprintf('--- Ejemplo 3: G(t) = (8e^(-7t) - 5cos(t) + 4) * e^(-2t) ---\n');
G3 = (8*exp(-7*t) - 5*cos(t) + 4)*exp(-2*t);
L_G3 = laplace(G3, t, s);
fprintf('G(t) = %s\n', char(G3));
fprintf('L{G(t)} = %s\n\n', char(L_G3));

%% =========================================================================
%  SECCIÓN 3.3: TRANSFORMADA DE LA MULTIPLICACIÓN POR t^n
% =========================================================================

fprintf('============================================================\n');
fprintf('  SECCIÓN 3.3: TRANSFORMADA DE t^n * F(t)\n');
fprintf('  L{t^n F(t)} = (-1)^n * d^n/ds^n [f(s)]\n');
fprintf('============================================================\n\n');

%% Ejemplo: F(t) = t^3 * e^(4t)
fprintf('--- Ejemplo: F(t) = t^3 * e^(4t) ---\n');
F_tn = t^3 * exp(4*t);
L_tn = laplace(F_tn, t, s);
fprintf('F(t) = %s\n', char(F_tn));
fprintf('L{F(t)} = %s\n\n', char(L_tn));

%% =========================================================================
%  SECCIÓN 3.4: TRANSFORMADA DE LA DERIVADA
% =========================================================================

fprintf('============================================================\n');
fprintf('  SECCIÓN 3.4: TRANSFORMADA DE LA DERIVADA\n');
fprintf('  L{F''(t)} = s*f(s) - F(0)\n');
fprintf('============================================================\n\n');

%% Ejemplo 1: dF/dt - 3F = e^(2t), F(0) = 1
fprintf('--- Ejemplo 1: dF/dt - 3F = e^(2t), F(0) = 1 ---\n');
syms F_s
eq1 = s*F_s - 1 - 3*F_s == 1/(s-2);
sol1 = solve(eq1, F_s);
fprintf('f(s) = %s\n\n', char(sol1));

%% Ejemplo 2: 4F''(t) + F(t) = -2, F(0)=0, F'(0)=1/2
fprintf('--- Ejemplo 2: 4F''''(t) + F(t) = -2, F(0)=0, F''(0)=1/2 ---\n');
eq2 = 4*(s^2*F_s - s*0 - 1/2) + F_s == -2/s;
sol2 = solve(eq2, F_s);
fprintf('f(s) = %s\n\n', char(sol2));

%% =========================================================================
%  SECCIÓN 3.5: TRANSFORMADA DE UNA INTEGRAL (CORREGIDO)
% =========================================================================

fprintf('============================================================\n');
fprintf('  SECCIÓN 3.5: TRANSFORMADA DE UNA INTEGRAL\n');
fprintf('  L{∫₀ᵗ F(u) du} = f(s)/s\n');
fprintf('============================================================\n\n');

%% Ejemplo: ∫₀ᵗ u*e^(a*u)*sin(u) du
fprintf('--- Ejemplo: ∫₀ᵗ u*e^(a*u)*sin(u) du ---\n');
% Definimos 'a' como símbolo real (ya está definida al inicio)
F_int = t * exp(a*t) * sin(t);
L_int_interna = laplace(F_int, t, s);
L_int_final = L_int_interna / s;
fprintf('F(t) = t*e^(a*t)*sin(t)\n');
fprintf('L{∫₀ᵗ F(u) du} = %s\n\n', char(L_int_final));

%% =========================================================================
%  SECCIÓN 4: EJERCICIOS DE PRÁCTICA (Página 12)
% =========================================================================

fprintf('============================================================\n');
fprintf('  SECCIÓN 4: EJERCICIOS DE PRÁCTICA\n');
fprintf('  Hallar la función en el dominio de la frecuencia\n');
fprintf('============================================================\n\n');

%% Ejercicio a) F(t) = 5 + 3t - t^2
fprintf('--- Ejercicio a) F(t) = 5 + 3t - t^2 ---\n');
F_prac_a = 5 + 3*t - t^2;
L_prac_a = laplace(F_prac_a, t, s);
fprintf('F(t) = %s\n', char(F_prac_a));
fprintf('L{F(t)} = %s\n\n', char(L_prac_a));

%% Ejercicio b) F(t) = (e^t + e^(-t))^2
fprintf('--- Ejercicio b) F(t) = (e^t + e^(-t))^2 ---\n');
F_prac_b = (exp(t) + exp(-t))^2;
L_prac_b = laplace(F_prac_b, t, s);
fprintf('F(t) = %s\n', char(F_prac_b));
fprintf('L{F(t)} = %s\n\n', char(L_prac_b));

%% Ejercicio c) F(t) = e^(2t) * cos(10t)
fprintf('--- Ejercicio c) F(t) = e^(2t) * cos(10t) ---\n');
F_prac_c = exp(2*t) * cos(10*t);
L_prac_c = laplace(F_prac_c, t, s);
fprintf('F(t) = %s\n', char(F_prac_c));
fprintf('L{F(t)} = %s\n\n', char(L_prac_c));

%% Ejercicio d) F(t) = t^2 * sin(8t)
fprintf('--- Ejercicio d) F(t) = t^2 * sin(8t) ---\n');
F_prac_d = t^2 * sin(8*t);
L_prac_d = laplace(F_prac_d, t, s);
fprintf('F(t) = %s\n', char(F_prac_d));
fprintf('L{F(t)} = %s\n\n', char(L_prac_d));

%% Ejercicio e) F(t) = t * e^t * cos(t)
fprintf('--- Ejercicio e) F(t) = t * e^t * cos(t) ---\n');
F_prac_e = t * exp(t) * cos(t);
L_prac_e = laplace(F_prac_e, t, s);
fprintf('F(t) = %s\n', char(F_prac_e));
fprintf('L{F(t)} = %s\n\n', char(L_prac_e));

%% =========================================================================
%  RESUMEN FINAL
% =========================================================================

fprintf('============================================================\n');
fprintf('  PROGRAMA COMPLETADO EXITOSAMENTE\n');
fprintf('============================================================\n');
# resultado en matlab
============================================================
  SECCIÓN 2: TRANSFORMADA DE LAPLACE - EJEMPLOS DIRECTOS
============================================================

--- Ejemplo a) F(t) = 8 ---
F(t) =
L{F(t)} = 8/s

--- Ejemplo b) F(t) = t^5 ---
F(t) = t^5
L{F(t)} = 120/s^6

--- Ejemplo c) F(t) = t^13 ---
F(t) = t^13
L{F(t)} = 6227020800/s^14

--- Ejemplo d) F(t) = e^(4t) ---
F(t) = exp(4*t)
L{F(t)} = 1/(s - 4)

--- Ejemplo e) F(t) = e^(-8t) ---
F(t) = exp(-8*t)
L{F(t)} = 1/(s + 8)

--- Ejemplo f) F(t) = sin(10t) ---
F(t) = sin(10*t)
L{F(t)} = 10/(s^2 + 100)

--- Ejemplo g) F(t) = cos(7t) ---
F(t) = cos(7*t)
L{F(t)} = s/(s^2 + 49)

--- Ejemplo h) F(t) = sinh(10t) ---
F(t) = sinh(10*t)
L{F(t)} = 10/(s^2 - 100)

============================================================
  SECCIÓN 3.1: PROPIEDAD DE LINEALIDAD
============================================================

--- Ejemplo de linealidad ---
F(t) = 8e^(-7t) - 5cos(t) + 4
L{F(t)} = 8/(s + 7) - (5*s)/(s^2 + 1) + 4/s

============================================================
  SECCIÓN 3.2: PRIMERA PROPIEDAD DE TRASLACIÓN
  L{e^(at)F(t)} = f(s-a)
============================================================

--- Ejemplo 1: G(t) = e^(8t) * t^5 ---
G(t) = t^5*exp(8*t)
L{G(t)} = 120/(s - 8)^6

--- Ejemplo 2: G(t) = 8e^(-2t) * sin(3t) ---
G(t) = 8*sin(3*t)*exp(-2*t)
L{G(t)} = 24/((s + 2)^2 + 9)

--- Ejemplo 3: G(t) = (8e^(-7t) - 5cos(t) + 4) * e^(-2t) ---
G(t) = exp(-2*t)*(8*exp(-7*t) - 5*cos(t) + 4)
L{G(t)} = 4/(s + 2) - (5*(s + 2))/((s + 2)^2 + 1) + 8/(s + 9)

============================================================
  SECCIÓN 3.3: TRANSFORMADA DE t^n * F(t)
  L{t^n F(t)} = (-1)^n * d^n/ds^n [f(s)]
============================================================

--- Ejemplo: F(t) = t^3 * e^(4t) ---
F(t) = t^3*exp(4*t)
L{F(t)} = 6/(s - 4)^4

============================================================
  SECCIÓN 3.4: TRANSFORMADA DE LA DERIVADA
  L{F'(t)} = s*f(s) - F(0)
============================================================

--- Ejemplo 1: dF/dt - 3F = e^(2t), F(0) = 1 ---
f(s) = (1/(s - 2) + 1)/(s - 3)

--- Ejemplo 2: 4F''(t) + F(t) = -2, F(0)=0, F'(0)=1/2 ---
f(s) = (2*s - 2)/(s + 4*s^3)

============================================================
  SECCIÓN 3.5: TRANSFORMADA DE UNA INTEGRAL
  L{∫₀ᵗ F(u) du} = f(s)/s
============================================================

--- Ejemplo: ∫₀ᵗ u*e^(a*u)*sin(u) du ---
F(t) = t*e^(a*t)*sin(t)
L{∫₀ᵗ F(u) du} = -(2*a - 2*s)/(s*((a - s)^2 + 1)^2)

============================================================
  SECCIÓN 4: EJERCICIOS DE PRÁCTICA
  Hallar la función en el dominio de la frecuencia
============================================================

--- Ejercicio a) F(t) = 5 + 3t - t^2 ---
F(t) = 3*t - t^2 + 5
L{F(t)} = (3*((5*s)/3 + 1))/s^2 - 2/s^3

--- Ejercicio b) F(t) = (e^t + e^(-t))^2 ---
F(t) = (exp(-t) + exp(t))^2
L{F(t)} = 1/(s - 2) + 1/(s + 2) + 2/s

--- Ejercicio c) F(t) = e^(2t) * cos(10t) ---
F(t) = cos(10*t)*exp(2*t)
L{F(t)} = (s - 2)/((s - 2)^2 + 100)

--- Ejercicio d) F(t) = t^2 * sin(8t) ---
F(t) = t^2*sin(8*t)
L{F(t)} = (64*s^2)/(s^2 + 64)^3 - 16/(s^2 + 64)^2

--- Ejercicio e) F(t) = t * e^t * cos(t) ---
F(t) = t*exp(t)*cos(t)
L{F(t)} = ((2*s - 2)*(s - 1))/((s - 1)^2 + 1)^2 - 1/((s - 1)^2 + 1)

============================================================
  PROGRAMA COMPLETADO EXITOSAMENTE
============================================================
>> 
