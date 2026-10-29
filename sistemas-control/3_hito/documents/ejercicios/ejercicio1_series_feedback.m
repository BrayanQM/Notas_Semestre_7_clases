% =========================================================================
% EJERCICIO 1: Lazo de Realimentación Simple con Bloques en Cascada
% =========================================================================
% Descripción: Reducción de un controlador G1(s) y una planta G2(s) en 
% cascada con un sensor de realimentación H1(s).
% =========================================================================

clear; clc; close all;

% Definición de la variable compleja de Laplace
s = tf('s');

% 1. Definición de funciones de transferencia de los bloques
G1 = 4;                 % Controlador proporcional
G2 = 1 / (s + 2);        % Planta de primer orden
H1 = 0.5;               % Sensor de realimentación

% 2. Combinación en cascada de la trayectoria directa
G_dir = series(G1, G2);
disp('--- Trayectoria Directa G_dir(s) ---');
disp(G_dir);

% 3. Reducción del lazo de realimentación negativa (-1)
T = feedback(G_dir, H1, -1);
disp('--- Función de Transferencia en Lazo Cerrado T(s) ---');
disp(T);

% 4. Respuesta al Escalón Unitario
figure('Name', 'Ejercicio 1 - Respuesta al Escalón');
step(T);
grid on;
title('Respuesta al Escalón Unitario - Lazo en Cascada');
xlabel('Tiempo (segundos)');
ylabel('Amplitud C(t)');
