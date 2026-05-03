<details>
<summary><strong>2. 技术栈</strong> - 技术栈选型、组合案例与学习路径。（点击展开/收起）</summary>

<a id="reference-technology-stack"></a>

## 2. 技术栈

> 技术栈选型、组合案例与学习路径。

> 本文件是技术栈参考入口，帮助读者理解软件系统通常由哪些技术层组成、不同场景如何组合技术栈、初学者应该如何选择学习路径。

<a id="reference-technology-stack-核心摘要"></a>
### 核心摘要

技术栈不是单个框架或语言，而是一组完成系统交付所需的技术组合，包括前端、后端、数据库、缓存、部署、监控、测试、AI、数据工程、安全和运维工具。选择技术栈时，不只看技术是否流行，还要看项目目标、团队能力、维护成本、生态成熟度、部署环境、合规要求和替换路径。

本文件适合三类场景：新手建立技术全景，开发者为项目选型，Agent 在生成方案前理解“应该优先复用哪些成熟技术组合”。

<a id="reference-technology-stack-顶部导航"></a>
### 顶部导航

| 主题 | 用途 |
|:---|:---|
| [什么是技术栈](#一什么是技术栈) | 建立基本概念，理解技术组合而非单点技术 |
| [技术栈通常包含哪些部分](#二技术栈通常包含哪些部分) | 前端、后端、数据库、部署、AI、数据、安全等层级 |
| [常见项目对应技术栈](#十三常见项目对应技术栈) | Web、移动端、桌面端、全栈、游戏、数据工程等组合案例 |
| [如何选择技术栈](#十四如何选择技术栈) | 从目标、约束、团队能力、生态成熟度和长期维护评估方案 |
| [初学者应该学什么技术栈](#十五初学者应该学什么技术栈) | 从可交付项目出发，选择最小必要技术路线 |

<a id="reference-technology-stack-使用方式"></a>
### 使用方式

- 做新项目选型时，先按项目类型定位候选技术栈，再用维护成本和成熟度筛选。
- 给 AI 提需求时，把目标平台、团队能力、部署环境、数据规模和必须规避的技术写清楚。
- 当成熟技术栈能满足需求时，遵循拼好码原则，优先复用成熟方案，不默认自研底层能力。

<a id="reference-technology-stack-一什么是技术栈"></a>
### 一、什么是技术栈

**技术栈**，英文叫 **Technology Stack**，指开发一个软件系统时使用的一整套技术、框架、语言、工具和平台。

它不是单独某一种技术，而是一个组合。

例如，一个网站可能会用：

* 前端：React、TypeScript、Tailwind CSS
* 后端：Java、Spring Boot
* 数据库：MySQL、Redis
* 部署：Docker、Nginx、Kubernetes
* 云服务：AWS
* 工具：Git、GitHub Actions

这些合起来，就是这个项目的技术栈。

---

<a id="reference-technology-stack-二技术栈通常包含哪些部分"></a>
### 二、技术栈通常包含哪些部分

<a id="reference-technology-stack-1-前端技术栈"></a>
### 1. 前端技术栈

前端负责用户看到的页面和交互。

常见内容包括：

<a id="reference-technology-stack-基础语言"></a>
#### 基础语言

* HTML：页面结构
* CSS：页面样式
* JavaScript：页面交互
* TypeScript：JavaScript 的增强版，更适合大型项目

<a id="reference-technology-stack-前端框架"></a>
#### 前端框架

* React
* Vue
* Angular
* Svelte
* SolidJS

<a id="reference-technology-stack-ui-框架和组件库"></a>
#### UI 框架和组件库

* Tailwind CSS
* Bootstrap
* Ant Design
* Element Plus
* Material UI
* Shadcn UI

<a id="reference-technology-stack-构建工具"></a>
#### 构建工具

* Vite
* Webpack
* Rollup
* Parcel
* esbuild

<a id="reference-technology-stack-状态管理"></a>
#### 状态管理

* Redux
* Zustand
* Pinia
* Vuex
* MobX
* Recoil

<a id="reference-technology-stack-前端路由"></a>
#### 前端路由

* React Router
* Vue Router
* Next.js Router
* Nuxt Router

<a id="reference-technology-stack-前端请求工具"></a>
#### 前端请求工具

* Fetch API
* Axios
* TanStack Query
* SWR

<a id="reference-technology-stack-前端测试"></a>
#### 前端测试

* Jest
* Vitest
* Cypress
* Playwright
* Testing Library

<a id="reference-technology-stack-前端常见组合"></a>
#### 前端常见组合

React 技术栈：

> React + TypeScript + Vite + Tailwind CSS + Zustand + Axios

Vue 技术栈：

> Vue 3 + TypeScript + Vite + Pinia + Vue Router + Element Plus

企业级前端技术栈：

> React + TypeScript + Next.js + Tailwind CSS + Shadcn UI + TanStack Query

---

<a id="reference-technology-stack-2-后端技术栈"></a>
### 2. 后端技术栈

后端负责业务逻辑、接口、权限、数据处理、文件处理、支付、消息通知等。

<a id="reference-technology-stack-常见后端语言"></a>
#### 常见后端语言

* Java
* Python
* JavaScript / TypeScript
* Go
* PHP
* C#
* Ruby
* Rust
* Kotlin
* Scala

<a id="reference-technology-stack-java-后端"></a>
#### Java 后端

常见技术：

* Spring Boot
* Spring MVC
* Spring Cloud
* MyBatis
* MyBatis-Plus
* Hibernate / JPA
* Maven
* Gradle

常见组合：

> Java + Spring Boot + MyBatis-Plus + MySQL + Redis

适合场景：

* 企业系统
* 电商平台
* 金融系统
* 大型后台系统
* 微服务架构

---

<a id="reference-technology-stack-python-后端"></a>
#### Python 后端

常见技术：

* Django
* Flask
* FastAPI
* SQLAlchemy
* Celery
* Pydantic
* Poetry

常见组合：

> Python + FastAPI + PostgreSQL + Redis + Celery

适合场景：

* API 服务
* 数据平台
* AI 应用
* 自动化工具
* 中小型 Web 后端

---

<a id="reference-technology-stack-nodejs-后端"></a>
#### Node.js 后端

常见技术：

* Express
* NestJS
* Koa
* Fastify
* Prisma
* TypeORM
* Sequelize

常见组合：

> Node.js + NestJS + TypeScript + Prisma + PostgreSQL

适合场景：

* 前后端统一 TypeScript
* 实时应用
* 中台系统
* API 服务
* 初创项目

---

<a id="reference-technology-stack-go-后端"></a>
#### Go 后端

常见技术：

* Gin
* Echo
* Fiber
* GORM
* Go kit
* gRPC

常见组合：

> Go + Gin + PostgreSQL + Redis + Docker

适合场景：

* 高并发服务
* 云原生系统
* 微服务
* 网关
* 基础设施工具

---

<a id="reference-technology-stack-php-后端"></a>
#### PHP 后端

常见技术：

* Laravel
* Symfony
* ThinkPHP
* Composer

常见组合：

> PHP + Laravel + MySQL + Redis

适合场景：

* 内容管理系统
* 企业官网
* 电商网站
* 快速 Web 开发

---

<a id="reference-technology-stack-c-后端"></a>
#### C# 后端

常见技术：

* ASP.NET Core
* Entity Framework Core
* LINQ
* NuGet

常见组合：

> C# + ASP.NET Core + SQL Server + Redis

适合场景：

* 企业系统
* Windows 生态
* 内部管理系统
* 大型后端服务

---

<a id="reference-technology-stack-3-数据库技术栈"></a>
### 3. 数据库技术栈

数据库负责存储、查询和管理数据。

<a id="reference-technology-stack-关系型数据库"></a>
### 关系型数据库

适合结构化数据。

常见数据库：

* MySQL
* PostgreSQL
* SQL Server
* Oracle
* SQLite
* MariaDB

适合存储：

* 用户信息
* 订单信息
* 商品信息
* 交易记录
* 权限数据

常见组合：

> MySQL + Redis
> PostgreSQL + Prisma
> SQL Server + Entity Framework

---

<a id="reference-technology-stack-非关系型数据库"></a>
### 非关系型数据库

适合灵活结构、文档、键值、图数据等。

<a id="reference-technology-stack-文档数据库"></a>
#### 文档数据库

* MongoDB
* CouchDB

适合：

* 内容数据
* 配置数据
* 半结构化数据

<a id="reference-technology-stack-键值数据库"></a>
#### 键值数据库

* Redis
* Memcached

适合：

* 缓存
* Session
* 排行榜
* 验证码
* 分布式锁

<a id="reference-technology-stack-搜索引擎"></a>
#### 搜索引擎

* Elasticsearch
* OpenSearch
* Solr

适合：

* 全文搜索
* 日志检索
* 商品搜索
* 数据分析

<a id="reference-technology-stack-图数据库"></a>
#### 图数据库

* Neo4j
* ArangoDB

适合：

* 社交关系
* 推荐系统
* 知识图谱
* 风控关系分析

<a id="reference-technology-stack-时序数据库"></a>
#### 时序数据库

* InfluxDB
* TimescaleDB
* Prometheus

适合：

* 监控数据
* 物联网数据
* 设备指标
* 时间序列分析

---

<a id="reference-technology-stack-三移动端技术栈"></a>
### 三、移动端技术栈

移动端负责开发手机 App。

<a id="reference-technology-stack-ios-原生开发"></a>
### iOS 原生开发

语言和工具：

* Swift
* Objective-C
* Xcode
* SwiftUI
* UIKit

适合：

* iPhone App
* iPad App
* Apple Watch App
* 高性能 iOS 应用

组合：

> Swift + SwiftUI + Combine + CoreData

---

<a id="reference-technology-stack-android-原生开发"></a>
### Android 原生开发

语言和工具：

* Kotlin
* Java
* Android Studio
* Jetpack Compose
* XML Layout

适合：

* Android 手机 App
* 平板 App
* Android TV
* 原生高性能应用

组合：

> Kotlin + Jetpack Compose + Retrofit + Room

---

<a id="reference-technology-stack-跨平台移动开发"></a>
### 跨平台移动开发

一套代码开发多个平台。

常见技术：

* Flutter
* React Native
* Ionic
* Expo
* Kotlin Multiplatform
* .NET MAUI

常见组合：

> Flutter + Dart + Firebase
> React Native + TypeScript + Expo

适合：

* 初创产品
* 多端快速开发
* 中小型 App
* 需要同时支持 iOS 和 Android 的项目

---

<a id="reference-technology-stack-四桌面端技术栈"></a>
### 四、桌面端技术栈

桌面端用于开发 Windows、macOS、Linux 软件。

常见技术：

* Electron
* Tauri
* Qt
* WPF
* WinUI
* JavaFX
* Avalonia
* Flutter Desktop

常见组合：

> Electron + React + TypeScript
> Tauri + Rust + Vue
> C# + WPF + SQL Server
> Qt + C++

适合：

* 桌面客户端
* 编辑器
* 企业内部软件
* 跨平台工具
* 即时通讯软件

---

<a id="reference-technology-stack-五全栈技术栈"></a>
### 五、全栈技术栈

全栈是指前端、后端、数据库、部署都能覆盖。

常见全栈组合：

<a id="reference-technology-stack-mern"></a>
### MERN

> MongoDB + Express + React + Node.js

适合：

* 初创项目
* SaaS
* Web 应用
* 快速原型

<a id="reference-technology-stack-mean"></a>
### MEAN

> MongoDB + Express + Angular + Node.js

适合：

* 企业级前端
* 大型后台系统

<a id="reference-technology-stack-mevn"></a>
### MEVN

> MongoDB + Express + Vue + Node.js

适合：

* Vue 项目
* 中小型 Web 应用

<a id="reference-technology-stack-pern"></a>
### PERN

> PostgreSQL + Express + React + Node.js

适合：

* 结构化数据较多的 Web 应用
* SaaS
* 管理后台

<a id="reference-technology-stack-t3-stack"></a>
### T3 Stack

> TypeScript + Next.js + tRPC + Prisma + Tailwind CSS

适合：

* 类型安全的全栈项目
* 现代 Web 应用
* 快速开发

<a id="reference-technology-stack-django-全栈"></a>
### Django 全栈

> Python + Django + PostgreSQL + Redis + Celery

适合：

* 内容平台
* 管理系统
* 数据型应用
* 中小企业系统

<a id="reference-technology-stack-spring-boot-全栈"></a>
### Spring Boot 全栈

> Java + Spring Boot + Vue / React + MySQL + Redis

适合：

* 企业系统
* 电商平台
* 后台管理系统
* 中大型项目

---

<a id="reference-technology-stack-六devops-和部署技术栈"></a>
### 六、DevOps 和部署技术栈

DevOps 负责让项目自动化构建、测试、部署、监控和运维。

<a id="reference-technology-stack-操作系统"></a>
### 操作系统

* Linux
* Ubuntu
* CentOS
* Debian
* Alpine Linux
* Windows Server

<a id="reference-technology-stack-web-服务器"></a>
### Web 服务器

* Nginx
* Apache
* Caddy
* IIS

<a id="reference-technology-stack-容器技术"></a>
### 容器技术

* Docker
* Docker Compose
* Podman

<a id="reference-technology-stack-容器编排"></a>
### 容器编排

* Kubernetes
* Docker Swarm
* Nomad
* OpenShift

<a id="reference-technology-stack-cicd"></a>
### CI/CD

* GitHub Actions
* GitLab CI
* Jenkins
* CircleCI
* Travis CI
* Argo CD
* Tekton

<a id="reference-technology-stack-云平台"></a>
### 云平台

* AWS
* Microsoft Azure
* Google Cloud
* 阿里云
* 腾讯云
* 华为云
* Cloudflare
* Vercel
* Netlify
* Railway
* Render
* Fly.io

<a id="reference-technology-stack-基础设施即代码"></a>
### 基础设施即代码

* Terraform
* Pulumi
* Ansible
* Chef
* Puppet

<a id="reference-technology-stack-监控和日志"></a>
### 监控和日志

* Prometheus
* Grafana
* ELK Stack
* Loki
* Datadog
* New Relic
* Sentry
* OpenTelemetry

常见部署组合：

> Docker + Nginx + GitHub Actions + AWS
> Kubernetes + Helm + Argo CD + Prometheus + Grafana
> Vercel + Next.js + Supabase

---

<a id="reference-technology-stack-七ai-机器学习技术栈"></a>
### 七、AI / 机器学习技术栈

AI 技术栈用于机器学习、深度学习、大模型应用、数据处理等。

<a id="reference-technology-stack-编程语言"></a>
### 编程语言

* Python
* R
* Julia
* C++
* Scala

<a id="reference-technology-stack-数据处理"></a>
### 数据处理

* NumPy
* Pandas
* Polars
* Dask
* Spark

<a id="reference-technology-stack-机器学习"></a>
### 机器学习

* Scikit-learn
* XGBoost
* LightGBM
* CatBoost

<a id="reference-technology-stack-深度学习"></a>
### 深度学习

* PyTorch
* TensorFlow
* Keras
* JAX

<a id="reference-technology-stack-大模型应用"></a>
### 大模型应用

* OpenAI API
* Anthropic API
* Gemini API
* LangChain
* LlamaIndex
* Haystack
* Transformers
* vLLM
* Ollama
* Hugging Face

<a id="reference-technology-stack-向量数据库"></a>
### 向量数据库

* Pinecone
* Weaviate
* Milvus
* Qdrant
* Chroma
* FAISS

<a id="reference-technology-stack-mlops"></a>
### MLOps

* MLflow
* Kubeflow
* Weights & Biases
* DVC
* Airflow
* Prefect

常见 AI 应用栈：

> Python + FastAPI + OpenAI API + PostgreSQL + Redis + Docker

RAG 应用栈：

> LangChain + OpenAI API + Chroma / Pinecone + FastAPI + React

机器学习训练栈：

> Python + Pandas + Scikit-learn + XGBoost + MLflow

深度学习训练栈：

> Python + PyTorch + Transformers + Hugging Face + Weights & Biases

---

<a id="reference-technology-stack-八数据工程技术栈"></a>
### 八、数据工程技术栈

数据工程负责采集、清洗、存储、计算和分析数据。

<a id="reference-technology-stack-数据采集"></a>
### 数据采集

* Kafka
* RabbitMQ
* Flume
* Logstash
* Debezium

<a id="reference-technology-stack-数据存储"></a>
### 数据存储

* Hadoop HDFS
* Amazon S3
* MinIO
* Hive
* HBase

<a id="reference-technology-stack-数据计算"></a>
### 数据计算

* Spark
* Flink
* Presto
* Trino
* Beam

<a id="reference-technology-stack-数据仓库"></a>
### 数据仓库

* Snowflake
* BigQuery
* Redshift
* ClickHouse
* Doris
* StarRocks

<a id="reference-technology-stack-数据调度"></a>
### 数据调度

* Airflow
* Prefect
* Dagster
* DolphinScheduler
* Azkaban

<a id="reference-technology-stack-数据可视化"></a>
### 数据可视化

* Tableau
* Power BI
* Superset
* Metabase
* Looker

常见组合：

> Kafka + Spark + Hive + Airflow + Superset
> dbt + Snowflake + Airflow + Tableau
> Flink + Kafka + ClickHouse + Grafana

---

<a id="reference-technology-stack-九游戏开发技术栈"></a>
### 九、游戏开发技术栈

游戏开发技术栈包括游戏引擎、图形渲染、物理系统、网络通信等。

<a id="reference-technology-stack-游戏引擎"></a>
### 游戏引擎

* Unity
* Unreal Engine
* Godot
* Cocos Creator

<a id="reference-technology-stack-游戏开发语言"></a>
### 游戏开发语言

* C#
* C++
* Lua
* GDScript
* JavaScript
* Python

<a id="reference-technology-stack-图形技术"></a>
### 图形技术

* OpenGL
* Vulkan
* DirectX
* Metal
* WebGPU

<a id="reference-technology-stack-常见组合"></a>
### 常见组合

Unity 游戏：

> Unity + C# + Blender + Photon

Unreal 游戏：

> Unreal Engine + C++ + Blueprint + Quixel

Web 游戏：

> Phaser + JavaScript + WebGL

---

<a id="reference-technology-stack-十嵌入式和物联网技术栈"></a>
### 十、嵌入式和物联网技术栈

用于硬件设备、传感器、智能家居、工业控制等。

<a id="reference-technology-stack-编程语言-2"></a>
### 编程语言

* C
* C++
* Rust
* MicroPython
* Assembly

<a id="reference-technology-stack-硬件平台"></a>
### 硬件平台

* Arduino
* Raspberry Pi
* ESP32
* STM32
* Nordic nRF
* Jetson Nano

<a id="reference-technology-stack-操作系统-2"></a>
### 操作系统

* FreeRTOS
* Zephyr
* Embedded Linux
* RT-Thread

<a id="reference-technology-stack-通信协议"></a>
### 通信协议

* MQTT
* CoAP
* Bluetooth
* Zigbee
* LoRa
* Modbus
* CAN
* HTTP

常见组合：

> ESP32 + FreeRTOS + MQTT + AWS IoT
> STM32 + C + FreeRTOS + CAN
> Raspberry Pi + Python + MQTT + Home Assistant

---

<a id="reference-technology-stack-十一区块链技术栈"></a>
### 十一、区块链技术栈

用于开发智能合约、钱包、去中心化应用等。

<a id="reference-technology-stack-智能合约语言"></a>
### 智能合约语言

* Solidity
* Rust
* Move
* Vyper

<a id="reference-technology-stack-区块链平台"></a>
### 区块链平台

* Ethereum
* Solana
* Polygon
* BNB Chain
* Aptos
* Sui

<a id="reference-technology-stack-开发工具"></a>
### 开发工具

* Hardhat
* Foundry
* Truffle
* Remix

<a id="reference-technology-stack-web3-前端"></a>
### Web3 前端

* ethers.js
* web3.js
* wagmi
* viem
* RainbowKit

常见组合：

> Solidity + Hardhat + ethers.js + React
> Rust + Solana + Anchor + React
> Move + Aptos + TypeScript

---

<a id="reference-technology-stack-十二网络安全技术栈"></a>
### 十二、网络安全技术栈

用于安全测试、防护、审计和监控。

<a id="reference-technology-stack-安全测试"></a>
### 安全测试

* Burp Suite
* OWASP ZAP
* Nmap
* Metasploit
* Wireshark
* SQLMap

<a id="reference-technology-stack-安全开发"></a>
### 安全开发

* OAuth 2.0
* OpenID Connect
* JWT
* HTTPS / TLS
* RBAC
* ABAC

<a id="reference-technology-stack-安全监控"></a>
### 安全监控

* SIEM
* Wazuh
* Splunk
* ELK
* Suricata
* Zeek

<a id="reference-technology-stack-代码安全"></a>
### 代码安全

* SonarQube
* Snyk
* Dependabot
* Trivy
* Checkmarx

---

<a id="reference-technology-stack-十三常见项目对应技术栈"></a>
### 十三、常见项目对应技术栈

<a id="reference-technology-stack-个人博客"></a>
### 个人博客

简单版：

> HTML + CSS + JavaScript

现代版：

> Next.js + Markdown + Tailwind CSS + Vercel

后端版：

> Django + PostgreSQL + Nginx + Docker

---

<a id="reference-technology-stack-企业官网"></a>
### 企业官网

> Vue / React + Tailwind CSS + Nuxt / Next.js + Vercel

---

<a id="reference-technology-stack-后台管理系统"></a>
### 后台管理系统

> Vue 3 + TypeScript + Vite + Pinia + Element Plus
> React + TypeScript + Ant Design + React Router + Axios

---

<a id="reference-technology-stack-电商系统"></a>
### 电商系统

> React / Vue + Java Spring Boot + MySQL + Redis + Elasticsearch + RabbitMQ

---

<a id="reference-technology-stack-即时聊天系统"></a>
### 即时聊天系统

> React + Node.js + WebSocket + Redis + MongoDB

---

<a id="reference-technology-stack-在线教育平台"></a>
### 在线教育平台

> React + Spring Boot + MySQL + Redis + OSS + WebRTC

---

<a id="reference-technology-stack-saas-系统"></a>
### SaaS 系统

> Next.js + TypeScript + PostgreSQL + Prisma + Stripe + Vercel

---

<a id="reference-technology-stack-ai-聊天机器人"></a>
### AI 聊天机器人

> React + FastAPI + OpenAI API + PostgreSQL + Redis + Vector Database

---

<a id="reference-technology-stack-短视频平台"></a>
### 短视频平台

> Flutter / React Native + Go / Java + MySQL + Redis + Kafka + CDN + Object Storage

---

<a id="reference-technology-stack-物联网平台"></a>
### 物联网平台

> ESP32 + MQTT + Node.js / Go + TimescaleDB + Grafana

---

<a id="tech-stack-selection"></a>
<a id="reference-technology-stack-十四如何选择技术栈"></a>
### 十四、如何选择技术栈

选择技术栈时，主要看以下因素：

<a id="reference-technology-stack-1-项目类型"></a>
### 1. 项目类型

不同项目适合不同技术。

网站：

> React、Vue、Next.js、Nuxt

企业系统：

> Java、Spring Boot、Vue、MySQL

AI 应用：

> Python、FastAPI、PyTorch、OpenAI API

移动 App：

> Flutter、React Native、Swift、Kotlin

高并发服务：

> Go、Java、Redis、Kafka

---

<a id="reference-technology-stack-2-团队能力"></a>
### 2. 团队能力

如果团队熟悉 Java，就优先选 Java。

如果团队熟悉 JavaScript，就可以选：

> React + Node.js

如果团队熟悉 Python，就可以选：

> Django / FastAPI

技术栈不是越新越好，而是团队能不能稳定开发和维护。

---

<a id="reference-technology-stack-3-项目规模"></a>
### 3. 项目规模

小项目：

> Vue / React + Firebase / Supabase

中型项目：

> React / Vue + Node.js / Django / Spring Boot + PostgreSQL

大型项目：

> Spring Boot / Go + 微服务 + Kubernetes + Redis + Kafka + Elasticsearch

---

<a id="reference-technology-stack-4-性能要求"></a>
### 4. 性能要求

普通网站：

> Node.js、Python、PHP、Java 都可以

高并发系统：

> Go、Java、Rust、Redis、Kafka

计算密集型系统：

> C++、Rust、Go、Python + C++ 扩展

AI 训练：

> Python + PyTorch + GPU

---

<a id="reference-technology-stack-5-成本"></a>
### 5. 成本

低成本上线：

> Next.js + Vercel + Supabase
> Vue + Firebase
> Django + SQLite / PostgreSQL

企业级部署：

> Kubernetes + 云服务器 + 数据库集群 + CI/CD

---

<a id="reference-technology-stack-6-生态成熟度"></a>
### 6. 生态成熟度

成熟生态通常意味着：

* 教程多
* 问题容易搜索
* 招人容易
* 插件多
* 社区活跃
* 维护成本低

比如：

* Java + Spring Boot
* Python + Django / FastAPI
* JavaScript + React / Vue
* Go + Gin
* PHP + Laravel

---

<a id="reference-technology-stack-十五初学者应该学什么技术栈"></a>
### 十五、初学者应该学什么技术栈

<a id="reference-technology-stack-如果你想做网页前端"></a>
### 如果你想做网页前端

推荐路线：

1. HTML
2. CSS
3. JavaScript
4. TypeScript
5. React 或 Vue
6. Vite
7. Tailwind CSS
8. Git
9. 一个后端基础

推荐组合：

> HTML + CSS + JavaScript + React + TypeScript + Vite

---

<a id="reference-technology-stack-如果你想做后端"></a>
### 如果你想做后端

推荐路线：

1. 一门后端语言
2. 数据库
3. Web 框架
4. API
5. 权限认证
6. 缓存
7. Docker
8. 部署

Java 路线：

> Java + Spring Boot + MySQL + Redis

Python 路线：

> Python + FastAPI / Django + PostgreSQL + Redis

Node.js 路线：

> TypeScript + Node.js + NestJS + PostgreSQL

Go 路线：

> Go + Gin + PostgreSQL + Redis

---

<a id="reference-technology-stack-如果你想做全栈"></a>
### 如果你想做全栈

推荐两条路线：

<a id="reference-technology-stack-路线一javascript-typescript-全栈"></a>
#### 路线一：JavaScript / TypeScript 全栈

> HTML + CSS + JavaScript + TypeScript + React + Node.js + PostgreSQL

进阶：

> Next.js + Prisma + PostgreSQL + Tailwind CSS

<a id="reference-technology-stack-路线二java-企业全栈"></a>
#### 路线二：Java 企业全栈

> Vue + Java + Spring Boot + MySQL + Redis

---

<a id="reference-technology-stack-如果你想做-ai"></a>
### 如果你想做 AI

推荐路线：

1. Python
2. NumPy
3. Pandas
4. Scikit-learn
5. PyTorch
6. FastAPI
7. 向量数据库
8. 大模型 API
9. Docker

推荐组合：

> Python + PyTorch + FastAPI + OpenAI API + PostgreSQL + Vector Database

---

<a id="reference-technology-stack-十六技术栈的层级结构"></a>
### 十六、技术栈的层级结构

可以把技术栈理解成这样：

```text
应用层：
React、Vue、Flutter、Spring Boot、Django、FastAPI

语言层：
JavaScript、TypeScript、Java、Python、Go、C#、C++

数据层：
MySQL、PostgreSQL、MongoDB、Redis、Elasticsearch

基础设施层：
Linux、Docker、Kubernetes、Nginx、云服务器

工程工具层：
Git、GitHub、CI/CD、测试工具、监控工具
```

更完整的结构：

```text
用户界面
  ↓
前端框架
  ↓
API 通信
  ↓
后端服务
  ↓
业务逻辑
  ↓
数据库 / 缓存 / 消息队列
  ↓
服务器 / 容器 / 云平台
  ↓
监控 / 日志 / 安全 / 自动化部署
```

---

<a id="reference-technology-stack-十七技术栈示例总表"></a>
### 十七、技术栈示例总表

| 项目类型   | 推荐技术栈                                                  |
| ------ | ------------------------------------------------------ |
| 个人博客   | Next.js + Markdown + Tailwind CSS + Vercel             |
| 企业官网   | Vue / React + Nuxt / Next.js + Tailwind CSS            |
| 后台管理系统 | Vue 3 + TypeScript + Vite + Pinia + Element Plus       |
| 电商系统   | Spring Boot + MySQL + Redis + Elasticsearch + RabbitMQ |
| SaaS   | Next.js + TypeScript + Prisma + PostgreSQL + Stripe    |
| AI 应用  | Python + FastAPI + OpenAI API + PostgreSQL + 向量数据库     |
| 移动 App | Flutter / React Native / Swift / Kotlin                |
| 桌面软件   | Electron / Tauri / Qt / WPF                            |
| 高并发服务  | Go / Java + Redis + Kafka + Kubernetes                 |
| 数据平台   | Kafka + Spark + Airflow + ClickHouse                   |
| 游戏     | Unity + C# / Unreal + C++                              |
| 物联网    | ESP32 + MQTT + Go / Node.js + TimescaleDB              |
| 区块链    | Solidity + Hardhat + ethers.js + React                 |

---

<a id="reference-technology-stack-十八常见误区"></a>
### 十八、常见误区

<a id="reference-technology-stack-误区一技术栈越多越厉害"></a>
### 误区一：技术栈越多越厉害

不是。

技术栈越多，维护成本越高。

小项目不要一上来就用：

> Kubernetes + 微服务 + Kafka + Elasticsearch

可能会过度设计。

---

<a id="reference-technology-stack-误区二只追求最新技术"></a>
### 误区二：只追求最新技术

新技术不一定稳定。

选技术时要考虑：

* 是否成熟
* 是否有人维护
* 是否容易招聘
* 是否适合项目
* 是否容易部署
* 是否容易排错

---

<a id="reference-technology-stack-误区三前端只会框架不懂基础"></a>
### 误区三：前端只会框架，不懂基础

React、Vue 很重要，但 HTML、CSS、JavaScript 基础更重要。

---

<a id="reference-technology-stack-误区四后端只会写接口不懂数据库"></a>
### 误区四：后端只会写接口，不懂数据库

后端必须理解：

* SQL
* 索引
* 事务
* 缓存
* 并发
* 安全
* 日志
* 部署

---

<a id="reference-technology-stack-误区五会技术栈等于会做项目"></a>
### 误区五：会技术栈等于会做项目

会技术只是第一步。

真正做项目还需要：

* 需求分析
* 数据库设计
* 接口设计
* 权限设计
* 异常处理
* 测试
* 部署
* 维护
* 性能优化

---

<a id="reference-technology-stack-十九一个完整-web-项目的技术栈案例"></a>
### 十九、一个完整 Web 项目的技术栈案例

假设做一个在线商城。

<a id="reference-technology-stack-前端"></a>
### 前端

* React
* TypeScript
* Vite
* Tailwind CSS
* React Router
* Zustand
* Axios
* TanStack Query

负责：

* 商品列表
* 购物车
* 登录注册
* 订单页面
* 支付页面
* 用户中心

<a id="reference-technology-stack-后端"></a>
### 后端

* Java
* Spring Boot
* Spring Security
* MyBatis-Plus
* Maven

负责：

* 用户管理
* 商品管理
* 订单管理
* 支付接口
* 权限认证
* 后台管理接口

<a id="reference-technology-stack-数据库"></a>
### 数据库

* MySQL：存储用户、商品、订单
* Redis：缓存、验证码、购物车、Session
* Elasticsearch：商品搜索
* RabbitMQ：订单消息、库存扣减

<a id="reference-technology-stack-文件存储"></a>
### 文件存储

* 阿里云 OSS / AWS S3

负责：

* 商品图片
* 用户头像
* 视频资料

<a id="reference-technology-stack-部署"></a>
### 部署

* Linux
* Docker
* Nginx
* GitHub Actions
* 云服务器

<a id="reference-technology-stack-监控"></a>
### 监控

* Prometheus
* Grafana
* Sentry
* ELK

完整技术栈可以写成：

> React + TypeScript + Vite + Tailwind CSS + Java + Spring Boot + MySQL + Redis + Elasticsearch + RabbitMQ + Docker + Nginx + GitHub Actions + Prometheus + Grafana

---

<a id="reference-technology-stack-二十面试中如何介绍自己的技术栈"></a>
### 二十、面试中如何介绍自己的技术栈

可以这样说：

> 我主要使用 Java 后端技术栈，熟悉 Spring Boot、MyBatis、MySQL、Redis，也了解消息队列、Docker 和 Linux 部署。前端方面使用过 Vue 3、TypeScript、Vite 和 Element Plus，能够独立完成后台管理系统的前后端开发。

前端方向可以这样说：

> 我主要使用 React / Vue 前端技术栈，熟悉 HTML、CSS、JavaScript、TypeScript，掌握组件化开发、路由、状态管理、接口请求、前端工程化和基础性能优化。

全栈方向可以这样说：

> 我熟悉 TypeScript 全栈开发，前端使用 React 和 Next.js，后端使用 Node.js、NestJS，数据库使用 PostgreSQL，ORM 使用 Prisma，部署方面了解 Docker、Vercel 和 GitHub Actions。

---

<a id="reference-technology-stack-二十一总结"></a>
### 二十一、总结

技术栈就是软件开发中使用的一整套技术组合。

它通常包括：

```text
编程语言
前端框架
后端框架
数据库
缓存
消息队列
搜索引擎
测试工具
构建工具
部署工具
云平台
监控工具
安全工具
开发协作工具
```

学习技术栈时，不要只背名字，而要理解：

```text
它解决什么问题？
它适合什么场景？
它和其他技术怎么配合？
它在项目中处于哪一层？
它有什么优点和缺点？
```

对初学者来说，推荐先掌握一条主线：

前端路线：

> HTML + CSS + JavaScript + TypeScript + React / Vue

后端路线：

> Java + Spring Boot + MySQL + Redis

Python 路线：

> Python + FastAPI / Django + PostgreSQL

全栈路线：

> TypeScript + React + Node.js + PostgreSQL

AI 路线：

> Python + PyTorch + FastAPI + 大模型 API

真正重要的不是“知道很多技术名词”，而是能用合适的技术栈，把一个项目稳定、清晰、可维护地做出来。

</details>
