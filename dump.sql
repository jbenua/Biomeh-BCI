-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Хост: 127.0.0.1
-- Время создания: Мар 21 2015 г., 18:19
-- Версия сервера: 5.5.25
-- Версия PHP: 5.2.12

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `headset`
--
CREATE DATABASE `headset` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `headset`;

-- --------------------------------------------------------

--
-- Структура таблицы `raw`
--

CREATE TABLE IF NOT EXISTS `raw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `f3` int(11) NOT NULL,
  `fc6` int(11) NOT NULL,
  `p7` int(11) NOT NULL,
  `t8` int(11) NOT NULL,
  `f7` int(11) NOT NULL,
  `f8` int(11) NOT NULL,
  `t7` int(11) NOT NULL,
  `p8` int(11) NOT NULL,
  `af4` int(11) NOT NULL,
  `f4` int(11) NOT NULL,
  `af3` int(11) NOT NULL,
  `o2` int(11) NOT NULL,
  `o1` int(11) NOT NULL,
  `fc5` int(11) NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  `unknown` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Дамп данных таблицы `raw`
--

INSERT INTO `raw` (`id`, `f3`, `fc6`, `p7`, `t8`, `f7`, `f8`, `t7`, `p8`, `af4`, `f4`, `af3`, `o2`, `o1`, `fc5`, `x`, `y`, `unknown`) VALUES
(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `sessions`
--

CREATE TABLE IF NOT EXISTS `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `raw_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `tag_id` (`tag_id`),
  KEY `raw` (`raw_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Дамп данных таблицы `sessions`
--

INSERT INTO `sessions` (`id`, `raw_id`, `user_id`, `tag_id`) VALUES
(1, 1, 0, 3),
(2, 1, 0, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `tags`
--

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Дамп данных таблицы `tags`
--

INSERT INTO `tags` (`id`, `tag`) VALUES
(1, 'blablabla'),
(2, 'laugh'),
(3, 'orly'),
(4, 'воркп');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `passwd` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `username`, `passwd`) VALUES
(0, 'Masha', 'marusya');

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `sessions`
--
ALTER TABLE `sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sessions_ibfk_2` FOREIGN KEY (`raw_id`) REFERENCES `raw` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `sessions_ibfk_3` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
