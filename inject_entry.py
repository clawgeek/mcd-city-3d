#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在工作台 index.html 注入「城市麦当劳」浮动入口（不改动原 3D 小屋逻辑）。"""
import sys, pathlib

GAME_URL = "https://www.workbuddy.cn/space/d/6fpJOhy9hjgnF16Qq3MOsZ"

INJECT = """<!-- ===== 城市麦当劳 · 经营模拟看板 入口（追加层，不影响原 3D 小屋） ===== -->
<a id="mcd-entry" href="__GAME_URL__" target="_blank" rel="noopener"
   aria-label="打开城市麦当劳 3D 经营模拟看板" title="城市麦当劳 · 3D 经营模拟看板">
  <span class="mcd-entry-badge">M</span>
  <span class="mcd-entry-txt"><b>城市麦当劳</b><i>经营模拟看板</i></span>
</a>
<style>
  #mcd-entry{
    position:fixed; right:18px; bottom:74px; z-index:9998;
    text-decoration:none;
    display:flex; align-items:center; gap:10px;
    padding:9px 16px 9px 10px; border-radius:999px; cursor:pointer;
    background:linear-gradient(135deg,#e8a410 0%,#ffbc1f 45%,#ffd75e 100%);
    color:#2b1d00; border:1px solid rgba(255,255,255,.35);
    box-shadow:0 10px 28px rgba(0,0,0,.42), 0 0 0 0 rgba(255,188,31,.5);
    font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;
    transition:transform .18s ease, box-shadow .18s ease;
    user-select:none; -webkit-tap-highlight-color:transparent;
  }
  #mcd-entry:hover{ transform:translateY(-3px); box-shadow:0 14px 34px rgba(0,0,0,.5), 0 0 0 6px rgba(255,188,31,.16); }
  #mcd-entry:focus-visible{ outline:3px solid #fff; outline-offset:3px; }
  #mcd-entry .mcd-entry-badge{
    width:30px; height:30px; border-radius:50%; flex:0 0 30px;
    display:flex; align-items:center; justify-content:center;
    background:#c8372b; color:#ffbc1f; font-weight:900; font-size:15px;
    border:2px solid rgba(255,255,255,.55);
  }
  #mcd-entry .mcd-entry-txt{ display:flex; flex-direction:column; line-height:1.2; }
  #mcd-entry .mcd-entry-txt b{ font-size:13.5px; font-weight:800; letter-spacing:.2px; }
  #mcd-entry .mcd-entry-txt i{ font-size:10.5px; font-style:normal; opacity:.72; }
  @media (max-width:560px){
    #mcd-entry{ right:12px; bottom:16px; padding:8px 13px 8px 8px; }
    #mcd-entry .mcd-entry-txt i{ display:none; }
  }
</style>

<script>
(function(){
  if (window.__MCD_ENTRY__) return;
  window.__MCD_ENTRY__ = true;
  // 入口是原生 <a target="_blank">，浏览器默认行为即可打开游戏；
  // 这里只做一次存在性校验（防止被页面其它脚本移除）。
  function ensure(){
    var el = document.getElementById("mcd-entry");
    if (el && !el.getAttribute("href")) el.setAttribute("href", "__GAME_URL__");
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ensure);
  else ensure();
  setInterval(ensure, 2000);
})();
</script></script>
"""在工作台 index.html 注入「城市麦当劳」浮动入口（不改动原 3D 小屋逻辑）。"""
import sys, pathlib

GAME_URL = "https://www.workbuddy.cn/space/d/6fpJOhy9hjgnF16Qq3MOsZ"

INJECT = """
<!-- ===== 城市麦当劳 · 经营模拟看板 入口（追加层，不影响原 3D 小屋） ===== -->
<a id="mcd-entry" href="__GAME_URL__" target="_blank" rel="noopener"
   aria-label="打开城市麦当劳 3D 经营模拟看板" title="城市麦当劳 · 3D 经营模拟看板">
  <span class="mcd-entry-badge">M</span>
  <span class="mcd-entry-txt"><b>城市麦当劳</b><i>经营模拟看板</i></span>
