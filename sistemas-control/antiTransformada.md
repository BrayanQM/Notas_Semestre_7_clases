% =========================================================================
% FUNDAMENTOS MATEMÁTICOS DE SISTEMAS DE CONTROL - TRANSFORMADA DE LAPLACE
% Código Completo en MATLAB (Segunda Mitad del PDF + Práctica)
% =========================================================================

clc; clear; close all;
syms t s a real

%% -------------------------------------------------------------------------
% 3.5 TRANSFORMADA DE UNA INTEGRAL
% -------------------------------------------------------------------------
fprintf('=== 3.5 TRANSFORMADA DE UNA INTEGRAL ===\n\n');

% Ejemplo 3.5: L{ int_0^t (u * e^(a*u) * sin(u)) du }
F_int = t * exp(a*t) * sin(t);
f_s_int = laplace(F_int, t, s);

% Por propiedad de la integral: L{ int_0^t F(u) du } = (1/s) * f(s)
f_s_integral_final = f_s_int / s;

fprintf('Ejemplo 3.5:\n');
fprintf('f(s) = \n');
disp(simplify(f_s_integral_final));


%% -------------------------------------------------------------------------
% 4. ANTI TRANSFORMADA DE LAPLACE Y PROPIEDADES
% -------------------------------------------------------------------------
fprintf('=== 4. ANTI TRANSFORMADA DE LAPLACE Y PROPIEDADES ===\n\n');

% Ejemplo 4.1: Propiedad de Linealidad
% f(s) = 1/s^5 + 4/(s-8) - 2/(s^2 + 25)
f1 = 1/s^5 + 4/(s-8) - 2/(s^2 + 25);
F1_t = ilaplace(f1, s, t);

fprintf('Ejemplo 4.1:\n');
fprintf('F(t) = \n');
disp(F1_t);

% Ejemplo 4.2: Propiedad de Traslación - Ejercicio 1
% f(s) = (s+2)/(s^2 + 4*s + 7)
f2 = (s+2)/(s^2 + 4*s + 7);
F2_t = ilaplace(f2, s, t);

fprintf('Ejemplo 4.2 (1):\n');
fprintf('F(t) = \n');
disp(F2_t);

% Ejemplo 4.2: Propiedad de Traslación - Ejercicio 2
% f(s) = (s+2)/(s^2 + 5*s + 7)
f3 = (s+2)/(s^2 + 5*s + 7);
F3_t = ilaplace(f3, s, t);

fprintf('Ejemplo 4.2 (2):\n');
fprintf('F(t) = \n');
disp(F3_t);


%% -------------------------------------------------------------------------
% 5. TRANSFORMADA INVERSA POR FRACCIONES PARCIALES
% -------------------------------------------------------------------------
fprintf('=== 5. FRACCIONES PARCIALES ===\n\n');

% Caso 1: Factores reales no repetidos
% f(s) = (11*s^2 - 2*s + 5) / ((s-2)*(2*s-1)*(s+1))
fprintf('Caso 1: Resolución del Sistema Matricial M*X = N del PDF:\n');

M = [ 2,  1,  2;
      1, -1, -5;
     -1, -2,  2];

N = [11; -2; 5];

% Solución matricial X = M^-1 * N
M1 = inv(M);
X = M1 * N;  % Obtiene A, B, C

fprintf('Variables [A; B; C] =\n');
disp(X);

% Obtención de F(t) directamente en MATLAB
f_case1 = (11*s^2 - 2*s + 5) / ((s-2)*(2*s-1)*(s+1));
F_case1_t = ilaplace(f_case1, s, t);

fprintf('Anti transformada Caso 1 F(t) =\n');
disp(F_case1_t);

% Caso 2: Factores complejos no repetidos
% f(s) = (s^2 - 2*s + 2) / ((s+3)*(s^2 + 2*s + 2))
fprintf('\nCaso 2: Factores complejos no repetidos\n');
f_case2 = (s^2 - 2*s + 2) / ((s+3)*(s^2 + 2*s + 2));
F_case2_t = ilaplace(f_case2, s, t);

fprintf('Anti transformada Caso 2 F(t) =\n');
disp(F_case2_t);


%% -------------------------------------------------------------------------
% PRÁCTICA - FUNDAMENTOS MATEMÁTICOS
% -------------------------------------------------------------------------
fprintf('\n=========================================================================\n');
fprintf('  PRÁCTICA - FUNDAMENTOS MATEMÁTICOS\n');
fprintf('=========================================================================\n\n');

fprintf('--- PARTE 1: Transformadas de Laplace L{F(t)} ---\n\n');

% a) F(t) = 5 + 3*t - t^10
F_pa = 5 + 3*t - t^10;
fprintf('a) F(t) = 5 + 3*t - t^10\nf(s) = \n');
disp(laplace(F_pa, t, s));

% b) F(t) = (e^t + e^-t)^2
F_pb = (exp(t) + exp(-t))^2;
fprintf('b) F(t) = (e^t + e^-t)^2\nf(s) = \n');
disp(simplify(laplace(F_pb, t, s)));

% c) F(t) = e^(5t) * cos(10t)
F_pc = exp(5*t) * cos(10*t);
fprintf('c) F(t) = e^(5t) * cos(10t)\nf(s) = \n');
disp(laplace(F_pc, t, s));

% d) F(t) = t^2 * sin(8t)
F_pd = t^2 * sin(8*t);
fprintf('d) F(t) = t^2 * sin(8t)\nf(s) = \n');
disp(simplify(laplace(F_pd, t, s)));

