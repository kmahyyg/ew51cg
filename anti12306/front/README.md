# Anti12306

# Project Structure

## 本地部署

本地部署 Cron Job 清理错误识别、清理过期未付款订单、进行错误订单退款、清理过期 Session Token.

```http request
OPTIONS http://localhost:<PORT>/api/cron
Origin: 127.0.0.1
User-Agent: curl/7.xx
```

## Login (login.html)

- [X] | 用户登陆界面，提交表单，登陆验证。注册需要由管理员手动添加。

## Administrator (adminmp.html)

管理员面板:

- [X] | 用户重置用户凭据
- [X] | 用户异常反馈审核 (表格处理)

Datatables 真香！

## Submit (request.html)

- [X] |用户提交 OCR 请求。

## Recharge (recharge.html)

- [X] |用户创建订单，提交返回，验证订单状态。支持支付方式：Py_pay, Alipay.

## User History (history.html)

- [ ] | 返回用户已经提交的历史，允许用户提交异常反馈。

## User Center (dashboard.html)

- [X] | 用户登出，注销 Token
- [X] | 显示用户状态，显示用户具体信息

## Term of Service (ToS.html)

- [X] | 显示服务条款

## Payment Gateway Callback

- [X] | 没有人工参与的订单处理流程。

# 前端公共库

Bootstrap:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.8.2/css/all.css" integrity="sha256-39jKbsb/ty7s7+4WzbtELS4vq9udJ+MDjGTD5mtxHZ0=" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha256-YLGeXaapI0/5IgZopewRJcFXomhRMlYYjugPLSyNjTY=" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/jquery@3.4.1/dist/jquery.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.bundle.min.js" integrity="sha256-fzFFyH01cBVPYzl16KT40wqjhgPtq6FFUB6ckN2+GGw=" crossorigin="anonymous"></script>
```

