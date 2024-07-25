-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-07-2024 a las 09:10:29
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `molitorm`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alimentoh`
--

CREATE TABLE `alimentoh` (
  `id_alimentoh` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alimentoh`
--

INSERT INTO `alimentoh` (`id_alimentoh`, `nombre`) VALUES
(1, 'Ninguno'),
(2, 'Papas'),
(3, 'Zanahoria'),
(4, 'Manzanas'),
(5, 'Pepino');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `anaquel`
--

CREATE TABLE `anaquel` (
  `id_anaquel` int(11) NOT NULL,
  `nombre` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `anaquel`
--

INSERT INTO `anaquel` (`id_anaquel`, `nombre`) VALUES
(1, 'A1'),
(2, 'A2'),
(3, 'A3'),
(4, 'A4'),
(5, 'A5');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cargo`
--

CREATE TABLE `cargo` (
  `id_cargo` int(11) NOT NULL,
  `nombre` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cargo`
--

INSERT INTO `cargo` (`id_cargo`, `nombre`) VALUES
(1, 'Administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

CREATE TABLE `configuracion` (
  `id` int(11) NOT NULL,
  `tiempo_alimentacion_larva_pequena` int(11) NOT NULL,
  `unidad_tiempo_alim_larva_pequena` enum('minutos','horas','dias') NOT NULL,
  `tiempo_alimentacion_larva_grande` int(11) NOT NULL,
  `unidad_tiempo_alim_larva_grande` enum('minutos','horas','dias') NOT NULL,
  `tiempo_alimentacion_imago` int(11) NOT NULL,
  `unidad_tiempo_alim_imago` enum('minutos','horas','dias') NOT NULL,
  `tiempo_limpieza_larva_grande` int(11) NOT NULL,
  `unidad_tiempo_limp_larva_grande` enum('minutos','horas','dias') NOT NULL,
  `tiempo_limpieza_pupa` int(11) NOT NULL,
  `unidad_tiempo_limp_pupa` enum('minutos','horas','dias') NOT NULL,
  `tiempo_limpieza_imago` int(11) NOT NULL,
  `unidad_tiempo_limp_imago` enum('minutos','horas','dias') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `configuracion`
--

INSERT INTO `configuracion` (`id`, `tiempo_alimentacion_larva_pequena`, `unidad_tiempo_alim_larva_pequena`, `tiempo_alimentacion_larva_grande`, `unidad_tiempo_alim_larva_grande`, `tiempo_alimentacion_imago`, `unidad_tiempo_alim_imago`, `tiempo_limpieza_larva_grande`, `unidad_tiempo_limp_larva_grande`, `tiempo_limpieza_pupa`, `unidad_tiempo_limp_pupa`, `tiempo_limpieza_imago`, `unidad_tiempo_limp_imago`) VALUES
(1, 2, 'minutos', 2, 'minutos', 2, 'minutos', 2, 'minutos', 2, 'minutos', 2, 'minutos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuarto`
--

CREATE TABLE `cuarto` (
  `id_cuarto` int(11) NOT NULL,
  `nombre` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cuarto`
--

INSERT INTO `cuarto` (`id_cuarto`, `nombre`) VALUES
(1, 'C1'),
(2, 'C2'),
(3, 'C3'),
(4, 'C4'),
(5, 'C5');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `duracion_fase`
--

CREATE TABLE `duracion_fase` (
  `id_fase` int(11) NOT NULL,
  `duracion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `duracion_fase`
--

INSERT INTO `duracion_fase` (`id_fase`, `duracion`) VALUES
(1, 7),
(2, 35),
(3, 28),
(4, 7),
(5, 999);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estante`
--

CREATE TABLE `estante` (
  `id_estante` int(11) NOT NULL,
  `nombre` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estante`
--

INSERT INTO `estante` (`id_estante`, `nombre`) VALUES
(1, 'E1'),
(2, 'E2'),
(3, 'E3'),
(4, 'E4'),
(5, 'E5');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fase`
--

CREATE TABLE `fase` (
  `id_fase` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `fase`
--

INSERT INTO `fase` (`id_fase`, `nombre`) VALUES
(1, 'Huevo'),
(2, 'Larva - Pequeña'),
(3, 'Larva - Grande'),
(4, 'Crisalida'),
(5, 'Imago');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones_vistas`
--

CREATE TABLE `notificaciones_vistas` (
  `id` int(11) NOT NULL,
  `id_unidad` int(11) NOT NULL,
  `tipo_notificacion` varchar(50) NOT NULL,
  `fecha_vista` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguimiento_alimentacion`
--

CREATE TABLE `seguimiento_alimentacion` (
  `id` int(11) NOT NULL,
  `id_unidad` int(11) NOT NULL,
  `ultima_alimentacion` datetime NOT NULL,
  `proxima_alimentacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguimiento_limpieza`
--

CREATE TABLE `seguimiento_limpieza` (
  `id_limpieza` int(11) NOT NULL,
  `id_unidad` int(11) NOT NULL,
  `ultima_limpieza` datetime NOT NULL,
  `proxima_limpieza` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sustrato`
--

CREATE TABLE `sustrato` (
  `id_sustrato` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sustrato`
--

INSERT INTO `sustrato` (`id_sustrato`, `nombre`) VALUES
(1, 'Ninguno'),
(2, 'Salvado de Trigo'),
(3, 'Harina de avena'),
(4, 'Harina de maiz');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tecnica`
--

CREATE TABLE `tecnica` (
  `id_tecnica` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tecnica`
--

INSERT INTO `tecnica` (`id_tecnica`, `nombre`) VALUES
(1, 'Recto por valdes'),
(2, 'Continuo por niveles');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `unidad`
--

CREATE TABLE `unidad` (
  `id_unidad` int(11) NOT NULL,
  `matricula` varchar(15) NOT NULL,
  `fecha` date NOT NULL,
  `id_fase` int(11) NOT NULL,
  `e_fechaInicio` date NOT NULL,
  `e_semana` int(11) NOT NULL,
  `d_ancho` float NOT NULL,
  `d_largo` float NOT NULL,
  `d_alto` float NOT NULL,
  `biomasa` float NOT NULL,
  `id_alimentoh` int(11) NOT NULL,
  `peso_alimentoh` float NOT NULL,
  `id_sustrato` int(11) NOT NULL,
  `peso_sustrato` float NOT NULL,
  `id_anaquel` int(11) NOT NULL,
  `id_estante` int(11) NOT NULL,
  `id_cuarto` int(11) NOT NULL,
  `id_tecnica` int(11) NOT NULL,
  `c_temperatura` float NOT NULL,
  `c_humedad` float NOT NULL,
  `c_oxigenacion` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `a_paterno` varchar(15) NOT NULL,
  `a_materno` varchar(15) NOT NULL,
  `correo` varchar(20) NOT NULL,
  `contraseña` varchar(15) NOT NULL,
  `id_cargo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `a_paterno`, `a_materno`, `correo`, `contraseña`, `id_cargo`) VALUES
(1, 'Allison Lia', 'Huerta', 'Ramirez', 'admin', '123', 1),
(2, 'Yamile', 'Chavez', 'Mendoza', 'yamile', '123', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alimentoh`
--
ALTER TABLE `alimentoh`
  ADD PRIMARY KEY (`id_alimentoh`);

--
-- Indices de la tabla `anaquel`
--
ALTER TABLE `anaquel`
  ADD PRIMARY KEY (`id_anaquel`);

--
-- Indices de la tabla `cargo`
--
ALTER TABLE `cargo`
  ADD PRIMARY KEY (`id_cargo`);

--
-- Indices de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `cuarto`
--
ALTER TABLE `cuarto`
  ADD PRIMARY KEY (`id_cuarto`);

--
-- Indices de la tabla `duracion_fase`
--
ALTER TABLE `duracion_fase`
  ADD PRIMARY KEY (`id_fase`);

--
-- Indices de la tabla `estante`
--
ALTER TABLE `estante`
  ADD PRIMARY KEY (`id_estante`);

--
-- Indices de la tabla `fase`
--
ALTER TABLE `fase`
  ADD PRIMARY KEY (`id_fase`);

--
-- Indices de la tabla `notificaciones_vistas`
--
ALTER TABLE `notificaciones_vistas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_unidad` (`id_unidad`);

--
-- Indices de la tabla `seguimiento_alimentacion`
--
ALTER TABLE `seguimiento_alimentacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_unidad` (`id_unidad`);

--
-- Indices de la tabla `seguimiento_limpieza`
--
ALTER TABLE `seguimiento_limpieza`
  ADD PRIMARY KEY (`id_limpieza`),
  ADD KEY `id_unidad` (`id_unidad`);

--
-- Indices de la tabla `sustrato`
--
ALTER TABLE `sustrato`
  ADD PRIMARY KEY (`id_sustrato`);

--
-- Indices de la tabla `tecnica`
--
ALTER TABLE `tecnica`
  ADD PRIMARY KEY (`id_tecnica`);

--
-- Indices de la tabla `unidad`
--
ALTER TABLE `unidad`
  ADD PRIMARY KEY (`id_unidad`),
  ADD KEY `fk_unidad_alimentoh` (`id_alimentoh`),
  ADD KEY `fk_unidad_sustrato` (`id_sustrato`),
  ADD KEY `fk_unidad_anaquel` (`id_anaquel`),
  ADD KEY `fk_unidad_estante` (`id_estante`),
  ADD KEY `fk_unidad_cuarto` (`id_cuarto`),
  ADD KEY `fk_unidad_tecnica` (`id_tecnica`),
  ADD KEY `fk_unidad_fase` (`id_fase`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `fk_usuarios_cargo` (`id_cargo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alimentoh`
--
ALTER TABLE `alimentoh`
  MODIFY `id_alimentoh` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `anaquel`
--
ALTER TABLE `anaquel`
  MODIFY `id_anaquel` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `cargo`
--
ALTER TABLE `cargo`
  MODIFY `id_cargo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `cuarto`
--
ALTER TABLE `cuarto`
  MODIFY `id_cuarto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `estante`
--
ALTER TABLE `estante`
  MODIFY `id_estante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `fase`
--
ALTER TABLE `fase`
  MODIFY `id_fase` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `notificaciones_vistas`
--
ALTER TABLE `notificaciones_vistas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `seguimiento_alimentacion`
--
ALTER TABLE `seguimiento_alimentacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `seguimiento_limpieza`
--
ALTER TABLE `seguimiento_limpieza`
  MODIFY `id_limpieza` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sustrato`
--
ALTER TABLE `sustrato`
  MODIFY `id_sustrato` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tecnica`
--
ALTER TABLE `tecnica`
  MODIFY `id_tecnica` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `unidad`
--
ALTER TABLE `unidad`
  MODIFY `id_unidad` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `duracion_fase`
--
ALTER TABLE `duracion_fase`
  ADD CONSTRAINT `duracion_fase_ibfk_1` FOREIGN KEY (`id_fase`) REFERENCES `fase` (`id_fase`);

--
-- Filtros para la tabla `notificaciones_vistas`
--
ALTER TABLE `notificaciones_vistas`
  ADD CONSTRAINT `notificaciones_vistas_ibfk_1` FOREIGN KEY (`id_unidad`) REFERENCES `unidad` (`id_unidad`);

--
-- Filtros para la tabla `seguimiento_alimentacion`
--
ALTER TABLE `seguimiento_alimentacion`
  ADD CONSTRAINT `seguimiento_alimentacion_ibfk_1` FOREIGN KEY (`id_unidad`) REFERENCES `unidad` (`id_unidad`);

--
-- Filtros para la tabla `seguimiento_limpieza`
--
ALTER TABLE `seguimiento_limpieza`
  ADD CONSTRAINT `seguimiento_limpieza_ibfk_1` FOREIGN KEY (`id_unidad`) REFERENCES `unidad` (`id_unidad`);

--
-- Filtros para la tabla `unidad`
--
ALTER TABLE `unidad`
  ADD CONSTRAINT `fk_unidad_alimentoh` FOREIGN KEY (`id_alimentoh`) REFERENCES `alimentoh` (`id_alimentoh`),
  ADD CONSTRAINT `fk_unidad_anaquel` FOREIGN KEY (`id_anaquel`) REFERENCES `anaquel` (`id_anaquel`),
  ADD CONSTRAINT `fk_unidad_cuarto` FOREIGN KEY (`id_cuarto`) REFERENCES `cuarto` (`id_cuarto`),
  ADD CONSTRAINT `fk_unidad_estante` FOREIGN KEY (`id_estante`) REFERENCES `estante` (`id_estante`),
  ADD CONSTRAINT `fk_unidad_fase` FOREIGN KEY (`id_fase`) REFERENCES `fase` (`id_fase`),
  ADD CONSTRAINT `fk_unidad_sustrato` FOREIGN KEY (`id_sustrato`) REFERENCES `sustrato` (`id_sustrato`),
  ADD CONSTRAINT `fk_unidad_tecnica` FOREIGN KEY (`id_tecnica`) REFERENCES `tecnica` (`id_tecnica`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `fk_usuarios_cargo` FOREIGN KEY (`id_cargo`) REFERENCES `cargo` (`id_cargo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
