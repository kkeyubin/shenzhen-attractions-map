# 深圳周边旅游景点地图

🌐 在线访问：**https://kkeyubin.github.io/shenzhen-attractions-map/**

交互式景点地图（Leaflet），收录深圳及周边 14 个城市（深圳、东莞、惠州、广州、佛山、中山、珠海、江门、汕尾、河源、清远、肇庆、香港、澳门）共 142 个旅游景点：

- 按城市、景点类型筛选，支持名称/简介关键词搜索
- 点击标记查看 A 级评定、门票参考、简介，并可跳转高德/百度地图
- 底图可切换 OpenStreetMap 与高德地图（自动纠偏）

## 文件

| 文件 | 说明 |
| --- | --- |
| `index.html` / `map.html` | 自包含地图页面（已内联 Leaflet 1.9.4 与 Leaflet.markercluster 1.5.3），也可下载后直接用浏览器打开 |
| `attractions.csv` | 景点数据（CSV，UTF-8 BOM，坐标 WGS84） |
| `attractions.json` | 景点数据（JSON） |

坐标主要来自 OpenStreetMap Nominatim；门票价格仅供参考，请以景区官方公布为准。
