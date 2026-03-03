# Oracle 版本兼容性指南

## 版本概览

### 主要版本

| 版本 | 发布年份 | 主要特性 | 支持状态 |
|------|---------|---------|---------|
| 11g | 2007 | 基础性能视图 | 已停止支持 |
| 12c | 2013 | 多租户架构 | 已停止支持 |
| 19c | 2019 | 自动化特性 | 长期支持 |
| 21c | 2021 | JSON 增强 | 创新版 |
| 23ai | 2024 | AI 原生特性 | 创新版 |
| 26ai | 2026 | 向量数据库 | 未来版本 |

### 版本兼容性标注

**标准标注格式：**
```sql
-- 适用版本：Oracle 11g / 12c / 19c / 26ai
```

**特殊标注格式：**
```sql
-- 适用版本：Oracle 12c / 19c / 26ai（多租户特性）
-- 适用版本：Oracle 23ai / 26ai（向量特性）
-- 适用版本：Oracle 19c / 26ai（自动索引）
```

## 视图版本兼容性

### 基础性能视图（11g+）

**V$ 系列视图：**
- `V$INSTANCE` - 11g/12c/19c/26ai
- `V$SESSION` - 11g/12c/19c/26ai
- `V$PROCESS` - 11g/12c/19c/26ai
- `V$SQL` - 11g/12c/19c/26ai
- `V$SQLAREA` - 11g/12c/19c/26ai
- `V$SQL_PLAN` - 11g/12c/19c/26ai
- `V$LOCK` - 11g/12c/19c/26ai
- `V$TRANSACTION` - 11g/12c/19c/26ai
- `V$SESSION_LONGOPS` - 11g/12c/19c/26ai
- `V$ACTIVE_SESSION_HISTORY` - 11g/12c/19c/26ai
- `V$OSSTAT` - 11g/12c/19c/26ai
- `V$SYSMETRIC` - 11g/12c/19c/26ai
- `V$SQL_MONITOR` - 11g/12c/19c/26ai
- `V$PGASTAT` - 11g/12c/19c/26ai
- `V$SGASTAT` - 11g/12c/19c/26ai

**DBA_ 系列视图：**
- `DBA_TABLES` - 11g/12c/19c/26ai
- `DBA_INDEXES` - 11g/12c/19c/26ai
- `DBA_TAB_COLUMNS` - 11g/12c/19c/26ai
- `DBA_DEPENDENCIES` - 11g/12c/19c/26ai
- `DBA_HIST_*` - 11g/12c/19c/26ai（AWR 历史视图）

### 多租户视图（12c+）

**V$CON_ 系列视图：**
- `V$CONTAINERS` - 12c/19c/26ai
- `V$PDBS` - 12c/19c/26ai
- `CDB_*` - 12c/19c/26ai（容器数据库视图）

**CON_ID 字段：**
- 大多数 V$ 视图在 12c+ 添加了 CON_ID 字段
- 用于区分容器数据库和可插拔数据库

### RAC 视图（11g+）

**GV$ 系列视图：**
- `GV$SESSION` - 11g/12c/19c/26ai
- `GV$SYSTEM_EVENT` - 11g/12c/19c/26ai
- `GV$SEGMENT_STATISTICS` - 11g/12c/19c/26ai
- `GV$INSTANCE` - 11g/12c/19c/26ai

**RAC 特性：**
- Cache Fusion - 11g/12c/19c/26ai
- Global Cache (GC) 等待事件 - 11g/12c/19c/26ai

### Data Guard 视图（11g+）

**V$ 系列视图：**
- `V$ARCHIVED_LOG` - 11g/12c/19c/26ai
- `V$DATAGUARD_STATS` - 11g/12c/19c/26ai
- `V$MANAGED_STANDBY` - 11g/12c/19c/26ai
- `V$RMAN_STATUS` - 11g/12c/19c/26ai

### 向量数据库视图（23ai+）

**V$ 系列视图：**
- `V$VECTOR_MEMORY_POOL` - 23ai/26ai
- `DBA_VECTOR_INDEXES` - 23ai/26ai

**向量特性：**
- VECTOR 数据类型 - 23ai/26ai
- HNSW 索引 - 23ai/26ai
- IVF 索引 - 23ai/26ai
- 向量相似度搜索 - 23ai/26ai

## 特性版本兼容性

### 统计信息特性

**直方图：**
- Frequency 直方图 - 11g/12c/19c/26ai
- Height-Balanced 直方图 - 11g/12c/19c/26ai
- Hybrid 直方图 - 12c/19c/26ai
- Top-N 直方图 - 12c/19c/26ai

**自动统计信息收集：**
- 基础自动收集 - 11g/12c/19c/26ai
- 增量统计信息 - 11g/12c/19c/26ai
- 并行统计信息收集 - 11g/12c/19c/26ai

### 索引特性

**基础索引：**
- B-Tree 索引 - 11g/12c/19c/26ai
- 位图索引 - 11g/12c/19c/26ai
- 函数索引 - 11g/12c/19c/26ai
- 反向键索引 - 11g/12c/19c/26ai

**高级索引：**
- 分区索引 - 11g/12c/19c/26ai
- 全局索引 - 11g/12c/19c/26ai
- 本地索引 - 11g/12c/19c/26ai
- 隐形索引 - 11g/12c/19c/26ai

