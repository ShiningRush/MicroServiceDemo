# Kong

该用来存放与Kong相关的文件

包括:

- 初始化脚本
- Followme网关打包

## 初始化脚本

### 环境要求

- [Python3](https://www.python.org/downloads/)
- [Request](https://github.com/requests/requests)

### 执行

```
py ./main.py [env] [module]
```

`[env]` 为要初始化的环境，可选为：
- dev
- beta
- pro

`[module]` 为要初始化的模块，可选为：
- lagoon
- contentmanage
- common
- oabackend

例如要初始化beta环境的lagoon模块，请运行：
```
py ./main.py beta lagoon
```