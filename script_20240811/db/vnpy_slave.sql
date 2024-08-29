/*
 Navicat Premium Data Transfer

 Source Server         : localhos
 Source Server Type    : MySQL
 Source Server Version : 80012
 Source Host           : localhost:3306
 Source Schema         : vnpy_slave

 Target Server Type    : MySQL
 Target Server Version : 80012
 File Encoding         : 65001

 Date: 29/08/2024 14:17:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `account_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '账户名',
  `initial_margin` decimal(20, 2) NOT NULL DEFAULT 0.00 COMMENT '初始保证金 (废弃)',
  `margin` decimal(20, 2) NOT NULL DEFAULT 0.00 COMMENT '现在保证金 (废弃)',
  `slice_num` int(11) NOT NULL DEFAULT 1 COMMENT '分片数量',
  `slice_margin` decimal(20, 2) NOT NULL DEFAULT 0.00 COMMENT '分片最大金额',
  `is_disable` tinyint(4) NOT NULL DEFAULT 0 COMMENT '是否禁用',
  `balance` decimal(20, 2) NOT NULL DEFAULT 0.00 COMMENT 'ctp余额',
  `frozen` decimal(20, 2) NOT NULL DEFAULT 0.00 COMMENT 'ctp冻结金额',
  `create_date` datetime(0) NOT NULL DEFAULT '2000-01-01 00:00:00',
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '账户' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for account_day_client_equity
-- ----------------------------
DROP TABLE IF EXISTS `account_day_client_equity`;
CREATE TABLE `account_day_client_equity`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '账号',
  `client_equity` decimal(65, 2) NOT NULL DEFAULT 0.00 COMMENT '客户权益',
  `date` date NOT NULL DEFAULT '2000-01-01' COMMENT '日期',
  `create_date` datetime(0) NOT NULL DEFAULT '2000-01-01 00:00:00',
  PRIMARY KEY (`pk_id`) USING BTREE,
  INDEX `index_date`(`date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '账户每日动态权益记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ctp_order
-- ----------------------------
DROP TABLE IF EXISTS `ctp_order`;
CREATE TABLE `ctp_order`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '账号',
  `order_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '下单时生成的订单id',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '名称',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '下单代码',
  `price` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '价格',
  `volume` int(10) NOT NULL DEFAULT 0 COMMENT '数量手',
  `order_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '下单类型 limit 限价单;',
  `is_complete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否全部完成 0 否; 1 是;',
  `complete_volume` int(255) NOT NULL DEFAULT 0 COMMENT '完成交易数量',
  `open_or_close` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '开或平 open 开; close 平;',
  `buy_or_sell` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '下单类型 buy 多; sell 空;',
  `is_close` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否已关闭 0 否; 1 是;',
  `slice_id` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '对应分仓id',
  `note` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '备注',
  `create_date` datetime(0) NOT NULL DEFAULT '2000-01-01 00:00:00',
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '挂单记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for kv
-- ----------------------------
DROP TABLE IF EXISTS `kv`;
CREATE TABLE `kv`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名称',
  `description` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '描述',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '键',
  `value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '值',
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '配置参数' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of kv
-- ----------------------------
INSERT INTO `kv` VALUES (1, '操作时间点', '', 'target_time', '14:58:00');
INSERT INTO `kv` VALUES (2, '鸡蛋投机手续费', '成交金额的万分之1.5', 'jd_speculation_charge', '0.00015');
INSERT INTO `kv` VALUES (3, '鸡蛋保值手续费', '成交金额的万分之0.75', 'jd_hedging_charge', '0.000075');
INSERT INTO `kv` VALUES (4, '鸡蛋交割手续费', '元/吨', 'jd_delivery_charge', '1');
INSERT INTO `kv` VALUES (5, '分仓最大数量', '总金额被分成多少份 达到后不会开新的仓', 'slice_num', '15');
INSERT INTO `kv` VALUES (6, '分仓每次交易手数', '每天交易开多少手', 'slice_open_num', '1');
INSERT INTO `kv` VALUES (7, '开仓模式', '1 投机; 2 保值;', 'open_method', '1');
INSERT INTO `kv` VALUES (8, '开仓代码', '', 'open_code', 'jd2410.DCE');
INSERT INTO `kv` VALUES (9, '接收操作邮箱', '用于接收操作提醒邮件的邮箱号', 'get_email_username', '');
INSERT INTO `kv` VALUES (10, '发送邮件的邮箱账号', '用与发送邮件的邮箱号 需要开启 smtp', 'send_email_username', '');
INSERT INTO `kv` VALUES (11, '发送邮箱密码', '邮箱发送密码', 'send_email_password', '');
INSERT INTO `kv` VALUES (12, '是否开启重新市价挂单机制', '是否开启现价挂单失败重新以市价挂单 (simnow模拟盘不支持市价单需要关闭)', 'is_open_re_order', '1');
INSERT INTO `kv` VALUES (13, '重新市价挂单间隔秒数', '限价单(a)秒后不成交自动取消该挂单, 重新上架市价单', 're_order_limit', '10');
INSERT INTO `kv` VALUES (14, '是否每日开仓', '是否开启每日开仓', 'is_open_slice', '1');
INSERT INTO `kv` VALUES (15, '是否每日平仓', '是否开启每日平仓', 'is_close_slice', '1');
INSERT INTO `kv` VALUES (16, '发送邮件smtp服务器地址', '发送邮件smtp服务器地址', 'send_email_smtp_server', 'smtp.qq.com');
INSERT INTO `kv` VALUES (17, '发送邮件smtp端口', '发送邮件smtp端口', 'send_email_smtp_port', '587');
INSERT INTO `kv` VALUES (18, '是否收盘后上传记录到数据中心', '', 'is_close_to_upload_data_center', '0');
INSERT INTO `kv` VALUES (19, '数据中心地址', '', 'data_center_url', 'https://test2.xinfajiazhi.com/dataCenter');
INSERT INTO `kv` VALUES (20, '收盘操作时间点', '到达时间后会停止脚本', 'after_trade_time', '15:01:00');

-- ----------------------------
-- Table structure for price
-- ----------------------------
DROP TABLE IF EXISTS `price`;
CREATE TABLE `price`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `price` decimal(10, 2) DEFAULT NULL,
  `create_date` datetime(0) DEFAULT NULL,
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '价格保存' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for slice
-- ----------------------------
DROP TABLE IF EXISTS `slice`;
CREATE TABLE `slice`  (
  `pk_id` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '账号',
  `buy_or_sell` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT 'buy sell',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `volume` int(11) NOT NULL DEFAULT 0,
  `open_price` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '开仓价格',
  `open_charge` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '开仓手续费',
  `open_order_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '开仓订单id',
  `close_price` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '平仓价格',
  `close_charge` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '平仓手续费',
  `close_order_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '平仓订单id',
  `is_close` tinyint(4) NOT NULL DEFAULT 0 COMMENT '是否关闭',
  `note` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '备注',
  `close_date` datetime(0) DEFAULT NULL COMMENT '关闭时间 平仓时间',
  `create_date` datetime(0) DEFAULT NULL COMMENT '创建时间 开仓时间',
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '分仓' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for slice_day_log
-- ----------------------------
DROP TABLE IF EXISTS `slice_day_log`;
CREATE TABLE `slice_day_log`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '账户',
  `date` date NOT NULL DEFAULT '2000-01-01' COMMENT '日期',
  `slice_num` int(11) NOT NULL DEFAULT 0 COMMENT '分仓数量',
  `slice_volume` int(11) NOT NULL DEFAULT 0 COMMENT '总持仓手数',
  `create_date` datetime(0) NOT NULL COMMENT '创建日期',
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '持仓信息每日记录' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `create_date` datetime(0) NOT NULL DEFAULT '2000-01-01 00:00:00',
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '展示板用户' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'vnpy', '$2y$10$sBOdJKhVwDkKIih50Wcr2e6z.LNV1PzwRE8h0qs67Zaq6NiEC7TZy', '2024-01-01 00:00:00');

-- ----------------------------
-- Table structure for user_log
-- ----------------------------
DROP TABLE IF EXISTS `user_log`;
CREATE TABLE `user_log`  (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `msg` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `create_date` datetime(0) DEFAULT NULL,
  PRIMARY KEY (`pk_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户日志' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