**向量索引：**
- HNSW 索引 - 23ai/26ai
- IVF 索引 - 23ai/26ai

### 内存管理特性

**SGA 管理：**
- 手动 SGA 管理 - 11g/12c/19c/26ai
- ASMM（自动共享内存管理） - 11g/12c/19c/26ai
- AMM（自动内存管理） - 11g/12c/19c/26ai

**PGA 管理：**
- 手动 PGA 管理 - 11g/12c/19c/26ai
- 自动 PGA 管理 - 11g/12c/19c/26ai

**向量内存池：**
- Vector Memory Pool - 23ai/26ai

### 性能监控特性

**ASH（Active Session History）：**
- V$ACTIVE_SESSION_HISTORY - 11g/12c/19c/26ai
- DBA_HIST_ACTIVE_SESS_HISTORY - 11g/12c/19c/26ai

**AWR（Automatic Workload Repository）：**
- DBA_HIST_SNAPSHOT - 11g/12c/19c/26ai
- DBA_HIST_SQLSTAT - 11g/12c/19c/26ai
- DBA_HIST_SEG_STAT - 11g/12c/19c/26ai
- DBA_HIST_SQL_PLAN - 11g/12c/19c/26ai

**SQL Monitor：**
- V$SQL_MONITOR - 11g/12c/19c/26ai
- DBMS_SQL_MONITOR 包 - 11g/12c/19c/26ai

### 备份恢复特性

**RMAN：**
- V$RMAN_STATUS - 11g/12c/19c/26ai
- 增量备份 - 11g/12c/19c/26ai
- 块级恢复 - 11g/12c/19c/26ai

**Data Guard：**
- 物理备库 - 11g/12c/19c/26ai
- 逻辑备库 - 11g/12c/19c/26ai
- 快照备库 - 11g/12c/19c/26ai
- Far Sync - 12c/19c/26ai

## 版本差异处理

### 11g 特有特性

**已废弃视图：**
- V$OBJECT_USAGE - 11g 中存在，12c+ 已废弃
- 部分性能视图在 12c+ 中被替代

**推荐替代方案：**
- V$OBJECT_USAGE → DBA_INDEXES.USED 列
- 旧性能视图 → 新性能视图

### 12c 特有特性

**多租户架构：**
- CDB/PDB 架构
- CON_ID 字段
- CDB_* 视图

**处理建议：**
- 在多租户环境中使用 CON_ID 过滤
- 使用 CDB_* 视图查询所有容器

### 19c 特有特性

**自动化特性：**
- 自动索引
- 自动 SQL 调优
- 自动并行度

**处理建议：**
- 标注自动化特性的版本要求
- 提供手动替代方案

### 23ai/26ai 特有特性

**AI 原生特性：**
- 向量数据类型
- 向量索引
- 向量相似度搜索
- AI Vector Search

**处理建议：**
- 明确标注仅适用于 23ai/26ai
- 提供传统数据库的替代方案

## 脚本版本兼容性示例

### 示例 1：基础性能监控（11g+）

```sql
-- 适用版本：Oracle 11g / 12c / 19c / 26ai
SELECT sid, serial#, status, sql_id
FROM v$session
WHERE status = 'ACTIVE';
```

### 示例 2：多租户环境（12c+）

```sql
-- 适用版本：Oracle 12c / 19c / 26ai（多租户特性）
SELECT con_id, name, open_mode
FROM v$containers;
```

### 示例 3：向量数据库（23ai+）

```sql
-- 适用版本：Oracle 23ai / 26ai（向量特性）
SELECT pool_name, bytes_allocated, bytes_used
FROM v$vector_memory_pool;
```

### 示例 4：RAC 集群（11g+）

```sql
-- 适用版本：Oracle 11g / 12c / 19c / 26ai（RAC 特性）
SELECT inst_id, sid, serial#, status
FROM gv$session
WHERE status = 'ACTIVE';
```

## 版本兼容性检查清单

### 脚本编写检查

**检查项：**
- [ ] 视图名称是否正确
- [ ] 字段名称是否正确
- [ ] 函数名称是否正确
- [ ] 版本兼容性是否标注
- [ ] 特殊特性是否说明

### 文章编写检查

**检查项：**
- [ ] 特性版本是否明确
- [ ] 版本差异是否说明
- [ ] 替代方案是否提供
- [ ] 兼容性标注是否准确

## 常见版本兼容性问题

### 问题 1：使用 12c+ 特性但标注为 11g+

**错误示例：**
```sql
-- 适用版本：Oracle 11g / 12c / 19c / 26ai
SELECT con_id, name FROM v$containers;
```

**正确示例：**
```sql
-- 适用版本：Oracle 12c / 19c / 26ai（多租户特性）
SELECT con_id, name FROM v$containers;
```

### 问题 2：使用 23ai+ 特性但标注为 19c+

**错误示例：**
```sql
-- 适用版本：Oracle 19c / 26ai
SELECT * FROM v$vector_memory_pool;
```

**正确示例：**
```sql
-- 适用版本：Oracle 23ai / 26ai（向量特性）
SELECT * FROM v$vector_memory_pool;
```

### 问题 3：未标注版本兼容性

**错误示例：**
```sql
SELECT * FROM v$session;
```

**正确示例：**
```sql
-- 适用版本：Oracle 11g / 12c / 19c / 26ai
SELECT * FROM v$session;
```
