# 小米商城抢购爬虫

- 使用selenium + chrome
- 以模拟浏览器行为的方式进行自动抢购
- 运行程序时，第一次模拟登录会保存cookie，以减少后续登录耗时
- 缺点是当有验证码时无法自动登录（没有引入图像识别），相较于动态页面逆向解析的方式速度较慢