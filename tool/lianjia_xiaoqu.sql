DROP TABLE IF EXISTS `xiaoqu`;

CREATE TABLE `xiaoqu` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `city` varchar(10) DEFAULT NULL,
  `date` varchar(8) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `area` varchar(50) DEFAULT NULL,
  `xiaoqu` varchar(100) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `sale` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `zufang`;
CREATE TABLE `zufang` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT  COMMENT '主键',
  `city` varchar(10) DEFAULT NULL  COMMENT '城市',
  `date` varchar(8) DEFAULT NULL  COMMENT '日期',
  `district` varchar(50) DEFAULT NULL  COMMENT '区域',
  `area` varchar(50) DEFAULT NULL  COMMENT '板块',
  `xiaoqu` varchar(100) DEFAULT NULL  COMMENT '小区',
  `rent_type` varchar(100) DEFAULT NULL  COMMENT '整租、合租',
  `layout` varchar(50) DEFAULT NULL  COMMENT '户型',
  `building_space` int(11) DEFAULT NULL COMMENT '建筑面积',
  `price` int(11) DEFAULT NULL COMMENT '价格',
  PRIMARY KEY (`id`),
  INDEX idx_main_index (date,district,area,xiaoqu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;