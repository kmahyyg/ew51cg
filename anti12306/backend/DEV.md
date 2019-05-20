# 关于用户验证

用户验证的 salt 使用 Python 3 内置库 secrets.token_hex(8) 生成 16 位字符串。

用户验证可以使用 APIKEY 或者 前端界面使用的 USR_TOKEN 方式验证，这几个参数由前端保存到站点的 Localstorage，由 Jquery 读出后按照 API 文档作为 Header 方式发送出来。

# 内部API

`/api/payment/callback` API 回调 Webhook，用于对接支付网关。

`/api/admin/review` 用于前端页面的管理员审核用户报错页面。采用类 RestFul API 设计。

# 关于系统内部的变量与验证状态传递

系统的前端使用 USR_TOKEN 24h 内有效，APIKEY 永久有效，用户重置密码时会被重置。

用户的每一个请求都应当携带对应请求头用于验证身份，每一个表单都应当携带时间戳用于抗重放攻击。

## 用户验证函数

用户每次登陆前端，应当优先调用 `/api/user/login` 拉取新的 token，系统将 revoke 原有 token。

登陆后的每次请求，使用 `check_batcredential()` 验证，返回如下：

- 类型：元组
- (None,-1) 上传的验证凭据为空
- (None,-2) 内部错误或验证凭据无效，联系管理员
- (Username,0) 通过，普通用户，Token 方式，前端登陆
- (Username,8) 通过，VIP用户，Token 方式，前端登陆
- (Username,9) 通过，管理员用户，Token 方式，前端登陆
- (Username,2) 通过，不区分用户，APIKEY 方式，开发者调用 API

# 系统返回 

遵守 Swagger 文档，通用和报错模板均为 `errResponse()`

# 踩的坑

- 数据库触发器定义异常不一定能在创建时显示出来，但插入数据时会有些莫名奇妙的错误代码，应当检查相关约束、触发器
- `Sqlalchemy` 使用 `session.query.filter.one()` 返回可能引起的 Exception 有：
    `InvalidRequestError`, `NoResultFound`, `MultipleResultsFound` 
    均包含在 `sqlalchemy.orm.exc.*` / `sqlalchemy.exc.*`
- 