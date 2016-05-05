$def with ()
$var title: 新用户注册
<div style="width:400px;margin:100px auto">
    <form method="POST" action="/register">
        <div class="row">
            <div class="formLeft">Email:</div>
            <div class="formRight"><input type="text" name="email"></div>
        </div>
        <div class="row">
            <div class="formLeft">密码:</div>
            <div class="formRight"><input type="password" name="password"></div>
        </div>
        <div class="row">
            <div class="formLeft">真实姓名:</div>
            <div class="formRight"><input type="text" name="name"></div>
        </div>
        <div>
            <input type="submit" value="提交注册">
        </div>
    </form>
</div>
