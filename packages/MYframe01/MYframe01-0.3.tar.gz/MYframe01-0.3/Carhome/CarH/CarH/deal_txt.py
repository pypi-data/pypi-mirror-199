#encoding:utf-8
import re

txt = '''
D:\python\python.exe D:/个人/Carhome/CarH/CarH/request_test.py
<!doctype html>
<html>
<head>
    <meta charset="gb2312">
    <meta http-equiv="X-UA-Compatible" content="IE =edge,chrome =1">
    <meta name="renderer" content="webkit">
    <script src="//x.autoimg.cn/bi/dealer/ahas_head.min.js" type="text/javascript"></script>
    <script src="//s.autoimg.cn/as/static/js/jquery-1.7.2.min.js" type="text/javascript"></script>
    <script src="https://x.autoimg.cn/dealer/dealerm/dist/pro/util/ics_yhz_fun.auto.generate.js?v=191211-06-14&amp;f=2021-04-08"></script>
  
    <!-- 标题及关键字 -->
    


    <title>【北京报价】北京海之沃四元桥店最新报价_汽车之家</title>
    <meta name="Keywords" content="北京报价,北京海之沃四元桥店最新价格" />
    <meta name="Description" content="汽车之家经销商频道,提供海之沃四元桥店4S店最新报价,北京4S店,海之沃四元桥店地址,电话,北京最新优惠信息,电话:4009972264" />

    
    <link href="//x.autoimg.cn/dealer/dealerm/dist/pro/resource/css/tip_carcolor_focusimg_layer.css?v=191211-06-14" rel="stylesheet" />
    <link href="//x.autoimg.cn/dealer/minisite/newMinisite/Resources/CSS/mini-blue20180211.css?v=191211-06-14" rel="stylesheet" />
    <link rel="stylesheet" href="https://x.autoimg.cn/dealer/dealerm/dist/pro/resource/dealer/css/frame-min.css?v=191211-06-14&amp;f=20230116">
    <link href="//x.autoimg.cn/dealer/custom/minisite/css/laydate.css?v=191211-06-14" rel="stylesheet" type="text/css" />
<!-- gray style -->
    <link rel="icon" type="image/x-icon" href="https://m.autohome.com.cn/favicon.ico"/>
<!-- /gray style -->
</head>
<body>
    



<script type="text/javascript">
    function IsPC() {
        var phone = "(ip(hone|od)|android|opera m(ob|in)i"
              + "|windows (phone|ce)|blackberry"
              + "|s(ymbian|eries60|amsung)|p(laybook|alm|rofile/midp"
              + "|laystation portable)|nokia|fennec|htc[-_]"
              + "|mobile|up.browser|[1-4][0-9]{2}x[1-4][0-9]{2})";
        var phoneReg=new RegExp(phone,"ig");
        var userAgentInfo = navigator.userAgent;
        if(phoneReg.test(userAgentInfo)){
            return false;
        }else{
            return true;
        }
    }
    if (!IsPC()) {
        var dealerid=60458;
        var seriesid=0;

        if(seriesid!=null&& seriesid!="" && seriesid>0)
        {
            window.location.replace("//dealer.m.autohome.com.cn/" + dealerid + "/Price?seriesid=" + seriesid);
        }else
        {
            window.location.replace("//dealer.m.autohome.com.cn/"+dealerid+"/Price");
        }
    }
    var url_dealerid = 60458, url_seriesid = 0 , url_factoryid = 0;
    var hasCloseOrder = false;
</script>


<!-- start头部 -->


<div class="header" id="skin_header">
    <!-- 导航头 begin -->
<link rel="stylesheet" href="//z.autoimg.cn/fe/topbar/1.0.39/topbar.css" />
<!-- 页面置灰样式 -->

<div id="auto-header" class="auto-header  auto-header--channel "><div id="auto-header-inner" class="auto-header__inner"><div class="auto-header-topbar"><div class="auto-header-topbar__content js-auto-header-responsive"><div class="auto-header-topbar__left"><div class="auto-header-logo"><a class="auto-header-logo__content" href="//www.autohome.com.cn/#pvareaid=3311664">汽车之家</a></div></div><div class="auto-header-topbar__middle"><div id="auto-header-search" class="search"><form id="souform" name="soform" action="//sou.autohome.com.cn/zonghe" target="_blank" accept-charset="gb2312"><div id="soudiv" class="search-box"><input type="text" class="search-text" id="q" name="q" autoComplete="off" value=""/><i class="auto-header-iconfont auto-header-iconfont-search"></i><input type="hidden" id="pvareaid" name="pvareaid" value="3311667"/><input type="hidden" id="mq" name="mq" value=""/></div><button type="submit" class="btn-search">搜索</button><div id="autocomplateTip" class="search-pop" style="display:none"></div><div class="search-history search-float-hide"><dl></dl><div><a href="javascript:void(0);" class="clearHis" target="_self">清除历史记录</a></div></div></form></div><div id="auto-header-club" class="auto-header-club"><div class="auto-header-club__title"><button type="button" id="auto-header-find-club"><span>找论坛</span><i class="auto-header-iconfont auto-header-iconfont-arrowdown"></i></button></div><div id="auto-header-club-list" class="auto-header-topchadiv auto-header-club__dropdown" style="display:none"><div class="auto-header-topchadiv__box"><span>最近浏览</span><div class="linedc"></div><div id="auto-header-club-listdata"></div></div></div></div></div><div class="auto-header-topbar__right"><div class="auto-header-status"><div id="auto-header-login" class="auto-header-login" style="display:none"></div><div id="auto-header-info" class="auto-header-message" style="display:none"><div class="auto-header-message__title"><a href="javascript:void(0);" target="_self">
            <span>消息</span>
            <span id="auto-header-info-allcount" class="num" style="display:none"></span>
            <i class="auto-header-iconfont auto-header-iconfont-arrowdown"></i>
          </a></div><div id="auto-header-info-list" class="auto-header-topchadiv auto-header-message__dropdown" style="display:none"><div class="auto-header-topchadiv__box"><div id="auto-header-info-listdata"></div><div class="linedc"></div><div><a id="auto-header-logoff" href="javascript:void(0);" target="_self">退出登录</a></div></div></div></div></div><div id="auto-header-sitemap" class="auto-header-sitemap"><div class="auto-header-sitemap__title"><a target="_self" href="javascript:void(0);">
          <span>网站导航</span>
          <i class="auto-header-iconfont auto-header-iconfont-arrowdown"></i>
        </a></div><div id="auto-header-sitemap-list" class="auto-header-topchadiv auto-header-sitemap__dropdown" style="display:none"><div class="auto-header-topchadiv__box"><a target="_blank" href="//www.autohome.com.cn/all/#pvareaid=3311757">文章</a><a target="_blank" href="//www.autohome.com.cn/bestauto/#pvareaid=3311757">评测</a><a target="_blank" href="//chejiahao.autohome.com.cn/#pvareaid=3311757">车家号</a><a target="_blank" href="//v.autohome.com.cn/#pvareaid=3311757">视频</a><a target="_blank" href="//live.autohome.com.cn/#pvareaid=3311757">直播</a><a target="_blank" href="//car.autohome.com.cn/duibi/chexing/#pvareaid=3311757">车型对比</a><a target="_blank" href="//car.autohome.com.cn/pic/index.html#pvareaid=3311757">图片</a><a target="_blank" href="//car.autohome.com.cn/#pvareaid=3311757">报价</a><a target="_blank" href="//mall.autohome.com.cn/#pvareaid=3311757">车商城</a><a target="_blank" href="//buy.autohome.com.cn/#pvareaid=3311757">降价</a><a target="_blank" href="//dealer.autohome.com.cn/#pvareaid=3311757">经销商</a><a id="auto-header-channel-che168-2" target="_blank" href="//www.che168.com/beijing/list/#pvareaid=3311757">二手车</a><a target="_blank" href="//j.autohome.com.cn/pcplatform/index.html?pt=_t&amp;pvareaid=3311757">金融</a><a target="_blank" href="//club.autohome.com.cn/#pvareaid=3311757">论坛</a><a target="_blank" href="//club.autohome.com.cn/jingxuan/#pvareaid=3311757">精选</a><a target="_blank" href="//k.autohome.com.cn/#pvareaid=3311757">口碑</a><a target="_blank" href="//yc.autohome.com.cn/list?pvareaid=3311757">养车</a></div></div></div><div id="auto-header-app" class="auto-header-more"><div class="auto-header-more__title"><a href="javascript:void(0);" target="_self">
          <span>更多</span>
          <i class="auto-header-iconfont auto-header-iconfont-arrowdown"></i>
        </a></div><div id="auto-header-app-list" class="auto-header-topchadiv auto-header-more__dropdown" style="display:none"><div class="auto-header-topchadiv__box"><a target="_blank" href="//www.athmapp.com/apps/#pvareaid=3311226">移动App</a><a target="_blank" href="//www.athmapp.com/apps/m/#pvareaid=3311226">触屏版</a><a target="_blank" href="//www.athmapp.com/apps/miniprogram/#pvareaid=35516820336">小程序</a><a target="_blank" href="//www.autohome.com.cn/chezhan/#pvareaid=3311226">车展</a><a target="_blank" href="//ics.autohome.com.cn/#pvareaid=3311226">i车商</a><a target="_blank" href="//www.che168.com/#pvareaid=3311226">二手车之家</a><a target="_blank" href="//shop.mall.autohome.com.cn/usercenter/user/login.do#pvareaid=3311226">商家后台</a><a target="_blank" href="//ai.autohome.com.cn">AI平台</a></div></div></div></div></div></div></div></div>
<script src="//z.autoimg.cn/fe/topbar/1.0.39/index.js"></script>
<script>
  AutoHeaderHelper.boot({
    sticky: false,
    hasCity: false,
    hasCityPop: false,
    hasSearch: true,
    hasClub: true
  });
  
</script>
<!-- 导航头 end -->
<!-- create 2023-03-16 19:11:51 -->
<!-- from uc-fe-api -->

    <div class="header-top" id="headertop">
        <div class="header-banner">

            <div class="header-newcont " id="newheader" style="background:url(https://dealer2.autoimg.cn/dealerdfs/g29/M07/52/6B/autohomedealer__ChwFk2HWYJWANgVcAACCktc3NJU279.jpg) no-repeat center center">
                <p class="newcontLogo">
                    <img src="" id="imgsrc" alt="">
                </p>
                <h2 class="newcontName"  id="dealerTitle" ></h2>
                <p class="newcontMsg"  id="groupName"></p>
                <p class="newcontPhone"  id="dealerTele"> 
                </p>
                <p class="newcontAddres" id="dealerAddress"> 
                </p>
                <p class="newcontAaod" id="adMessage"></p>
               
            </div>
        </div>



        <div class="header-nav">
            <ul class="nav-ul">
                <li id="nav_0"><a  href="/60458/">首页</a></li>
                <li id="nav_1"><a class=current href="/60458/price.html">车型报价</a></li>
                <li id="nav_2"><a  href="/60458/newslist.html">促销信息</a></li>
                <li id="nav_3"><a  href="/60458/informationList.html">新闻资讯</a></li>
                    <li id="nav_35"><a  href="/60458/maintain.html#pvareaid=6834817">维护保养</a></li>
                                    <li id="nav_4"><a  href="/60458/info.html">公司介绍</a></li>
                <li id="nav_5"><a  href="/60458/salerlist.html">销售顾问</a></li>
                    <li id="show_vr" class="linkright fn-hide">
                        <a href="javascript:void(0)" target="_blank" class="mark-360">
                            <i class="icon20 icon20-360"></i>智能展厅<i class="icon20 icon20-right"></i>
                        </a>
                    </li>
            </ul>
        </div>
    </div>
    <div class="header-hot" id="divheadhot">
        <div class="hot-main">
            <div class="main-left" id="hotcar"></div>
            <div class="main-right" id="400set">

                <span>咨询电话：</span>
                <span class="dealer-api">
                    <span class="dealer-api-phone">4009972264</span>
<i class="icon icon-24h1" title="24小时恭候致电！"></i><i title="可销往全国" class="icon icon-saleqg"></i>
                </span>
                <a target="_blank" id="dealer-order" href="/60458/order.html?siteId=2&pvareaid=2113141&eid=1|4|72|102|201014|300000&enfrom=1npc10000146" class="link" onclick='trackEvent("dlr_enter_source_click", "1npc10000146",0);'><i class="icon16 icon16-mail"></i>询价</a>
                <a target="_blank" id="dealer-drive" href="/60458/drive.html?siteId=2&pvareaid=2113114&eid=1|4|72|102|200087|300074&orderType=2&enfrom=1npc10000145" class="link" onclick='trackEvent("dlr_enter_source_click", "1npc10000145",0);'><i class="icon16 icon16-wheel"></i>试驾</a>

            </div>
        </div>
    </div>
</div>

<script type="text/javascript">
    function readCookie(e, t) {
        for (var a = e + "=", i = document.cookie.split(";"), n = 0; i.length > n; n++) {
            for (var o = i[n];
            " " == o.charAt(0) ;) o = o.substring(1, o.length);
            if (0 == o.indexOf(a)) return decodeURIComponent(o.substring(a.length, o.length))
        }
        return t !== void 0 ? t : null
    }
    function AutohomeJsLoad(e) {
        var t = document.createElement("script");
        t.setAttribute("type", "text/javascript"),
        t.setAttribute("src", e.url),
        t.onload = t.onreadystatechange = function () {
            if (!this.readyState || "loaded" == this.readyState || "complete" == this.readyState) {
                "function" == typeof e.callBack && e.callBack(e.args),
                t.onload = t.onreadystatechange = null;
                try {
                    t.parentNode && t.parentNode.removeChild(t)
                } catch (a) { }
            }
        },
        document.getElementsByTagName("head")[0].appendChild(t)
    }
    /*
    // 和Vue代码造成冲突, 导致Vue方法的参数无法传递.
    Array.prototype.indexOf = function (e) {
        for (var t, a = 0; t = this[a]; a++) if (t == e) return a;
        return -1
    },
    Function.prototype.bind = function (e, t) {
        var a = this;
        return function () {
            return a.apply(e, [].concat(t))
        }
    };
    */
    $(function () {
        $.ajax({
            url: "/Ajax/GetDealerHotSeries",
            type: "GET",
            dataType: 'html',
            data: {DealerId:60458},
            success: function (data) {
                if (data) {
                    $("#hotcar").prepend(data);
                }
                
            }
        });
        $.ajax({
            url: "/handler/other/getdata",
            type: "GET",
            dataType: 'json',
            data: { __action: "dealerlq.getsitesettings",DealerId:60458},
            success: function (data) {
                if (data && data.result && data.result.skinForPC) {
                    $("#skin_header").addClass("skin0" + data.result.skinForPC);

                }
            }
        });
        var newstats=1;
        if (newstats== 1) {
             $.ajax({
            url: "/handler/other/getdata",
            type: "GET",
                 dataType: 'json',
                 data: { __action: "dealerlq.getdealerheaderinfo", dealerIds:60458},
                 success: function (data) {
                     if (data && data.result && data.result && data.result.list && data.result.list.length > 0) {
                         var headerInfo = data.result.list[0];
                         
                         $("#newheader").addClass("typeColor_" + headerInfo.fontColor); 
                         if (headerInfo.dealerTitle!=null&&headerInfo.dealerTitle!="") {
                             $("#dealerTitle").text(headerInfo.dealerTitle);
                         }
                         if (headerInfo.address!=null&&headerInfo.address!="") {
                            $("#dealerAddress").html("<i class='iconAddres'></i>"+headerInfo.address);
                         }
                         if (headerInfo.freePhone != null && headerInfo.freePhone != "") {
                            $("#dealerTele").html("<i class='iconPhone'></i>"+headerInfo.freePhone);
                         }
                         if (headerInfo.adMessage!=null&&headerInfo.adMessage!="") {
                            $("#adMessage").text(headerInfo.adMessage);
                         }
                         if (headerInfo.groupName!=null&&headerInfo.groupName!="") {
                            $("#groupName").text(headerInfo.groupName);
                         }
                         if (headerInfo.saleBrandImg!=null&&headerInfo.saleBrandImg!="") {
                            $("#imgsrc").attr("src",headerInfo.saleBrandImg);
                         }
                    }
                }
            });
        }
        
        var dealerpayType =300;
        if (dealerpayType > 10) {
              $.ajax({
                url: "/handler/other/getdata",
                    type: "GET",
                    dataType: 'json',
                  data: { __action: "dealercloud.checkIsOnlineContractVrDealer", dealerIds:60458},
                    success: function (data) {
                        if (data && data.result && data.result.length > 0 && data.result[0].vrState==1) {
                            var href = data.result[0].pcUrl;
                            if (href.indexOf('?') == -1) {
                                href += "?pvareaid=2594445";
                            }
                            else {
                                href += "&pvareaid=2594445";
                            }
                            $("#show_vr a").attr("href", href);
                            $("#show_vr").removeClass(" fn-hide");

                            trackCustomEvent("auto_common_event", {
                                biz: "dlr",
                                type: "show ",
                                action: "dlr_ics_minisite_homepage_znzt_show",
                                ctime: new Date().getTime(),
                                area: "middle",
                                element: "details",
                                pmark: "0"
                            });
                        }

                    }
                });
        }
        $("#dealer-order").on("click", function(){
            window.trackCustomEvent("auto_common_event", { biz: "dlr", type: "click", action: "auto_dlr_ics_common_xj_click", ctime: new Date().getTime(), }, {eid: "1|4|72|102|201014|300000"});
        });
        $("#dealer-drive").on("click", function(){
            window.trackCustomEvent("auto_common_event", { biz: "dlr", type: "click", action: "auto_dlr_ics_common_xj_click", ctime: new Date().getTime(), }, {eid: "2113114&eid=1|4|72|102|200087|300074"});
        });
        window.trackCustomEvent("auto_common_event", { biz: "dlr", type: "show", action: "auto_dlr_ics_common_xj_show", ctime: new Date().getTime(), }, {eid: "1|4|72|102|201014|300000"});
        window.trackCustomEvent("auto_common_event", { biz: "dlr", type: "show", action: "auto_dlr_ics_common_xj_show", ctime: new Date().getTime(), }, {eid: "2113114&eid=1|4|72|102|200087|300074"});
    })
</script>
<!-- start ASS控件库焦点图1 -->


<!-- end头部 -->
<!-- start中间 -->
<div class="content">

    <!-- 面包屑 -->
<div class="breadnav" id="breadnav">
    <p>
        当前位置
            ：
            <a href="/beijing/">北京</a>
                    <span class="fn-font-st">&gt;</span><a href="/60458">海之沃四元桥店</a>
                        <span class="fn-font-st">&gt;</span><span class="fn-font-st">车型报价</span>
    </p>
    
</div>


    <div class="row">
        <!-- start左侧 -->
        <div class="grid-240 fn-left" id="divRight">
            <div class="seller">
                <div class="seller-title"><span class="title-text">主营品牌</span></div>

<div class="seller-cont">
    <div class="brandtree">
                <div class="brandtree-name">
                    <p class="pic"><img src="//m1.autoimg.cn/cardfs/series/g7/M09/D3/58/100x100_f40_autohomecar__ChsEvmFNNr-ALaiJAAA-q3aAE8E438.png" width="60" height="60"></p>
                    <p class="text">沃尔沃</p>
                </div>
                <div class="brandtree-cont">
                        <dl class="tree-dl">
                                <dt><a class="" target="_self" href="/60458/f_367.html">沃尔沃亚太</a></dt>

                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_6049.html">沃尔沃C40</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_3158.html">沃尔沃S60</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_4335.html">沃尔沃S60新能源</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_4206.html">沃尔沃S90</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_4864.html">沃尔沃S90新能源</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_5198.html">沃尔沃XC40</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_5904.html">沃尔沃XC40新能源</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_3411.html">沃尔沃XC60</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_4609.html">沃尔沃XC60新能源</a></dd>
                        </dl>
                        <dl class="tree-dl">
                                <dt><a class="" target="_self" href="/60458/f_84.html">沃尔沃(进口)</a></dt>

                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_2190.html">沃尔沃V60</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_4029.html">沃尔沃V90</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_177.html">沃尔沃XC90</a></dd>
                                    <dd><i class="icon12 icon12-jtr3"></i><a class="" target="_self" href="/60458/b_4337.html">沃尔沃XC90新能源</a></dd>
                        </dl>
                </div>
    </div>
</div>
<script type="text/javascript">



</script>
            </div>
            
        </div>
        <!-- end左侧 -->
        <!-- start右侧 -->
        <div id="app">
        </div>
        <!-- end右侧 -->
    </div>

</div>


<!-- end中间 -->
<!-- start右侧悬浮二维码 -->


<div class="fixedright fn-hide" id="div_qrcode">
    <a href="javascript:;" class="btn-close" id="a_qrcode">×</a>
    <p class="ewmpic" ><img id="img_qrcode" /></p>
    <p class="red" id="p1_qrcode"></p>
    <p class="red" id="p2_qrcode"></p>

</div>

<script>
    $(function () {
        var dealerId = 60458;

        var qrcode={
            qrcodeshow: function (show) {
                var flag = $("#div_qrcode").hasClass("fn-hide");
                if (show) {
                    if(flag)
                    {
                        $("#div_qrcode").removeClass('fn-hide');
                    }

                }
                else {
                    if(!flag)
                    {
                        $("#div_qrcode").addClass('fn-hide');
                    }
                    ics_yhz_fun.setCookie("_isqrcodeclose", "1", 1000 * 60 * 60 * 24);
                }
            },
            init:function(){
                $("#a_qrcode").click(function(){
                    qrcode.qrcodeshow(false);
                });

                $.getJSON("/handler/other/getdata", {
                    __action: "dealerlq.checkIsOnlineContractVrDealer",
                    dealerIds: dealerId,
                    qrType: 1
                }).then(function(response){ 
                    if(response && response.result && response.result[0] && response.result[0].dealerId === dealerId && response.result[0].vrState === 1 && response.result[0].linkUrlQrCode){
                        var qrCodeValue = response.result[0].linkUrlQrCode;
                        qrcode.qrcodeshow(true);
                        $("#img_qrcode").attr('src', qrCodeValue);
                        $("#p1_qrcode").text("全景逛店")
                        $("#p2_qrcode").text("VR看车")
                    }
                });

            }
        
        };
        var isclose = ics_yhz_fun.getCookie("_isqrcodeclose", "0");
        if (isclose == "0") {
            qrcode.init();
          }
        });
</script>
<!-- end右侧悬浮二维码 -->



    <!-- 品牌升级统一底部 -->
    <!-- footer -->
<style type="text/css">.athm-footer .footios:before,.athm-footer .footand:before,.athm-footer .footwp:before,.athm-footer .footphone:before,.athm-footer .footweibo:before,.athm-footer .footweibo:after{display:inline-block;vertical-align:middle;margin:-4px 10px 0 0;background:url(//s.autoimg.cn/www/site/index/images/icon-footer.png) no-repeat}.athm-footer{width:1200px;margin:20px auto 0;border-top:solid 2px #386ed3}.athm-footer .footer-content{padding:20px 0;text-align:center;white-space:nowrap}.athm-footer .footer-content>p{font-size:0;color:#7e7e7e;line-height:2.5}.athm-footer a,.athm-footer span,.athm-footer em{display:inline-block;font-size:14px;color:#7e7e7e;font-style:normal;text-decoration:none}.athm-footer a,.athm-footer span{padding:0 10px}.athm-footer a:hover{color:#f43636}.athm-footer .footios:before{content:'';width:18px;height:22px;background-position:0 0}.athm-footer .footand{position:relative}.athm-footer .footand:before{content:'';width:20px;height:24px;background-position:-25px 0}.athm-footer .footwp{position:relative}.athm-footer .footwp:before{content:'';width:22px;height:22px;background-position:-50px 0}.athm-footer .footphone{position:relative}.athm-footer .footphone:before{content:'';width:17px;height:24px;background-position:-75px 0}.athm-footer .footweibo{position:relative}.athm-footer .footweibo:before{content:'';width:24px;height:20px;background-position:0 -25px}.athm-footer .footweibo:after{content:'';width:20px;height:20px;margin:-4px 0 0 0;background-position:-25px -25px}.athm-footer--dark{width:100%;color:#C5CAD4;background-color:#333;border-top:0 none}.athm-footer--dark .footios:before,.athm-footer--dark .footand:before,.athm-footer--dark .footwp:before,.athm-footer--dark .footphone:before,.athm-footer--dark .footweibo:before{background:url(//s.autoimg.cn/www/site/index/images/icon-footer-s.png) no-repeat}.athm-footer--dark .footweibo:after{background:url(//s.autoimg.cn/www/site/index/images/icon-footer-s.png) no-repeat}.athm-footer--dark .footios:before{background-position:0 0}.athm-footer--dark .footand:before{background-position:-40px 0}.athm-footer--dark .footwp:before{background-position:-80px 0}.athm-footer--dark .footphone:before{background-position:-120px 0}.athm-footer--dark .footweibo:before{background-position:-160px 0}.athm-footer--dark .footweibo:after{margin-left:5px;background-position:-205px 0}@media only screen and (-webkit-min-device-pixel-ratio: 1.5), only screen and (min--moz-device-pixel-ratio: 1.5), only screen and (min-device-pixel-ratio: 1.5){.athm-footer--dark .footios:before,.athm-footer--dark .footand:before,.athm-footer--dark .footwp:before,.athm-footer--dark .footphone:before,.athm-footer--dark .footweibo:before{background:url(//s.autoimg.cn/www/site/index/images/icon-footer-s@2x.png) no-repeat}.athm-footer--dark .footweibo:after{background:url(//s.autoimg.cn/www/site/index/images/icon-footer-s@2x.png) no-repeat}.athm-footer--dark .footios:before{background-size:auto 30px;background-position:0 0}.athm-footer--dark .footand:before{background-size:auto 30px;background-position:-20px 0}.athm-footer--dark .footwp:before{background-size:auto 30px;background-position:-40px 0}.athm-footer--dark .footphone:before{background-size:auto 30px;background-position:-60px 0}.athm-footer--dark .footweibo:before{background-size:auto 30px;background-position:-80px 0}.athm-footer--dark .footweibo:after{background-size:auto 30px;background-position:-105px 0}}</style>
<div style="clear: both;"></div>
<div class="athm-footer ">
  <div class="footer-content">
    <p>
      <a href="//www.autohome.com.cn/about/index.html" target="_blank">关于我们</a>
      <a href="//www.autohome.com.cn/about/lianxi.html" target="_blank">联系我们</a>
      <a href="//talent.autohome.com.cn/" target="_blank">招贤纳士</a>
      <em class="fline">|</em>
      <a class="footios" href="//www.athmapp.com/apps/main/" target="_blank">iPhone客户端</a>
      <a class="footand" href="//www.athmapp.com/apps/main/" target="_blank">Android客户端</a>
      <a class="footphone" href="//www.athmapp.com/apps/m/" target="_blank">手机版</a>
      <em class="fline">|</em>
      <a class="footweibo" href="http://weibo.com/qichezhijia" target="_blank">汽车之家</a>
      <em class="fline">|</em>
      <a href="//www.autohome.com.cn/bug/default.aspx" target="_blank">意见反馈</a>
    </p>
    <p>
      <span>&copy; 2004-2023 www.autohome.com.cn All Rights Reserved. 汽车之家 版权所有</span>
    </p>
  </div>
</div>
<script>
  (function() {
    "use strict";function dateFormat(e,t){var g={"M+":e.getMonth()+1,"d+":e.getDate(),"h+":e.getHours(),"m+":e.getMinutes(),"s+":e.getSeconds(),"q+":Math.floor((e.getMonth()+3)/3),S:e.getMilliseconds()};/(y+)/.test(t)&&(t=t.replace(RegExp.$1,(e.getFullYear()+"").substr(4-RegExp.$1.length)));for(var r in g)new RegExp("("+r+")").test(t)&&(t=t.replace(RegExp.$1,1==RegExp.$1.length?g[r]:("00"+g[r]).substr((""+g[r]).length)));return t}
    var timeStamp=dateFormat(new Date(), "yyyyMMddhh");var script=document.createElement('script');script.type='text/javascript';script.defer="true";script.async="true";script.src="//z.autoimg.cn/chat/pc-chatroom/js/imtrack.js?v="+timeStamp;document.body.appendChild(script);
  })();
</script>
<!-- create 2023-03-16 19:11:47 -->
<!-- from uc-fe-api -->

    <!-- end底部 -->
    <script type="text/javascript" src="//s.autoimg.cn/as/js-2.0.2/sea.js" id="seajsnode"></script>
    

    <script type="text/javascript">
    $(function(){
        $.ajax({
            type: 'GET',
            url: "/Common/jiangjia",
            data: { dealerId: 60458 },
            dataType: "html",
            beforeSend: function(XMLHttpRequest) {
            },
            success: function(html) {
                if (html) {
                    $(html).appendTo($("#divRight"));
                }
            },
            complete: function(XMLHttpRequest, textStatus) {

            }
        });
    });
    </script>

    <script type="text/javascript" src="https://x.autoimg.cn/bi/common/pvevent_all_s.js"></script>

    
    


<script language="javascript" type="text/javascript">
    var pvTrack = function () { };
    pvTrack.site = 4;
    pvTrack.category =  72;
    pvTrack.subcategory = 103;
    pvTrack.object=0;
    pvTrack.typeid = window["pvtype"];
    pvTrack.dealer = 60458;
    pvTrack.series=0;
    pvTrack.spec=0;
    pvTrack.type=0;
</script>

<!-- 发送无3秒和过滤3秒日志的代码，统计接口从这里统一提供，后续升级此文件即可 -->
<script type="text/javascript">
    (function(doc){
        var _as = doc.createElement('script');
        _as.type = 'text/javascript';
        _as.async = true;
        _as.src = '//x.autoimg.cn/bi/dealer/ahas_body.min.js?d=' + Math.floor((new Date()).getTime()/(1000*60*60*24));
        var s = doc.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(_as, s);
    })(document);
</script>

<script language=javascript type=text/javascript>


    function func_get_url_stats() {
        var url_stats = "https://al.autohome.com.cn/pv_count.php?SiteId=";
        var doc = document, t = pvTrack;
        var pv_site, pv_category, pv_subcategory, pv_object, pv_series, pv_type, pv_typeid, pv_spec, pv_level, pv_dealer, pv_ref, pv_cur;
        pv_ref = escape(doc.referrer); pv_cur = escape(doc.URL);
        pv_site = t.site; pv_category = t.category; pv_subcategory = t.subcategory; pv_object = t.object; pv_series = t.series; pv_type = t.type; pv_typeid = t.typeid; pv_spec = t.spec; pv_level = t.level; pv_dealer = t.dealer;
        url_stats += pv_site + (pv_category != null ? "&CategoryId=" + pv_category : "") + (pv_subcategory != null ? "&SubCategoryId=" + pv_subcategory : "") + (pv_object != null ? "&objectid=" + pv_object : "") + (pv_series != null ? "&seriesid=" + pv_series : "") + (pv_type != null ? "&type=" + pv_type : "") + (pv_typeid != null ? "&typeid=" + pv_typeid : "") + (pv_spec != null ? "&specid=" + pv_spec : "") + (pv_level != null ? "&jbid=" + pv_level : "") + (pv_dealer != null ? "&dealerid=" + pv_dealer : "") + "&ref=" + pv_ref + "&cur=" + pv_cur + "&rnd=" + Math.random();
        return url_stats;
    }
    (function () {
        if (pvTrack != null) {
            setTimeout("func_stats()", 3000);
            //var len_url_stats = url_stats.length;
        }
    })();
    document.write('<iframe id="PageView_stats" style="display:none;"></iframe>');
    function func_stats() { document.getElementById('PageView_stats').src = func_get_url_stats(); }

    //!(function (doc) {
    //    var _as = doc.createElement('script');
    //    _as.type = 'text/javascript';
    //    _as.async = true;
    //    _as.src = 'http://s.autoimg.cn/hf/master.js?d=' + (new Date()).toLocaleDateString().replace(/\//g, "");
    //    var s = doc.getElementsByTagName('script')[0];
    //    s.parentNode.insertBefore(_as, s);
    //})(document);

</script>




    <script src="//x.autoimg.cn/dealer/minisite/newMinisite/Resources/js/SeriesColor.min.js"></script>
    <!-- start ASS控件库焦点图 -->
    <script type="text/javascript">
        seajs.config({ version: "1413012708869" });
        seajs.use(["jquery", "overlay", "pop"], function ($) {
            getColor();
        });
    </script>
    <!-- end ASS控件库焦点图 -->

    <script type="text/javascript">
        var expends = function (seriesId) {
            jQuery("#tab_" + seriesId).show();
            jQuery("#btn_" + seriesId).hide();
            jQuery("#div_" + seriesId).show();
        }

        var packup = function (seriesId) {
            jQuery("#tab_" + seriesId).hide();
            jQuery("#btn_" + seriesId).show();
            jQuery("#div_" + seriesId).hide();
        }
        expends();
        var ViewBagDealerID=60458;

        //点击事件
        var __seriesid='';
        function trackEvent(action, enfrom) {
            var _city = 0;
            if (_tools != null && typeof (_tools) != "undefined") {
                _city = _tools.getCookie("area");
            }

            var params = { 'esfrom': enfrom, 'business': 'CSH', 'series': __seriesid, 'city': _city };
            trackDealerEvent(action, params);
        }

        //added by sujunhui 20170324 新统计埋码
        function initenfrom_serieslist()
        {
            var xunjia_enfrom='1npc10000131';
            var drive_enfrom='1npc10000106';
            var change_enfrom='1npc10000107';

            trackEvent("dlr_enter_source_load", xunjia_enfrom);
            trackEvent("dlr_enter_source_load", drive_enfrom);
            trackEvent("dlr_enter_source_load", change_enfrom);

            trackEvent("dlr_enter_source_show", xunjia_enfrom);
            trackEvent("dlr_enter_source_show", drive_enfrom);
            trackEvent("dlr_enter_source_show", change_enfrom);
        }

        //added by sujunhui 20170324 等待脚本加载完成，执行埋码统计
        setTimeout("initenfrom_serieslist()",2000);
    </script>
    
    <script>
        var praise = {
            init: function () {
                jQuery(".icon16 icon16-book2").click(function () {
                    jQuery(this).next().removeClass().addClass("pop pop-refer fn-show");
                })
                jQuery(".icon16 icon16-book2").mouseout(function () {
                    jQuery(this).next().removeClass().addClass("pop pop-refer fn-hide");
                })
                jQuery("[id^=btn_]").bind('click', function () {
                    expends(jQuery(this).attr("atr-sid"));
                    if (ViewBagDealerID > 0) {
                        praise.track(jQuery(this).attr("atr-sid"), jQuery(this).attr("atr-did"));
                    }
                })
                jQuery("[id^=div_]").bind('click', function () {
                    packup(jQuery(this).attr("atr-sid"));
                    if (ViewBagDealerID > 0) {
                        praise.track(jQuery(this).attr("atr-sid"), jQuery(this).attr("atr-did"));
                    }
                });
                this.init_price_detail();
            },
            track: function (sid, dealerid) {
                _trackEvent.push({ 'curl': encodeURIComponent(document.URL), 'rurl': encodeURIComponent(document.referrer), 'ctime': (new Date()).valueOf(), 'eid': '1|4|72|103|200038|300033', 'val': 1, 'a1': sid, 'a2': dealerid });
            },
            init_price_detail: function () {
                window.seajs.use(['jquery', 'pop'], function ($) {
                    window._$$ = $;
                    $('[data-toggle=\'pop2\']').pop();
                });

                jQuery("a[data-toggle='pop2']").hover(function () {
                    var data = window.dataA || jQuery(this).attr("data-view").split('|');

                    var price = (parseFloat(data[0]) / 10000).toFixed(2);
                    jQuery("#price").text(price + "万元");

                    var strpurchaseTax, strpurchaseTaxPrice, purchaseTaxPrice = 0;
                    var item = data[1].split(',');
                    if (item[0] == '0') {
                        strpurchaseTax = "";
                        strpurchaseTaxPrice = item[1] + "元";
                        purchaseTaxPrice = parseFloat(item[1]);
                    } else if (item[0] == '50') {
                        strpurchaseTax = "赠送50%";
                        strpurchaseTaxPrice = "自付" + item[1] + "元";
                        purchaseTaxPrice = parseFloat(item[1]);
                    } else if (item[0] == '100') {
                        strpurchaseTax = "赠送100%";
                        strpurchaseTaxPrice = "";
                    }
                    else if (item[0] == '110') {
                        strpurchaseTax = "免税";
                        strpurchaseTaxPrice = "";
                    }
                    jQuery("#purchasetax").text(strpurchaseTax);
                    jQuery("#purchasetaxprice").text(strpurchaseTaxPrice);

                    jQuery("#vehicleTaxPrice").text(data[2] + "元");

                    item = data[3].split(',');
                    var strcommercialInsurancePrice = (item[0] == '0') ? item[1] + "元" : "赠送" + item[0] + "年";
                    jQuery("#commercialInsurancePrice").text(strcommercialInsurancePrice);
                    var commercialInsurancePrice = parseFloat(item[1]);

                    item = data[4].split(',');
                    var strcompulsoryInsurancePrice = (item[0] == '0') ? item[1] + "元" : "赠送" + item[0] + "年";
                    var compulsoryInsurancePrice = parseFloat(item[1]);

                    jQuery("#compulsoryInsurancePrice").text(strcompulsoryInsurancePrice);
                    jQuery("#insuranceDiscount").text(data[5] + "元");
                    jQuery("#licensePrice").text(data[6] + "元");
                    jQuery("#otherPrice").text(data[7] + "元");

                    var dealerPrice = (parseFloat(data[8]) / 10000).toFixed(2);
                    
                    jQuery("#dealPrice").text(dealerPrice + "万");                    
                    window._$$(this).pop('show');
                }, function () { });
            }
        }
        praise.init();


        jQuery("span[id^=carColor1]").click(function (e) {
            jQuery(e.target).closest(".name-color").last().click();
        })

        function getperpor(obj) {
            jQuery(obj).removeAttr("style").attr("style", "background: background: #A7A5A7;");
        }

        function getColor() {
            //jQuery("div[class='name-color']").each(function () {
            //    var data = jQuery(this).attr("data-view").split('|');
            //    if (data.length > 1) {
            //        getColorList(data[0], data[1]);
            //    }

            //});
        }
    </script>


    <script src="//x.autoimg.cn/dealer/dealerm/dist/pro/vendor/vendor.64114747d178e0a8a6b7.js" type="text/javascript"></script>
    <script src="https://x.autoimg.cn/dealer/dealerm/dist/pro/dealerpc/dealer_series_list.auto.generate.js?v=191211-06-14&amp;f=2022-05-13-1"></script>

    
    <script>
        var ahas_tjfr = ics_yhz_fun.get("tjfr", "");

        var _tools = {
            getCookie: function (name, defval) {
                var nameEQ = name + "=";
                var ca = document.cookie.split(';');
                for (var i = 0; i < ca.length; i++) {
                    var c = ca[i];
                    while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                    if (c.indexOf(nameEQ) == 0) return decodeURIComponent(c.substring(nameEQ.length, c.length));
                };
                return typeof defval == "undefined" ? null : defval;
            },
            setCookie: function (name, value, time) {
                var Days = 30;
                var domain = "autohome.com.cn";//window.location.hostname;
                var str = name + "=" + escape(value) + ";domain=" + domain + ";path=/;" ;
                if (time > 0) {
                    var exp = new Date();
                    exp.setTime(exp.getTime() + time);
                    str += "expires=" + exp.toGMTString();
                }
                document.cookie = str;
            },
            get: function (name, def) {
                var result = location.search.match(new RegExp("[\?\&]" + name + "=([^\&]+)", "i"));
                if (result == null || result.length < 1) {
                    return def;
                }
                return result[1];
            },
            //获取url中查询参数
            getUrlQuery: function () {
                //window.location.origin
                var window_location_origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port : '')
                var paras = window.location.href.substr(window_location_origin.length);
                if (paras.indexOf("/") == 0)
                    paras = paras = paras.substr(1);
                return paras;
            },
            get_dealerid: function () {
                var url = window.location.href;
                var reg = /\/\d+\/*/;
                if (reg.test(url)) {
                    var result = reg.exec(url);
                    var idstr = result[0];
                    var regDealerId = /\d+/;
                    var result_id = regDealerId.exec(idstr);
                    var id = result_id[0];
                    return id;
                }
                return "";
            },
            follow_siteid: [178, 179, 180, 181, 182,190],
            get_order_siteid: function (def) {
                var siteid = _tools.get("siteid", "");
                var dealerId = _tools.get_dealerid();
                for (var i in _tools.follow_siteid) {
                    if (siteid == _tools.follow_siteid[i]) {
                        _tools.setCookie("_osid_" + dealerId, siteid, 0);
                    }
                }
                if (dealerId === "")
                    return def;
                var id = _tools.getCookie("_osid_" + dealerId, _tools.get("siteid", def));
                //console.info("siteid=" + id);
                return id;
            },
            get_order_success_siteid: function (dealerId, def) {
                var id = _tools.getCookie("_osid_" + dealerId, def);
                //console.info("siteid=" + id);
                return id;
            }
        };
       
    </script>
</body>
</html>


Process finished with exit code 0

'''
import parsel
selector = parsel.Selector(txt)

#经销商
# links = selector.xpath('//ul//li[@class="tit-row"]//a//@href').extract()
# title = selector.xpath('//ul//li[@class="tit-row"]//a//span/text()').extract()
#
# for l, t in zip(links, title):
#     print(l)
#     print(t)

#车型报价
# links = selector.xpath('//ul//li[@id="nav_1"]//a/@href').extract_first()
# print(links)




#获取车型id
# links = selector.xpath('//div[@class="brandtree-cont"]//dd/a/@href').extract()
# title = selector.xpath('//div[@class="brandtree-cont"]//dd/a/text()').extract()
# for l, t in zip(links, title):
#     id = re.findall(r'b_(\d+)\.',l)[0]
#     print(id)
#     print(t)

# aaa = '/60458/price.html'
# id = re.findall(r'/(\d+)/',aaa)[0]
# print(id)

# txt = 'https://123.123.456.89:500'
# proxy = re.sub('(.*?)//','',txt)
# host = proxy.split(':')[0]
# port = proxy.split(':')[1]
# print(host)
# print(port)


from CarH.CPProxyPool import ProxyPool
pool = ProxyPool()
pool._delete_proxy('https://215.27.159.204:3541')
