***
# ***<code>内部资料，请勿外泄</code>***
***
## <span id="api-submenu-server">01. 服务器地址</span>


**正式服务器：**
  <code>https://api.health.com/m/v1.0</code>

**公网测试服：**
  <code>https://api.health.com/m/v1.0b</code>

**内部测试服：**
  <code>http://192.168.7.111:8880/m/v1.0b</code>
  
***
## <span id="api-submenu-http">02. HTTP方法</span>
<table>
    <thead>
        <tr>
            <th style="text-align:left; width:180px;">Http Method(方法)</th>
            <th style="text-align:center">功能</th>
        </tr>
    </thead>
    <tbody>
        <tr><td style="text-align:left; color:green;">GET</td><td style="text-align:left">获取：从服务器取出资源（一项或多项）。</td></tr>
        <tr><td style="text-align:left; color:#4070ec;">POST</td><td style="text-align:left">提交：向服务器提交一个数据。</td></tr>
        <tr><td style="text-align:left; color:#c7254e;">DELETE</td><td style="text-align:left">删除：从服务器删除资源。</td></tr>
    </tbody>
</table>

***
## <span id="api-submenu-http-code">03. HTTP状态码</span>
<table>
    <thead>
        <tr>
            <th style="text-align:left; width:180px;">Http Code(状态码)</th>
            <th style="text-align:center">描述</th>
        </tr>
    </thead>
    <tbody>
        <tr><td style="text-align:left; color:green;">200</td><td style="text-align:left; color:green;">服务器成功返回用户请求的数据。</td></tr>
        <tr><td style="text-align:left; color:#c7254e;">404</td><td style="text-align:left; color:#c7254e;">用户发出的请求有错误，接口不存在，服务器没有进行新建或修改数据的操作。</td></tr>
        <tr><td style="text-align:left; color:#c7254e;">405</td><td style="text-align:left; color:#c7254e;">请求的方法不被允许 比如只提供 get 方法 请求的是 post。</td></tr>
        <tr><td style="text-align:left; color:#c7254e;">500</td><td style="text-align:left; color:#c7254e;">服务器发生错误，用户将无法判断发出的请求是否成功。</td></tr>
    </tbody>
</table>

***
## <span id="api-submenu-return">05. 返回数据JSON结构</span>
接口返回的结构定义，此API文档中"JSON.result"中返回的数据仅包含在接口成功后的result的返回对象，如下所示：

    {
        "code": 0,                         # 返回代码：[0=正常, 非0=错误代码]
        "result": {                        # 返回对象：子属性为各种返回的数据，例如：
            "user": {...},
            "msg": "无效的用户"              # 当返回代码非0时返回的错误消息
        },
        "timestamp": 1486743420            # 时间戳，用来校准客户端时间戳
    }
    
***
## <span id="api-submenu-result-code">06. 返回状态码定义</span>
<table>
    <thead>
        <tr><th style="text-align:left; width:180px;">JSON Code(状态码)</th><th style="text-align:center">描述</th></tr>
    </thead>
    <tbody>
        <tr><td style="text-align:left">0</td><td style="text-align:left">成功：服务器成功返回用户请求的数据。</td></tr>
        <tr><td style="text-align:left">10000</td><td style="text-align:left">不正确的接口调用：请求参数不足或格式错误，具体原因参考 result.msg 返回内容。</td></tr>
        <tr><td style="text-align:left">10001</td><td style="text-align:left">AppKey 或 AppSecure 参数无效：应用不存在或已停用，或需要更新到最新版本。</td></tr>
        <tr><td style="text-align:left">10002</td><td style="text-align:left">手机设备信息无效：DeviceToken 是无效的，需要重新请求。</td></tr>
        <tr><td style="text-align:left">10003</td><td style="text-align:left">手机设备已被禁用：具体原因参考 result.msg 返回内容。</td></tr>
    </tbody>
</table>