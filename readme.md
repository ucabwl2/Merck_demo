```c++
|- figure
|- vis                // 前端插件
    |- vis.js
    |- vis.css
|- config.py
|- KG_DEMO.IPYNB      // demo 用 Notebook
|- utils.py           // 图谱可视化工具
|- demo_script.py     // demo函数包装处
```

## 环境依赖

### 安装 neo4j desktop

根据 neo4j desktop 的 license。该软件只能够用于本地的项目开发和调试，**不能够提供外部服务（即不能开启对外的 server 功能）**。neo4j desktop 中可以免费使用专业版 neo4j 所具有的全部功能，相比于 neo4j 免费社区版，它支持更多节点的储存。在本地环境下，neo4j desktop 支持一切 neo4j server 的功能。
[官网 neo4j desktop 下载链接](https://neo4j.com/download/?ref=get-started-dropdown-cta) 

### 准备知识图谱数据

从 [哈佛肺癌公开知识图谱](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/RIXLG8) 网站下载 *.zip 的文件。我们只需要用到解压后文件夹中的 `./raw/lung-cancer-graph-neo4j-2021-07-15T022024.bin` 文件。
启动 neo4j desktop 应用。首先我们停用掉默认启动的数据库，点击上方的红色 STOP。而后创建一个新的项目，点击左边 project 栏目中的 **+new** 按钮。选中我们刚刚创建的project，点击右侧的 Add -> local DBMS。创建一个空的图数据库。**注意：不要启动我们刚刚创建的这个数据库！**

<img src="readme/img/image-20221107113247677.png" alt="image-20221107113247677" style="zoom:50%;" />

打开新创建的数据库的后台终端：点击 三个黑点 **“ ··· ”**，选择 Terminal。

<img src="readme/img/image-20221107113212993.png" alt="image-20221107113212993" style="zoom:50%;" />

导入哈佛知识图谱：在终端中输入以下代码，一键导入哈佛提供的 neo4j 数据库（文件路径需要改一下)：`.\bin\neo4j-admin load --from=<你解压的哈佛文件夹路径>\raw\lung-cancer-graph-neo4j-2021-07-15T022024.bin`

## Notebook Demo 启动

1. 在 `config.py` 中配置好你的 neo4j 账户和密码。

2. python>=3.6；`pip install py2neo pandas`

3. 启动 `KG_DEMO.IPYNB`

## 备注

+ 通过 vis 进行 notebook 可视化，原理其实就是把 html 页面在 notebook 上显示。

+ 通过 py2neo 进行数据生成，其实也可以用其他的语言或 python 包来获取数据，要求是最后数据的格式符合 vis 输入要求的 `json` 格式即可。

+ HTML 生成内容都是 hard code 的，主要是为了避免系统权限导致的各种问题，比如 浏览器的禁止加载其他来源数据等。

+ 相比于 VIS.JS ，官网更推荐使用 D3.js。官网的 movie 案例就是通过 d3.js 完成的。

