/*
 Navicat Premium Data Transfer

 Source Server         : demo
 Source Server Type    : MySQL
 Source Server Version : 80031
 Source Host           : localhost:3306
 Source Schema         : tmp_db

 Target Server Type    : MySQL
 Target Server Version : 80031
 File Encoding         : 65001

 Date: 01/04/2026 16:07:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bugs
-- ----------------------------
DROP TABLE IF EXISTS `bugs`;
CREATE TABLE `bugs`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` int UNSIGNED NOT NULL,
  `testcase_id` int UNSIGNED NULL DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('新建','打开','处理中','已修复','测试通过','已关闭') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '新建',
  `priority` enum('p0','p1','p2','p3') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'p3',
  `assignee_id` int UNSIGNED NULL DEFAULT NULL,
  `reporter_id` int UNSIGNED NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_project_id`(`project_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_priority`(`priority`) USING BTREE,
  INDEX `idx_assignee_id`(`assignee_id`) USING BTREE,
  INDEX `idx_project_status_priority`(`project_id`, `status`, `priority`) USING BTREE,
  INDEX `testcase_id`(`testcase_id`) USING BTREE,
  INDEX `reporter_id`(`reporter_id`) USING BTREE,
  CONSTRAINT `bugs_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `bugs_ibfk_2` FOREIGN KEY (`testcase_id`) REFERENCES `test_cases` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `bugs_ibfk_3` FOREIGN KEY (`assignee_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `bugs_ibfk_4` FOREIGN KEY (`reporter_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bugs
-- ----------------------------
INSERT INTO `bugs` VALUES (1, 1, 1, '用户登录时偶发性白屏', '在执行测试用例\"验证普通用户使用正确凭据登录成功\"时，偶尔出现登录后页面完全空白，F5刷新后恢复正常。概率约为1/10。', '打开', 'p1', 1, 3, '2026-04-01 13:00:21', '2026-04-01 13:00:21', NULL);
INSERT INTO `bugs` VALUES (2, 2, 2, '支付成功后未发送确认邮件', '按照测试步骤完成支付后，支付结果显示成功，但用户未收到预期的支付确认邮件。检查了垃圾邮件箱也未找到。', '处理中', 'p0', 2, 1, '2026-04-01 13:00:21', '2026-04-01 13:00:21', NULL);
INSERT INTO `bugs` VALUES (3, 3, NULL, '报告导出功能在大数据量下崩溃', '当系统中存在大量错误日志时（例如超过1万条），尝试使用\"导出为PDF\"功能会导致整个报告模块无响应甚至崩溃。', '打开', 'p1', 1, 2, '2026-04-01 13:00:21', '2026-04-01 13:00:21', NULL);

-- ----------------------------
-- Table structure for executions
-- ----------------------------
DROP TABLE IF EXISTS `executions`;
CREATE TABLE `executions`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` int UNSIGNED NOT NULL,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `type` enum('手动执行','自动化执行') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '手动执行',
  `status` enum('等待中','执行中','已完成','失败','已取消') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '等待中',
  `result` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `total_cases` int UNSIGNED NULL DEFAULT 0,
  `passed_cases` int UNSIGNED NULL DEFAULT 0,
  `failed_cases` int UNSIGNED NULL DEFAULT 0,
  `pass_rate` decimal(5, 2) NULL DEFAULT 0.00,
  `executed_by` int UNSIGNED NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_project_id`(`project_id`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_project_status`(`project_id`, `status`) USING BTREE,
  INDEX `executed_by`(`executed_by`) USING BTREE,
  CONSTRAINT `executions_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `executions_ibfk_2` FOREIGN KEY (`executed_by`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of executions
-- ----------------------------
INSERT INTO `executions` VALUES (1, 1, 'Sprint 1 回归测试', '手动执行', '已完成', '本次回归测试覆盖了核心功能。发现一个次要bug，已在JIRA中记录。', 5, 4, 1, 80.00, 3, '2026-04-01 12:48:41', '2026-04-01 12:48:41');
INSERT INTO `executions` VALUES (2, 2, '部署后自动化冒烟测试', '自动化执行', '失败', '自动化脚本执行时，支付网关模拟器无响应，导致关键支付流程用例失败。', 10, 7, 3, 70.00, 1, '2026-04-01 12:48:41', '2026-04-01 12:48:41');
INSERT INTO `executions` VALUES (3, 3, '新报告模块 Alpha 版测试', '手动执行', '执行中', '正在执行针对新报告模块的探索性测试。', 8, 2, 1, 25.00, 3, '2026-04-01 12:48:41', '2026-04-01 12:48:41');

-- ----------------------------
-- Table structure for project_members
-- ----------------------------
DROP TABLE IF EXISTS `project_members`;
CREATE TABLE `project_members`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` int UNSIGNED NOT NULL,
  `user_id` int UNSIGNED NOT NULL,
  `role` enum('PM','tester','developer') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `joined_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_project_user`(`project_id`, `user_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `project_members_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `project_members_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_members
-- ----------------------------
INSERT INTO `project_members` VALUES (1, 1, 1, 'developer', '2026-04-01 11:37:38');
INSERT INTO `project_members` VALUES (2, 1, 2, 'PM', '2026-04-01 11:37:38');
INSERT INTO `project_members` VALUES (3, 1, 3, 'tester', '2026-04-01 11:37:38');
INSERT INTO `project_members` VALUES (4, 2, 2, 'PM', '2026-04-01 11:37:38');
INSERT INTO `project_members` VALUES (5, 2, 1, 'developer', '2026-04-01 11:37:38');
INSERT INTO `project_members` VALUES (6, 3, 3, 'tester', '2026-04-01 11:37:38');
INSERT INTO `project_members` VALUES (7, 3, 2, 'PM', '2026-04-01 11:37:38');

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `owner_id` int UNSIGNED NOT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_owner_id`(`owner_id`) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at`) USING BTREE,
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO `projects` VALUES (1, 'Normal Management Project', '一个普通的管理系统', 1, '2026-04-01 11:37:38', '2026-04-01 11:37:38', NULL);
INSERT INTO `projects` VALUES (2, 'HBNU Payment System', 'HBNU 支付系统', 2, '2026-04-01 11:37:38', '2026-04-01 11:37:38', NULL);
INSERT INTO `projects` VALUES (3, 'QA Testing Suite', 'QA 质量保证系统', 3, '2026-04-01 11:37:38', '2026-04-01 11:37:38', NULL);

-- ----------------------------
-- Table structure for reports
-- ----------------------------
DROP TABLE IF EXISTS `reports`;
CREATE TABLE `reports`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` int UNSIGNED NOT NULL,
  `execution_id` int UNSIGNED NULL DEFAULT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `pass_rate` decimal(5, 2) NOT NULL DEFAULT 0.00,
  `fail_rate` decimal(5, 2) NOT NULL DEFAULT 0.00,
  `total_cases` int UNSIGNED NULL DEFAULT 0,
  `passed_cases` int UNSIGNED NULL DEFAULT 0,
  `failed_cases` int UNSIGNED NULL DEFAULT 0,
  `created_by` int UNSIGNED NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_project_id`(`project_id`) USING BTREE,
  INDEX `idx_created_at`(`created_at`) USING BTREE,
  INDEX `idx_project_created`(`project_id`, `created_at`) USING BTREE,
  INDEX `execution_id`(`execution_id`) USING BTREE,
  INDEX `created_by`(`created_by`) USING BTREE,
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`execution_id`) REFERENCES `executions` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `reports_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of reports
-- ----------------------------
INSERT INTO `reports` VALUES (1, 1, 1, 'Sprint 1 回归测试报告', 80.00, 20.00, 5, 4, 1, 3, '2026-04-01 13:50:32', '2026-04-01 13:50:32');
INSERT INTO `reports` VALUES (2, 2, 2, 'HBNU支付系统部署后冒烟测试报告', 70.00, 30.00, 10, 7, 3, 1, '2026-04-01 13:50:32', '2026-04-01 13:50:32');
INSERT INTO `reports` VALUES (3, 3, 3, 'QA系统新报告模块Alpha版测试报告', 25.00, 75.00, 8, 2, 6, 3, '2026-04-01 13:50:32', '2026-04-01 13:50:32');

-- ----------------------------
-- Table structure for test_cases
-- ----------------------------
DROP TABLE IF EXISTS `test_cases`;
CREATE TABLE `test_cases`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` int UNSIGNED NOT NULL,
  `module` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `steps` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expected` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('草稿','有效','已弃用','阻塞') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '有效',
  `priority` enum('p0','p1','p2','p3') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'p3',
  `created_by` int UNSIGNED NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_project_id`(`project_id`) USING BTREE,
  INDEX `idx_module`(`module`) USING BTREE,
  INDEX `idx_status`(`status`) USING BTREE,
  INDEX `idx_project_module_status`(`project_id`, `module`, `status`) USING BTREE,
  INDEX `created_by`(`created_by`) USING BTREE,
  CONSTRAINT `test_cases_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `test_cases_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test_cases
-- ----------------------------
INSERT INTO `test_cases` VALUES (1, 1, '用户登录模块', '验证普通用户使用正确凭据登录成功', '1. 打开登录页面\n2. 输入用户名 \"testuser\"\n3. 输入密码 \"correct_password\"\n4. 点击登录按钮', '用户应成功登录，跳转到主页', '有效', 'p1', 1, '2026-04-01 11:43:03', '2026-04-01 11:43:03', NULL);
INSERT INTO `test_cases` VALUES (2, 2, '支付处理模块', '验证信用卡支付流程', '1. 选择商品并进入支付页面\n2. 选择信用卡支付方式\n3. 输入有效的信用卡号、有效期、CVV\n4. 点击支付按钮', '支付应成功处理，显示成功页面并生成订单', '有效', 'p0', 2, '2026-04-01 11:43:03', '2026-04-01 11:43:03', NULL);
INSERT INTO `test_cases` VALUES (3, 3, '报告生成模块', '验证错误报告能否成功导出为PDF', '1. 在系统中触发一个已知错误\n2. 导航到错误报告页面\n3. 选择该错误报告\n4. 点击“导出为PDF”按钮', 'PDF文件应成功下载，内容包含完整的错误详情和日志', '阻塞', 'p2', 3, '2026-04-01 11:43:03', '2026-04-01 11:43:03', NULL);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(110) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `role` enum('PM','developer','tester') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username`) USING BTREE,
  UNIQUE INDEX `uk_email`(`email`) USING BTREE,
  INDEX `idx_role`(`role`) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'Eric', '$2b$12$U2bBC7V4RYdTgC3DLcRuU.ZE9TGeXshLnuR9N9fJsNb6EG0LGJlCW', 'developer', 'eric@163.com', '2026-04-01 10:28:04', '2026-04-01 10:28:04', NULL);
INSERT INTO `users` VALUES (2, 'Taylor', '$2b$12$vKyfe8XtCc5OP3cC1/uKpuOylJQ4egiTJeuq5ed4k2fBebNSQiwKy', 'PM', 'taylor@163.com', '2026-04-01 10:28:04', '2026-04-01 10:28:04', NULL);
INSERT INTO `users` VALUES (3, 'Charlie', '$2b$12$SKCIVK3vIS.OklGImi3K0uR7sJ1V54SLfERMrIXQZQss4Y6dpQ1ZG', 'tester', 'charlie@163.com', '2026-04-01 10:28:04', '2026-04-01 10:28:04', NULL);

SET FOREIGN_KEY_CHECKS = 1;
