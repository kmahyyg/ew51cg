# About Database

Database schema:

```sql
set autocommit = 0;
start transaction;
set time_zone = "+00:00";

create table users (
    username varchar(20) not null,
    password varchar(64) not null,
    is_vip tinyint(1) not null default 0,
    balance float not null default 0.0,
    apikey varchar(80) not null,
    break_law tinyint(1) not null default 0,
    salt varchar(16) not null,
    total_topup float not null default 0.0,
    primary key (username)
)engine = innodb default charset = utf8mb4 collate = utf8mb4_unicode_ci;

/* is_vip: admin 9, user 0, vip 1 */

create trigger usrpwd before insert on users
    for each row begin set new.password = md5(concat(new.password,new.salt));
end;

create trigger usrpwd2 before update on users
    for each row begin set new.password = md5(concat(new.password,new.salt));
end;

create trigger vip_change before update on users
    for each row
    begin
        if total_topup > 100 then set new.is_vip = 1;
        end if;     /* the vip status will change at the next time you recharge. */
    end;

/* The VIP judgement and user discount should be done on web backend, not here. */

create table sessions (
    username varchar(20) not null,
    usrtoken varchar(80) not null,
    logged int(11) not null default unix_timestamp(current_timestamp),
    primary key (username),
    unique key uka (username, usrtoken),
    constraint usa foreign key (username) references users (username)
)engine = innodb default charset = utf8mb4 collate = utf8mb4_unicode_ci;

create table upload (
    username varchar(20) not null,
    eventid varchar(80) not null,
    chnchars int not null,
    upltime int(11) not null default unix_timestamp(current_timestamp),
    status tinyint(1) not null default 1, /* 1=created, 0=success, 2=failed, 3=fraud*/
    primary key (eventid),
    unique key ukb (username, eventid),
    constraint usb foreign key (username) references users (username)
)engine = innodb default charset = utf8mb4 collate = utf8mb4_unicode_ci;

/* cost decrease should be done on the web backend */

create table orders (
    orderid varchar(80) not null,
    username varchar(20) not null,
    submitat int(11) not null default unix_timestamp(current_timestamp),
    amount float not null,
    gateway varchar(10) not null,
    status tinyint(1) not null,
    constraint gateway_contract check (gateway = 'alipay' or gateway = 'py_pay'),
    constraint usc foreign key (username) references users (username),
    primary key (orderid),
    unique key single_time (orderid, submitat),
    unique key anti_replay (orderid, username)
)engine = innodb default charset = utf8mb4 collate = utf8mb4_unicode_ci;

create trigger topupd after update on orders
    for each row
    begin
        if new.status = 0 then
            update users set balance = balance + new.amount where username = new.username;
            update users set total_topup = total_topup + new.amount where username = new.username;
        end if;
    end;

commit;
```

# About Web Design

Please go to [API Reference](https://ew51cg.55lovecn.top/apidocs/index.html).