% e) F(t) = t * e^t * cos(t)
F_pe = t * exp(t) * cos(t);
fprintf('e) F(t) = t * e^t * cos(t)\nf(s) = \n');
disp(simplify(laplace(F_pe, t, s)));

fprintf('-------------------------------------------------------------------------\n');
fprintf('--- PARTE 2: Anti transformadas de Laplace L^-1{f(s)} ---\n\n');

% a) f(s) = (5*s - 15) / (s^2 + 7)
f_pa2 = (5*s - 15)/(s^2 + 7);
fprintf('a) f(s) = (5*s - 15)/(s^2 + 7)\nF(t) = \n');
disp(ilaplace(f_pa2, s, t));

% b) f(s) = 1 / (4*s - 3)
f_pb2 = 1/(4*s - 3);
fprintf('b) f(s) = 1/(4*s - 3)\nF(t) = \n');
disp(ilaplace(f_pb2, s, t));

% c) f(s) = (3*s + 8) / (s^2 - 2!)  [Nota: 2! = 2]
f_pc2 = (3*s + 8)/(s^2 - 2);
fprintf('c) f(s) = (3*s + 8)/(s^2 - 2)\nF(t) = \n');
disp(simplify(ilaplace(f_pc2, s, t)));

% d) f(s) = s / (s + 1)^5
f_pd2 = s / (s + 1)^5;
fprintf('d) f(s) = s / (s + 1)^5\nF(t) = \n');
disp(ilaplace(f_pd2, s, t));

% e) f(s) = (2*s - 6) / (s^3 - s)
f_pe2 = (2*s - 6)/(s^3 - s);
fprintf('e) f(s) = (2*s - 6)/(s^3 - s)\nF(t) = \n');
disp(ilaplace(f_pe2, s, t));

% f) f(s) = (5*s + 24) / (s^2 + 4)
f_pf2 = (5*s + 24)/(s^2 + 4);
fprintf('f) f(s) = (5*s + 24)/(s^2 + 4)\nF(t) = \n');
disp(ilaplace(f_pf2, s, t));

fprintf('=========================================================================\n');
# RESULTADO DE MATLAB
=== 3.5 TRANSFORMADA DE UNA INTEGRAL ===

Ejemplo 3.5:
f(s) = 
-(2*a - 2*s)/(s*((a - s)^2 + 1)^2)
 
=== 4. ANTI TRANSFORMADA DE LAPLACE Y PROPIEDADES ===

Ejemplo 4.1:
F(t) = 
4*exp(8*t) - (2*sin(5*t))/5 + t^4/24
 
Ejemplo 4.2 (1):
F(t) = 
exp(-2*t)*cos(3^(1/2)*t)
 
Ejemplo 4.2 (2):
F(t) = 
exp(-(5*t)/2)*(cos((3^(1/2)*t)/2) - (3^(1/2)*sin((3^(1/2)*t)/2))/3)
 
=== 5. FRACCIONES PARCIALES ===

Caso 1: Resolución del Sistema Matricial M*X = N del PDF:
Variables [A; B; C] =
    5.0000
   -3.0000
    2.0000

Anti transformada Caso 1 F(t) =
2*exp(-t) + 5*exp(2*t) - (3*exp(t/2))/2
 

Caso 2: Factores complejos no repetidos
Anti transformada Caso 2 F(t) =
(17*exp(-3*t))/5 - (12*exp(-t)*(cos(t) - sin(t)/3))/5
 

=========================================================================
  PRÁCTICA - FUNDAMENTOS MATEMÁTICOS
=========================================================================

--- PARTE 1: Transformadas de Laplace L{F(t)} ---

a) F(t) = 5 + 3*t - t^10
f(s) = 
(3*((5*s)/3 + 1))/s^2 - 3628800/s^11
 
b) F(t) = (e^t + e^-t)^2
f(s) = 
(4*(s^2 - 2))/(s*(s^2 - 4))
 
c) F(t) = e^(5t) * cos(10t)
f(s) = 
(s - 5)/((s - 5)^2 + 100)
 
d) F(t) = t^2 * sin(8t)
f(s) = 
(16*(3*s^2 - 64))/(s^2 + 64)^3
 
e) F(t) = t * e^t * cos(t)
f(s) = 
(s*(s - 2))/(s^2 - 2*s + 2)^2
 
-------------------------------------------------------------------------
--- PARTE 2: Anti transformadas de Laplace L^-1{f(s)} ---

a) f(s) = (5*s - 15)/(s^2 + 7)
F(t) = 
5*cos(7^(1/2)*t) - (15*7^(1/2)*sin(7^(1/2)*t))/7
 
b) f(s) = 1/(4*s - 3)
F(t) = 
exp((3*t)/4)/4
 
c) f(s) = (3*s + 8)/(s^2 - 2)
F(t) = 
3*cosh(2^(1/2)*t) + 4*2^(1/2)*sinh(2^(1/2)*t)
 
d) f(s) = s / (s + 1)^5
F(t) = 
(t^3*exp(-t))/6 - (t^4*exp(-t))/24
 
e) f(s) = (2*s - 6)/(s^3 - s)
F(t) = 
6 - 2*exp(t) - 4*exp(-t)
 
f) f(s) = (5*s + 24)/(s^2 + 4)
F(t) = 
5*cos(2*t) + 12*sin(2*t)
 
=========================================================================
>> 
