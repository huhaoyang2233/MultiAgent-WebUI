#!/bin/bash

echo "正在安装依赖包..."
npm install

echo ""
echo "依赖安装完成！正在启动开发服务器..."
echo ""
echo "项目将在浏览器中自动打开 http://localhost:3000"
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev
