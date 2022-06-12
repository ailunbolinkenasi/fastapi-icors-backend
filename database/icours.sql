/*
 Navicat Premium Data Transfer

 Source Server         : 本地数据库
 Source Server Type    : MySQL
 Source Server Version : 50737
 Source Host           : localhost:3306
 Source Schema         : icours

 Target Server Type    : MySQL
 Target Server Version : 50737
 File Encoding         : 65001

 Date: 24/05/2022 11:14:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for access
-- ----------------------------
DROP TABLE IF EXISTS `access`;
CREATE TABLE `access` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `access_name` varchar(15) NOT NULL COMMENT '权限名称',
  `parent_id` int(11) NOT NULL DEFAULT '0' COMMENT '父id',
  `scopes` varchar(255) NOT NULL COMMENT '权限范围标识',
  `access_desc` varchar(255) DEFAULT NULL COMMENT '权限描述',
  `menu_icon` varchar(255) DEFAULT NULL COMMENT '菜单图标',
  `is_check` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否验证权限 True为验证 False不验证',
  `is_menu` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为菜单 True菜单 False不是菜单',
  PRIMARY KEY (`id`),
  UNIQUE KEY `scopes` (`scopes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='权限表';

-- ----------------------------
-- Table structure for access_log
-- ----------------------------
DROP TABLE IF EXISTS `access_log`;
CREATE TABLE `access_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `target_url` varchar(255) DEFAULT NULL COMMENT '访问的url',
  `user_agent` varchar(255) DEFAULT NULL COMMENT '访问UA',
  `request_params` json DEFAULT NULL COMMENT '请求参数get|post',
  `ip` varchar(32) DEFAULT NULL COMMENT '访问IP',
  `note` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户操作记录表';

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `role_name` varchar(15) NOT NULL COMMENT '角色名称',
  `role_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'True:启用 False:禁用',
  `role_desc` varchar(255) DEFAULT NULL COMMENT '角色描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- ----------------------------
-- Table structure for role_access
-- ----------------------------
DROP TABLE IF EXISTS `role_access`;
CREATE TABLE `role_access` (
  `role_id` int(11) NOT NULL,
  `access_id` int(11) NOT NULL,
  KEY `role_id` (`role_id`),
  KEY `access_id` (`access_id`),
  CONSTRAINT `role_access_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `role_access_ibfk_2` FOREIGN KEY (`access_id`) REFERENCES `access` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for role_user
-- ----------------------------
DROP TABLE IF EXISTS `role_user`;
CREATE TABLE `role_user` (
  `role_id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  KEY `role_id` (`role_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `role_user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE,
  CONSTRAINT `role_user_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `create_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  `username` varchar(20) NOT NULL COMMENT '用户名',
  `user_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '用户类型 True:超级管理员 False:普通管理员',
  `password` varchar(255) DEFAULT NULL,
  `nickname` varchar(255) NOT NULL DEFAULT '请更改用户名' COMMENT '昵称',
  `user_phone` varchar(11) NOT NULL COMMENT '手机号',
  `user_email` varchar(255) NOT NULL COMMENT '邮箱',
  `full_name` varchar(255) NOT NULL COMMENT '姓名',
  `is_activate` int(11) NOT NULL DEFAULT '0' COMMENT '0未激活 1正常 2禁用',
  `header_img` varchar(255) DEFAULT NULL COMMENT '用户头像',
  `sex` int(11) DEFAULT '0' COMMENT '0未知 1男 2女',
  `login_host` varchar(19) DEFAULT NULL COMMENT '访问IP',
  PRIMARY KEY (`username`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `user_phone` (`user_phone`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

SET FOREIGN_KEY_CHECKS = 1;
