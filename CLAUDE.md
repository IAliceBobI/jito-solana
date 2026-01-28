# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是 Jito Foundation 维护的 Solana 验证器客户端 fork（基于 Agave）。这是一个 Rust 工作空间项目，包含 145 个 crate，实现了高性能区块链验证器，支持交易捆绑（MEV）和 Jito 特定功能。

## 构建和测试命令

### 基础构建
```bash
./cargo build                    # 构建 debug 版本（不适用于生产环境）
./cargo build --release          # 构建 release 版本
./cargo build --bins --release   # 仅构建二进制文件
```

### 测试
```bash
./cargo test                     # 运行所有测试
./cargo test --package <name>    # 运行指定包的测试
./cargo test --lib               # 仅运行库测试
./cargo test --bins              # 仅运行二进制测试
```

### 单个测试
```bash
# 运行特定测试
./cargo test --package solana-core <test_name>

# 运行特定模块的测试
./cargo test --package solana-core --lib banking_stage::tests::<test_name>

# 测试时输出
./cargo test -- --nocapture      # 显示 print! 输出
./cargo test -- --test-threads=1 # 单线程运行测试
```

### 代码质量检查
```bash
./cargo clippy                   # 运行 linter
./cargo fmt                      # 格式化代码
./cargo doc --no-deps            # 生成文档
```

### 性能测试
```bash
cargo +nightly bench             # 运行基准测试（需要 nightly）
```

### 代码覆盖率
```bash
scripts/coverage.sh              # 生成覆盖率报告
open target/cov/lcov-local/index.html
```

## Rust 工具链

- 项目使用 `rust-toolchain.toml` 指定 Rust 版本（当前 1.90.0）
- 使用 `./cargo` 包装脚本自动使用正确的工具链版本
- CI 定义了 stable 和 nightly 版本（见 `ci/rust-version.sh`）

**重要**: 始终使用 `./cargo` 而不是直接使用 `cargo`，以确保使用正确的 Rust 版本。

## 工作空间结构

### 核心组件（Core Components）

- **`core/`** - 验证器核心逻辑
  - `banking_stage/` - 银行阶段（交易处理的核心）
  - `banking_stage.rs` - 主要的银行阶段入口
  - `block_creation_loop/` - 区块创建逻辑
  - `consensus/` - 共识机制实现
  - `bam_*` - Jito BAM (Block Auction Manager) 相关组件
  - `bundle_stage/` - 交易捆绑处理（Jito MEV）

- **`runtime/`** - Solana 运行时
  - 交易执行、账户管理、程序加载
  - SVM (Solana Virtual Machine) 集成

- **`validator/`** - 验证器主程序入口点
  - 启动和配置验证器节点

- **`ledger/`** - 区块链账本
  - 区块存储、 shred 处理、状态恢复

- **`entry/`** - 交易入口点
  - 接收和转发交易到 TPU

### 客户端和 RPC

- **`client/`** - 客户端库
- **`rpc-client/`** - RPC 客户端实现
- **`rpc/`** - JSON-RPC 服务器
- **`tpu-client/`** - TPU 客户端（直接发送交易到验证器）

### 网络层

- **`gossip/`** - Gossip 协议（节点发现）
- **`turbine/`** - Turbine 分块传播协议
- **`quic-client/`** - QUIC 网络客户端
- **`udp-client/`** - UDP 网络客户端
- **`streamer/`** - 高性能数据流处理

### 内置程序（Native Programs）

位于 `programs/` 目录：
- **`system/`** - 系统程序（创建账户、转账等）
- **`vote/`** - 投票程序（权益证明）
- **`compute-budget/`** - 计算预算程序
- **`bpf_loader/`** - BPF 程序加载器
- **`loader-v4/`** - 可升级程序加载器
- **`zk-*`** - 零知识证明相关程序

### 存储和数据库

- **`accounts-db/`** - 账户数据库
  - 高性能账户存储和检索
  - 使用 AppendVec 和增量存储

- **`snapshots/`** - 快照管理
- **`storage-bigtable/`** - Google BigTable 集成

### 测试和开发工具

- **`cli/`** - 命令行工具（`solana-cli`）
- **`test-validator/`** - 本地测试验证器
- **`program-test/`** - 程序测试框架
- **`local-cluster/`** - 本地集群模拟

### Jito 特定组件

- **`jito-protos/`** - Jito protobuf 定义（Git 子模块）
- **`bundle/`** - 交易捆绑功能
- **`xdp/`** - XDP (eXpress Data Path) 内核级网络处理
- **`bam-*`** - Block Auction Manager 相关模块

## 代码架构关键概念

### 交易处理流程

1. **Entry Stage** (`entry/`) - 接收交易
2. **Bundle Stage** (`bundle_stage/`) - 处理 Jito 交易捆绑
3. **Banking Stage** (`core/banking_stage/`) - 验证和执行交易
4. **Consensus** (`core/consensus/`) - 达成共识
5. **Block Creation** (`core/block_creation_loop/`) - 创建区块

### 银行阶段（Banking Stage）

这是交易处理的核心：
- **多阶段处理**：接收、验证、执行、转发
- **优先级费用**：基于费用的交易调度
- **账户锁定**：处理账户依赖关系
- **并行执行**：利用多核 CPU 并行处理

