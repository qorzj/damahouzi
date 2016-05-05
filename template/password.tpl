$def with ()
$var title: 修改密码
<div style="width:400px;margin:100px auto">
    <form method="POST" action="/setting/password">
        <div class="row">
            <div class="formLeft">原密码:</div>
            <div class="formRight"><input type="password" name="old_password"></div>
        </div>
        <div class="row">
            <div class="formLeft">新密码:</div>
            <div class="formRight"><input type="password" name="password"></div>
        </div>
        <div class="row">
            <div class="formLeft">确认新密码:</div>
            <div class="formRight"><input type="password" name="password2"></div>
        </div>
        <div>
            <input type="submit" value="提交修改密码">
        </div>
    </form>
</div>
