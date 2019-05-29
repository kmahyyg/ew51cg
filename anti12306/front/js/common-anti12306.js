function notLoggedUser(){
    if (localStorage.getItem('X-User-Token') == null){
        document.body.style.background = "#007bff linear-gradient(to right, #0062E6, #33AEFF)";
        document.body.innerHTML = "<div class='container' style='text-align: center;'><p style='font-size: xx-large; color: snow; font-weight: bold; font-style: italic;'>Please login first!</p></div>";
        setTimeout(function(){
            console.log("Not logged in, redirect to login page.");
            window.location = '/login.html';
        }, 3500);
    }
}

function logoutCleanup(){
    $.ajax({
        url: 'https://anti12306.55lovecn.top/api/user/logout',
        type: 'get',
        dataType: 'text',
        timeout: 1500,
        headers: {'X-User-Token': localStorage.getItem('X-User-Token')},
    })
        .done(function (dataresp){
            console.log(dataresp);
        })
        .fail(function (dataresp) {
            console.log(dataresp);
        });
    localStorage.removeItem('X-User-Token');
    localStorage.removeItem('X-Username');
    return true;
}

function abuseUpload(tbtn){
    var evntid = tbtn.parentNode.parentNode.firstChild.innerText;
    var reptdt = "eventid=" + evntid + "&op=3";
    $.ajax({
        url: 'https://anti12306.55lovecn.top/api/admin/review',
        type: 'post',
        datatype: 'json',
        headers: {'X-User-Token': localStorage.getItem('X-User-Token')},
        timeout: 3000,
        data: reptdt
    })
        .done(function (resp){
            console.log(resp);
            alert(resp.retmsg);
            console.log("Report Abuse Done.");
            setTimeout(function(){
                var current_row = tbtn.parentNode.parentNode;
                var whole_tree = tbtn.parentNode.parentNode.parentNode;
                whole_tree.removeChild(current_row);
            }, 1000);
        })
        .fail(function (resp){
            console.log(resp);
            alert(resp.statusText);
            console.log("Report Abuse Failed.");
        });
}

function failRecgUpld(tbtn){
    var evntid = tbtn.parentNode.parentNode.firstChild.innerText;
    var reptdt = "eventid=" + evntid + "&op=2";
    $.ajax({
        url: 'https://anti12306.55lovecn.top/api/admin/review',
        type: 'post',
        datatype: 'json',
        headers: {'X-User-Token': localStorage.getItem('X-User-Token')},
        timeout: 3000,
        data: reptdt
    })
        .done(function (resp){
            console.log(resp);
            alert(resp.retmsg);
            console.log("Report Abuse Done.");
            setTimeout(function(){
                var current_row = tbtn.parentNode.parentNode;
                var whole_tree = tbtn.parentNode.parentNode.parentNode;
                whole_tree.removeChild(current_row);
            }, 1000);
        })
        .fail(function (resp){
            console.log(resp);
            alert(resp.statusText);
            console.log("Report Abuse Failed.");
        });
}

function userReportFail(tbtn){
    var evntid = tbtn.parentNode.parentNode.firstChild.innerText;
    $.ajax({
        url: 'https://anti12306.55lovecn.top/api/report/error',
        type: 'post',
        dataType: 'json',
        headers: {'X-User-Token': localStorage.getItem('X-User-Token')},
        timeout: 3000,
        data: "eventid=" + evntid +  "&timestamp=" + Math.floor(Date.now() / 1000)
    })
        .done(function (dataresp){
            tbtn.disabled = true;
            tbtn.value = "Reported";
            tbtn.classList.remove("btn-warning");
            tbtn.classList.add("btn-light");
            console.log("Successfully reported");
            console.log(dataresp);
            setTimeout(function(){
                var current_row = tbtn.parentNode.parentNode;
                var whole_tree = tbtn.parentNode.parentNode.parentNode;
                whole_tree.removeChild(current_row);
            }, 2000);
        })
        .fail(function (dataresp){
            tbtn.value = "Failed, Retry!";
            setTimeout(function (){tbtn.value = "Report Failure";},2000);
            console.log(dataresp);
            console.log("Failed to report");
        });
}

function padTime(number) {
    if (number < 10){
        var padded = '0' + number.toString();
        return padded;
    }
    else {return number.toString();}
}

function showTime(e){
    if (e != null){var today = new Date(e);}
    else {var today = new Date();}
    var date = today.getFullYear()+'-'+(padTime(today.getMonth()+1))+'-'+(padTime(today.getDate()));
    var time = padTime(today.getHours()) + ":" + padTime(today.getMinutes()) + ":" + padTime(today.getSeconds());
    var dateTime = time +' on '+ date;
    document.getElementById('curDateTime').innerText = dateTime;
}
