$def with ()
$var title: 用户登录
<div style="width:400px;margin:100px auto">
    <form method="POST" action="/login">
        <div class="row">
            <div class="formLeft">Email:</div>
            <div class="formRight"><input type="text" name="email"></div>
        </div>
        <div class="row">
            <div class="formLeft">密码:</div>
            <div class="formRight"><input type="password" name="password"></div>
        </div>
        <div>
            <input type="submit" value="登录">
        </div>
    </form>
</div>