### PoH (Proof of History)

- **`poh/`** - PoH 实现和哈希链
- 时间戳服务，为整个网络提供时间排序

### Turbine 协议

- **`turbine/`** - 区块分块和传播
- 将大区块分成小 shards 并广播到网络

### 账户管理

- **`accounts-db/`** - 使用高效存储格式
- **AppendVec** - 追加存储，支持快照
- **索引** - 支持 program_id、owner 等多种索引

## Cargo 特性（Features）

### 关键特性标志

- **`agave-unstable-api`** - 启用不稳定 API（大多数 crate 默认启用）
- **`frozen-abi`** - 冻结 ABI 以确保向后兼容
- **`dev-context-only-utils`** - 开发工具

### 构建配置

项目使用多个 profile：
- `dev` - 开发构建
- `release` - 标准发布（thin LTO）
- `release-with-lto` - 胖 LTO，最大优化
- `release-with-debug` - 带调试符号的发布版本

特殊优化：
- `curve25519-dalek` 在 dev profile 下使用 opt-level 3（避免测试超时）

## 编码规范（来自 CONTRIBUTING.md）

### 代码风格

- 使用 `rustfmt` 格式化所有代码
- 使用 `clippy` 进行 lint 检查
- 变量命名：拼写完整，避免缩写（除非是闭包参数）
- 函数命名：`<verb>_<subject>` 格式
- 测试函数名以 `test_` 开头，基准测试以 `bench_` 开头

### 错误处理

- 仅在可以证明不会 panic 时使用 `unwrap()`
- 如果 panic 是期望行为，使用 `.expect()` 而不是 `unwrap()`
- 优先使用 `?` 运算符传播错误
- 使用 `thiserror` 和 `anyhow` 进行错误处理

### 测试要求

- 所有更改需要单元测试和集成测试
- 测试覆盖率至少 90%
- 测试应快速且不 flaky
- 使用 `serial_test` 防止测试间冲突

### PR 规范

- 小而频繁的 PR（<1000 行变更更佳）
- 功能性变更使用 Draft PR
- PR 标题：用户视角，祈使句，首字母大写
- 详细的 PR 描述：问题描述、建议变更、测试方法
- 避免在同一个 PR 中混合重构和逻辑变更

### 性能要求

- 所有性能改进需要基准测试证据
- 增加复杂度必须伴随相应的性能提升
- 使用 `criterion` 进行微基准测试
- 相关变更需要压力测试

## 常见开发模式

### 特性门控（Feature Gates）

破坏共识的更改必须在特性门控后：
```rust
#[cfg(feature = "some-feature")]
fn new_feature() {
    // 新实现
}

#[cfg(not(feature = "some-feature"))]
fn new_feature() {
    // 旧实现
}
```

### 日志记录

使用项目定义的日志 crate：
- 使用 `agave-logger` 或 `log` crate
- 适当的日志级别：`error!`, `warn!`, `info!`, `debug!`, `trace!`

### 指标收集

- 使用 `agave-metrics` 或 `solana-metrics`
- 关键操作应有相应的指标

### 并发和线程

- 使用 `agave-thread-manager` 管理线程池
- `tokio` 用于异步操作
- `rayon` 用于并行计算
- 注意跨线程通信使用适当的同步原语（`crossbeam-channel`）

## Jito 特定功能

### 交易捆绑（Bundles）

- `solana-bundle` crate 提供捆绑功能
- `bundle_stage` 处理捆绑交易的优先级处理
- 允许交易打包在一起按顺序执行

### BAM (Block Auction Manager)

- `bam_*` 模块实现区块拍卖逻辑
- 管理与 Jito block engine 的连接
- 处理区块空间拍卖和 MEV 提取

### XDP (eXpress Data Path)

- `xdp/` 和 `xdp-ebpf/` 提供内核级网络处理
- 显著降低网络延迟
- 需要 Linux 和特定硬件支持

## 重要注意事项

### SemVer 兼容性

- 尽量避免破坏 semver
- 如果必须，适当增加版本号
- 公共 API 变更需要谨慎考虑

### 依赖管理

- 所有依赖在根 `Cargo.toml` 的 `[workspace.dependencies]` 中定义
- 使用工作空间依赖而非 crates.io 依赖
- 本地 path 依赖使用 `=` 版本要求

### Git 子模块

- `jito-protos` 是 Git 子模块
- 克隆后需要运行 `git submodule update --init --recursive`

### 测试验证器

- 使用 `solana-test-validator` 进行本地测试
- 程序开发使用 `solana-program-test`
- 集成测试使用 `local-cluster`

## CI/CD

- CI 使用 Buildkite
- 自动运行测试、clippy、fmt 检查
- PR 需要 CI 通过才能合并
- 使用 `.mergify.yml` 自动化合并小 PR

## 资源链接

- **Jito GitBook**: https://jito-foundation.gitbook.io/mev/jito-solana
- **Anza 文档**: https://docs.anza.xyz
- **GitHub 仓库**: https://github.com/jito-foundation/jito-solana
- **问题追踪**: GitHub Issues
