# 展示字体

`zcool-kuaile-display.woff2` 是 **ZCOOL KuaiLe** 的本地子集，覆盖当前 410 件藏品的标题、分类名、聚落名与固定展签文字（536 个字），文件约 56 KB。新增标题若命中未覆盖的字，浏览器会回退到 `--display` 的系统字体栈，不会出现方框。

- 原字体：ZCOOL KuaiLe Regular
- 许可：SIL Open Font License 1.1，全文见 `OFL.txt`
- 重新生成：用 `pyftsubset ZCOOLKuaiLe-Regular.ttf --text-file=<标题字符集> --flavor=woff2 --no-hinting --desubroutinize --output-file=fonts/zcool-kuaile-display.woff2`
