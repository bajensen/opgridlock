CREATE TABLE `holder_type` (
  `holder_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `holder_type_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`holder_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `holder_type_access` (
  `holder_type_access_id` int(11) NOT NULL AUTO_INCREMENT,
  `holder_type_id` int(11) NOT NULL,
  `weekday` varchar(3) DEFAULT NULL COMMENT 'MON, TUE, WED, THR, FRI, SAT, SUN or ANY (wildcard)',
  `start_time` time NOT NULL DEFAULT '00:00:00',
  `end_time` time NOT NULL DEFAULT '23:59:59',
  PRIMARY KEY (`holder_type_access_id`),
  KEY `holder_type_access_holder_type_holder_type_id_fk` (`holder_type_id`),
  CONSTRAINT `holder_type_access_holder_type_holder_type_id_fk` FOREIGN KEY (`holder_type_id`) REFERENCES `holder_type` (`holder_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `holder` (
  `holder_id` int(11) NOT NULL AUTO_INCREMENT,
  `holder_name` varchar(100) NOT NULL DEFAULT '',
  `holder_phone` varchar(16) DEFAULT NULL,
  `holder_type_id` int(11) NOT NULL,
  PRIMARY KEY (`holder_id`),
  KEY `holder_holder_type_holder_type_id_fk` (`holder_type_id`),
  CONSTRAINT `holder_holder_type_holder_type_id_fk` FOREIGN KEY (`holder_type_id`) REFERENCES `holder_type` (`holder_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `tag` (
  `tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_code` varchar(32) NOT NULL COMMENT 'Eg. 1E00EBE63D2E',
  `tag_number` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `tag_tag_code_uindex` (`tag_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `tag_assignment` (
  `tag_assignment_id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) NOT NULL,
  `holder_id` int(11) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime DEFAULT NULL COMMENT 'NULL if active assignment.',
  PRIMARY KEY (`tag_assignment_id`),
  KEY `tag_assignment_tag_tag_id_fk` (`tag_id`),
  KEY `tag_assignment_holder_holder_id_fk` (`holder_id`),
  CONSTRAINT `tag_assignment_holder_holder_id_fk` FOREIGN KEY (`holder_id`) REFERENCES `holder` (`holder_id`),
  CONSTRAINT `tag_assignment_tag_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type` varchar(10) NOT NULL,
  `event_date` datetime DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `details` text,
  PRIMARY KEY (`event_id`),
  KEY `event_tag_tag_id_fk` (`tag_id`),
  CONSTRAINT `event_tag_tag_id_fk` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;