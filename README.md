# 客运抽样扩推台

城际客运统计员把问询回收与班次出票表相联，按票号复核重访，按当前分层扩推各问项人数。入口默认展示「重访与改层」样例。

## 运行

`docker compose up --build` 后访问 `http://localhost:18473`。本机可安装 `requirements.txt`，执行 `python -m app.main`。归档数据库由 `SURVEY_ARCHIVE` 指定，默认 `var/survey.db`。停止服务后移除该数据库或 Compose 命名卷可重新试跑。

## 复核路线

1. 在首页查看有效矩阵、样本阶梯和偏差横条，核对 290 人 = 250 人扩推 + 40 人不可推断。
2. 到班次与分层校验查票号 `00011` 改入枢纽，到非响应权重校准查基础权 3、校准后 50。
3. 在扩推整数分配切换城北与枢纽，查看余数及补 1 的类别。
4. 打开批次留档复跑，归档并复算。进入样本证据签发，下载带隔离行和规则版本的 JSON。

`GET /api/survey/<stage>` 执行样例阶段，阶段名见 [DEPTH](docs/DEPTH.md)。向同一路径 POST `{"tables":{"returns":"...","frame":"..."}}` 可复核自己的 CSV。`POST /api/runs` 提交同样的 `tables` 或 `{"sample":"dirty"}`。`GET /api/runs/<id>` 查档，`POST /api/runs/<id>/rerun` 复算，`GET /api/export/<id>` 领取证据。

字段和计算规则详见 [数据字典](docs/DATA-DICTIONARY.md)。本机测试执行 `python -m pytest -q`。