</a>
<style>
  #mcd-entry{
    position:fixed; right:18px; bottom:74px; z-index:9998;
    text-decoration:none;
    display:flex; align-items:center; gap:10px;
    padding:9px 16px 9px 10px; border-radius:999px; cursor:pointer;
    background:linear-gradient(135deg,#e8a410 0%,#ffbc1f 45%,#ffd75e 100%);
    color:#2b1d00; border:1px solid rgba(255,255,255,.35);
    box-shadow:0 10px 28px rgba(0,0,0,.42), 0 0 0 0 rgba(255,188,31,.5);
    font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;
    transition:transform .18s ease, box-shadow .18s ease;
    user-select:none; -webkit-tap-highlight-color:transparent;
  }
  #mcd-entry:hover{ transform:translateY(-3px); box-shadow:0 14px 34px rgba(0,0,0,.5), 0 0 0 6px rgba(255,188,31,.16); }
  #mcd-entry:focus-visible{ outline:3px solid #fff; outline-offset:3px; }
  #mcd-entry .mcd-entry-badge{
    width:30px; height:30px; border-radius:50%; flex:0 0 30px;
    display:flex; align-items:center; justify-content:center;
    background:#c8372b; color:#ffbc1f; font-weight:900; font-size:15px;
    border:2px solid rgba(255,255,255,.55);
  }
  #mcd-entry .mcd-entry-txt{ display:flex; flex-direction:column; line-height:1.2; }
  #mcd-entry .mcd-entry-txt b{ font-size:13.5px; font-weight:800; letter-spacing:.2px; }
  #mcd-entry .mcd-entry-txt i{ font-size:10.5px; font-style:normal; opacity:.72; }
  @media (max-width:560px){
    #mcd-entry{ right:12px; bottom:16px; padding:8px 13px 8px 8px; }
    #mcd-entry .mcd-entry-txt i{ display:none; }
  }
</style>
<script>
(function(){
  if (window.__MCD_ENTRY__) return;
  window.__MCD_ENTRY__ = true;
  var URL_GAME = "__GAME_URL__";
  function openGame(){
    // 优先新标签打开；被浏览器/iframe 策略拦截时回退为当前窗口跳转
    var w = null;
    try { w = window.open(URL_GAME, "_blank"); } catch(e) { w = null; }
    if (!w || w.closed) {
      try { window.top.location.href = URL_GAME; }
      catch(e) { window.location.href = URL_GAME; }
    }
  }
  window.openMcdGame = openGame;
  window.closeMcdGame = closeGame;
  function mount(){
    if (document.getElementById("mcd-entry")) return;
    var el = document.createElement("div");
    el.id = "mcd-entry";
    el.setAttribute("role", "button");
    el.setAttribute("tabindex", "0");
    el.setAttribute("aria-label", "打开城市麦当劳经营模拟看板");
    el.title = "城市麦当劳 · 经营模拟看板";
    el.innerHTML = '<span class="mcd-entry-badge">M</span>' +
                   '<span class="mcd-entry-txt"><b>城市麦当劳</b><i>经营模拟看板</i></span>';
    el.addEventListener("click", openGame);
    el.addEventListener("keydown", function(e){
      if (e.key === "Enter" || e.key === " "){ e.preventDefault(); openGame(); }
    });
    document.body.appendChild(el);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mount);
  else mount();
})();
</script>
"""

path = pathlib.Path(sys.argv[1])
html = path.read_text(encoding="utf-8")
if "mcd-entry" in html:
    print("ALREADY_PRESENT")
    sys.exit(0)

block = INJECT.replace("__GAME_URL__", GAME_URL)
idx = html.rfind("</body>")
if idx == -1:
    print("NO_BODY_TAG")
    sys.exit(1)
new_html = html[:idx] + block + html[idx:]
path.write_text(new_html, encoding="utf-8")
print("INJECTED", len(html), "->", len(new_html))
