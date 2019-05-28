# 关于用户验证

传输过程使用 HTTPS 保证传输安全。

用户验证的 salt 使用 Python 3 内置库 secrets.token_hex(8) 生成 16 位字符串。

用户验证可以使用 APIKEY 或者 前端界面使用的 USR_TOKEN 方式验证，这几个参数由前端保存到站点的 LocalStorage，由 jQuery 读出后按照 API 文档作为 Header 方式发送出来。

# 内部API

`/api/payment/callback` API 回调 Webhook，用于对接支付网关。

`/api/admin/review` 用于前端页面的管理员审核用户报错页面。采用类 RestFul API 设计。

# 关于系统内部的变量与验证状态传递

系统的前端使用 USR_TOKEN 24h 内有效，APIKEY 永久有效，用户重置密码时会被重置。

用户的每一个请求都应当携带对应请求头用于验证身份，每一个表单都应当携带时间戳用于抗重放攻击。

## 用户 Token 验证函数

由于系统特殊性，这个系统的用户需要人工添加。

用户每次登陆前端，应当优先调用 `/api/user/login` 拉取新的 token，系统将 revoke 原有 token。

登陆后的每次请求，使用 `check_batcredential()` 验证，返回如下：

- 类型：元组
- (None,-1) 上传的验证凭据为空
- (None,-2) 内部错误或验证凭据无效，联系管理员
- (Username,0) 通过，普通用户，Token 方式，前端登陆
- (Username,8) 通过，VIP用户，Token 方式，前端登陆
- (Username,9) 通过，管理员用户，Token 方式，前端登陆
- (Username,2) 通过，不区分用户，APIKEY 方式，开发者调用 API

用户验证函数返回的唯一用户名将用于下一步处理与进一步表示用户事件。

## 用户登陆表单验证函数

`login_process()` 读取数据库中的盐值，数据字符串必须 Encode 为 Byte 类型，然后进行 md5 带盐 hash，如果 hash 与数据库中的 hash 相符，返回 0, 否则返回 -1.

接下来，调用用户 Token 判断函数 `frontend_token_renew()`，存在 Token 且未过期，直接返回 Token，否则 Renew Token 并 Revoke。若存在异常，返回 str("-5").

# 用户上传

上传的文件或字符串应当保存在对应 `userimgs/<EVENTID>.png`，裁剪和图片预处理由 Tensorflow 后端完成。

# 系统返回 

遵守 Swagger 文档，通用和报错模板均为 `errResponse()`

# 关于订单与充值处理

充值成功的订单会自动使用数据库触发器自动处理添加账户余额。充值总额超过 100 的会在下次充值时升级为 VIP。

`process_gateway(req)` 用于处理支付网关返回的数据，目前来说为不做操作，对应的请求直接处理函数为 `recv_payment_callback()` ，一直返回 -1，正在施工。

`writeOrderData(orderjson)` 用于创建订单，最终返回订单号，`retcode` 表示处理状态。

`check_payment(orderid)` 用于检查订单状态，最终参照 API 文档返回字典。

# 踩的坑

- 数据库触发器定义异常不一定能在创建时显示出来，但插入数据时会有些莫名奇妙的错误代码，应当检查相关约束、触发器，并尽量避免使用过多触发器
- `Sqlalchemy` 使用 `session.query.filter.one()` 返回可能引起的 Exception 有：
    `InvalidRequestError`, `NoResultFound`, `MultipleResultsFound` 
    均包含在 `sqlalchemy.orm.exc.*` / `sqlalchemy.exc.*`
- 数据库为了避免 UUID 在 M-S 模式下出现全局不唯一的情况，UUID 的生成应当在处理服务器完成，而不是使用 SQL 服务器内建函数 `UUID()`
- 传输到服务器的 HTTP Form 内的数据，类型全为 String，需要自主转换
- GET 方式的 HTTP Form 实际是 HTTP URL Parameter 处理
- 前端的 jQuery 上传数据需要注意格式和请求处理，POST JSON 需要使用 `JSON.stringify()` 并设定 `Content-Type`
